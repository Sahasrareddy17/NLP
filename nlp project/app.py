from flask import Flask, request, render_template_string
from model import predict_language

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Language Detection</title>

    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1f4037, #99f2c8);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            backdrop-filter: blur(12px);
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 35px;
            width: 420px;
            color: #fff;
            box-shadow: 0 8px 32px rgba(0,0,0,0.25);
            text-align: center;
        }

        h2 {
            margin-bottom: 20px;
            font-weight: 600;
        }

        textarea {
            width: 100%;
            height: 110px;
            padding: 12px;
            border-radius: 10px;
            border: none;
            outline: none;
            resize: none;
            font-size: 14px;
            background: rgba(255,255,255,0.9);
            color: #333;
            transition: 0.3s;
        }

        textarea:focus {
            box-shadow: 0 0 8px rgba(255,255,255,0.6);
        }

        button {
            margin-top: 18px;
            padding: 12px 25px;
            border-radius: 25px;
            border: none;
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: white;
            font-size: 15px;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        .result {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            background: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 10px;
        }

        .error {
            margin-top: 15px;
            color: #ffdddd;
            background: rgba(255,0,0,0.2);
            padding: 8px;
            border-radius: 8px;
        }

        .loading {
            margin-top: 15px;
            font-style: italic;
            opacity: 0.9;
        }

        .footer {
            margin-top: 15px;
            font-size: 12px;
            opacity: 0.7;
        }
    </style>

</head>

<body>

<div class="container">
    <h2>🌐 Language Detection</h2>

    <form method="POST" onsubmit="return validateForm()">
        <textarea id="text" name="text" placeholder="Type or paste text here...">{{ text }}</textarea>
        <br>
        <button type="submit">Detect Language</button>
    </form>

    {% if error %}
        <div class="error">⚠️ {{ error }}</div>
    {% endif %}

    {% if loading %}
        <div class="loading">⏳ Detecting language...</div>
    {% endif %}

    {% if prediction %}
        <div class="result">
            🔍 {{ prediction }}
        </div>
    {% endif %}

    <div class="footer">
        AI Powered Language Identifier
    </div>
</div>

<script>
function validateForm() {
    let text = document.getElementById("text").value;

    if (text.trim() === "") {
        alert("Please enter some text!");
        return false;
    }

    if (text.trim().length < 3) {
        alert("Enter at least 3 characters!");
        return false;
    }

    return true;
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = ""
    error = ""
    text = ""
    loading = False

    if request.method == "POST":
        text = request.form["text"]

        if text.strip() == "":
            error = "Please enter some text."
        elif len(text.strip()) < 3:
            error = "Enter at least 3 characters."
        else:
            loading = True
            prediction = predict_language(text)

    return render_template_string(
        HTML_PAGE,
        prediction=prediction,
        error=error,
        text=text,
        loading=loading
    )

if __name__ == "__main__":
    app.run(debug=True)