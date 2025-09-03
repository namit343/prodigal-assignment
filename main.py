import os
import json
import re
from typing import List, Dict, Optional
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------
# JSON Loaders
# --------------------------

def load_conversation_json(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_all_conversations_json(folder_path: str) -> Dict[str, List[Dict]]:
    all_conversations = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            call_id = os.path.splitext(file_name)[0]
            all_conversations[call_id] = load_conversation_json(file_path)
    return all_conversations

# --------------------------
# Profanity Detection
# --------------------------

PROFANITY_WORDS = [
    r"\bhell\b", r"\bdamn\b", r"\bshit\b", r"\bfuck\b",
    r"\basshole\b", r"\bbitch\b", r"\bcrap\b"
]
PROFANITY_REGEX = re.compile("|".join(PROFANITY_WORDS), re.IGNORECASE)

def detect_profanity(conversation: List[Dict]) -> Dict[str, bool]:
    agent_flag = False
    customer_flag = False
    for utt in conversation:
        if PROFANITY_REGEX.search(utt["text"]):
            spk = utt["speaker"].lower()
            if spk == "agent":
                agent_flag = True
            elif spk in ["customer", "borrower"]:
                customer_flag = True
    return {"agent_profanity": agent_flag, "customer_profanity": customer_flag}

def scan_profanity_all(all_conversations: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    results = {"agent_profanity_calls": [], "customer_profanity_calls": [], "details": {}}
    for call_id, convo in all_conversations.items():
        result = detect_profanity(convo)
        results["details"][call_id] = result
        if result["agent_profanity"]:
            results["agent_profanity_calls"].append(call_id)
        if result["customer_profanity"]:
            results["customer_profanity_calls"].append(call_id)
    return results

# --------------------------
# Privacy & Compliance
# --------------------------

AGENT_VERIFY_REQ = re.compile(r"(verify|confirm).*(address|date of birth|dob|ssn|social security number)", re.IGNORECASE)
DOB_PATTERN = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
ADDR_HINTS = re.compile(r"\b\d{1,5}\s+\w+.*(street|st|road|rd|avenue|ave|lane|ln|boulevard|blvd|drive|dr)\b", re.IGNORECASE)

CUSTOMER_VERIFIED_RESP = lambda text: (
    bool(DOB_PATTERN.search(text) or SSN_PATTERN.search(text) or ADDR_HINTS.search(text))
)

SENSITIVE_INFO_BY_AGENT = re.compile(
    r"\b(balance|amount\s+due|outstanding\s+balance|you\s+owe|account\s*(number|no\.?)|loan\s*number|last\s*four|card\s*number|routing)\b|\$\s*\d+",
    re.IGNORECASE
)

def detect_privacy_violation(conversation: List[Dict]) -> Dict[str, Optional[object]]:
    verified = False
    verify_requested = False
    for i, utt in enumerate(conversation):
        text = str(utt.get("text", ""))
        speaker = str(utt.get("speaker", "")).strip().lower()

        if speaker == "agent":
            if SENSITIVE_INFO_BY_AGENT.search(text) and not verified:
                return {"violation": True, "first_sensitive_utt_index": i, "evidence": text, "verified_before_sensitive": False}
            if AGENT_VERIFY_REQ.search(text):
                verify_requested = True
        elif speaker in ("customer", "borrower"):
            if verify_requested and CUSTOMER_VERIFIED_RESP(text):
                verified = True
    return {"violation": False, "first_sensitive_utt_index": None, "evidence": None, "verified_before_sensitive": verified}

def scan_privacy_violations_all(all_conversations: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    violating, non_violating, details = [], [], {}
    for call_id, convo in all_conversations.items():
        result = detect_privacy_violation(convo)
        details[call_id] = result
        if result["violation"]:
            violating.append(call_id)
        else:
            non_violating.append(call_id)
    return {"violating_calls": violating, "non_violating_calls": non_violating, "details": details}

# --------------------------
# Call Metrics
# --------------------------

def to_seconds(t) -> float:
    if isinstance(t, (int, float)):
        return float(t)
    if isinstance(t, str):
        parts = t.split(":")
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)
        elif len(parts) == 2:
            m, s = parts
            return int(m) * 60 + float(s)
        else:
            return float(parts[0])
    return 0.0

def compute_call_metrics(conversation: List[Dict]) -> Dict[str, float]:
    if not conversation:
        return {"total_duration": 0, "silence_pct": 0, "overtalk_pct": 0}
    utts = [(to_seconds(u["stime"]), to_seconds(u["etime"])) for u in conversation]
    utts.sort(key=lambda x: x[0])
    total_duration = utts[-1][1] - utts[0][0]
    silence_duration = 0.0
    overtalk_duration = 0.0
    prev_end = utts[0][1]
    for start, end in utts[1:]:
        if start > prev_end:
            silence_duration += start - prev_end
        elif start < prev_end:
            overtalk_duration += prev_end - start
        prev_end = max(prev_end, end)
    return {
        "total_duration": round(total_duration, 2),
        "silence_duration": round(silence_duration, 2),
        "overtalk_duration": round(overtalk_duration, 2),
        "silence_pct": round((silence_duration / total_duration) * 100, 2) if total_duration > 0 else 0,
        "overtalk_pct": round((overtalk_duration / total_duration) * 100, 2) if total_duration > 0 else 0,
    }

def compute_metrics_all(all_conversations: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    return {call_id: compute_call_metrics(convo) for call_id, convo in all_conversations.items()}

def llm_check_profanity(text: str) -> bool:
    """
    Uses LLM to check if text contains profanity.
    """
    prompt = f"Does the following text contain profanity? Answer only Yes or No.\n\nText: {text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o if available
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5
    )
    answer = response.choices[0].message.content.strip().lower()
    return "yes" in answer

def llm_check_compliance(text: str, verified: bool) -> bool:
    """
    Uses LLM to check if text contains sensitive financial/account information
    shared without verification.
    """
    verification_note = "The customer has already been verified." if verified else "The customer has not been verified yet."
    prompt = f"""
    Does the following agent statement disclose sensitive financial/account information 
    (like balance, account number, due amount, etc.)? 
    Answer Yes or No.
    {verification_note}

    Text: {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5
    )
    answer = response.choices[0].message.content.strip().lower()
    return "yes" in answer