# tools/compliance_checker.py

import json
import os

def load_policies() -> list:
    path = os.path.join("data", "compliance_policies.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data["policies"]

def keyword_precheck(document_text: str, policies: list) -> dict:
    """
    Fast pass: flags which policies have NO matching keywords at all
    (likely missing) vs which have at least partial keyword presence
    (needs LLM judgment to confirm quality/completeness).
    """
    text_lower = document_text.lower()
    results = {}
    for policy in policies:
        matched = [kw for kw in policy["required_keywords"] if kw.lower() in text_lower]
        results[policy["id"]] = {
            "category": policy["category"],
            "rule": policy["rule"],
            "keyword_matches": matched,
            "likely_present": len(matched) > 0
        }
    return results