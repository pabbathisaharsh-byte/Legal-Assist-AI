# tests/test_scenarios.py

"""
Automated scenario tests for LegalAssist AI.
Runs core routing and output scenarios directly against the compiled graph,
without needing Streamlit. Useful for quick regression checks before a demo.

Usage:
    python tests/test_scenarios.py
"""

import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph import build_graph

# A short sample "contract" for document-dependent test cases.
# Deliberately missing payment terms and dispute resolution language,
# so compliance checks have something real to flag.
SAMPLE_INCOMPLETE_CONTRACT = """
SERVICE AGREEMENT

This Agreement is between Acme Consulting ("Consultant") and Beta Corp ("Client").

1. SCOPE OF WORK
Consultant agrees to provide software development services as described in Exhibit A.

2. CONFIDENTIALITY
Both parties agree to keep all shared information confidential and not disclose it
to third parties without written consent.

3. TERMINATION
Either party may terminate this Agreement with thirty (30) days written notice.

4. INDEMNIFICATION
Consultant agrees to indemnify and hold harmless Client from any claims arising
from Consultant's negligence.
"""

PASS = "PASS"
FAIL = "FAIL"

def run_case(graph, thread_id, label, user_request, document_text=None,
             expected_agents=None, check_fn=None):
    config = {"configurable": {"thread_id": thread_id}}
    graph_input = {
        "user_request": user_request,
        "document_text": document_text,
        "document_name": "sample_contract.txt" if document_text else None,
    }

    print(f"\n--- {label} ---")
    print(f"Request: {user_request!r}  |  Document: {'yes' if document_text else 'no'}")

    try:
        result = graph.invoke(graph_input, config=config)
    except Exception as e:
        print(f"{FAIL} — graph raised an exception: {e}")
        return False

    actual_agents = result.get("next_agents", [])
    print(f"next_agents: {actual_agents}")
    print(f"is_response_approved: {result.get('is_response_approved')}")

    ok = True

    if expected_agents is not None:
        if set(actual_agents) != set(expected_agents):
            print(f"{FAIL} — expected agents {expected_agents}, got {actual_agents}")
            ok = False

    if check_fn is not None:
        try:
            check_fn(result)
        except AssertionError as e:
            print(f"{FAIL} — check failed: {e}")
            ok = False

    if ok:
        print(f"{PASS}")
    return ok


def main():
    graph = build_graph()
    results = []

    # Each scenario gets its own thread_id to avoid state bleeding between
    # unrelated test cases (mirrors a fresh user session).

    # 1. Extract clauses from a document
    results.append(run_case(
        graph, str(uuid.uuid4()),
        "Extract key clauses",
        "Extract the key clauses from this contract.",
        document_text=SAMPLE_INCOMPLETE_CONTRACT,
        expected_agents=["contract_analysis_agent"],
        check_fn=lambda r: assert_true(
            "error" not in (r.get("clause_summary") or {}),
            "clause_summary should not contain an error"
        )
    ))

    results.append(run_case(
        graph, str(uuid.uuid4()),
        "Compliance review (fan-out)",
        "Check this contract for compliance issues.",
        document_text=SAMPLE_INCOMPLETE_CONTRACT,
        expected_agents=["contract_analysis_agent", "compliance_review_agent"],
        check_fn=lambda r: assert_true(
            r.get("compliance_report") and "missing_requirements" in r["compliance_report"],
            "compliance_report should include missing_requirements"
        )
    ))

    results.append(run_case(
        graph, str(uuid.uuid4()),
        "Legal research, no document",
        "What should a confidentiality clause include?",
        document_text=None,
        expected_agents=["legal_research_agent"],
        check_fn=lambda r: assert_true(
            r.get("research_summary") and r["research_summary"].get("sources"),
            "research_summary should have at least one source"
        )
    ))

    results.append(run_case(
        graph, str(uuid.uuid4()),
        "Document drafting",
        "Draft a termination notice for a service agreement.",
        document_text=None,
        expected_agents=["document_drafting_agent"],
        check_fn=lambda r: assert_true(
            r.get("drafted_document") and r["drafted_document"].get("draft_content"),
            "drafted_document should have draft_content"
        )
    ))

    results.append(run_case(
        graph, str(uuid.uuid4()),
        "No document safety net",
        "Extract the key clauses from this contract.",
        document_text=None,
        check_fn=lambda r: assert_true(
            "contract_analysis_agent" not in r.get("next_agents", []),
            "contract_analysis_agent should not run without a document"
        )
    ))

    memory_thread = str(uuid.uuid4())
    run_case(
        graph, memory_thread,
        "Memory turn 1 (upload + analyze)",
        "Extract the key clauses from this contract.",
        document_text=SAMPLE_INCOMPLETE_CONTRACT,
        expected_agents=["contract_analysis_agent"]
    )
    results.append(run_case(
        graph, memory_thread,
        "Memory turn 2 (follow-up, no re-upload)",
        "Now check that same contract for compliance.",
        document_text=None,  # deliberately NOT re-sending the document
        check_fn=lambda r: assert_true(
            r.get("compliance_report") and "error" not in r["compliance_report"],
            "compliance_report should succeed using remembered document_text from turn 1"
        )
    ))

    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"\n=== {passed}/{total} scenarios passed ===")
    if passed != total:
        sys.exit(1)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    main()