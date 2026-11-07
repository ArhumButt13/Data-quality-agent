import re
import pandas as pd

VAT_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{8,12}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
FIELDS = ["name", "country", "vat_id", "email", "phone"]


def load_suppliers(path="data/suppliers.csv"):
    """Read the CSV file. Empty cells become empty text ("")."""
    return pd.read_csv(path, dtype=str).fillna("")


def missing_fields(row):
    """Return the names of all empty fields in one supplier row."""
    return [field for field in FIELDS if row[field].strip() == ""]


def is_valid_vat(vat_id):
    """A VAT ID is 2 letters followed by 8 to 12 letters or digits."""
    return bool(VAT_PATTERN.match(vat_id.strip()))


def is_valid_email(email):
    """An email needs text, an @, and a domain with a dot."""
    return bool(EMAIL_PATTERN.match(email.strip()))


def find_duplicates(df, supplier_id):
    """Return IDs of earlier suppliers with the same name (ignoring case and spaces)."""
    names = df["name"].str.lower().str.strip()
    position = df.index[df["supplier_id"] == supplier_id][0]
    earlier = df[(names == names[position]) & (df.index < position)]
    return earlier["supplier_id"].tolist()
