from flask import Flask, render_template, request, jsonify
import re
import tldextract

app = Flask(__name__)

def check_url_safety(url):

    issues = []

    # 1 - HTTPS or not
    if url.startswith("http://"):
        issues.append("❗ Uses unsecure HTTP instead of HTTPS")

    # 2 - Domain analysis
    ext = tldextract.extract(url)
    domain = ext.domain

    if len(domain) > 15:
        issues.append("❗ Unusually long domain name")

    if re.search(r"\d", domain):
        issues.append("❗ Domain contains numbers (common in fake sites)")

    # 3 - Phishing keywords
    phishing_words = ["free", "win", "prize", "bonus", "gift", "verify", "secure"]
    if any(word in url.lower() for word in phishing_words):
        issues.append("❗ Contains phishing-related keywords")

    # 4 - Shorteners
    shorteners = ["bit.ly", "tinyurl", "t.co"]
    if any(s in url for s in shorteners):
        issues.append("⚠ URL shortener detected (destination hidden)")

    safe = len(issues) == 0

    return {
        "safe": safe,
        "summary": "No major red flags found. Looks safe!" if safe else "Suspicious patterns detected!",
        "issues": issues if not safe else ["✔ URL passed all safety checks"]
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_link():
    url = request.get_json().get("url")
    return jsonify(check_url_safety(url))


if __name__ == "__main__":
    app.run(debug=True)
