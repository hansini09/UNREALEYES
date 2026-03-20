import re
import urllib.parse

# ---------------- STRUCTURE ----------------
def analyze_structure(text):
    score = 0
    findings = []

    if len(text) > 50:
        upper = sum(1 for c in text if c.isupper())
        if upper / len(text) > 0.3:
            score += 3
            findings.append("Too many capital letters")

    if text.count('!') > 3:
        score += 2
        findings.append("Too many exclamation marks")

    if re.search(r'dear (customer|user)', text.lower()):
        score += 2
        findings.append("Generic greeting")

    return score, findings


# ---------------- DOMAIN TRICKS ----------------
def analyze_domain(url):
    score = 0
    findings = []

    try:
        domain = urllib.parse.urlparse(url).netloc.lower()

        if "@" in domain:
            score += 5
            findings.append("Hidden domain using @ trick")

        if "-" in domain:
            score += 2
            findings.append("Suspicious hyphen in domain")

    except:
        pass

    return score, findings


# ---------------- LINKS ----------------
def analyze_links(text):
    score = 0
    findings = []

    urls = re.findall(r'https?://[^\s]+', text)

    for url in urls:
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            score += 5
            findings.append("IP address link")

        d_score, d_find = analyze_domain(url)
        score += d_score
        findings.extend(d_find)

    return score, findings


# ---------------- PSYCHOLOGY ----------------
def analyze_psychology(text):
    score = 0
    findings = []

    if re.search(r'urgent|asap|immediately', text.lower()):
        score += 3
        findings.append("Time pressure tactic")

    if re.search(r'suspend|blocked|legal', text.lower()):
        score += 4
        findings.append("Threat language")

    if re.search(r'won|free money|100%', text.lower()):
        score += 3
        findings.append("Unrealistic reward")

    return score, findings


# ---------------- MAIN ----------------
def check_content(text, type="text"):
    structure_score, structure_findings = analyze_structure(text)
    link_score, link_findings = analyze_links(text)
    psych_score, psych_findings = analyze_psychology(text)

    total = structure_score + link_score + psych_score

    if total >= 10:
        result = "🚨 High Risk – Likely Scam"
        color = "red"
        confidence = 90
        explanation = "This message shows multiple strong scam indicators such as urgency, threats, and suspicious links."
        advice = "Do NOT click any links or share personal information. Ignore or report this message."

    elif total >= 5:
        result = "⚠ Medium Risk – Suspicious"
        color = "orange"
        confidence = 60
        explanation = "This content contains some suspicious patterns that may indicate phishing or manipulation."
        advice = "Be cautious. Verify the source before taking any action."

    else:
        result = "✅ Low Risk – Appears Safe"
        color = "green"
        confidence = 20
        explanation = "No major scam patterns detected. The content appears mostly safe."
        advice = "Still stay alert and verify unknown messages."

    return {
        "result": result,
        "color": color,
        "confidence": confidence,
        "explanation": explanation,
        "advice": advice,
        "structure": structure_findings,
        "links": link_findings,
        "psychology": psych_findings
    }