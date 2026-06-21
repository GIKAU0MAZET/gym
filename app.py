from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date, datetime

from database import get_connection
from service.auth_service import authenticate
from service.clients_service import list_clients, get_client, create_client, edit_client
from service.requests_service import list_requests, get_request, create_request, edit_request
from service.abonements_service import list_abonement_types, list_client_abonements, get_abonement, sell_abonement, edit_abonement
from service.trainings_service import list_trainings, get_training, create_training, edit_training, get_clients_of_training, add_client_to_training, set_attendance
from service.director_service import get_gym, list_employees, get_employee, create_employee, edit_employee, report_sales, report_active, report_trainers
from service.trainer_service import list_my_trainings, get_clients_for_training, set_attendance as trainer_set_attendance
from repositories.abonement_types_repo import get_all_types, get_type_by_id, add_type, update_type
from repositories.visits_repo import get_all_visits, add_visit

app = Flask(__name__)
app.secret_key = "gym_secret_key_2026"


@app.context_processor
def inject_globals():
    gym_name = "FitManager"
    current_user = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT название_зала FROM тренажерный_зал LIMIT 1")
        row = cur.fetchone()
        if row:
            gym_name = row[0]
        if "employee_id" in session:
            cur.execute(
                "SELECT фамилия || ' ' || имя FROM сотрудники WHERE id_сотрудника=%s",
                (session["employee_id"],)
            )
            r = cur.fetchone()
            if r:
                current_user = r[0]
        conn.close()
    except:
        pass
    return {"gym_name": gym_name, "current_user": current_user,
            "today": date.today(), "now": datetime.now()}


def require_role(*roles):
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in roles:
        return redirect("/login")
    return None


# ── AUTH ──────────────────────────────────────────────────────

@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form.get("login"), request.form.get("password"))
    if not user:
        return render_template("login.html", error="Неверный логин или пароль")
    session["user_id"] = user[0]
    session["employee_id"] = user[3]
    session["role"] = user[4]
    role = user[4]
    if role == "Администратор":
        return redirect("/clients")
    elif role == "Директор":
        return redirect("/director/employees")
    elif role == "Тренер":
        return redirect("/trainer/trainings")
    return redirect("/clients")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    role = session.get("role")
    if role == "Директор":
        return redirect("/director/employees")
    elif role == "Тренер":
        return redirect("/trainer/trainings")
    return redirect("/clients")


# ── КЛИЕНТЫ ───────────────────────────────────────────────────

@app.route("/clients")
def clients():
    err = require_role("Администратор")
    if err: return err
    return render_template("clients.html", clients=list_clients())


@app.route("/clients/add", methods=["GET", "POST"])
def add_client():
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        create_client(request.form["last_name"], request.form["first_name"],
                      request.form.get("middle_name"), request.form.get("phone"), request.form.get("email"))
        return redirect("/clients")
    return render_template("client_form.html", client=None)


@app.route("/clients/edit/<int:client_id>", methods=["GET", "POST"])
def edit_client_route(client_id):
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        edit_client(client_id, request.form["last_name"], request.form["first_name"],
                    request.form.get("middle_name"), request.form.get("phone"), request.form.get("email"))
        return redirect("/clients")
    return render_template("client_form.html", client=get_client(client_id))


# ── ЗАЯВКИ ────────────────────────────────────────────────────

@app.route("/requests")
def requests_list():
    err = require_role("Администратор")
    if err: return err
    return render_template("requests.html", requests=list_requests())


@app.route("/requests/add", methods=["GET", "POST"])
def add_request():
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        create_request(request.form["client_id"], request.form["type_id"], session["employee_id"])
        return redirect("/requests")
    return render_template("request_form.html", req=None,
                           clients=list_clients(), types=list_abonement_types())


@app.route("/requests/edit/<int:req_id>", methods=["GET", "POST"])
def edit_request_route(req_id):
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        edit_request(req_id, request.form["client_id"], request.form["type_id"], request.form["status"])
        return redirect("/requests")
    return render_template("request_form.html", req=get_request(req_id),
                           clients=list_clients(), types=list_abonement_types())


# ── АБОНЕМЕНТЫ ────────────────────────────────────────────────

@app.route("/abonements")
def abonements():
    err = require_role("Администратор")
    if err: return err
    return render_template("abonements.html", abonements=list_client_abonements(), today=date.today())


@app.route("/abonements/sell", methods=["GET", "POST"])
@app.route("/abonements/sell/<int:request_id>", methods=["GET", "POST"])
def sell_abonement_route(request_id=None):
    err = require_role("Администратор")
    if err: return err
    types = list_abonement_types()
    if request.method == "POST":
        t = next((x for x in types if x[0] == int(request.form["type_id"])), None)
        sell_abonement(request.form["client_id"], request.form["type_id"],
                       request.form["start_date"], t[3] if t else 30,
                       session["employee_id"], request.form.get("request_id") or None)
        return redirect("/abonements")
    selected_client = None
    selected_type = None
    if request_id:
        req = get_request(request_id)
        if req:
            selected_client = req[1]
            selected_type = req[2]
    return render_template("sell_abonement.html", clients=list_clients(), types=types,
                           request_id=request_id, selected_client=selected_client,
                           selected_type=selected_type, today=date.today().isoformat())


@app.route("/abonements/edit/<int:abo_id>", methods=["GET", "POST"])
def edit_abonement_route(abo_id):
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        edit_abonement(abo_id, request.form["client_id"], request.form["type_id"],
                       request.form["start_date"], request.form["end_date"])
        return redirect("/abonements")
    return render_template("edit_abonement.html", abo=get_abonement(abo_id),
                           clients=list_clients(), types=list_abonement_types())


# ── ТРЕНИРОВКИ (Администратор) ────────────────────────────────

@app.route("/trainings")
def trainings():
    err = require_role("Администратор")
    if err: return err
    return render_template("trainings.html", trainings=list_trainings())


@app.route("/trainings/add", methods=["GET", "POST"])
def add_training():
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        create_training(request.form["employee_id"], 1,
                        request.form["datetime_val"], request.form["name"],
                        request.form["max_participants"])
        return redirect("/trainings")
    trainers = [(e[0], e[1], e[2]) for e in list_employees() if e[4] == "Тренер"]
    return render_template("training_form.html", training=None, trainers=trainers)


@app.route("/trainings/edit/<int:tr_id>", methods=["GET", "POST"])
def edit_training_route(tr_id):
    err = require_role("Администратор")
    if err: return err
    if request.method == "POST":
        edit_training(tr_id, request.form["employee_id"],
                      request.form["datetime_val"], request.form["name"],
                      request.form["max_participants"])
        return redirect("/trainings")
    trainers = [(e[0], e[1], e[2]) for e in list_employees() if e[4] == "Тренер"]
    return render_template("training_form.html", training=get_training(tr_id), trainers=trainers)


@app.route("/trainings/<int:tr_id>/clients")
def training_clients(tr_id):
    err = require_role("Администратор")
    if err: return err
    return render_template("training_clients.html", training_id=tr_id,
                           enrolled=get_clients_of_training(tr_id), clients=list_clients())


@app.route("/trainings/<int:tr_id>/enroll", methods=["POST"])
def enroll_client(tr_id):
    err = require_role("Администратор")
    if err: return err
    add_client_to_training(tr_id, request.form["client_id"])
    return redirect(f"/trainings/{tr_id}/clients")


@app.route("/trainings/<int:tr_id>/attend", methods=["POST"])
def attend_training(tr_id):
    err = require_role("Администратор")
    if err: return err
    set_attendance(tr_id, request.form["client_id"], request.form["attended"] == "1")
    return redirect(f"/trainings/{tr_id}/clients")


# ── ДИРЕКТОР ──────────────────────────────────────────────────

@app.route("/director/employees")
def director_employees():
    err = require_role("Директор")
    if err: return err
    return render_template("director_employees.html", employees=list_employees())


@app.route("/director/employees/add", methods=["GET", "POST"])
def director_add_employee():
    err = require_role("Директор")
    if err: return err
    if request.method == "POST":
        create_employee(request.form["last_name"], request.form["first_name"],
                        request.form.get("middle_name"), request.form["position"],
                        request.form.get("phone"), request.form.get("email"), request.form["hire_date"])
        return redirect("/director/employees")
    return render_template("director_employee_form.html", emp=None)


@app.route("/director/employees/edit/<int:emp_id>", methods=["GET", "POST"])
def director_edit_employee(emp_id):
    err = require_role("Директор")
    if err: return err
    if request.method == "POST":
        edit_employee(emp_id, request.form["last_name"], request.form["first_name"],
                      request.form.get("middle_name"), request.form["position"],
                      request.form.get("phone"), request.form.get("email"), request.form["hire_date"])
        return redirect("/director/employees")
    return render_template("director_employee_form.html", emp=get_employee(emp_id))


@app.route("/director/gym-info")
def director_gym_info():
    err = require_role("Директор")
    if err: return err
    return render_template("director_gym_info.html", info=get_gym())


@app.route("/director/requests")
def director_requests():
    err = require_role("Директор")
    if err: return err
    return render_template("director_requests.html", requests=list_requests())


@app.route("/director/reports")
def director_reports():
    err = require_role("Директор")
    if err: return err
    return render_template("director_reports.html")


@app.route("/director/reports/sales")
def director_report_sales():
    err = require_role("Директор")
    if err: return err
    date_from = request.args.get("date_from", date.today().replace(day=1).isoformat())
    date_to = request.args.get("date_to", date.today().isoformat())
    return render_template("report_sales.html", rows=report_sales(date_from, date_to),
                           date_from=date_from, date_to=date_to)


@app.route("/director/reports/active")
def director_report_active():
    err = require_role("Директор")
    if err: return err
    return render_template("report_active.html", rows=report_active())


@app.route("/director/reports/trainers")
def director_report_trainers():
    err = require_role("Директор")
    if err: return err
    return render_template("report_trainers.html", rows=report_trainers())


# ── ТРЕНЕР ────────────────────────────────────────────────────

@app.route("/trainer/trainings")
def trainer_trainings():
    err = require_role("Тренер")
    if err: return err
    return render_template("trainer_trainings.html",
                           trainings=list_my_trainings(session["employee_id"]),
                           now=datetime.now())


@app.route("/trainer/trainings/<int:tr_id>/attend")
def trainer_attend_page(tr_id):
    err = require_role("Тренер")
    if err: return err
    return render_template("trainer_attend.html",
                           training=get_training(tr_id),
                           clients=get_clients_for_training(tr_id))


@app.route("/trainer/trainings/<int:tr_id>/attend", methods=["POST"])
def trainer_attend(tr_id):
    err = require_role("Тренер")
    if err: return err
    trainer_set_attendance(tr_id, request.form["client_id"], request.form["attended"] == "1")
    return redirect(f"/trainer/trainings/{tr_id}/attend")



# ── ТИПЫ АБОНЕМЕНТОВ (Директор) ──────────────────────────────

@app.route("/director/abo-types")
def director_abo_types():
    err = require_role("Директор")
    if err: return err
    return render_template("director_abo_types.html", types=get_all_types())


@app.route("/director/abo-types/add", methods=["GET", "POST"])
def director_add_abo_type():
    err = require_role("Директор")
    if err: return err
    if request.method == "POST":
        add_type(request.form["name"], request.form["cost"], request.form["days"])
        return redirect("/director/abo-types")
    return render_template("director_abo_type_form.html", t=None)


@app.route("/director/abo-types/edit/<int:type_id>", methods=["GET", "POST"])
def director_edit_abo_type(type_id):
    err = require_role("Директор")
    if err: return err
    if request.method == "POST":
        update_type(type_id, request.form["name"], request.form["cost"], request.form["days"])
        return redirect("/director/abo-types")
    return render_template("director_abo_type_form.html", t=get_type_by_id(type_id))


# ── ПОСЕЩЕНИЯ (Администратор) ─────────────────────────────────

@app.route("/visits")
def visits():
    err = require_role("Администратор")
    if err: return err
    return render_template("visits.html", visits=get_all_visits(), clients=list_clients())


@app.route("/visits/add", methods=["POST"])
def add_visit_route():
    err = require_role("Администратор")
    if err: return err
    add_visit(request.form["client_id"])
    return redirect("/visits")


if __name__ == "__main__":
    app.run(debug=True)
