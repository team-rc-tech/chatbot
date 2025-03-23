from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import psycopg2

class ActionGetDepartments(Action):
    def name(self):
        return "action_get_departments"

    def run(self, dispatcher, tracker, domain):
        # Connect to Supabase PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="rootmywill",
            host="db.nucutcyuiznpgrlxzlte.supabase.co",
            port="5432"
        )
        cursor = conn.cursor()

        # Fetch departments from the database
        cursor.execute("SELECT name FROM departments")
        departments = cursor.fetchall()

        # Format the response
        department_names = ", ".join([dept[0] for dept in departments])
        dispatcher.utter_message(text=f"There are {len(departments)} departments: {department_names}")

        # Close the connection
        cursor.close()
        conn.close()
        return []
    
class ActionGetDoctorsInDepartment(Action):
    def name(self):
        return "action_get_doctors_in_department"

    def run(self, dispatcher, tracker, domain):
        department = tracker.get_slot("department")
        if not department:
            dispatcher.utter_message(text="Please specify a department.")
            return []

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="rootmywill",
            host="db.nucutcyuiznpgrlxzlte.supabase.co",
            port="5432"
        )
        cursor = conn.cursor()

        # Fetch all departments and create a mapping
        cursor.execute("SELECT id, name FROM departments")
        departments = cursor.fetchall()
        department_map = {name.lower(): id for id, name in departments}

        # Get the department ID
        department_id = department_map.get(department.lower())
        if not department_id:
            dispatcher.utter_message(text=f"Department '{department}' not found.")
            return []

        # Fetch doctors in the department
        cursor.execute("SELECT name FROM doctors WHERE department = %s", (department_id,))
        doctors = cursor.fetchall()

        if doctors:
            doctor_names = ", ".join([doc[0] for doc in doctors])
            dispatcher.utter_message(text=f"Doctors in {department}: {doctor_names}")
        else:
            dispatcher.utter_message(text=f"No doctors found in {department}.")

        cursor.close()
        conn.close()
        return []
    
class ActionGetRoomAvailability(Action):
    def name(self):
        return "action_get_room_availability"

    def run(self, dispatcher, tracker, domain):
        room_number = tracker.get_slot("room_number")
        if not room_number:
            dispatcher.utter_message(text="Please specify a room number.")
            return []

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="rootmywill",
            host="db.nucutcyuiznpgrlxzlte.supabase.co",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT available FROM rooms WHERE room_number = %s", (room_number,))
        room = cursor.fetchone()

        if room:
            status = "available" if room[0] == 1 else "occupied"
            dispatcher.utter_message(text=f"Room {room_number} is {status}.")
        else:
            dispatcher.utter_message(text=f"Room {room_number} not found.")

        cursor.close()
        conn.close()
        return []
    

class ActionGetHospitalInfo(Action):
    def name(self):
        return "action_get_hospital_info"

    def run(self, dispatcher, tracker, domain):
        field = tracker.get_slot("field")
        if not field:
            dispatcher.utter_message(text="Please specify what information you need (e.g., name, address).")
            return []

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="rootmywill",
            host="db.nucutcyuiznpgrlxzlte.supabase.co",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM hospital WHERE field = %s", (field,))
        info = cursor.fetchone()

        if info:
            dispatcher.utter_message(text=f"Hospital {field}: {info[0]}")
        else:
            dispatcher.utter_message(text=f"No information found for {field}.")

        cursor.close()
        conn.close()
        return []