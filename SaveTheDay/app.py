from flask import Flask, request, render_template, flash
import requests
import time
import ipaddress
import socket
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "wheel_secret_key"

@app.route("/", methods=["GET", "POST"])
def control_panel():
    if request.method == "POST":
        target = request.form.get("module", "").strip()

        if not target:
            flash("No diagnostic target provided")
            return render_template("index.html")

        try:
            parsed = urlparse(target)
            host = parsed.hostname
            if not host:
                flash("Invalid target")
                return render_template("index.html")

            # -----------------------------
            # 1️⃣ BLOCK LITERALS & NUMERICS
            # -----------------------------
            # This forces the player to stop using 127.0.0.1 or Hex/Octal
            try:
                ipaddress.ip_address(host)
                flash("Error: Direct IP access is blocked. Use a registered Module Domain.")
                return render_template("index.html")
            except ValueError:
                pass 

            if host.replace(".", "").isdigit():
                flash("Error: Numeric hostnames are blocked.")
                return render_template("index.html")

            # -----------------------------
            # 2️⃣ DNS RESOLUTION
            # -----------------------------
            try:
                resolved_ip = socket.gethostbyname(host)
            except socket.gaierror:
                flash("Error: Unable to resolve hostname.")
                return render_template("index.html")

            # -----------------------------
            # 3️⃣ THE "DNS-ONLY" GOAL
            # -----------------------------
            # This ensures that ONLY local loopback is allowed, 
            # but since literals are blocked above, they MUST use a DNS record.
            ip_obj = ipaddress.ip_address(resolved_ip)
            if not ip_obj.is_loopback:
                flash(f"Error: {host} ({resolved_ip}) is not an internal module.")
                return render_template("index.html")

            # -----------------------------
            # 4️⃣ SUCCESSFUL FETCH
            # -----------------------------
            r = requests.get(target, timeout=(2, 2), allow_redirects=False)
            flash(f"Module response: {r.text}")

        except Exception as e:
            flash("Diagnostic failed")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)