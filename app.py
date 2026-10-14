import os
from flask import Flask, jsonify

app = Flask(__name__)

GREETING = os.getenv("GREETING", "Hello")
STUDENT = os.getenv("STUDENT", "student")
VARIANT = os.getenv("VARIANT", "24")

@app.route("/")
def index():
    return f"{GREETING}, {STUDENT}! Variant {VARIANT} v2\n"

@app.route("/health")
def health():
    return jsonify(status="ok", variant=VARIANT)

@app.route("/visits")
def visits():
    if "DB_HOST" not in os.environ:
        return jsonify(error="DB_HOST is not set"), 503

    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"]
        )
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, ts TIMESTAMP DEFAULT now())")
        cur.execute("INSERT INTO visits DEFAULT VALUES")
        cur.execute("SELECT COUNT(*) FROM visits")
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(visits=count)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
