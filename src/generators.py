import json
from src.bedrock_client import invoke_claude
from src.vectorstore import retrieve_context
from src.prompts import TEST_CASE_SYSTEM, EDGE_CASE_SYSTEM, RISK_SYSTEM
from src.schemas import TestCase, EdgeCase, QualityRisk

def _parse_json_array(raw: str) -> list:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned.strip())

def generate_test_cases(requirement: dict) -> list:
    context = retrieve_context(requirement["text"])
    prompt = f"Requirement {requirement['id']}: {requirement['text']}\n\nReference context:\n{context}"
    system = TEST_CASE_SYSTEM.format(schema=TestCase.model_json_schema())
    raw = invoke_claude(system, prompt, max_tokens=2000)
    try:
        return [TestCase(**tc) for tc in _parse_json_array(raw)]
    except Exception:
        return []

def generate_edge_cases(requirement: dict, existing: list) -> list:
    context = retrieve_context(requirement["text"])
    titles = [tc.title for tc in existing]
    prompt = f"Requirement {requirement['id']}: {requirement['text']}\n\nExisting: {titles}\n\nContext:\n{context}"
    system = EDGE_CASE_SYSTEM.format(schema=EdgeCase.model_json_schema())
    raw = invoke_claude(system, prompt, max_tokens=1500)
    try:
        return [EdgeCase(**ec) for ec in _parse_json_array(raw)]
    except Exception:
        return []

def generate_risks(requirement: dict, doc_context: str) -> list:
    prompt = f"Requirement {requirement['id']}: {requirement['text']}\n\nDoc context:\n{doc_context[:2000]}"
    system = RISK_SYSTEM.format(schema=QualityRisk.model_json_schema())
    raw = invoke_claude(system, prompt, max_tokens=1000)
    try:
        return [QualityRisk(**r) for r in _parse_json_array(raw)]
    except Exception:
        return []