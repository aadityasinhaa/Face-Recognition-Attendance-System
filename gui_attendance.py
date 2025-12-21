import customtkinter as ctk
import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime
from PIL import Image


# ================= GLOBAL STATE =================
marked_students = set()
camera_running = False
cap = None
known_encodings = []
known_names = []

# ================= LOAD KNOWN FACES =================
def load_known_faces():
    global known_encodings, known_names

    path = "images"
    known_encodings.clear()
    known_names.clear()

    if not os.path.exists(path):
        print("❌ images folder not found")
        return

    for file in os.listdir(path):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        try:
            img_path = os.path.join(path, file)

            # FORCE TRUE RGB (VERY IMPORTANT)
            pil_img = Image.open(img_path).convert("RGB")
            img = np.array(pil_img, dtype=np.uint8)
            img = np.ascontiguousarray(img)

            enc = face_recognition.face_encodings(img)
            if len(enc) == 0:
                print(f"[SKIP] No face in {file}")
                continue

            known_encodings.append(enc[0])
            known_names.append(os.path.splitext(file)[0])
            print(f"Loaded {file}")

        except Exception as e:
            print(f"[ERROR] {file} → {e}")

# ================= ATTENDANCE CSV =================
def mark_attendance(name):
    global marked_students

    #Prevent duplicate attendance
    if name in marked_students:
        return

    marked_students.add(name)

    file_exists = os.path.exists("attendance.csv")

    with open("attendance.csv", "a", newline="") as f:
        writer = csv.writer(f)

        # Write header only once
        if not file_exists:
            writer.writerow(["Name", "Date", "Time"])

        date_today = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H:%M:%S")

        writer.writerow([name, date_today, time_now])

    print(f"Attendance marked for {name} on {date_today}")

# ================= CAMERA FUNCTIONS =================
def start_attendance():
    global camera_running, cap

    if camera_running:
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not opened")
        return

    camera_running = True
    print("Camera started")

    def update_frame():
        global camera_running, cap

        if not camera_running:
            return

        ret, frame = cap.read()
        if not ret:
            stop_attendance()
            return

        # Convert BGR → RGB (CRITICAL)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = np.ascontiguousarray(rgb)

        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_enc)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]
                mark_attendance(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Attendance Camera", frame)

        app.after(10, update_frame)

    update_frame()

def stop_attendance():
    global camera_running, cap

    if not camera_running:
        return

    camera_running = False

    if cap is not None:
        cap.release()
        cap = None

    cv2.destroyAllWindows()
    print("Camera stopped")

# ================= GUI SETUP =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Face Recognition Attendance System")
app.geometry("400x350")

title = ctk.CTkLabel(app, text="Attendance System", font=("Arial", 22))
title.pack(pady=20)

start_btn = ctk.CTkButton(app, text="Start Attendance", command=start_attendance)
start_btn.pack(pady=10)

stop_btn = ctk.CTkButton(app, text="Stop Attendance", command=stop_attendance)
stop_btn.pack(pady=10)

exit_btn = ctk.CTkButton(app, text="Exit", command=lambda: on_close())
exit_btn.pack(pady=10)

# ================= CLEAN EXIT =================
def on_close():
    stop_attendance()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)

# ================= INIT =================
load_known_faces()
app.mainloop()


