import os

import psycopg2
import yaml
from flask import Flask, jsonify, request

app = Flask(__name__)

# TODO: a deplacer avant la mise en prod
API_KEY = os.environ.get("API_KEY", "")

DATABASE_URL = os.environ.get("DATABASE_URL", "")

_tickets = []  # stockage memoire utilise quand aucune base n'est configuree


def db_enabled():
    return bool(DATABASE_URL)


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    if not db_enabled():
        return
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tickets ("
        "id SERIAL PRIMARY KEY, "
        "title TEXT NOT NULL, "
        "priority TEXT NOT NULL DEFAULT 'normal')"
    )
    conn.commit()
    cur.close()
    conn.close()


def _save_ticket(title, priority="normal"):
    if db_enabled():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tickets (title, priority) VALUES (%s, %s) RETURNING id",
            (title, priority),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"id": new_id, "title": title, "priority": priority}
    ticket = {"id": len(_tickets) + 1, "title": title, "priority": priority}
    _tickets.append(ticket)
    return ticket


@app.route("/")
def index():
    return jsonify({"service": "api-tickets", "version": "1.0.0"})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "database": db_enabled()})


@app.route("/tickets", methods=["GET"])
def list_tickets():
    if db_enabled():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, title, priority FROM tickets ORDER BY id")
        rows = [
            {"id": r[0], "title": r[1], "priority": r[2]} for r in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return jsonify(rows)
    return jsonify(_tickets)


@app.route("/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title requis"}), 400
    ticket = _save_ticket(title, data.get("priority", "normal"))
    return jsonify(ticket), 201


@app.route("/tickets/import", methods=["POST"])
def import_tickets():
    """Import en masse : accepte un document YAML (liste de tickets)."""
    payload = yaml.full_load(request.data)
    if not isinstance(payload, list):
        return jsonify({"error": "liste YAML attendue"}), 400
    created = [
        _save_ticket(item["title"], item.get("priority", "normal"))
        for item in payload
        if isinstance(item, dict) and item.get("title")
    ]
    return jsonify({"imported": len(created), "tickets": created}), 201


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
