import re
import tldextract

def check_url_safety(url):

    issues = []

    # 1. Check for http vs https
    if url.startswith("http://"):
        issues.append("❗ Uses 'http' instead of secure 'https'")

    # 2. Check for suspicious domain
    extracted = tldextract.extract(url)
    domain = extracted.domain
    suffix = extracted.suffix

    if len(domain) > 15:
        issues.append("❗ Domain name looks unusually long")

    # 3. Check for numbers in the domain
    if re.search(r"\d", domain):
        issues.append("❗ Domain contains numbers (often used by fake sites)")

    # 4. Check for phishing patterns
    phishing_keywords = ["free", "win", "prize", "bonus", "gift", "verify", "login", "secure"]
    if any(word in url.lower() for word in phishing_keywords):
        issues.append("❗ Contains suspicious phishing keywords")

    # 5. Check for URL shorteners
    shorteners = ["bit.ly", "tinyurl", "shorturl", "t.co"]
    if any(s in url for s in shorteners):
        issues.append("⚠ Detected URL shortener — could hide real destination")

    # Final output
    if issues:
        return {"url": url, "safe": False, "issues": issues}
    else:
        return {"url": url, "safe": True, "issues": ["✔ No major issues found. Seems safe!"]}
