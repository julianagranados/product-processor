"""Read a product CSV, validate each record, and print a summary."""
import csv
import sys

REQUIRED_FIELDS = ["product_id", "name", "price", "quantity"]


def validate_product(product):
    """Return a list of error messages for one product row (empty list = valid)."""
    errors = []

    # Required fields must be present and non-empty
    for field in REQUIRED_FIELDS:
        value = product.get(field)
        if value is None or value.strip() == "":
            errors.append(f"{field} is missing")

    # Only run the format checks on fields that are present
    product_id = (product.get("product_id") or "").strip()
    if product_id and not product_id.startswith("P"):
        errors.append("product_id must start with 'P'")

    price = (product.get("price") or "").strip()
    if price:
        try:
            if float(price) < 0:
                errors.append("price is negative")
        except ValueError:
            errors.append("price is not a number")

    quantity = (product.get("quantity") or "").strip()
    if quantity:
        try:
            if int(quantity) < 0:
                errors.append("quantity is negative")
        except ValueError:
            errors.append("quantity is not a whole number")

    return errors


def process_file(path):
    """Validate every row in the CSV at `path`.

    Returns (total, invalid_records) where invalid_records is a list of
    (product_id, errors) tuples.
    """
    total = 0
    invalid_records = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_FIELDS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row in reader:
            total += 1
            errors = validate_product(row)
            if errors:
                invalid_records.append((row.get("product_id") or "<no id>", errors))

    return total, invalid_records


def print_summary(total, invalid_records):
    invalid = len(invalid_records)
    for product_id, errors in invalid_records:
        print(product_id, errors)
    print()
    print("PRODUCT PROCESSING SUMMARY")
    print("--------------------------")
    print("Total records:", total)
    print("Valid records:", total - invalid)
    print("Invalid records:", invalid)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "products.csv"
    try:
        total, invalid_records = process_file(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    print_summary(total, invalid_records)


if __name__ == "__main__":
    main()
