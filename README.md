# MockAI LocalFAQ Assistant 🚀

Turn your FAQs into a smart, AI-like assistant—completely offline! Ask questions naturally and get instant answers, thanks to fuzzy matching and polished responses. No APIs, no AI, just local Python magic. Perfect for teams, docs, or personal projects that want a “virtual assistant” feel without sending data anywhere.

---

**Features:** Loads FAQ documents from the `docs/` folder (`.txt` or `.md`). Parses FAQ-style files into `{question: answer}` pairs. Fuzzy matches your question to the closest FAQ question using [rapidfuzz](https://github.com/maxbachmann/rapidfuzz). Polishes answers slightly to feel like an assistant (removes backticks, adds friendly prefix). Interactive loop for asking multiple questions. Fully local and rule-based—no AI or online calls.

**Project Structure:**
```
mockai-localfaq/
├─ docs/           ← your FAQ documents (.txt or .md)
│    ├─ faq.md
│    ├─ support.md
│    └─ pricing.txt
├─ agent.py        ← main Python script
├─ requirements.txt← Python dependencies
└─ README.md       ← this file
```

**Example FAQ File (`docs/faq.md`):**
```
## How do I reset my password?
Go to Settings > Security > Reset Password.

## Where are logs stored?
Logs are stored in `C:\ProgramData\MyApp\logs`.
```

**Installation:**
1. Clone the repository:
```
git clone https://github.com/nihal-dcunha/mockai-localfaq.git
cd mockai-localfaq
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Add your FAQ files to the `docs/` folder.

**Usage:** Run the agent:
```
python agent.py
```
Then ask questions interactively:
```
Ask a question: password
Matched FAQ question: How do I reset my password?
Here’s what I found:
Go to Settings > Security > Reset Password.
```
Type `exit` or `quit` to leave.

**How It Works:** Loads all `.txt`/`.md` files from `docs/`, parses FAQs into `{question: answer}` pairs, fuzzy matches user queries to the closest FAQ, polishes answers to feel assistant-like, and loops interactively until you exit.

**Fuzzy Matching Details:** Short queries match loosely, long queries require stronger matches. Nonsense queries return a “not found” message. Dynamic thresholds prevent accidental matches.

**Notes:** Works offline. Best with clear FAQ-style docs. Highlighted matched questions shown in green.

**License:** MIT License
