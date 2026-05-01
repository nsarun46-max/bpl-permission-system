from flask import Flask, request, redirect, session, render_template_string, url_for
import sqlite3
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "bpl_secret"

DB = "bpl_permission.db"

SENDER_EMAIL = "yourcompanyemail@gmail.com"
SENDER_APP_PASSWORD = "your_gmail_app_password"
GATE_SUPERVISOR_EMAIL = "gatesecurity@company.com"

def send_gate_email(emp_id, name, department, date, permission_type, reason, out_time, return_time):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Gate Permission Approved"
        msg["From"] = "nsarun46@gmail.com"
        msg["To"] = "arunkumar.ns@gmail.com"

        msg.set_content(f"""
Dear Gate Supervisor,

Permission has been approved by Manager and HR.

Employee ID   : {emp_id}
Employee Name : {name}
Department    : {department}
Date          : {date}
Type          : {permission_type}
Reason        : {reason}
Out Time      : {out_time}
Return Time   : {return_time}

Please allow the employee as per approved permission.

Regards,
HR Department
BPL MEDICAL TECHNOLOGIES PVT LTD
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, "dkja ixgh krsp etjj")
            smtp.send_message(msg)

    except Exception as e:
        print("Email sending failed:", e)

def db():
    return sqlite3.connect(DB)

def create_tables():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT UNIQUE,
        name TEXT,
        email TEXT,
        department TEXT,
        manager_emp_id TEXT,
        manager_name TEXT,
        position TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS permission_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT,
        manager_emp_id TEXT,
        date TEXT,
        type TEXT,
        reason TEXT,
        out_time TEXT,
        return_time TEXT,
        manager TEXT DEFAULT 'Pending',
        hr TEXT DEFAULT 'Pending',
        gate_mail TEXT DEFAULT 'Not Sent'
    )
    """)

    cur.execute("SELECT COUNT(*) FROM employees")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO employees
        (emp_id,name,email,department,manager_emp_id,manager_name,position,password,role)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, ("HR001","HR","hr@bpl.com","HR","-","-","HR","1234","hr"))

        cur.execute("""
        INSERT INTO employees
        (emp_id,name,email,department,manager_emp_id,manager_name,position,password,role)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, ("MGR001","Manager","manager@bpl.com","PED","-","-","Senior Manager","1234","manager"))

        cur.execute("""
        INSERT INTO employees
        (emp_id,name,email,department,manager_emp_id,manager_name,position,password,role)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, ("EMP001","Arun","arun@bpl.com","PED","MGR001","Manager","Employee","1234","employee"))

    conn.commit()
    conn.close()

create_tables()

STYLE = """
<style>
*{box-sizing:border-box;font-family:Segoe UI,Arial;}
body{margin:0;background:#eef3f9;}
.login-page{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#062b55,#0f6c9e,#00a6a6);
}
.login-card{
    width:430px;
    background:white;
    padding:35px;
    border-radius:18px;
    box-shadow:0 20px 45px rgba(0,0,0,.25);
}
.logo{text-align:center;}
.logo img{width:120px;margin-bottom:10px;}
.logo h2{color:#063b70;font-size:20px;}
.input-group{margin-bottom:15px;}
.input-group label{font-weight:600;color:#333;}
input,select,textarea{
    width:100%;
    padding:12px;
    margin-top:6px;
    border:1px solid #cbd6e2;
    border-radius:9px;
}
textarea{height:90px;}
button{
    width:100%;
    padding:13px;
    background:#0077b6;
    color:white;
    border:none;
    border-radius:9px;
    font-weight:bold;
    cursor:pointer;
}
.topbar{
    height:75px;
    background:#063b70;
    color:white;
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:0 30px;
}
.brand{display:flex;align-items:center;gap:15px;}
.brand img{
    width:55px;height:55px;object-fit:contain;
    background:white;border-radius:8px;padding:5px;
}
.logout{
    color:white;text-decoration:none;background:#e63946;
    padding:10px 18px;border-radius:8px;
}
.container{
    max-width:1200px;
    margin:35px auto;
    background:white;
    padding:25px;
    border-radius:16px;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px;}
.full{grid-column:1/3;}

.request-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
    gap:20px;
    margin-top:20px;
}
.request-card{
    background:#f8fbff;
    border:1px solid #d9e6f2;
    border-radius:14px;
    padding:18px;
    box-shadow:0 5px 15px rgba(0,0,0,.06);
}
.request-card h4{
    margin:0 0 12px 0;
    color:#063b70;
    font-size:18px;
}
.info-row{
    display:flex;
    justify-content:space-between;
    gap:12px;
    padding:7px 0;
    border-bottom:1px solid #e5edf5;
    font-size:14px;
}
.info-row b{color:#333;}
.reason-box{
    background:white;
    padding:10px;
    border-radius:8px;
    margin-top:10px;
    border:1px solid #e1e8f0;
}
.action-area{
    display:flex;
    gap:10px;
    margin-top:15px;
}
.action-btn{
    flex:1;
    padding:10px;
    text-align:center;
    color:white;
    border-radius:8px;
    text-decoration:none;
    font-weight:bold;
    font-size:14px;
}
.approve{background:#198754;}
.reject{background:#dc3545;}
.badge{
    padding:5px 10px;
    border-radius:20px;
    font-size:13px;
    font-weight:bold;
}
.pending{background:#fff3cd;color:#856404;}
.approved{background:#d1e7dd;color:#0f5132;}
.rejected{background:#f8d7da;color:#842029;}
.sent{background:#cfe2ff;color:#084298;}
.waiting{color:#856404;font-weight:bold;text-align:center;margin-top:15px;}

@media(max-width:700px){
    .login-card{width:92%;}
    .grid{grid-template-columns:1fr;}
    .full{grid-column:1;}
    .topbar{padding:0 15px;}
    .brand h2{font-size:16px;}
    .container{margin:20px 10px;padding:15px;}
}
</style>
"""

def get_managers():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT emp_id, name, position FROM employees WHERE role='manager'")
    managers = cur.fetchall()
    conn.close()
    return managers

@app.route("/", methods=["GET","POST"])
def login():
    error = ""

    if request.method == "POST":
        emp = request.form["emp_id"]
        pwd = request.form["password"]

        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE emp_id=? AND password=?", (emp, pwd))
        user = cur.fetchone()
        conn.close()

        if user:
            session["emp_id"] = user[1]
            session["name"] = user[2]
            session["role"] = user[9]

            if user[9] == "employee":
                return redirect("/employee")
            elif user[9] == "manager":
                return redirect("/manager")
            elif user[9] == "hr":
                return redirect("/hr")
            else:
                error = "Invalid role"
        else:
            error = "Invalid Employee ID or Password"

    return render_template_string(STYLE + """
<div class="login-page">
<div class="login-card">
    <div class="logo">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <h2>BPL MEDICAL TECHNOLOGIES PVT LTD</h2>
        <p>Employee Permission Management System</p>
    </div>

    <form method="post">
        <div class="input-group">
            <label>User Name / Employee ID</label>
            <input name="emp_id" required>
        </div>

        <div class="input-group">
            <label>Password</label>
            <input type="password" name="password" required>
        </div>

        <p style="color:red;text-align:center;">{{error}}</p>
        <button>Login</button>
    </form>

    <div style="text-align:center;margin-top:15px;">
        <a href="/register_employee">Employee Register</a> |
        <a href="/register_manager">Manager Register</a>
    </div>

    <p style="text-align:center;color:#555;">
        
    </p>
</div>
</div>
""", error=error)

@app.route("/register_employee", methods=["GET","POST"])
def register_employee():
    msg = ""
    managers = get_managers()

    if request.method == "POST":
        try:
            manager_emp_id, manager_name = request.form["manager"].split("|")

            conn = db()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO employees
            (emp_id,name,email,department,manager_emp_id,manager_name,position,password,role)
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                request.form["emp_id"],
                request.form["name"],
                request.form["email"],
                request.form["department"],
                manager_emp_id,
                manager_name,
                "Employee",
                request.form["password"],
                "employee"
            ))
            conn.commit()
            conn.close()
            msg = "Employee registered successfully. Now login."

        except sqlite3.IntegrityError:
            msg = "Employee ID already exists."
        except:
            msg = "Please select manager properly."

    return render_template_string(STYLE + """
<div class="login-page">
<div class="login-card">
    <div class="logo">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <h2>Employee Registration</h2>
    </div>

    <form method="post">
        <div class="input-group"><label>Employee ID / User Name</label><input name="emp_id" required></div>
        <div class="input-group"><label>Full Name</label><input name="name" required></div>
        <div class="input-group"><label>Email ID</label><input type="email" name="email" required></div>
        <div class="input-group"><label>Department</label><input name="department" required></div>

        <div class="input-group">
            <label>Select Reporting Manager</label>
            <select name="manager" required>
                <option value="">Select Manager</option>
                {% for m in managers %}
                <option value="{{m[0]}}|{{m[1]}}">{{m[1]}} - {{m[2]}} - {{m[0]}}</option>
                {% endfor %}
            </select>
        </div>

        <div class="input-group"><label>Create Password</label><input type="password" name="password" required></div>
        <button>Register Employee</button>
    </form>

    <p style="text-align:center;color:green;">{{msg}}</p>
    <p style="text-align:center;"><a href="/">Back to Login</a></p>
</div>
</div>
""", msg=msg, managers=managers)

@app.route("/register_manager", methods=["GET","POST"])
def register_manager():
    msg = ""

    if request.method == "POST":
        try:
            conn = db()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO employees
            (emp_id,name,email,department,manager_emp_id,manager_name,position,password,role)
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                request.form["emp_id"],
                request.form["name"],
                request.form["email"],
                request.form["department"],
                "-",
                "-",
                request.form["position"],
                request.form["password"],
                "manager"
            ))
            conn.commit()
            conn.close()
            msg = "Manager registered successfully. Now login."
        except sqlite3.IntegrityError:
            msg = "Manager User Name / Employee ID already exists."

    return render_template_string(STYLE + """
<div class="login-page">
<div class="login-card">
    <div class="logo">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <h2>Manager Registration</h2>
    </div>

    <form method="post">
        <div class="input-group"><label>Manager User Name / Employee ID</label><input name="emp_id" required></div>
        <div class="input-group"><label>Manager Name</label><input name="name" required></div>
        <div class="input-group"><label>Email ID</label><input type="email" name="email" required></div>
        <div class="input-group"><label>Department</label><input name="department" required></div>

        <div class="input-group">
            <label>Manager Position</label>
            <select name="position" required>
                <option value="">Select Position</option>
                <option>Assistant Manager</option>
                <option>Senior Manager</option>
                <option>AGM</option>
                <option>GM</option>
            </select>
        </div>

        <div class="input-group"><label>Create Password</label><input type="password" name="password" required></div>
        <button>Register Manager</button>
    </form>

    <p style="text-align:center;color:green;">{{msg}}</p>
    <p style="text-align:center;"><a href="/">Back to Login</a></p>
</div>
</div>
""", msg=msg)

@app.route("/employee", methods=["GET","POST"])
def employee():
    if session.get("role") != "employee":
        return redirect("/")

    msg = ""

    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT manager_emp_id FROM employees WHERE emp_id=?", (session["emp_id"],))
    manager = cur.fetchone()
    conn.close()

    manager_emp_id = manager[0] if manager else ""

    if request.method == "POST":
        conn = db()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO permission_requests
        (emp_id,manager_emp_id,date,type,reason,out_time,return_time)
        VALUES (?,?,?,?,?,?,?)
        """, (
            session["emp_id"],
            manager_emp_id,
            request.form["date"],
            request.form["type"],
            request.form["reason"],
            request.form["out"],
            request.form["ret"]
        ))
        conn.commit()
        conn.close()
        msg = "Permission request submitted to your reporting manager."

    return render_template_string(STYLE + """
<div class="topbar">
    <div class="brand">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <h2>Employee Dashboard</h2>
    </div>
    <a class="logout" href="/logout">Logout</a>
</div>

<div class="container">
<h3>Apply Out Permission</h3>

<form method="post">
<div class="grid">
    <div class="input-group">
        <label>Date</label>
        <input type="date" name="date" required>
    </div>

    <div class="input-group">
        <label>Permission Type</label>
        <select name="type" required>
            <option value="">Select Type</option>
            <option>Official</option>
            <option>Personal</option>
            <option>1 Hour Permission</option>
            <option>Late Permission</option>
        </select>
    </div>

    <div class="input-group"><label>Out Time</label><input type="time" name="out" required></div>
    <div class="input-group"><label>Return Time</label><input type="time" name="ret" required></div>
    <div class="input-group full"><label>Reason</label><textarea name="reason" required></textarea></div>
</div>
<button>Submit Request</button>
</form>

<p style="color:green;">{{msg}}</p>
</div>
""", msg=msg)

@app.route("/manager")
def manager():
    if session.get("role") != "manager":
        return redirect("/")

    conn = db()
    cur = conn.cursor()
    cur.execute("""
    SELECT p.id, p.emp_id, e.name, e.department, e.manager_name,
           p.date, p.type, p.reason, p.out_time, p.return_time,
           p.manager, p.hr, p.gate_mail
    FROM permission_requests p
    LEFT JOIN employees e ON p.emp_id = e.emp_id
    WHERE p.manager_emp_id=?
    ORDER BY p.id DESC
    """, (session["emp_id"],))
    data = cur.fetchall()
    conn.close()

    return render_template_string(STYLE + """
<div class="topbar">
    <div class="brand">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <h2>Manager Dashboard</h2>
    </div>
    <a class="logout" href="/logout">Logout</a>
</div>

<div class="container">
<h3>Requests Assigned To You</h3>

<div class="request-grid">
{% for r in data %}
<div class="request-card">
    <h4>Request #{{r[0]}} - {{r[2]}}</h4>

    <div class="info-row"><b>Emp ID</b><span>{{r[1]}}</span></div>
    <div class="info-row"><b>Department</b><span>{{r[3]}}</span></div>
    <div class="info-row"><b>Date</b><span>{{r[5]}}</span></div>
    <div class="info-row"><b>Type</b><span>{{r[6]}}</span></div>
    <div class="info-row"><b>Out Time</b><span>{{r[8]}}</span></div>
    <div class="info-row"><b>Return Time</b><span>{{r[9]}}</span></div>
    <div class="info-row"><b>Manager Status</b><span class="badge {% if r[10]=='Approved' %}approved{% elif r[10]=='Rejected' %}rejected{% else %}pending{% endif %}">{{r[10]}}</span></div>
    <div class="info-row"><b>HR Status</b><span class="badge {% if r[11]=='Approved' %}approved{% elif r[11]=='Rejected' %}rejected{% else %}pending{% endif %}">{{r[11]}}</span></div>
    <div class="info-row"><b>Gate Mail</b><span class="badge sent">{{r[12]}}</span></div>

    <div class="reason-box">
        <b>Reason:</b><br>{{r[7]}}
    </div>

    {% if r[10] == "Pending" %}
    <div class="action-area">
        <a class="action-btn approve" href="/manager_action/{{r[0]}}/approve">Approve</a>
        <a class="action-btn reject" href="/manager_action/{{r[0]}}/reject">Reject</a>
    </div>
    {% else %}
    <p class="waiting">Decision Completed</p>
    {% endif %}
</div>
{% endfor %}
</div>
</div>
""", data=data)

@app.route("/manager_action/<int:req_id>/<action>")
def manager_action(req_id, action):
    if session.get("role") != "manager":
        return redirect("/")

    status = "Approved" if action == "approve" else "Rejected"

    conn = db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE permission_requests
        SET manager=?
        WHERE id=? AND manager_emp_id=?
    """, (status, req_id, session["emp_id"]))
    conn.commit()
    conn.close()

    return redirect("/manager")

@app.route("/hr")
def hr():
    if session.get("role") != "hr":
        return redirect("/")

    conn = db()
    cur = conn.cursor()
    cur.execute("""
    SELECT p.id, p.emp_id, e.name, e.email, e.department, e.manager_name,
           p.date, p.type, p.reason, p.out_time, p.return_time,
           p.manager, p.hr, p.gate_mail
    FROM permission_requests p
    LEFT JOIN employees e ON p.emp_id = e.emp_id
    ORDER BY p.id DESC
    """)
    data = cur.fetchall()
    conn.close()

    return render_template_string(STYLE + """
<div class="topbar">
    <div class="brand">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <h2>HR Dashboard</h2>
    </div>
    <a class="logout" href="/logout">Logout</a>
</div>

<div class="container">
<h3>HR Permission Approval Panel</h3>

<div class="request-grid">
{% for r in data %}
<div class="request-card">
    <h4>Request #{{r[0]}} - {{r[2]}}</h4>

    <div class="info-row"><b>Emp ID</b><span>{{r[1]}}</span></div>
    <div class="info-row"><b>Email</b><span>{{r[3]}}</span></div>
    <div class="info-row"><b>Department</b><span>{{r[4]}}</span></div>
    <div class="info-row"><b>Manager</b><span>{{r[5]}}</span></div>
    <div class="info-row"><b>Date</b><span>{{r[6]}}</span></div>
    <div class="info-row"><b>Type</b><span>{{r[7]}}</span></div>
    <div class="info-row"><b>Out Time</b><span>{{r[9]}}</span></div>
    <div class="info-row"><b>Return Time</b><span>{{r[10]}}</span></div>
    <div class="info-row"><b>Manager Status</b><span class="badge {% if r[11]=='Approved' %}approved{% elif r[11]=='Rejected' %}rejected{% else %}pending{% endif %}">{{r[11]}}</span></div>
    <div class="info-row"><b>HR Status</b><span class="badge {% if r[12]=='Approved' %}approved{% elif r[12]=='Rejected' %}rejected{% else %}pending{% endif %}">{{r[12]}}</span></div>
    <div class="info-row"><b>Gate Mail</b><span class="badge sent">{{r[13]}}</span></div>

    <div class="reason-box">
        <b>Reason:</b><br>{{r[8]}}
    </div>

    {% if r[11] == "Approved" and r[12] == "Pending" %}
    <div class="action-area">
        <a class="action-btn approve" href="/hr_action/{{r[0]}}/approve">Approve</a>
        <a class="action-btn reject" href="/hr_action/{{r[0]}}/reject">Reject</a>
    </div>
    {% elif r[11] == "Pending" %}
        <p class="waiting">Waiting for Manager Approval</p>
    {% elif r[11] == "Rejected" %}
        <p class="waiting">Rejected by Manager</p>
    {% else %}
        <p class="waiting">Decision Completed</p>
    {% endif %}
</div>
{% endfor %}
</div>
</div>
""", data=data)

@app.route("/hr_action/<int:req_id>/<action>")
def hr_action(req_id, action):
    if session.get("role") != "hr":
        return redirect("/")

    status = "Approved" if action == "approve" else "Rejected"

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE permission_requests
        SET hr=?
        WHERE id=? AND manager='Approved'
    """, (status, req_id))

    conn.commit()

    if status == "Approved":
        cur.execute("""
        SELECT p.emp_id, e.name, e.department, p.date, p.type, p.reason, p.out_time, p.return_time
        FROM permission_requests p
        LEFT JOIN employees e ON p.emp_id = e.emp_id
        WHERE p.id=?
        """, (req_id,))
        data = cur.fetchone()

        if data:
            send_gate_email(
                data[0], data[1], data[2], data[3],
                data[4], data[5], data[6], data[7]
            )

            cur.execute("""
            UPDATE permission_requests
            SET gate_mail='Sent'
            WHERE id=?
            """, (req_id,))
            conn.commit()

    conn.close()
    return redirect("/hr")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)