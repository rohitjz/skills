#!/usr/bin/env python3
"""
Eval harness for the PM writing skill. Standard library only, nothing to install.

For each sample it scores two drafts of the same message, one written WITHOUT the
skill and one WITH it, on two tracks:

  1. Objective metrics (computed in code, fully reproducible):
       - word count
       - AI-tell count: em-dashes, AI-vocabulary words, hedges, and filler phrases

  2. An LLM-as-judge rubric (0-5 on six dimensions, 30 max), so the quality
     judgment comes from an independent model, not from the author.

Config via environment variables (no secrets in this file):

  Azure OpenAI:
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT (default gpt-4o), AZURE_OPENAI_API_VERSION (default 2024-10-21)

  Or any OpenAI-compatible API:
    OPENAI_API_KEY, OPENAI_BASE_URL (default https://api.openai.com/v1), OPENAI_MODEL (default gpt-4o)

Run:  python3 evals/run_evals.py
Writes evals/results.json and prints a scorecard.
"""
import os, re, json, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = json.load(open(os.path.join(HERE, "samples.json")))

# --- Objective metrics ------------------------------------------------------
AI_VOCAB = ["delve", "crucial", "landscape", "tapestry", "foster", "underscore",
            "showcase", "leverage", "leverages", "pivotal", "paradigm", "seamless",
            "seamlessly", "groundbreaking", "transformative", "revolutionize",
            "empower", "optimize", "streamline", "robust", "cutting-edge",
            "innovative", "curate"]
HEDGES = ["very", "really", "somewhat", "probably", "potentially", "sort of",
          "kind of", "a bit", "a number of", "i think", "i believe"]
FILLER = ["i wanted to", "reach out", "it's important to note",
          "it is important to note", "happy to discuss", "let me know your thoughts",
          "as part of our ongoing", "i am pleased to announce", "i am confident",
          "thrilled", "excited", "commitment to excellence"]

def count_words(text):
    return len(re.findall(r"\b\w+\b", text))

def count_tells(text):
    t = text.lower()
    em = text.count("—")
    vocab = sum(len(re.findall(r"\b" + re.escape(w) + r"\b", t)) for w in AI_VOCAB)
    hedge = sum(len(re.findall(r"\b" + re.escape(w) + r"\b", t)) for w in HEDGES)
    fill = sum(t.count(p) for p in FILLER)
    return em + vocab + hedge + fill

# --- LLM judge (OpenAI-compatible, stdlib only) -----------------------------
RUBRIC = """You are a strict, consistent evaluator of business and product-management writing.
Score the DRAFT on each dimension from 0 (poor) to 5 (excellent):
- lead_strength: does the first sentence carry the main point with no warm-up?
- concision: every word earns its place; no padding or hedging.
- concreteness: specific numbers and nouns, not vague claims.
- clarity_of_ask: the single takeaway or requested action is unmistakable.
- voice_no_ai_tells: free of AI tells (em-dashes, words like leverage/crucial/seamless, significance inflation, empty enthusiasm).
- reader_fit: tone and length fit the stated audience.
Return ONLY a JSON object with those six integer keys."""

DIMS = ["lead_strength", "concision", "concreteness", "clarity_of_ask",
        "voice_no_ai_tells", "reader_fit"]

def chat(messages):
    """One chat-completion call. Returns (content_str, model_label)."""
    az = os.environ.get("AZURE_OPENAI_ENDPOINT")
    if az:
        dep = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
        ver = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21")
        url = az.rstrip("/") + f"/openai/deployments/{dep}/chat/completions?api-version={ver}"
        headers = {"api-key": os.environ["AZURE_OPENAI_KEY"], "Content-Type": "application/json"}
        body = {"messages": messages, "temperature": 0,
                "response_format": {"type": "json_object"}}
        label = dep
    else:
        base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        url = base + "/chat/completions"
        headers = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
                   "Content-Type": "application/json"}
        label = os.environ.get("OPENAI_MODEL", "gpt-4o")
        body = {"model": label, "messages": messages, "temperature": 0,
                "response_format": {"type": "json_object"}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"], label

def judge(audience, draft):
    content, label = chat([
        {"role": "system", "content": RUBRIC},
        {"role": "user", "content": f"Audience: {audience}\n\nDRAFT:\n{draft}"}])
    sc = json.loads(content)
    return {d: int(sc.get(d, 0)) for d in DIMS}, label

def main():
    rows, agg, model = [], {"without": 0, "with": 0}, None
    for s in SAMPLES:
        row = {"id": s["id"], "task": s["task"], "audience": s["audience"]}
        for cond in ("without", "with"):
            draft = s[cond]
            scores, model = judge(s["audience"], draft)
            total = sum(scores.values())
            row[cond] = {"scores": scores, "total": total,
                         "words": count_words(draft), "ai_tells": count_tells(draft)}
            agg[cond] += total
        rows.append(row)

    out = {"judge_model": model, "max_per_sample": 30,
           "n_samples": len(rows), "aggregate": agg, "rows": rows}
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=2)

    print(f"\nJudge model: {model}   ({len(rows)} samples, 30 pts each)\n")
    print(f"{'Sample':<26}{'Without':>9}{'With':>8}{'Delta':>7}{'Words':>13}{'AI-tells':>12}")
    print("-" * 76)
    for r in rows:
        w, wi = r["without"], r["with"]
        print(f"{r['id']:<26}{w['total']:>6}/30{wi['total']:>5}/30{wi['total']-w['total']:>+7}"
              f"{(str(w['words'])+'->'+str(wi['words'])):>13}{(str(w['ai_tells'])+'->'+str(wi['ai_tells'])):>12}")
    n = len(rows)
    print("-" * 76)
    print(f"{'AGGREGATE':<26}{agg['without']:>4}/{n*30}{agg['with']:>5}/{n*30}{agg['with']-agg['without']:>+7}")

if __name__ == "__main__":
    main()
