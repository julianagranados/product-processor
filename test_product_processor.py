import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from product_processor import process_file, validate_product


def make_product(**overrides):
    product = {"product_id": "P001", "name": "Laptop", "price": "999.99", "quantity": "10"}
    product.update(overrides)
    return product


def test_valid_product_has_no_errors():
    assert validate_product(make_product()) == []


def test_missing_name_is_flagged():
    assert "name is missing" in validate_product(make_product(name=""))


def test_negative_price_is_flagged():
    assert "price is negative" in validate_product(make_product(price="-10"))


def test_non_numeric_quantity_is_flagged():
    assert "quantity is not a whole number" in validate_product(make_product(quantity="abc"))


def test_negative_quantity_is_flagged():
    assert "quantity is negative" in validate_product(make_product(quantity="-5"))


def test_process_file_counts_valid_and_invalid(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "product_id,name,price,quantity\n"
        "P001,Laptop,999.99,10\n"
        "P002,,25.50,50\n"
        "P003,Desk,250.00,-5\n"
    )
    total, invalid = process_file(str(csv_file))
    assert total == 3
    assert [pid for pid, _ in invalid] == ["P002", "P003"]


def test_process_file_rejects_missing_columns(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("product_id,name\nP001,Laptop\n")
    with pytest.raises(ValueError):
        process_file(str(csv_file))
