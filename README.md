# Product Processor

A small Python script that reads a product CSV, validates every record,
flags invalid ones, and prints a summary.

## Validation rules

| Field        | Rule                                   |
|--------------|----------------------------------------|
| `product_id` | required, must start with `P`          |
| `name`       | required, not empty                    |
| `price`      | required, a number, not negative       |
| `quantity`   | required, a whole number, not negative |

## Usage

```bash
python3 product_processor.py products.csv
```

If no file is given, it defaults to `products.csv`.

Example output:

```
P003 ['name is missing']
P004 ['price is negative']
...

PRODUCT PROCESSING SUMMARY
--------------------------
Total records: 12
Valid records: 7
Invalid records: 5
```

## Error handling

- Missing file: prints an error and exits with code 1.
- CSV missing a required column: prints an error and exits with code 1.
- Bad values in individual rows are reported, not crashed on.

## Tests

```bash
pip install pytest
python3 -m pytest
```

## Project structure

```
product_processor.py        # script
products.csv                # sample data
tests/test_product_processor.py
```
