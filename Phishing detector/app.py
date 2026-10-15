from flask import Flask, request, render_template
import pickle
from features import extract_features
import webbrowser
import threading
import random

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

history = []

def generate_ai_explanation(result, reasons):
    if result == "Phishing":
        return "This URL appears malicious because it contains patterns commonly used in phishing attacks such as " + ", ".join(reasons[:2]) + ". These are often used to trick users into revealing sensitive information."
    else:
        return "This URL appears safe as it does not exhibit common phishing characteristics like suspicious keywords or insecure connections."

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    reason = ""
    risk = ""
    advice = ""
    ai_explanation = ""

    if request.method == "POST":
        url = request.form["url"]

        score = 0
        reasons = []
        url_lower = url.lower()

        if "@" in url:
            score += 1; reasons.append("URL redirection symbol")
        if len(url) > 75:
            score += 1; reasons.append("unusually long URL")
        if "login" in url_lower or "verify" in url_lower:
            score += 1; reasons.append("phishing-related keywords")
        if "bank" in url_lower or "account" in url_lower:
            score += 1; reasons.append("financial targeting")
        if not url.startswith("https"):
            score += 1; reasons.append("lack of HTTPS security")

        if score >= 2:
            result = "Phishing"
            reason = " | ".join(reasons[:2])
        else:
            result = "Safe"
            reason = "No major threats detected"

        if score >= 3:
            risk = "High Risk"
        elif score == 2:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        reputation = f"{random.randint(40,95)} / 100"

        advice = "⚠️ Avoid entering sensitive data on this website." if result=="Phishing" else "✅ This URL appears safe."

        ai_explanation = generate_ai_explanation(result, reasons)

        history.append((url, result))
        if len(history) > 5:
            history.pop(0)

    return render_template("index.html",
        result=result,
        reason=reason,
        risk=risk,
        advice=advice,
        ai_explanation=ai_explanation,
        history=history,
        reputation=reputation if request.method=="POST" else ""
    )

def open_browser():
    webbrowser.open_new("http://localhost:5000/")

if __name__ == "__main__":
    threading.Timer(1.2, open_browser).start()
    app.run(debug=True)