import sqlite3
from datetime import datetime


DATABASE = "doctor_patient.db"

db = sqlite3.connect(DATABASE)

current_time = datetime.utcnow().isoformat(sep=" ")


# Add audit columns to doctors table
doctor_columns = [
    "created_at",
    "updated_at",
    "created_by",
    "updated_by"
]

existing_doctor_columns = [
    row[1]
    for row in db.execute("PRAGMA table_info(doctors)").fetchall()
]

for column in doctor_columns:
    if column not in existing_doctor_columns:
        if column in ["created_at", "updated_at"]:
            db.execute(
                f"ALTER TABLE doctors ADD COLUMN {column} DATETIME"
            )
        else:
            db.execute(
                f"ALTER TABLE doctors ADD COLUMN {column} INTEGER"
            )


# Add audit columns to patients table
patient_columns = [
    "created_at",
    "updated_at",
    "created_by",
    "updated_by"
]

existing_patient_columns = [
    row[1]
    for row in db.execute("PRAGMA table_info(patients)").fetchall()
]

for column in patient_columns:
    if column not in existing_patient_columns:
        if column in ["created_at", "updated_at"]:
            db.execute(
                f"ALTER TABLE patients ADD COLUMN {column} DATETIME"
            )
        else:
            db.execute(
                f"ALTER TABLE patients ADD COLUMN {column} INTEGER"
            )


# Fill audit values for existing doctors
db.execute(
    """
    UPDATE doctors
    SET created_at = COALESCE(created_at, ?),
        updated_at = COALESCE(updated_at, ?)
    """,
    (current_time, current_time)
)


# Fill audit values for existing patients
db.execute(
    """
    UPDATE patients
    SET created_at = COALESCE(created_at, ?),
        updated_at = COALESCE(updated_at, ?)
    """,
    (current_time, current_time)
)

appointment_columns = [
    "created_at",
    "updated_at",
    "created_by",
    "updated_by"
]

existing_appointment_columns = [
    row[1]
    for row in db.execute(
        "PRAGMA table_info(appointments)"
    ).fetchall()
]

for column in appointment_columns:
    if column not in existing_appointment_columns:
        if column in ["created_at", "updated_at"]:
            db.execute(
                f"ALTER TABLE appointments ADD COLUMN {column} DATETIME"
            )
        else:
            db.execute(
                f"ALTER TABLE appointments ADD COLUMN {column} INTEGER"
            )

db.execute(
    """UPDATE appointments
       SET created_at = COALESCE(created_at, ?),
           updated_at = COALESCE(updated_at, ?)""",
    (current_time, current_time)
)

db.commit()
db.close()

print("Database migration completed successfully.")