from flask import Flask, request, render_template, abort, send_file
import jwt
import time
import os

app = Flask(__name__)

JWT_SECRET = open("secret.txt").read().strip()
JWT_ALGO = "HS256"

# -------------------------------
# Helpers
# -------------------------------

def generate_hidden_jwt():
    payload = {
        "user": "system",
        "tier": "observer",
        "hint": "same secrets repeat",
        "iat": int(time.time())
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Rabbit hole login
    return render_template("login.html", error="Invalid credentials")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/vault")
def vault():
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        abort(403)

    token = auth.split(" ")[1]

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except:
        abort(403)

    if decoded.get("tier") != "warden":
        return "Vault locked. Clearance insufficient.", 403

    return render_template("vault.html")


# -------------------------------
# 🔥 JWT LEAK — BACKGROUND IMAGE
# -------------------------------
@app.route("/static/background.png")
def background():
    token = generate_hidden_jwt()

    response = send_file("static/background.png", mimetype="image/png")
    response.headers["X-Auth-Token"] = token   # 👈 KEY PART
    return response


# -------------------------------
# Hidden file (password protected)
# -------------------------------
@app.route("/vault/flag.txt", methods=["GET", "POST"])
def flag_file():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == JWT_SECRET:
            return open("vault/flag.txt").read()
        return "Wrong password", 403

    return "Authentication required", 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
