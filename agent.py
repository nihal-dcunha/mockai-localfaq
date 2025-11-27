# MockAI LocalFAQ Assistant 
# Fully local Python FAQ agent/bot (“LLM-like FAQ bot”) without any AI.
# Local FAQ assistant that feels AI-like but doesn’t actually call a model.
#----------------------------
# 
# How it works
#
# Loads documents from the docs/ folder.
# Parses FAQ-style files into {question: answer} pairs.
# Fuzzy matches your user question to the closest FAQ question using rapidfuzz.
#    Example: “password” → “How do I reset my password?”
# Polishes the answer slightly (removes backticks, adds a friendly prefix) to make it feel “assistant-like.”
# Interactive loop lets you type questions and get answers.
# 
# Where “AI” is faked
#   The script pretends to be smart by matching questions fuzzily and slightly rewording answers.
#   There’s no natural language understanding or generation like GPT.
#   It’s entirely rule-based: matching strings + some text cleanup.
# ----------------------------
# 
# Project structure
#
# faq-agent/
# ├─ docs/             ← put .txt or .md docs here
# │    ├─ pricing.txt
# │    ├─ faq.md
# │    └─ support.md
# └─ agent.py           ← Python script
#` 
# ----------------------------
# 
# Run it 
# python agent.py
#
#----------------------------
# 
# Smart matching
# - Will match questions with different phrasing:
#     “Where logs” → “Where are logs stored?”
#     “location of logs” → “Where are logs stored?”
#     “Where are the application log files stored?” → same FAQ
# - Short queries (“password”) are matched correctly.
# - Nonsense queries (“qlll”, “reee”) will not match (returns not found).
#
# Fuzzy matching details:
# - Uses rapidfuzz’s token_set_ratio.
# - Dynamic threshold based on query length.
# - Minimum floor prevents nonsense matches.
#
# Polished responses:
# - Removes raw markdown backticks.
# - Adds a natural “Here’s what I found:” prefix.
# - Highlights the matched FAQ question in green.
#
# Interactive loop:
# - Users can ask multiple questions.
# - Type "exit" or "quit" to end the program.
#
# ----------------------------
import os
import re
from colorama import init, Fore, Style
from rapidfuzz import fuzz

# Initialize colorama
init(autoreset=True)

# ----------------------------
# 1) Load ALL docs
# ----------------------------
def load_docs(folder):
    # Check folder exists
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Docs folder not found: {folder}")

    docs = {}
    # Loop through all files in folder
    for filename in os.listdir(folder):
        if filename.endswith((".txt", ".md")):
            # Read file content as UTF-8 string
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    # Return dict: {filename: content}
    return docs


# ----------------------------
# 2) Parse FAQ file into {question: answer}

# Scan the FAQ file line-by-line.
# Whenever you see “## ”, that’s a question.
# Everything after it — until the next “## ” — is that question’s answer.
# Save each Q/A pair into a dictionary. i.e., when a new question appears, the previous question must be finalized and saved before we move on.
# Return the dictionary.
#     qas = {
#            "How do I install the product?": "Run `install.exe` and follow the prompts.",
#            "How do I reset my password?": "Go to Settings > Security > Reset Password.",
#            "Where are logs stored?": "Logs are stored in `C:\\ProgramData\\MyApp\\logs`."
#           }
# ----------------------------
def parse_faq(md_text):
    qas = {}
    lines = md_text.split("\n")
    current_q = None
    current_a = []

    # Process each line
    for line in lines:
        if line.startswith("## "):  # New question
            if current_q:   # Save previous Q/A if exists
                qas[current_q] = "\n".join(current_a).strip()
            current_q = line.replace("## ", "").strip() # Remove ## prefix
            current_a = []  # reset answer
        else:
            if current_q:
                current_a.append(line)

    # Save last question-answer pair
    if current_q:
        qas[current_q] = "\n".join(current_a).strip()

    return qas

# ----------------------------
# 3) Fuzzy matching: Finds the closest FAQ question even with different phrasing.
# Uses token_set_ratio from rapidfuzz for flexible matching.
# - Dynamic threshold: shorter queries have lower threshold to allow single-word matches.
# - Minimum floor: prevents nonsense queries from accidentally matching.
# 
# Examples:
#   "password"          → matches "How do I reset my password?"
#   "where logs?"       → matches "Where are logs stored?"
#   "reee"              → returns None (not found)
#
# Behavior:
#   - Computes a fuzzy score for each FAQ question.
#   - Picks the question with the highest score.
#   - Compares score to a threshold based on query length and minimum floor.
#   - Returns the matched question if score ≥ threshold, else None.
# ----------------------------
def best_match(user_question, questions):
    best_q = None
    best_score = 0

    # Find FAQ question with highest fuzzy score
    for q in questions: 
        score = fuzz.token_set_ratio(user_question, q) # fuzzy score
        if score > best_score:
            best_score = score
            best_q = q

    # Dynamic threshold based on length of query
    length = len(user_question.split())
    if length <= 2:
        threshold = 40  # short queries can match loosely
    elif length <= 4:
        threshold = 45
    else:
        threshold = 50  # longer queries require stronger match

    # Minimum floor prevents nonsense queries from matching
    floor = 35
    threshold = max(threshold, floor)

    # Return matched question only if score passes threshold
    if best_score >= threshold:
        return best_q
    else:
        return None


# ----------------------------
# 4) Mock AI polish: Removes backticks and adds a “Here’s what I found” prefix.
# Makes the answer feel "assistant-like"
# ----------------------------
def polish_answer(answer_text):
    # If no answer found
    if not answer_text:
        return f"{Fore.RED}I don’t have information about that yet.{Style.RESET_ALL}"

    # Tiny readability tweaks
    cleaned = answer_text.strip()
    cleaned = cleaned.replace("`", "")  # remove markdown backticks

    # Add natural intro and color
    return f"{Fore.CYAN}Here’s what I found:\n\n{cleaned}{Style.RESET_ALL}"

# ----------------------------
# 5) Main Interactive FAQ Agent
# ----------------------------
if __name__ == "__main__":
    # Load all docs
    docs = load_docs("docs")

    # Combine all FAQs into a single dict
    all_qas = {}
    for text in docs.values():
        all_qas.update(parse_faq(text))

    questions = list(all_qas.keys())  # list of FAQ questions

    print(f"{Fore.GREEN}FAQ Agent ready! Type 'exit' to quit.{Style.RESET_ALL}")

    # Interactive loop
    while True:
        question = input(f"{Fore.YELLOW}Ask a question: {Style.RESET_ALL}").strip()
        if question.lower() in ("exit", "quit"):
            print(f"{Fore.MAGENTA}Goodbye!{Style.RESET_ALL}")
            break

        # Find best match
        best_q = best_match(question, questions)
        answer = all_qas.get(best_q)

        if best_q:
            # Highlight matched FAQ question
            print(f"{Fore.GREEN}Matched FAQ question: {best_q}{Style.RESET_ALL}")
            print(polish_answer(answer))
        else:
            print(f"{Fore.RED}Sorry, I couldn’t find anything about that.{Style.RESET_ALL}")

        print("\n" + "-"*40 + "\n")


 
