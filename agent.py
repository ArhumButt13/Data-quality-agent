import json
from dotenv import load_dotenv
from anthropic import Anthropic
from checks import load_suppliers, is_valid_vat, is_valid_email, find_duplicates
from ai_check import parse_json

load_dotenv()
client = Anthropic()
MODEL = "claude-haiku-5-5"
df = load_suppliers()

# 1. Describe the tools so Claude knows what it can call
TOOLS = [
    {
        "name": "check_vat_format",
        "description": "Checks if a VAT ID has a valid format: 2 letters followed by 8 to 12 letters or digits.",
        "input_schema": {
            "type": "object",
            "properties": {"vat_id": {"type": "string"}},
            "required": ["vat_id"],
        },
    },
    {
        "name": "check_email_format",
        "description": "Checks if an email address has a valid format.",
        "input_schema": {
            "type": "object",
            "properties": {"email": {"type": "string"}},
            "required": ["email"],
        },
    },
    {
        "name": "find_duplicates",
        "description": "Returns the IDs of earlier suppliers with the same name as this supplier.",
        "input_schema": {
            "type": "object",
            "properties": {"supplier_id": {"type": "string"}},
            "required": ["supplier_id"],
        },
    },
]


# 2. Run the real Python function when Claude asks for a tool
def run_tool(name, args):
    if name == "check_vat_format":
        return {"valid": is_valid_vat(args["vat_id"])}
    if name == "check_email_format":
        return {"valid": is_valid_email(args["email"])}
    if name == "find_duplicates":
        return {"duplicates_of": find_duplicates(df, args["supplier_id"])}
    return {"error": f"unknown tool {name}"}


SYSTEM = """You are a master data quality agent. You check one supplier record.
A record is clean only if no field is empty, the VAT ID and email have valid formats,
and it is not a duplicate of an earlier supplier.
Use the tools to check the VAT ID, the email and duplicates.
When you are finished, answer ONLY with JSON in this format, with no other text:
{"clean": true or false, "issues": ["short description of each problem"]}"""


# 3. The agent loop: ask, run the tools Claude wants, send results back, repeat
def run_agent(record, show_steps=True):
    messages = [{"role": "user", "content": "Check this supplier record: " + json.dumps(record)}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason != "tool_use":  # Claude is done: read its final answer
            text = "".join(block.text for block in response.content if block.type == "text")
            return parse_json(text)

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                output = run_tool(block.name, block.input)
                if show_steps:
                    print(f"  tool: {block.name}({block.input}) -> {output}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(output),
                })
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    for supplier_id in ["S003", "S006"]:
        record = df[df["supplier_id"] == supplier_id].iloc[0].to_dict()
        print(supplier_id)
        print(run_agent(record))
