import os

from flask import Flask, request, render_template_string

app = Flask(__name__)

# These values are supplied through environment variables.
APP_TITLE = os.getenv("APP_TITLE", "Python Calculator")
DEVELOPER_NAME = os.getenv("DEVELOPER_NAME", "Pugal")
APP_VERSION = os.getenv("APP_VERSION", "3.0.0")
APP_TAGLINE = os.getenv("APP_TAGLINE", "Simple calculations. Clean results.")
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "Kubernetes Lab")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_title }}</title>
    <style>
        :root {
            color-scheme: dark;
            --bg: #0b1220;
            --panel: #121d31;
            --panel-border: #263650;
            --text: #edf3ff;
            --muted: #9aabc4;
            --accent: #65e6c4;
            --accent-dark: #102f31;
            --danger: #ff9b9b;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            padding: 40px 18px;
            display: grid;
            place-items: center;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at 15% 10%, #1b3650 0, transparent 34%),
                radial-gradient(circle at 90% 85%, #153a3a 0, transparent 30%),
                var(--bg);
        }
        .page { width: 100%; max-width: 470px; }
        .brand { margin-bottom: 20px; text-align: center; }
        .eyebrow {
            display: inline-block;
            padding: 6px 11px;
            border: 1px solid #31506a;
            border-radius: 999px;
            color: var(--accent);
            background: #102235;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .12em;
            text-transform: uppercase;
        }
        h1 {
            margin: 15px 0 7px;
            font-size: clamp(30px, 7vw, 40px);
            letter-spacing: -1.5px;
        }
        .tagline { margin: 0; color: var(--muted); font-size: 14px; }
        .calculator {
            padding: 28px;
            border: 1px solid var(--panel-border);
            border-radius: 22px;
            background: rgba(18, 29, 49, .94);
            box-shadow: 0 24px 70px rgba(0, 0, 0, .35);
        }
        .field { margin-bottom: 16px; }
        label {
            display: block;
            margin: 0 0 8px;
            color: #c7d4e8;
            font-size: 13px;
            font-weight: 600;
        }
        input, select {
            width: 100%;
            min-height: 48px;
            padding: 12px 14px;
            border: 1px solid #344761;
            border-radius: 11px;
            outline: none;
            color: var(--text);
            background: #0c1728;
            font: inherit;
        }
        input:focus, select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(101, 230, 196, .12);
        }
        button {
            width: 100%;
            min-height: 49px;
            margin-top: 5px;
            border: 0;
            border-radius: 11px;
            color: #06251f;
            background: var(--accent);
            font: inherit;
            font-weight: 800;
            cursor: pointer;
            transition: transform .15s ease, filter .15s ease;
        }
        button:hover { filter: brightness(1.06); transform: translateY(-1px); }
        .result, .error {
            margin-top: 20px;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
        }
        .result {
            border: 1px solid #286c5c;
            background: var(--accent-dark);
        }
        .result small { display: block; color: var(--muted); }
        .result strong {
            display: block;
            margin-top: 5px;
            color: var(--accent);
            font-size: 27px;
            overflow-wrap: anywhere;
        }
        .error {
            border: 1px solid #75434a;
            color: var(--danger);
            background: #351d29;
        }
        footer {
            margin-top: 20px;
            color: var(--muted);
            text-align: center;
            font-size: 12px;
            line-height: 1.8;
        }
        footer strong { color: #dce8f8; }
        @media (max-width: 420px) {
            .calculator { padding: 22px 18px; }
        }
    </style>
</head>
<body>
    <main class="page">
        <header class="brand">
            <span class="eyebrow">{{ app_environment }}</span>
            <h1>{{ app_title }}</h1>
            <p class="tagline">{{ app_tagline }}</p>
        </header>

        <section class="calculator" aria-label="Calculator">
            <form method="POST">
                <div class="field">
                    <label for="num1">First number</label>
                    <input id="num1" type="number" step="any" name="num1"
                           placeholder="Enter first number" required>
                </div>

                <div class="field">
                    <label for="operation">Operation</label>
                    <select id="operation" name="operation">
                        <option value="+">Addition (+)</option>
                        <option value="-">Subtraction (-)</option>
                        <option value="*">Multiplication (*)</option>
                        <option value="/">Division (/)</option>
                    </select>
                </div>

                <div class="field">
                    <label for="num2">Second number</label>
                    <input id="num2" type="number" step="any" name="num2"
                           placeholder="Enter second number" required>
                </div>

                <button type="submit">Calculate result</button>
            </form>

            {% if result is not none %}
                <div class="result" role="status">
                    <small>Calculation result</small>
                    <strong>{{ result }}</strong>
                </div>
            {% endif %}

            {% if error %}
                <div class="error" role="alert">{{ error }}</div>
            {% endif %}
        </section>

        <footer>
            <strong>{{ app_title }}</strong> · v{{ app_version }}<br>
            Developed by {{ developer_name }}
        </footer>
    </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    error = None

    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    error = "Cannot divide by zero."
                else:
                    result = num1 / num2
            else:
                error = "Unsupported operation."
        except (ValueError, KeyError):
            error = "Please enter valid numbers and select an operation."

    return render_template_string(
        HTML,
        result=result,
        error=error,
        app_title=APP_TITLE,
        developer_name=DEVELOPER_NAME,
        app_version=APP_VERSION,
        app_tagline=APP_TAGLINE,
        app_environment=APP_ENVIRONMENT,
    )


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
