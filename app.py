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