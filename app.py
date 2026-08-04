from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/fraud-detection")
def fraud_detection():
    return render_template("fraud_detection.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/ai-investigator")
def ai():
    return render_template("ai_investigator.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)