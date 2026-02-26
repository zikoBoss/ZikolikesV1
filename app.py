from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import base64
import os
import urllib.parse
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ziko_boss_secret_key_2026'

USERNAME = "ZikoBoss"
PASSWORD = "Ziko@2006V1"
TEAM_NAME = "ZIKO-TEAM"

def get_api_url(uid, server_name):
    try:
        encoded_url = "aHR0cHM6Ly9kdXJhbnRvLWxpa2UtcGVhcmwudmVyY2VsLmFwcC9saWtlP3VpZD17dWlkfSZzZXJ2ZXJfbmFtZT17c2VydmVyX25hbWV9"
        decoded_url = base64.b64decode(encoded_url).decode()
        return decoded_url.format(uid=uid, server_name=server_name)
    except:
        return None

regions = {
    'me': {'ar': 'الشرق الأوسط', 'en': 'Middle East'},
    'eu': {'ar': 'أوروبا', 'en': 'Europe'},
    'us': {'ar': 'أمريكا الشمالية', 'en': 'North America'},
    'in': {'ar': 'الهند', 'en': 'India'},
    'br': {'ar': 'البرازيل', 'en': 'Brazil'},
    'id': {'ar': 'إندونيسيا', 'en': 'Indonesia'},
    'tr': {'ar': 'تركيا', 'en': 'Turkey'},
    'th': {'ar': 'تايلاند', 'en': 'Thailand'}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def format_timestamp(timestamp):
    try:
        if timestamp and timestamp > 0:
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"
    except:
        return "N/A"

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZIKO-TEAM Login</title>
    <style>
        body {
            background-color: black;
            color: red;
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            max-width: 400px;
            width: 100%;
            background: #1a1a1a;
            padding: 40px;
            border-radius: 15px;
            border: 2px solid red;
            box-shadow: 0 0 20px rgba(255,0,0,0.3);
        }
        h1 {
            color: red;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        h2 {
            color: white;
            margin-bottom: 30px;
            font-size: 1.2em;
        }
        .input-group {
            margin-bottom: 20px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: red;
            font-weight: bold;
            font-size: 0.9em;
        }
        input {
            width: 100%;
            padding: 12px;
            background: black;
            border: 2px solid red;
            color: red;
            border-radius: 8px;
            font-size: 1em;
            box-sizing: border-box;
        }
        input:focus {
            outline: none;
            border-color: white;
        }
        button {
            background: red;
            color: black;
            border: none;
            padding: 15px 30px;
            font-size: 1.2em;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 20px;
            width: 100%;
        }
        button:hover {
            background: #cc0000;
            box-shadow: 0 0 15px red;
            transform: scale(1.02);
        }
        .error-message {
            color: red;
            background: #330000;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid red;
        }
        .social-icons {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #333;
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .social-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: #1a1a1a;
            border: 2px solid red;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .social-icon:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px red;
            background: red;
        }
        .social-icon:hover svg {
            fill: black;
        }
        .social-icon svg {
            width: 22px;
            height: 22px;
            fill: red;
            transition: all 0.3s ease;
        }
        .footer {
            margin-top: 20px;
            color: #666;
            font-size: 0.8em;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>ZIKO-TEAM</h1>
        <h2>Access Control System</h2>
        
        {% if error %}
        <div class="error-message">
            {{ error }}
        </div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="input-group">
                <label>👤 Username</label>
                <input type="text" name="username" placeholder="Enter username" required>
            </div>
            
            <div class="input-group">
                <label>🔑 Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            
            <button type="submit">Login</button>
        </form>
        
        <div class="social-icons">
            <a href="https://youtube.com/@ziko_boss?si=Te3gus_-91NNFkfP" target="_blank" class="social-icon" title="YouTube">
                <svg viewBox="0 0 24 24">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
            </a>
            <a href="https://t.me/Ziko_Tim" target="_blank" class="social-icon" title="Telegram">
                <svg viewBox="0 0 24 24">
                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
                </svg>
            </a>
        </div>
        
        <div class="footer">
            {{ team_name }}
        </div>
    </div>
</body>
</html>
"""

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{% if lang == 'ar' %}rtl{% else %}ltr{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZIKO-TEAM FREE FIRE TOOLS</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            background-color: black;
            color: red;
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: #1a1a1a;
            padding: 30px;
            border-radius: 15px;
            border: 2px solid red;
            box-shadow: 0 0 20px rgba(255,0,0,0.3);
            flex: 1;
            position: relative;
        }
        .logout-btn {
            position: absolute;
            top: 20px;
            {% if lang == 'ar' %}
            left: 20px;
            {% else %}
            right: 20px;
            {% endif %}
            background: transparent;
            color: red;
            border: 2px solid red;
            padding: 8px 15px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.9em;
            transition: 0.3s;
        }
        .logout-btn:hover {
            background: red;
            color: black;
        }
        h1 {
            color: red;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        h2 {
            color: white;
            margin-bottom: 30px;
        }
        .tabs {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .tab-btn {
            background: transparent;
            color: red;
            border: 2px solid red;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: 0.3s;
            flex: 1;
            min-width: 120px;
        }
        .tab-btn:hover, .tab-btn.active {
            background: red;
            color: black;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: red;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 12px;
            background: black;
            border: 2px solid red;
            color: red;
            border-radius: 8px;
            font-size: 1.1em;
            margin-bottom: 15px;
        }
        input:focus, select:focus {
            outline: none;
            border-color: white;
        }
        button {
            background: red;
            color: black;
            border: none;
            padding: 15px 30px;
            font-size: 1.3em;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 10px;
            width: 100%;
        }
        button:hover {
            background: #cc0000;
            box-shadow: 0 0 15px red;
            transform: scale(1.02);
        }
        .result-box {
            margin-top: 30px;
            padding: 20px;
            background: black;
            border: 2px solid red;
            border-radius: 10px;
            color: red;
            text-align: {% if lang == 'ar' %}right{% else %}left{% endif %};
        }
        .result-box pre {
            font-family: 'Courier New', monospace;
            color: white;
            background: #111;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid red;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 100%;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        .info-item {
            background: #111;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid red;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        .info-label {
            color: red;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .info-value {
            color: white;
            font-size: 1.1em;
            font-weight: bold;
            word-break: break-word;
        }
        .ban-safe {
            color: #00ff00;
        }
        .ban-banned {
            color: #ff0000;
        }
        .language-switch {
            margin: 20px 0;
        }
        .language-switch a {
            color: red;
            text-decoration: none;
            margin: 0 10px;
            font-weight: bold;
        }
        .language-switch a:hover {
            text-decoration: underline;
        }
        .social-icons {
            margin-top: 30px;
            padding: 20px 0;
            border-top: 1px solid #333;
            display: flex;
            justify-content: center;
            gap: 30px;
        }
        .social-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #1a1a1a;
            border: 2px solid red;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .social-icon:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px red;
            background: red;
        }
        .social-icon:hover svg {
            fill: black;
        }
        .social-icon svg {
            width: 30px;
            height: 30px;
            fill: red;
            transition: all 0.3s ease;
        }
        .footer {
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }
        .user-badge {
            position: absolute;
            top: 20px;
            {% if lang == 'ar' %}
            right: 20px;
            {% else %}
            left: 20px;
            {% endif %}
            color: red;
            font-size: 0.9em;
            border: 1px solid red;
            padding: 5px 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/logout" class="logout-btn">{% if lang == 'ar' %}🚪 خروج{% else %}🚪 Logout{% endif %}</a>
        <div class="user-badge">{{ username }}</div>
        
        <h1>ZIKO-TOOLS</h1>
        <h2>{{ team_name }}</h2>

        <div class="language-switch">
            <a href="?lang=ar">العربية</a> | <a href="?lang=en">English</a>
        </div>

        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('likes')">{% if lang == 'ar' %}إرسال لايكات{% else %}Send Likes{% endif %}</button>
            <button class="tab-btn" onclick="showTab('check')">{% if lang == 'ar' %}فحص الحظر{% else %}Ban Check{% endif %}</button>
            <button class="tab-btn" onclick="showTab('info')">{% if lang == 'ar' %}معلومات الحساب{% else %}Player Info{% endif %}</button>
        </div>

        {% if error %}
        <div style="color: red; background: #330000; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            {{ error }}
        </div>
        {% endif %}

        <div id="likes-tab" class="tab-content active">
            <form method="POST" action="/send_likes">
                <input type="hidden" name="lang" value="{{ lang }}">
                
                <label>{% if lang == 'ar' %}UID{% else %}UID{% endif %}</label>
                <input type="text" name="uid" placeholder="Your UID here" required>

                <label>{% if lang == 'ar' %}المنطقة{% else %}Region{% endif %}</label>
                <select name="server">
                    {% for code, names in regions.items() %}
                    <option value="{{ code }}">{{ names[lang] }}</option>
                    {% endfor %}
                </select>

                <button type="submit">
                    {% if lang == 'ar' %}إرسال{% else %}Send{% endif %}
                </button>
            </form>
        </div>

        <div id="check-tab" class="tab-content">
            <form method="POST" action="/check_ban">
                <input type="hidden" name="lang" value="{{ lang }}">
                
                <label>{% if lang == 'ar' %}UID{% else %}UID{% endif %}</label>
                <input type="text" name="uid" placeholder="Your UID here" required>

                <button type="submit">
                    {% if lang == 'ar' %}فحص{% else %}Check{% endif %}
                </button>
            </form>
        </div>

        <div id="info-tab" class="tab-content">
            <form method="POST" action="/player_info">
                <input type="hidden" name="lang" value="{{ lang }}">
                
                <label>{% if lang == 'ar' %}UID{% else %}UID{% endif %}</label>
                <input type="text" name="uid" placeholder="Your UID here" required>

                <button type="submit">
                    {% if lang == 'ar' %}جلب المعلومات{% else %}Get Info{% endif %}
                </button>
            </form>
        </div>

        {% if result %}
        <div class="result-box">
            {{ result|safe }}
        </div>
        {% endif %}

        <div class="social-icons">
            <a href="https://youtube.com/@ziko_boss?si=Te3gus_-91NNFkfP" target="_blank" class="social-icon" title="YouTube">
                <svg viewBox="0 0 24 24">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
            </a>
            <a href="https://t.me/Ziko_Tim" target="_blank" class="social-icon" title="Telegram">
                <svg viewBox="0 0 24 24">
                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
                </svg>
            </a>
        </div>
        
        <div class="footer">
            {{ team_name }} - Dev ZAKARIA
        </div>
    </div>

    <script>
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById(tabName + '-tab').classList.add('active');
            
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        const urlParams = new URLSearchParams(window.location.search);
        const activeTab = urlParams.get('tab');
        if (activeTab) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.getElementById(activeTab + '-tab').classList.add('active');
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector(`[onclick="showTab('${activeTab}')"]`).classList.add('active');
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index', lang='en'))
        else:
            error = "❌ Invalid username or password"
            return render_template_string(LOGIN_TEMPLATE, team_name=TEAM_NAME, error=error)
    
    return render_template_string(LOGIN_TEMPLATE, team_name=TEAM_NAME, error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET'])
@login_required
def index():
    lang = request.args.get('lang', 'ar')
    if lang not in ['ar', 'en']:
        lang = 'ar'
    return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, 
                                   lang=lang, error=None, result=None, username=session.get('username', ''))

@app.route('/send_likes', methods=['POST'])
@login_required
def send_likes():
    uid = request.form.get('uid', '').strip()
    server = request.form.get('server', 'me')
    lang = request.form.get('lang', 'ar')

    if not uid:
        error = "⚠️ الرجاء إدخال UID" if lang == 'ar' else "⚠️ Please enter UID"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

    api_url = get_api_url(uid, server)
    if not api_url:
        error = "❌ خطأ في النظام" if lang == 'ar' else "❌ System error"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()

        likes_given = data.get('LikesGivenByAPI', 0)
        likes_after = data.get('LikesafterCommand', 0)
        likes_before = data.get('LikesbeforeCommand', 0)
        player_nickname = data.get('PlayerNickname', 'Unknown')
        status = data.get('status', 0)

        if lang == 'ar':
            status_text = {0: "فشل", 1: "محدود", 2: "ناجح", 3: "مغلق"}.get(status, 'غير معروف')
            region_name = regions.get(server, {}).get('ar', server.upper())
        else:
            status_text = {0: "Failed", 1: "Limited", 2: "Success", 3: "Locked"}.get(status, 'Unknown')
            region_name = regions.get(server, {}).get('en', server.upper())

        result_lines = []
        result_lines.append(f"Player: {player_nickname}")
        result_lines.append(f"UID: {uid}")
        result_lines.append(f"Region: {region_name}")
        result_lines.append("")
        result_lines.append("Likes:")
        result_lines.append(f"  Before: {likes_before}")
        result_lines.append(f"  After: {likes_after}")
        result_lines.append(f"  Added: {likes_given}")
        result_lines.append("")
        result_lines.append(f"Status: {status_text}")

        if likes_given > 0:
            result_lines.append("")
            result_lines.append("Successfully added")
        elif status == 2:
            result_lines.append("")
            result_lines.append("Maximum limit reached")
        else:
            result_lines.append("")
            result_lines.append("Not added")

        result_text = "\n".join(result_lines)

        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=None, result=f"<pre>{result_text}</pre>", username=session.get('username', ''))

    except Exception as e:
        error = "❌ فشل الاتصال بالخادم" if lang == 'ar' else "❌ Connection failed"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

@app.route('/check_ban', methods=['POST'])
@login_required
def check_ban():
    uid = request.form.get('uid', '').strip()
    lang = request.form.get('lang', 'ar')

    if not uid:
        error = "⚠️ الرجاء إدخال UID" if lang == 'ar' else "⚠️ Please enter UID"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

    try:
        url = f"https://foubia-ban-check.vercel.app/bancheck?key=xTzPrO&uid={uid}"
        response = requests.get(url, timeout=10)
        data = response.json()

        username = data.get('username', 'Unknown')
        ban_status = data.get('BanStatus', False)
        ban_period = data.get('BanDuration', 0)
        
        result_lines = []
        result_lines.append(f"✨ Result for UID: {uid}")
        result_lines.append("━━━━━━━━━━━━━━━")
        result_lines.append(f"username: {username}")
        result_lines.append(f"uid: {uid}")
        result_lines.append(f"status: {'NOT BANNED' if not ban_status else 'BANNED'}")
        result_lines.append(f"ban_period: {ban_period}")
        result_lines.append(f"is_banned: {'✅ لا' if not ban_status else '❌ نعم' if lang == 'ar' else '✅ No' if not ban_status else '❌ Yes'}")
        result_lines.append("━━━━━━━━━━━━━━━")
        result_lines.append("💎 Powered by: @ZikoB0SS")

        result_text = "\n".join(result_lines)

        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=None, result=f"<pre>{result_text}</pre>", username=session.get('username', ''))

    except Exception as e:
        error = f"❌ خطأ: {str(e)}" if lang == 'ar' else f"❌ Error: {str(e)}"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

@app.route('/player_info', methods=['POST'])
@login_required
def player_info():
    uid = request.form.get('uid', '').strip()
    lang = request.form.get('lang', 'ar')

    if not uid:
        error = "⚠️ الرجاء إدخال UID" if lang == 'ar' else "⚠️ Please enter UID"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

    try:
        # 1. جلب معلومات اللاعب
        url = f"https://foubia-info-ff.vercel.app/{uid}"
        response = requests.get(url, timeout=10)
        data = response.json()

        basic = data.get("basicinfo", [{}])[0]
        clan = data.get("claninfo", [{}])[0]
        clan_admin = data.get("clanadmin", [{}])[0]

        player_name = basic.get('username', 'Unknown')
        player_level = basic.get('level', '1')
        guild_name = clan.get('clanname', '')

        # 2. القيم الثابتة للبانر
        AVATAR_ID = "902028017"
        BANNER_ID = "901043008"
        PIN_ID = "0"
        PRIME_LEVEL = "1"

        # 3. بناء رابط البانر مع ترميز الاسم
        encoded_name = urllib.parse.quote(player_name)
        encoded_guild = urllib.parse.quote(guild_name) if guild_name else ""
        
        banner_url = (f"https://banner-apibykala-api.vercel.app/profile"
                      f"?avatar_id={AVATAR_ID}"
                      f"&banner_id={BANNER_ID}"
                      f"&pin_id={PIN_ID}"
                      f"&prime_level={PRIME_LEVEL}"
                      f"&level={player_level}"
                      f"&name={encoded_name}"
                      f"&guild={encoded_guild}")

        # 4. التحقق من البانر (اختياري)
        try:
            banner_response = requests.get(banner_url, timeout=5)
            banner_ok = banner_response.status_code == 200
        except:
            banner_ok = False

        # 5. تنسيق التواريخ
        last_login = format_timestamp(basic.get('lastlogin', 0))
        create_at = format_timestamp(basic.get('createat', 0))

        # 6. بناء HTML النتيجة مع البانر
        result_html = f"""
<div style="font-family: 'Courier New', monospace;">
    <h4 style="color: red; text-align: center;">{'معلومات اللاعب' if lang == 'ar' else 'Player Information'}</h4>
    
    <div style="background: #111; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h5 style="color: red; margin: 0 0 10px 0;">{'المعلومات الأساسية' if lang == 'ar' else 'Basic Info'}</h5>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">{'الاسم' if lang == 'ar' else 'Name'}</div>
                <div class="info-value" style="word-break: break-all;">{basic.get('username', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'المستوى' if lang == 'ar' else 'Level'}</div>
                <div class="info-value">{basic.get('level', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'الخبرة' if lang == 'ar' else 'Exp'}</div>
                <div class="info-value">{basic.get('Exp', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">BR</div>
                <div class="info-value">{basic.get('brrankscore', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">CS</div>
                <div class="info-value">{basic.get('csrankscore', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'الإعجابات' if lang == 'ar' else 'Likes'}</div>
                <div class="info-value">{basic.get('likes', 0):,}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'المنطقة' if lang == 'ar' else 'Region'}</div>
                <div class="info-value">{basic.get('region', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'السيرة' if lang == 'ar' else 'Bio'}</div>
                <div class="info-value" style="word-break: break-all;">{basic.get('bio', 'N/A')}</div>
            </div>
        </div>
    </div>

    <div style="background: #111; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h5 style="color: red; margin: 0 0 10px 0;">{'التواريخ' if lang == 'ar' else 'Dates'}</h5>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">{'تاريخ الإنشاء' if lang == 'ar' else 'Created'}</div>
                <div class="info-value">{create_at}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'آخر دخول' if lang == 'ar' else 'Last Login'}</div>
                <div class="info-value">{last_login}</div>
            </div>
        </div>
    </div>

    <div style="background: #111; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h5 style="color: red; margin: 0 0 10px 0;">{'معلومات العشيرة' if lang == 'ar' else 'Guild Info'}</h5>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">{'اسم العشيرة' if lang == 'ar' else 'Guild Name'}</div>
                <div class="info-value" style="word-break: break-all;">{clan.get('clanname', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'مستوى العشيرة' if lang == 'ar' else 'Guild Level'}</div>
                <div class="info-value">{clan.get('guildlevel', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'الأعضاء' if lang == 'ar' else 'Members'}</div>
                <div class="info-value">{clan.get('livemember', 'N/A')}</div>
            </div>
        </div>
    </div>

    <div style="background: #111; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h5 style="color: red; margin: 0 0 10px 0;">{'أدمن العشيرة' if lang == 'ar' else 'Guild Admin'}</h5>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">{'الاسم' if lang == 'ar' else 'Name'}</div>
                <div class="info-value" style="word-break: break-all;">{clan_admin.get('adminname', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'المستوى' if lang == 'ar' else 'Level'}</div>
                <div class="info-value">{clan_admin.get('level', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{'الخبرة' if lang == 'ar' else 'Exp'}</div>
                <div class="info-value">{clan_admin.get('exp', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">BR</div>
                <div class="info-value">{clan_admin.get('brpoint', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">CS</div>
                <div class="info-value">{clan_admin.get('cspoint', 'N/A')}</div>
            </div>
        </div>
    </div>

    <div style="margin-top: 30px; text-align: center;">
        <h5 style="color: red;">{'بانر اللاعب' if lang == 'ar' else 'Player Banner'}</h5>
        <div style="background: #111; padding: 15px; border-radius: 10px;">
            <img src="{banner_url}" alt="Player Banner" style="max-width: 100%; border: 2px solid red; border-radius: 10px;">
            <p style="color: #888; font-size: 0.8em; margin-top: 10px;">
                {'تم التوليد تلقائياً' if lang == 'ar' else 'Auto-generated'}
            </p>
        </div>
    </div>

    <div style="margin-top: 15px; color: #888; font-size: 0.9em; text-align: center;">
        💎 ZIKO-TEAM
    </div>
</div>
"""

        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=None, result=result_html, username=session.get('username', ''))

    except Exception as e:
        error = f"❌ خطأ: {str(e)}" if lang == 'ar' else f"❌ Error: {str(e)}"
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=error, result=None, username=session.get('username', ''))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)