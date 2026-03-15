from flask import Flask, request, render_template, abort
import sqlite3

from waf import waf_check
from crypto import decrypt_flag
from crypto import encrypt_flag

app = Flask(__name__)

FLAG = "CultRang{5ql_4nd_h45h_m4p5}"
FLAG_CIPHER = encrypt_flag(FLAG, "voila")
print(FLAG_CIPHER)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    uid = request.args.get('uid', '')

    if not waf_check(uid):
        abort(403)

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    query = f"SELECT name, clearance_hash FROM prisoners WHERE id = {uid}"

    res = cur.execute(query).fetchone()

    if not res:
        return "No prisoner found"

    return render_template(
        'profile.html',
        name=res[0],
        chash=res[1]
    )


@app.route('/vault')
def vault():
    secret = request.args.get('secret')

    if not secret:
        return render_template('vault.html', msg="Missing clearance")

    try:
        flag = decrypt_flag(FLAG_CIPHER, secret)
        if flag.startswith('CultRang'):
            return render_template(
                'vault.html',
                msg=f"ACCESS GRANTED!<br><br>{flag}"
            )
    except Exception:
        pass

    return render_template('vault.html', msg="Access denied")



if __name__ == '__main__':
    app.run(port=4004)

