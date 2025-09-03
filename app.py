import streamlit as st
import json
import matplotlib.pyplot as plt
from main import (
    load_conversation_json,
    detect_profanity,
    detect_privacy_violation,
    compute_call_metrics,
    llm_check_profanity,
    llm_check_compliance
)

st.title("Conversation Compliance & Quality Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload a conversation JSON file", type=["json"])

# Dropdowns
approach = st.selectbox("Select Approach", ["Pattern Matching", "ML/LLM"])
analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Profanity Detection", "Privacy & Compliance", "Call Metrics"]
)

if uploaded_file is not None:
    conversation = json.load(uploaded_file)

    # ------------------------
    # Profanity Detection
    # ------------------------
    if analysis_type == "Profanity Detection":
        if approach == "Pattern Matching":
            result = detect_profanity(conversation)
            st.write("**Profanity Detection (Regex):**")
            st.json(result)
        else:  # LLM
            flags = {"agent_profanity": False, "customer_profanity": False}
            for utt in conversation:
                if llm_check_profanity(utt["text"]):
                    if utt["speaker"].lower() == "agent":
                        flags["agent_profanity"] = True
                    elif utt["speaker"].lower() in ["customer", "borrower"]:
                        flags["customer_profanity"] = True
            st.write("**Profanity Detection (LLM):**")
            st.json(flags)

    # ------------------------
    # Privacy & Compliance
    # ------------------------
    elif analysis_type == "Privacy & Compliance":
        if approach == "Pattern Matching":
            result = detect_privacy_violation(conversation)
            st.write("**Privacy & Compliance (Regex):**")
            st.json(result)
        else:  # LLM
            verified = False
            violation = False
            for utt in conversation:
                spk = utt["speaker"].lower()
                if spk == "agent":
                    if llm_check_compliance(utt["text"], verified):
                        violation = True
                        st.write("⚠️ Violation detected at line:", utt["text"])
                        break
                elif spk in ["customer", "borrower"]:
                    if any(x in utt["text"].lower() for x in ["street", "ssn", "dob", "date of birth"]):
                        verified = True
            st.write("**Privacy & Compliance (LLM):**")
            st.json({"violation": violation})

    # ------------------------
    # Call Metrics
    # ------------------------
    elif analysis_type == "Call Metrics":
        result = compute_call_metrics(conversation)
        st.write("**Call Metrics:**")
        st.json(result)

        # Visualization
        labels = ["Silence %", "Overtalk %"]
        values = [result["silence_pct"], result["overtalk_pct"]]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Percentage")
        ax.set_title("Call Quality Metrics")
        st.pyplot(fig)
