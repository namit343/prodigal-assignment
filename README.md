# Conversation Compliance & Quality Analyzer

This project analyzes debt collection call transcripts for **profanity**, **privacy/compliance violations**, and **call quality metrics** (silence & overtalk).  
It supports both **regex-based pattern matching** and **LLM-based analysis**.

---

## 🚀 Features
- **Profanity Detection**
  - Detects if **agent** or **customer** used profane language.
  - Implemented with regex (pattern matching) and LLM.
- **Privacy & Compliance**
  - Flags when agents disclose **sensitive financial/account info** before verifying identity.
  - Implemented with regex (pattern matching) and LLM.
- **Call Quality Metrics**
  - Calculates **silence %** and **overtalk %** in calls.
  - Displays bar chart visualizations.
- **Streamlit App**
  - Upload a `.json` conversation file.
  - Dropdowns to select **Approach** (Pattern Matching / LLM) and **Analysis Type** (Profanity / Compliance / Metrics).
  - Interactive output + visualization.

---

## 🗂️ Project Structure
```
conversation-analyzer/
│
├── main.py          # Backend functions (pattern + LLM)
├── app.py           # Streamlit frontend
├── requirements.txt # Dependencies
├── data/            # Folder containing JSON call transcripts
└── README.md        # Documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/conversation-analyzer.git
cd conversation-analyzer
```

### 2. Create and activate a virtual environment (Windows)
```bash
py -m venv .venv
.\.venv\Scripts ctivate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run locally
```bash
py -m streamlit run app.py
```
App will open at [http://localhost:8501](http://localhost:8501).

---

## ☁️ Deployment (Streamlit Cloud)
1. Push repo to GitHub.  
2. Go to [Streamlit Cloud](https://share.streamlit.io).  
3. Deploy `app.py` as entry point.  
4. Add your OpenAI API key in **App Secrets**:
   ```toml
   OPENAI_API_KEY="your_api_key_here"
   ```

---

## 📊 Example Workflow
- Upload a conversation JSON file.  
- Select `Pattern Matching` + `Profanity Detection` → see if agent or customer used profanity.  
- Select `Pattern Matching` + `Privacy & Compliance` → check for violations.  
- Select `Call Metrics` → see silence/overlap percentages + chart.  
- Switch to `LLM` approach to compare results.

---

## 🧠 Comparative Analysis (Summary)

### Profanity Detection
- Regex is reliable because profanity is explicit and has a finite vocabulary.  
- LLM may overcomplicate, slower, and cost API credits.  
- ✅ Recommendation: **Pattern Matching** is better for profanity.

### Privacy & Compliance
- Regex catches obvious disclosures (balance, account number, etc.) but may miss indirect/nuanced cases.  
- LLM can interpret natural language better and detect subtle compliance risks.  
- ✅ Recommendation: **LLM** is better for compliance in production.

### Call Quality Metrics
- Purely numeric (based on timestamps). Regex/ML not applicable.  
- Deterministic calculation with silence and overlap detection.  
- ✅ Recommendation: Use **deterministic computation** (no AI needed).

---

## 📌 Deliverables
1. **GitHub Repository**  
   - Includes backend (`main.py`), frontend (`app.py`), visualization, requirements, README.  

2. **Technical Report**  
   - Implementation explanation + recommendations.
