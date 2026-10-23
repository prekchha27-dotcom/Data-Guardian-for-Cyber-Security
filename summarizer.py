"""
Summarization service for Data Guardian.

Uses a LOCAL extractive summarizer built entirely from Python's standard library.
No API key, no internet connection, no extra packages needed.

How it works (plain English):
  1. The pasted policy text is split into sentences.
  2. Each sentence gets a score based on how often its key words appear in the
     whole document (more common words = more important sentence).
  3. The highest-scoring sentences are selected and arranged under the headings
     that match the chosen policy category.
  4. The result is labelled clearly as a basic extractive summary, not legal advice.

Limitation: this summarizer copies real sentences from the document — it does not
rewrite or interpret them. It works best on long, structured documents. Short or
unusual documents may produce incomplete results.
"""

import re
import math
import heapq
import textwrap
import collections

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_MAX_CHARS   = 300_000   # generous limit for a local summarizer
_MIN_CHARS   = 200
AI_CONFIGURED = False    # no external AI — local summarizer is always available

# Common English stopwords — excluded from keyword scoring
_STOPWORDS = {
    "a","about","above","after","all","also","an","and","any","are","as","at",
    "be","been","being","but","by","can","do","each","for","from","get","had",
    "has","have","he","her","him","his","how","if","in","into","is","it","its",
    "just","may","me","more","most","my","no","not","of","on","one","or","our",
    "out","shall","she","so","some","than","that","the","their","them","then",
    "there","these","they","this","those","to","up","us","was","we","were",
    "what","when","which","who","will","with","would","you","your",
    # legal filler words
    "including","without","limitation","hereby","thereof","therein","herein",
    "pursuant","provided","accordance","whether","otherwise","however","therefore",
}

# ---------------------------------------------------------------------------
# Category-specific section headings
# ---------------------------------------------------------------------------
_HEADINGS = {
    "privacy_policy": [
        "Information Collected",
        "Why Information Is Collected",
        "How Information Is Used",
        "Information Sharing",
        "Advertising and Personalization",
        "User Privacy Controls",
        "Data Retention and Account Deletion",
        "Security and Privacy Risks",
        "What This Means for You",
        "Important Things to Watch Out For",
    ],
    "terms_of_service": [
        "Who Can Use the Service",
        "Rights You Grant the Platform",
        "Privacy",
        "Personalization and Recommendations",
        "Moderation, Enforcement and Appeals",
        "User Responsibilities and Prohibited Activities",
        "Account Suspension and Termination",
        "Payments and Subscriptions",
        "Third-Party Services",
        "Intellectual Property and Ownership",
        "Changes to the Terms",
        "Disputes and Governing Law",
        "Liability and Disclaimers",
        "What This Means for You",
    ],
    "community_guidelines": [
        "What Is Allowed",
        "What Is Prohibited",
        "Harassment, Abuse, Spam and Scams",
        "Content Restrictions",
        "Reporting Violations",
        "Moderation and Enforcement",
        "Content Removal and Account Suspension",
        "Appeals",
        "What This Means for You",
    ],
    "third_party": [
        "What Counts as a Third-Party Service",
        "Examples Relevant to the Platform",
        "Responsibility for Third-Party Content",
        "External Links and Applications",
        "Data Sharing and Privacy Risks",
        "Disclaimers and Liability",
        "Precautions Users Can Take",
        "What This Means for You",
    ],
    "limitation_liability": [
        "What the Platform Says It Is Responsible For",
        "Types of Losses or Damages Covered",
        "Liability Limits and Financial Caps",
        "Disclaimers and Service Availability",
        "Exceptions and Protected Legal Rights",
        "Practical Examples",
        "What This Means for You",
    ],
    "arbitration": [
        "Does the Agreement Contain an Arbitration Clause?",
        "Individual Arbitration",
        "Class Action Waiver",
        "Jury Trial Waiver",
        "Exceptions and Small-Claims Options",
        "Opt-Out Procedures, If Available",
        "Notice and Dispute-Resolution Steps",
        "Applicable Country or Region",
        "What This Means for You",
    ],
}

# Keywords that help match sentences to each heading
_HEADING_KEYWORDS = {
    "Information Collected":               ["collect","gather","receive","information","data","personal"],
    "Why Information Is Collected":        ["purpose","why","reason","order to","in order","so that"],
    "How Information Is Used":             ["use","process","provide","improve","develop","service"],
    "Information Sharing":                 ["share","third","partner","disclose","transfer","sell","provide to"],
    "Advertising and Personalization":     ["advertis","personaliz","recommend","target","interest","ad "],
    "User Privacy Controls":               ["control","opt","delete","access","request","manage","right"],
    "Data Retention and Account Deletion": ["retain","retention","delet","remov","period","store"],
    "Security and Privacy Risks":          ["secur","protect","breach","risk","encrypt","unauthoriz"],
    "What This Means for You":             ["you","your","user"],
    "Important Things to Watch Out For":   ["important","note","aware","caution","warn"],
    "Who Can Use the Service":             ["age","eligib","account","register","user","minor","13","18"],
    "Rights You Grant the Platform":       ["license","grant","content","rights","royalt","worldwide"],
    "Privacy":                             ["privacy","personal","data","information"],
    "Personalization and Recommendations": ["personaliz","recommend","suggest","feed","algorith"],
    "Moderation, Enforcement and Appeals": ["enforce","moderat","appeal","review","decision","action"],
    "User Responsibilities and Prohibited Activities": ["prohibit","must not","may not","responsib","forbidden","illegal"],
    "Account Suspension and Termination":  ["suspend","terminat","ban","remov","close","account"],
    "Payments and Subscriptions":          ["payment","subscript","fee","charge","purchas","billing"],
    "Third-Party Services":                ["third","partner","external","link","integrat"],
    "Intellectual Property and Ownership": ["intellectu","copyright","trademark","own","propert"],
    "Changes to the Terms":                ["change","updat","modif","amend","revise","new version"],
    "Disputes and Governing Law":          ["dispute","govern","law","jurisdict","court","legal"],
    "Liability and Disclaimers":           ["liabilit","disclaim","warrant","damage","loss","responsible"],
    "What Is Allowed":                     ["allow","permit","may","can","accept"],
    "What Is Prohibited":                  ["prohibit","not allow","forbid","violat","illegal","must not"],
    "Harassment, Abuse, Spam and Scams":   ["harass","abuse","spam","scam","bully","threat","intimidat"],
    "Content Restrictions":                ["content","restrict","adult","graphic","violent","nudity"],
    "Reporting Violations":                ["report","flag","complain","submit","notify"],
    "Moderation and Enforcement":          ["moderat","enforce","review","action","team"],
    "Content Removal and Account Suspension": ["remov","delet","suspend","terminat","taken down"],
    "Appeals":                             ["appeal","contest","review","object","disput decision"],
    "What Counts as a Third-Party Service":["third party","external","integrat","app","plugin","service"],
    "Examples Relevant to the Platform":   ["example","such as","includ","like"],
    "Responsibility for Third-Party Content": ["responsib","liab","not responsible","no control"],
    "External Links and Applications":     ["link","url","website","click","redirect"],
    "Data Sharing and Privacy Risks":      ["share","data","privacy","risk","access","third"],
    "Disclaimers and Liability":           ["disclaim","liab","warrant","not responsible"],
    "Precautions Users Can Take":          ["recommend","suggest","best practice","should","careful"],
    "What the Platform Says It Is Responsible For": ["responsib","liable","accountab","obligat"],
    "Types of Losses or Damages Covered":  ["damage","loss","harm","cost","injur","consequential"],
    "Liability Limits and Financial Caps": ["cap","limit","maximum","dollar","amount","exceed"],
    "Disclaimers and Service Availability":["disclaim","availab","uninterrupt","downtime","warrant"],
    "Exceptions and Protected Legal Rights":["except","notwithstanding","consumer","rights","law"],
    "Practical Examples":                  ["example","such as","instance","scenario"],
    "Does the Agreement Contain an Arbitration Clause?": ["arbitrat","binding","clause"],
    "Individual Arbitration":              ["individual","arbitrat","binding","private"],
    "Class Action Waiver":                 ["class action","waiver","group","collective"],
    "Jury Trial Waiver":                   ["jury","trial","waiver","court"],
    "Exceptions and Small-Claims Options": ["small claim","exception","court","opt"],
    "Opt-Out Procedures, If Available":    ["opt out","opt-out","optout","30 day","written notice"],
    "Notice and Dispute-Resolution Steps": ["notice","informal","negotiat","attempt","60 day","30 day"],
    "Applicable Country or Region":        ["india","united states","country","region","jurisdict","applicable"],
}


# ---------------------------------------------------------------------------
# Core extractive summarizer
# ---------------------------------------------------------------------------

def _sentences(text: str) -> list:
    """Split text into sentences."""
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in raw if len(s.strip()) > 30]


def _score_sentences(sentences: list) -> dict:
    """Score each sentence by TF-IDF-inspired word frequency."""
    word_freq: collections.Counter = collections.Counter()
    for sent in sentences:
        for word in re.findall(r'\b[a-z]{3,}\b', sent.lower()):
            if word not in _STOPWORDS:
                word_freq[word] += 1

    # Normalize by total sentences (IDF-lite)
    n = max(len(sentences), 1)
    scores = {}
    for i, sent in enumerate(sentences):
        words = re.findall(r'\b[a-z]{3,}\b', sent.lower())
        score = sum(
            word_freq[w] / n for w in words if w not in _STOPWORDS
        )
        # Slight boost for sentences that start with a capital word or number
        if re.match(r'^[A-Z0-9]', sent):
            score *= 1.1
        scores[i] = score
    return scores


def _top_sentences(sentences: list, scores: dict, n: int) -> list:
    """Return the top-n scoring sentences in their original order."""
    top_indices = heapq.nlargest(n, scores, key=lambda i: scores[i])
    top_indices_sorted = sorted(top_indices)
    return [sentences[i] for i in top_indices_sorted]


def _match_heading(sentences: list, heading: str) -> list:
    """Return sentences most relevant to a given heading (up to 3)."""
    keywords = _HEADING_KEYWORDS.get(heading, [heading.lower().split()])
    matched = []
    for sent in sentences:
        s_lower = sent.lower()
        if any(kw.lower() in s_lower for kw in keywords):
            matched.append(sent)
    return matched[:3]


def _build_summary(platform: str, category_key: str, sentences: list, scores: dict) -> str:
    """Build a structured summary organized under category-specific headings."""
    headings = _HEADINGS.get(category_key, ["Summary"])
    lines = []

    lines.append(
        f"## Extractive Summary: {platform} — "
        + {
            "privacy_policy":       "Privacy Policy",
            "terms_of_service":     "Terms of Service",
            "community_guidelines": "Community Guidelines",
            "third_party":          "Third-Party Material & Services",
            "limitation_liability": "Limitation of Liability",
            "arbitration":          "Arbitration & Legal Dispute Waivers",
        }.get(category_key, category_key)
    )
    lines.append("")
    lines.append(
        "⚠️ **This is a basic extractive summary.** It copies real sentences from "
        "the document you pasted — it does not rewrite, interpret, or add legal meaning. "
        "It is not legal advice. Always read the original official document."
    )
    lines.append("")

    found_any = False
    top_global = set(_top_sentences(sentences, scores, min(30, len(sentences))))

    for heading in headings:
        matched = _match_heading(sentences, heading)
        # If no keyword match, fall back to top global sentences not yet used
        if not matched:
            fallback = [s for s in top_global if s not in
                        [m for sublist in [_match_heading(sentences, h) for h in headings] for m in sublist]]
            matched = fallback[:1]
        if matched:
            lines.append(f"### {heading}")
            for sent in matched:
                wrapped = textwrap.fill(sent, width=100)
                lines.append(f"- {wrapped}")
            lines.append("")
            found_any = True

    if not found_any:
        lines.append("The pasted text did not contain enough recognizable content to organize under headings.")
        lines.append("Try pasting a longer section of the policy document.")

    lines.append("---")
    lines.append(
        "_This summary was generated locally on your device using a basic sentence-extraction "
        "method. No data was sent to any server or AI service. For accurate legal understanding, "
        "consult the original document or a qualified legal professional._"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API  (same interface as before — no other files need to change)
# ---------------------------------------------------------------------------

def summarize(platform: str, category_key: str, policy_text: str) -> dict:
    """
    Summarize the supplied policy text using local extraction.

    Returns a dict with keys:
      ok      (bool) — True if a summary was produced
      summary (str)  — the summary text, or "" on failure
      error   (str)  — human-readable error, or "" on success
      source  (str)  — always "local" for this implementation
    """
    text = policy_text.strip()

    if not text:
        return {
            "ok": False,
            "summary": "",
            "error": "No policy text was provided. Paste the full policy document into the text area first.",
            "source": "local",
        }

    if len(text) < _MIN_CHARS:
        return {
            "ok": False,
            "summary": "",
            "error": (
                f"The pasted text is too short ({len(text)} characters). "
                "Please paste the complete policy document for a useful summary."
            ),
            "source": "local",
        }

    if len(text) > _MAX_CHARS:
        return {
            "ok": False,
            "summary": "",
            "error": (
                f"The pasted text is very long ({len(text):,} characters). "
                f"The limit is {_MAX_CHARS:,} characters. "
                "Try pasting one section at a time."
            ),
            "source": "local",
        }

    try:
        sents  = _sentences(text)
        if len(sents) < 3:
            return {
                "ok": False,
                "summary": "",
                "error": "The pasted text could not be split into enough sentences. Try pasting more complete paragraphs.",
                "source": "local",
            }
        scores  = _score_sentences(sents)
        summary = _build_summary(platform, category_key, sents, scores)
        return {"ok": True, "summary": summary, "error": "", "source": "local"}
    except Exception as exc:
        return {
            "ok": False,
            "summary": "",
            "error": f"Summarization error: {exc}",
            "source": "local",
        }
