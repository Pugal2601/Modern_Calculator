
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Calculator</title>
    <style>
        body {
            font-family: Arial;
            background: #172033;
            color: white;
            text-align: center;
            padding-top: 100px;
        }
        .calculator {
            background: #26344d;
            padding: 30px;
            width: 320px;
            margin: auto;
            border-radius: 15px;
        }
        input, select, button {
            padding: 12px;
            margin: 8px;
            width: 85%;
            border-radius: 6px;
            border: none;
        }
        button {
            background: #00c9a7;
            font-weight: bold;
            cursor: pointer;
        }
        h2 { color: #00c9a7; }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Python Calculator</h1>

        <form method="POST">
            <input type="number" step="any" name="num1"
                   placeholder="First number" required>

            <select name="operation">
                <option value="+">Addition (+)</option>
                <option value="-">Subtraction (-)</option>
                <option value="*">Multiplication (*)</option>
                <option value="/">Division (/)</option>
            </select>

            <input type="number" step="any" name="num2"
                   placeholder="Second number" required>

            <button type="submit">Calculate</button>
        </form>

        {% if result is not none %}
            <h2>Result: {{ result }}</h2>
        {% endif %}

        {% if error %}
            <h2>{{ error }}</h2>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    error = None

    if request.method == "POST":
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
                error = "Cannot divide by zero!"
            else:
                result = num1 / num2

    return render_template_string(
        HTML, result=result, error=error
    )

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
