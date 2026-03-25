import json
import re
from typing import Any

def parse_fenced_json(raw_output: Any) -> dict:
    # Handle tuple/list inputs
    if isinstance(raw_output, (tuple, list)):
        raw_output = "".join(str(x) for x in raw_output)

    # Normalize to string
    text = str(raw_output).strip()

    # Remove markdown fences: ```json ... ```
    text = re.sub(r"^\s*```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*```\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)

    # Parse JSON
    return json.loads(text)