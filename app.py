from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import base64
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'ziko_boss_secret_key_2026'  # مطلوب للجلسات

# بيانات تسجيل الدخول
USERNAME = "ZikoBoss"
PASSWORD = "Ziko@2006V1"

# اسم الفريق
TEAM_NAME = "ZIKO-TEAM"

# فك تشفير رابط API
def get_api_url(uid, server_name):
    try:
        encoded_url = "aHR0cHM6Ly9kdXJhbnRvLWxpa2UtcGVhcmwudmVyY2VsLmFwcC9saWtlP3VpZD17dWlkfSZzZXJ2ZXJfbmFtZT17c2VydmVyX25hbWV9"
        decoded_url = base64.b64decode(encoded_url).decode()
        return decoded_url.format(uid=uid, server_name=server_name)
    except:
        return None

# أسماء المناطق
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

# دالة للتحقق من تسجيل الدخول
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# قالب HTML لصفحة تسجيل الدخول
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
            text-shadow: 0 0 10px red;
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
        <h1>🔐 ZIKO-TEAM</h1>
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
            
            <button type="submit">Login to Dashboard</button>
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
            {{ team_name }} - Authorized Personnel Only
        </div>
    </div>
</body>
</html>
"""

# قالب HTML الرئيسي (مع إضافة زر تسجيل الخروج)
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTA LIKES</title>
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
            flex-direction: column;
        }
        .container {
            max-width: 600px;
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
            left: 20px;
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
            text-shadow: 0 0 10px red;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        h2 {
            color: white;
            margin-bottom: 30px;
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
            box-sizing: border-box;
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
            text-align: right;
        }
        .result-box pre {
            font-family: 'Courier New', monospace;
            color: white;
            background: #111;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid red;
        }
        .footer {
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }
        .lang-switch {
            margin-bottom: 20px;
        }
        .lang-switch a {
            color: red;
            text-decoration: none;
            margin: 0 10px;
            font-weight: bold;
        }
        .lang-switch a:hover {
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
        .footer-note {
            margin-top: 10px;
            color: #666;
            font-size: 0.9em;
        }
        .user-badge {
            position: absolute;
            top: 20px;
            right: 20px;
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
        <a href="/logout" class="logout-btn">🚪 Logout</a>
        <div class="user-badge">👤 {{ username }}</div>
        
        <h1>ZAKARIA LIKES</h1>
        <h2>{{ team_name }}</h2>

        <div class="lang-switch">
            <a href="?lang=ar"> العربية</a> | <a href="?lang=en"> English</a>
        </div>

        {% if error %}
        <div style="color: red; background: #330000; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            {{ error }}
        </div>
        {% endif %}

        <form method="POST" action="/send_likes">
            <input type="hidden" name="lang" value="{{ lang }}">

            <label>{% if lang == 'ar' %} UID الخاص بك{% else %}Your UID{% endif %}</label>
            <input type="text" name="uid" placeholder="مثال: 13708567247" required>

            <label>{% if lang == 'ar' %}🌍 المنطقة{% else %}🌍 Region{% endif %}</label>
            <select name="server">
                {% for code, names in regions.items() %}
                <option value="{{ code }}">{{ names[lang] }}</option>
                {% endfor %}
            </select>

            <button type="submit">
                {% if lang == 'ar' %}📥 إرسال لايكات{% else %}📥 Send Likes{% endif %}
            </button>
        </form>

        {% if result %}
        <div class="result-box">
            <h3 style="color: red; margin-top: 0;">
                {% if lang == 'ar' %}📊 النتيجة{% else %}📊 Result{% endif %}
            </h3>
            <pre>{{ result }}</pre>
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
        <div class="footer-note">
            © 2024 جميع الحقوق محفوظة
        </div>
    </div>
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
            return redirect(url_for('index'))
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
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error="⚠️ الرجاء إدخال UID" if lang=='ar' else "⚠️ Please enter UID",
                                       result=None, username=session.get('username', ''))

    api_url = get_api_url(uid, server)
    if not api_url:
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error="❌ خطأ في النظام" if lang=='ar' else "❌ System error",
                                       result=None, username=session.get('username', ''))

    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()

        likes_given = data.get('LikesGivenByAPI', 0)
        likes_after = data.get('LikesafterCommand', 0)
        likes_before = data.get('LikesbeforeCommand', 0)
        player_nickname = data.get('PlayerNickname', 'غير معروف' if lang=='ar' else 'Unknown')
        status = data.get('status', 0)

        if lang == 'ar':
            status_icons = {0: "❌ فشل", 1: "⚠️ محدود", 2: "✅ ناجح", 3: "🔒 مغلق"}
            region_name = regions.get(server, {}).get('ar', server.upper())
        else:
            status_icons = {0: "❌ Failed", 1: "⚠️ Limited", 2: "✅ Success", 3: "🔒 Locked"}
            region_name = regions.get(server, {}).get('en', server.upper())

        result_text = f"""
🎮 اللاعب: {player_nickname}
🔢 UID: {uid}
🌍 المنطقة: {region_name}

📊 اللايكات:
   قبل: {likes_before} 👍
   بعد: {likes_after} 👍
   أضيف: {likes_given} 🆕

📈 الحالة: {status_icons.get(status, '❓')}
"""
        if likes_given > 0:
            result_text += "\n✅ تمت الإضافة بنجاح"
        elif status == 2:
            result_text += "\nℹ️ الحد الأقصى متوفر"
        else:
            result_text += "\n❌ لم تتم الإضافة"

        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error=None, result=result_text, username=session.get('username', ''))

    except Exception as e:
        return render_template_string(MAIN_TEMPLATE, team_name=TEAM_NAME, regions=regions, lang=lang,
                                       error="❌ فشل الاتصال بالخادم" if lang=='ar' else "❌ Connection failed",
                                       result=None, username=session.get('username', ''))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)