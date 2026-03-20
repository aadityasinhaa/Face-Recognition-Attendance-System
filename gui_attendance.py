import customtkinter as ctk
import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime
from PIL import Image


# ================= CONSTANTS =================
# Scale factor applied to each frame before face recognition.
# A value of 0.5 reduces the image to 25% of its original area, cutting
# recognition time to roughly 25% while still detecting faces reliably.
FRAME_SCALE = 0.5

# Run expensive face recognition every Nth frame and reuse results for the
# frames in between.  This keeps the display smooth while reducing CPU load.
PROCESS_EVERY_N_FRAMES = 3

# Maximum face-distance threshold for a positive match (lower = stricter).
FACE_DISTANCE_THRESHOLD = 0.6

# ================= GLOBAL STATE =================
marked_students = set()
camera_running = False
cap = None
known_encodings = []
known_names = []

# Cached results from the last processed frame (list of ((top, right, bottom, left), name))
_last_face_data = []
_frame_count = 0

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
            # np.array() already produces a C-contiguous array; no need for
            # an extra np.ascontiguousarray() call.
            img = np.array(pil_img, dtype=np.uint8)

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

        # Call datetime.now() once to guarantee date and time are consistent.
        now = datetime.now()
        date_today = now.strftime("%Y-%m-%d")
        time_now = now.strftime("%H:%M:%S")

        writer.writerow([name, date_today, time_now])

    print(f"Attendance marked for {name} on {date_today}")

# ================= CAMERA FUNCTIONS =================
def start_attendance():
    global camera_running, cap, _last_face_data, _frame_count

    if camera_running:
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not opened")
        return

    camera_running = True
    _last_face_data = []
    _frame_count = 0
    print("Camera started")

    def update_frame():
        global camera_running, cap, _last_face_data, _frame_count

        if not camera_running:
            return

        ret, frame = cap.read()
        if not ret:
            stop_attendance()
            return

        _frame_count += 1

        # Only run the expensive face-recognition pipeline every
        # PROCESS_EVERY_N_FRAMES frames.  Display the cached bounding boxes
        # on the intermediate frames so the preview still looks smooth.
        if _frame_count % PROCESS_EVERY_N_FRAMES == 0:
            # Convert BGR → RGB (CRITICAL)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = np.ascontiguousarray(rgb)

            # Downscale before detection – processes ~FRAME_SCALE² of the
            # pixels, giving a large speed-up with minimal accuracy loss.
            small_rgb = cv2.resize(rgb, (0, 0), fx=FRAME_SCALE, fy=FRAME_SCALE)

            face_locations = face_recognition.face_locations(small_rgb)
            face_encodings = face_recognition.face_encodings(small_rgb, face_locations)

            _last_face_data = []
            inv = 1.0 / FRAME_SCALE  # scale factor back to original size
            for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
                # Scale coordinates back to the original frame size.
                orig_loc = (int(top * inv), int(right * inv),
                            int(bottom * inv), int(left * inv))

                name = "Unknown"
                if known_encodings:
                    # face_distance gives a continuous similarity score; pick
                    # the closest known encoding instead of the first match.
                    face_distances = face_recognition.face_distance(known_encodings, face_enc)
                    best_idx = np.argmin(face_distances)
                    if face_distances[best_idx] < FACE_DISTANCE_THRESHOLD:
                        name = known_names[best_idx]
                        mark_attendance(name)

                _last_face_data.append((orig_loc, name))

        # Draw cached results on every frame so the display is always current.
        for (top, right, bottom, left), name in _last_face_data:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Attendance Camera", frame)

        # 30 ms ≈ 33 fps – sufficient for smooth preview and leaves the CPU
        # free for recognition work on the processed frames.
        app.after(30, update_frame)

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


