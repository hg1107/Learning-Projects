import json
from pathlib import Path

# pyrefly: ignore [missing-import]
import streamlit as st

DATABASE = "School_data.json"


def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"students": [], "teachers": []}


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


def validate_email(email):
    return "@" in email and "." in email


st.set_page_config(page_title="School Manager", page_icon="🏫", layout="wide")

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

st.markdown(
    """
    <style>
    .main { background-color: #f7f8fa; }
    h1 { color: #1f2937; }
    .stat-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
    }
    .stat-num { font-size: 28px; font-weight: 700; color: #2563eb; }
    .stat-label { font-size: 13px; color: #6b7280; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("School Manager")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="stat-box"><div class="stat-num">{len(data["students"])}</div>'
                f'<div class="stat-label">Students</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box"><div class="stat-num">{len(data["teachers"])}</div>'
                f'<div class="stat-label">Teachers</div></div>', unsafe_allow_html=True)
with col3:
    total_grades = sum(len(s["grades"]) for s in data["students"])
    st.markdown(f'<div class="stat-box"><div class="stat-num">{total_grades}</div>'
                f'<div class="stat-label">Grades Recorded</div></div>', unsafe_allow_html=True)

st.write("")

tabs = st.tabs(["Register Student", "Register Teacher", "Add Grades", "Students", "Teachers"])

# ---------- Register Student ----------
with tabs[0]:
    st.subheader("New Student")
    with st.form("student_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name")
        age = c2.number_input("Age", min_value=1, max_value=100, step=1)
        email = c1.text_input("Email")
        roll_no = c2.text_input("Roll No")
        submitted = st.form_submit_button("Register Student")

        if submitted:
            if not name or not roll_no or not email:
                st.error("Please fill in all fields.")
            elif not validate_email(email):
                st.error("Invalid email address.")
            elif any(s["roll_no"] == roll_no for s in data["students"]):
                st.warning("A student with this roll number already exists.")
            else:
                data["students"].append({
                    "name": name,
                    "age": age,
                    "email": email,
                    "roll_no": roll_no,
                    "grades": {},
                })
                save_data(data)
                st.success(f"Student {name} registered.")

# ---------- Register Teacher ----------
with tabs[1]:
    st.subheader("New Teacher")
    with st.form("teacher_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name", key="t_name")
        age = c2.number_input("Age", min_value=18, max_value=100, step=1, key="t_age")
        email = c1.text_input("Email", key="t_email")
        emp_id = c2.text_input("Employee ID")
        subject = st.text_input("Subject")
        submitted = st.form_submit_button("Register Teacher")

        if submitted:
            if not name or not emp_id or not email:
                st.error("Please fill in all fields.")
            elif not validate_email(email):
                st.error("Invalid email address.")
            elif any(t["emp_id"] == emp_id for t in data["teachers"]):
                st.warning("A teacher with this employee ID already exists.")
            else:
                data["teachers"].append({
                    "name": name,
                    "age": age,
                    "email": email,
                    "emp_id": emp_id,
                    "subjects": subject,
                })
                save_data(data)
                st.success(f"Teacher {name} registered.")

# ---------- Add Grades ----------
with tabs[2]:
    st.subheader("Add Grades")
    if not data["students"]:
        st.info("No students registered yet.")
    else:
        roll_lookup = {f'{s["name"]} ({s["roll_no"]})': s for s in data["students"]}
        selection = st.selectbox("Select student", list(roll_lookup.keys()))
        c1, c2 = st.columns(2)
        subject = c1.text_input("Subject")
        marks = c2.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5)

        if st.button("Add Grade"):
            if not subject:
                st.error("Enter a subject.")
            else:
                roll_lookup[selection]["grades"][subject] = marks
                save_data(data)
                st.success("Grade added.")

# ---------- Students list ----------
with tabs[3]:
    st.subheader("Students")
    if not data["students"]:
        st.info("No students registered yet.")
    for s in data["students"]:
        grades = s["grades"]
        avg = (sum(grades.values()) / len(grades)) if grades else 0
        with st.expander(f'{s["name"]} — Roll No {s["roll_no"]}'):
            st.write(f"**Age:** {s['age']}")
            st.write(f"**Email:** {s['email']}")
            if grades:
                st.table(
                    {"Subject": list(grades.keys()), "Marks": list(grades.values())}
                )
                st.write(f"**Average:** {avg:.2f}")
            else:
                st.write("No grades recorded yet.")

# ---------- Teachers list ----------
with tabs[4]:
    st.subheader("Teachers")
    if not data["teachers"]:
        st.info("No teachers registered yet.")
    for t in data["teachers"]:
        with st.expander(f'{t["name"]} — ID {t["emp_id"]}'):
            st.write(f"**Age:** {t['age']}")
            st.write(f"**Email:** {t['email']}")
            st.write(f"**Subject:** {t['subjects']}")