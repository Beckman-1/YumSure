import pytest
import asyncio
from app.services.barcode_resolver import BarcodeResolver, _NEGATIVE_CACHE
from app.core.database import AsyncSessionLocal

def test_validate_valid_barcodes():
    """Verify check-digit algorithm passes valid EAN-13, EAN-8, and UPC-A."""
    # Valid EAN-13: Maggi (8901058852394)
    valid_ean13, clean, err = BarcodeResolver.validate_barcode("8901058852394")
    assert valid_ean13 is True
    assert clean == "8901058852394"
    assert err is None

    # Valid EAN-13: Coca-Cola (5449000000996)
    valid_coke, _, _ = BarcodeResolver.validate_barcode("5449000000996")
    assert valid_coke is True

    # Valid EAN-8: 96385074
    valid_ean8, clean8, _ = BarcodeResolver.validate_barcode("96385074")
    assert valid_ean8 is True

    # Valid UPC-A: 011110038364
    valid_upc, _, _ = BarcodeResolver.validate_barcode("011110038364")
    assert valid_upc is True

def test_reject_invalid_check_digit():
    """Verify check-digit algorithm rejects corrupted or forged barcodes."""
    # Last digit changed from 4 to 5
    corrupt_maggi = "8901058852395"
    valid, _, err = BarcodeResolver.validate_barcode(corrupt_maggi)
    assert valid is False
    assert "Invalid barcode check digit" in err

def test_reject_invalid_formats():
    """Verify non-numeric or abnormal length barcodes are rejected."""
    # Alphanumeric
    valid_alpha, _, err_alpha = BarcodeResolver.validate_barcode("ABC1234567890")
    assert valid_alpha is False
    
    # Too short
    valid_short, _, err_short = BarcodeResolver.validate_barcode("12345")
    assert valid_short is False
    assert "length" in err_short

    # Empty
    valid_empty, _, _ = BarcodeResolver.validate_barcode("")
    assert valid_empty is False

@pytest.mark.anyio
async def test_resolve_seed_catalog_item():
    """Verify seed items resolve and return separated facts and versioned assessment."""
    async with AsyncSessionLocal() as session:
        res = await BarcodeResolver.resolve_barcode("8901058852394", session)
        assert res is not None
        assert res["barcode"] == "8901058852394"
        assert "Maggi" in res["name"]
        assert "nutrition_facts" in res
        assert "assessment" in res
        assert res["assessment"]["rule_version"] == "2026.1"

@pytest.mark.anyio
async def test_negative_caching():
    """Verify non-existent barcodes are stored in negative cache to prevent upstream hammering."""
    # Generate a syntactically valid EAN-13 barcode that does not exist in any DB: 8909999999999 -> check digit calculation
    # 8*1 + 9*3 + 0*1 + 9*3 + 9*1 + 9*3 + 9*1 + 9*3 + 9*1 + 9*3 + 9*1 + 9*3 = 8+27+0+27+9+27+9+27+9+27+9+27 = 216 -> check = 4
    fake_barcode = "8909999999994"
    valid, clean, _ = BarcodeResolver.validate_barcode(fake_barcode)
    assert valid is True

    async with AsyncSessionLocal() as session:
        # First resolve: attempts DB + seed + upstream (will return None)
        res1 = await BarcodeResolver.resolve_barcode(clean, session)
        assert res1 is None
        assert clean in _NEGATIVE_CACHE

        # Second resolve: hits negative cache immediately without upstream network calls
        res2 = await BarcodeResolver.resolve_barcode(clean, session)
        assert res2 is None
