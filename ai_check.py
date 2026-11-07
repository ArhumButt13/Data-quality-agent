import json
from dotenv import load_dotenv
from anthropic import Anthropic
from checks import load_suppliers

load_dotenv()          # reads your API key from the .env file
client = Anthropic()   # connects to Claude
MODEL = "claude-haiku-5-5"

PROMPT = """You are a master data quality assistant.
Check the supplier record below. A record is clean only if no field is empty,
the VAT ID looks valid and the email looks valid.
Answer ONLY with JSON in exactly this format, with no other text:
{"clean": true or false, "issues": ["short description of each problem"]}

Record:
"""


def parse_json(text):
    """Turn the model's reply into a Python dictionary.
    Takes everything from the first { to the last }, in case the model adds extra words."""
    start = text.find("{")
    end = text.rfind("}")
    return json.loads(text[start:end + 1])


def check_with_ai(record):
    """Send one supplier record to Claude and get its verdict back as a dictionary."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": PROMPT + json.dumps(record)}],
    )
    return parse_json(response.content[0].text)


if __name__ == "__main__":
    df = load_suppliers()
    for supplier_id in ["S001", "S006", "S009"]:
        record = df[df["supplier_id"] == supplier_id].iloc[0].to_dict()
        print(supplier_id, check_with_ai(record))
