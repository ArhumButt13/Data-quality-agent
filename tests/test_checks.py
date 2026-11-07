import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checks import find_duplicates, is_valid_email, is_valid_vat, missing_fields  # noqa: E402


def test_vat_format():
    assert is_valid_vat("DE123456789")
    assert not is_valid_vat("123456789")


def test_email_format():
    assert is_valid_email("info@acme.de")
    assert not is_valid_email("info.acme.de")


def test_missing_fields():
    row = {"name": "A", "country": "DE", "vat_id": "", "email": "a@b.de", "phone": ""}
    assert missing_fields(row) == ["vat_id", "phone"]


def test_find_duplicates():
    df = pd.DataFrame({"supplier_id": ["S1", "S2"], "name": ["ACME GmbH", " acme gmbh "]})
    assert find_duplicates(df, "S2") == ["S1"]
    assert find_duplicates(df, "S1") == []
