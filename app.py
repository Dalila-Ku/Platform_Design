"""
Platform_Design — Web App con CRUD y Export ETL
Autor: Esaú Palomo | TeamX UPY 2026

Local:
    pip install flask
    python app.py  →  http://localhost:5000

Docker:
    docker-compose up  →  http://localhost:5000
"""

import sqlite3, os, csv, json, io
from datetime import date
from flask import Flask, jsonify, render_template, g, request, Response

app = Flask(__name__)
DB   = os.path.join(os.path.dirname(__file__), "platform.db")
SQL  = os.path.join(os.path.dirname(__file__), "db_files", "esau", "schema.sql")
DATA = os.path.join(os.path.dirname(__file__), "db_files", "esau", "sample_data.sql")

# ── DB ─────────────────────────────────────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    if not os.path.exists(DB):
        print("[INIT] Creando platform.db ...")
        conn = sqlite3.connect(DB)
        conn.execute("PRAGMA foreign_keys = ON")
        with open(SQL, encoding="utf-8") as f: conn.executescript(f.read())
        with open(DATA, encoding="utf-8") as f: conn.executescript(f.read())
        conn.commit(); conn.close()
        print("[INIT] platform.db lista.")

# ── Pages ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

# ── API: Stats ─────────────────────────────────────────────────────────────────

@app.route("/api/stats")
def api_stats():
    db = get_db()
    def one(q): return db.execute(q).fetchone()[0]
    return jsonify({
        "total":       one("SELECT COUNT(*) FROM tasks"),
        "done":        one("SELECT COUNT(*) FROM tasks WHERE status='done'"),
        "in_progress": one("SELECT COUNT(*) FROM tasks WHERE status='in_progress'"),
        "in_review":   one("SELECT COUNT(*) FROM tasks WHERE status='in_review'"),
        "todo":        one("SELECT COUNT(*) FROM tasks WHERE status='todo'"),
        "overdue":     one("SELECT COUNT(*) FROM tasks WHERE due_date < DATE('now') AND status NOT IN ('done','cancelled')"),
        "by_priority":   [dict(r) for r in db.execute("SELECT priority, COUNT(*) n FROM tasks GROUP BY priority").fetchall()],
        "by_status":     [dict(r) for r in db.execute("SELECT status,   COUNT(*) n FROM tasks GROUP BY status").fetchall()],
        "by_difficulty": [dict(r) for r in db.execute("SELECT difficulty, COUNT(*) n FROM tasks GROUP BY difficulty").fetchall()],
    })

# ── API: Users ─────────────────────────────────────────────────────────────────

@app.route("/api/users")
def api_users():
    db = get_db()
    rows = db.execute("""
        SELECT u.id, u.full_name, u.email, u.role,
               COUNT(ta.task_id) as task_count
        FROM users u
        LEFT JOIN task_assignments ta ON ta.user_id = u.id
        GROUP BY u.id ORDER BY u.full_name
    """).fetchall()
    return jsonify([dict(r) for r in rows])

# ── API: Tasks CRUD ────────────────────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
def api_tasks_get():
    db = get_db()
    rows = db.execute("""
        SELECT t.id, t.title, t.status, t.priority, t.difficulty,
               t.assignment_date, t.start_date, t.due_date, t.completed_date,
               t.estimated_hours, t.actual_hours,
               u.full_name as assigned_to, u.id as user_id
        FROM tasks t
        LEFT JOIN task_assignments ta ON ta.task_id = t.id
        LEFT JOIN users u ON u.id = ta.user_id
        ORDER BY t.priority DESC, t.due_date ASC
    """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/tasks", methods=["POST"])
def api_tasks_create():
    db   = get_db()
    body = request.get_json()
    today = str(date.today())
    cur = db.execute("""
        INSERT INTO tasks
          (project_id, title, status, priority, difficulty,
           assignment_date, due_date, estimated_hours, created_by)
        VALUES (1, ?, 'todo', ?, ?, ?, ?, ?, 1)
    """, (
        body.get("title","Sin título"),
        body.get("priority","medium"),
        body.get("difficulty","medium"),
        body.get("assignment_date", today),
        body.get("due_date"),
        body.get("estimated_hours"),
    ))
    task_id = cur.lastrowid
    user_id = body.get("user_id")
    if user_id:
        db.execute("INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (?,?,1)",
                   (task_id, user_id))
    db.commit()
    return jsonify({"id": task_id, "message": "Tarea creada"}), 201

@app.route("/api/tasks/<int:tid>", methods=["PATCH"])
def api_tasks_update(tid):
    db   = get_db()
    body = request.get_json()
    fields, vals = [], []
    for col in ["title","status","priority","difficulty","assignment_date","start_date","due_date","completed_date","estimated_hours","actual_hours"]:
        if col in body:
            fields.append(f"{col}=?")
            vals.append(body[col])
    # Auto set completed_date
    if body.get("status") == "done" and "completed_date" not in body:
        fields.append("completed_date=?"); vals.append(str(date.today()))
    if body.get("status") == "in_progress" and "start_date" not in body:
        existing = db.execute("SELECT start_date FROM tasks WHERE id=?", (tid,)).fetchone()
        if existing and not existing["start_date"]:
            fields.append("start_date=?"); vals.append(str(date.today()))
    if not fields:
        return jsonify({"error": "Nada que actualizar"}), 400
    vals.append(tid)
    db.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id=?", vals)
    # Update assignment if user_id provided
    if "user_id" in body:
        db.execute("DELETE FROM task_assignments WHERE task_id=?", (tid,))
        if body["user_id"]:
            db.execute("INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (?,?,1)",
                       (tid, body["user_id"]))
    db.commit()
    return jsonify({"message": "Actualizado"})

@app.route("/api/tasks/<int:tid>", methods=["DELETE"])
def api_tasks_delete(tid):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id=?", (tid,))
    db.commit()
    return jsonify({"message": "Eliminado"})

# ── API: Research P4 ───────────────────────────────────────────────────────────

@app.route("/api/research")
def api_research():
    db = get_db()
    rows = db.execute("""
        SELECT u.full_name,
               COUNT(t.id)                                         as total,
               SUM(CASE WHEN t.status NOT IN ('done','cancelled') THEN 1 ELSE 0 END) as active,
               SUM(CASE WHEN t.status='done' THEN 1 ELSE 0 END)   as done_count,
               SUM(CASE WHEN t.status='done' AND t.completed_date IS NOT NULL
                        AND t.completed_date <= t.due_date THEN 1 ELSE 0 END) as on_time
        FROM users u
        LEFT JOIN task_assignments ta ON ta.user_id = u.id
        LEFT JOIN tasks t ON t.id = ta.task_id
        GROUP BY u.id HAVING total > 0 ORDER BY active DESC
    """).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["rate"] = round(d["on_time"] / d["done_count"] * 100, 1) if d["done_count"] else 0
        result.append(d)
    return jsonify(result)

# ── API: Export para ETL ───────────────────────────────────────────────────────

@app.route("/api/export/csv")
def export_csv():
    db   = get_db()
    rows = db.execute("""
        SELECT t.id, t.title, t.status, t.priority, t.difficulty,
               t.assignment_date, t.start_date, t.due_date, t.completed_date,
               t.estimated_hours, t.actual_hours, u.full_name as assigned_to
        FROM tasks t
        LEFT JOIN task_assignments ta ON ta.task_id = t.id
        LEFT JOIN users u ON u.id = ta.user_id
        ORDER BY t.id
    """).fetchall()
    buf = io.StringIO()
    w   = csv.DictWriter(buf, fieldnames=rows[0].keys() if rows else [])
    w.writeheader()
    for r in rows: w.writerow(dict(r))
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=tasks_export.csv"})

@app.route("/api/export/json")
def export_json():
    db   = get_db()
    rows = db.execute("""
        SELECT t.*, u.full_name as assigned_to
        FROM tasks t
        LEFT JOIN task_assignments ta ON ta.task_id = t.id
        LEFT JOIN users u ON u.id = ta.user_id
        ORDER BY t.id
    """).fetchall()
    data = {"exported": str(date.today()), "tasks": [dict(r) for r in rows]}
    return Response(json.dumps(data, ensure_ascii=False, indent=2),
                    mimetype="application/json",
                    headers={"Content-Disposition": "attachment; filename=tasks_export.json"})

# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("[INFO] http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
