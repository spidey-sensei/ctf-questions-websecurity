from flask import Flask

app = Flask(__name__)

FLAG = "Cultrang{55RF_S4v5d_Th3_D4y}"

@app.route("/status")
def status():
    return "WHEEL SPEED: CRITICAL"

@app.route("/shutdown")
def shutdown():
    return FLAG

if __name__ == "__main__":
    # IMPORTANT: Internal only
    app.run(host="127.0.0.1", port=8081)
