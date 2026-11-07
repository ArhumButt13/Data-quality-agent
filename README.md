# Supplier Data Quality Agent

> A self-learning project I built to get hands-on with AI engineering: calling an LLM through an API, giving it tools, getting structured output and measuring whether it is right.

A small AI agent that checks supplier master data for problems: missing fields, invalid VAT IDs, invalid emails and duplicate suppliers. It uses Claude through the Anthropic API with **tool use**: the model decides which Python check to run, reads the result and returns a clean or not-clean verdict.

```
supplier record ──► Claude ──► calls tools (VAT check, email check, duplicate search) ──► verdict as JSON
```

## What is in the project

| File | What it does |
|---|---|
| `checks.py` | Plain Python rules: missing fields, VAT format, email format, duplicate names |
| `check_data.py` | Runs the rules on all suppliers and saves `output/issues_report.csv` (no API key needed) |
| `ai_check.py` | Asks Claude to judge one record from a prompt alone |
| `agent.py` | The agent: Claude calls the Python checks as tools, then gives a verdict |
| `evaluate.py` | Compares the agent's verdicts with hand-made labels in `data/labels.csv` and prints the accuracy |
| `tests/` | Automated tests for the rule functions |

The data in `data/suppliers.csv` is a small made-up sample with planted errors.

## Run it

```bash
pip install -r requirements.txt
python check_data.py      # rule-based check, no API key needed
pytest                    # run the tests
```

To use the AI parts, create an API key at console.anthropic.com, copy `.env.example` to `.env` and paste the key there. `.env` is never uploaded.

```bash
python ai_check.py        # prompt-only check
python agent.py           # agent with tool use
python evaluate.py        # accuracy against the labels
```

## Why an agent and not only a prompt

A prompt alone can guess whether a VAT ID looks right. The agent instead calls exact Python checks, so the verdict is based on rules that can be tested, while the model decides what to check and explains the result.

## What I learned

- How to call an LLM through the Anthropic API and get structured JSON back
- How tool use works: the model asks for a function, my code runs it and returns the result
- Why exact, tested rules make an AI application more reliable than a prompt alone
- How to evaluate an AI system against labelled data instead of trusting its output

## Next steps

- Check VAT numbers against the EU VIES service instead of only the format
- Add more tools, for example phone-number and country checks
- Test on a larger, real-world dataset

## Tools

Python · pandas · Anthropic API (Claude, tool use) · pytest
