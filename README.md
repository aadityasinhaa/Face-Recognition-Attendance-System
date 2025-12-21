📸 Face Recognition Attendance System (Python)

A GUI-based Face Recognition Attendance System built using Python, OpenCV, face_recognition, dlib, and CustomTkinter.
The system captures live video from a webcam, recognizes faces, and records one-time attendance per student with date and time in a CSV file.

🚀 Features
🔐 Login system (GUI based)
🎥 Real-time webcam face detection
🧠 Face recognition using dlib & face_recognition
📝 Attendance stored in CSV file
📅 Date and time included
🚫 Duplicate attendance prevention (one student → one entry)
▶️ Start / Stop camera buttons
🖥️ Modern GUI using CustomTkinter
🛑 Proper camera release on exit
🧠 Working Principle:

User logs in using valid credentials.

Webcam starts capturing video.

Faces are detected and encoded.

Encodings are matched with stored images.

Attendance is marked only once per student.

Attendance is saved with Name, Date, Time.

📂 Project Structure
Attendance System/
│
├── gui_attendance.py        # Main attendance GUI
├── login.py                 # Login window
├── camera_test.py           # Camera backend test
├── test_imports.py          # Dependency check
├── attendance.csv           # Attendance records
│
├── images/
│   ├── aadi.jpg
│   ├── rishi.jpg
│   └── varun.jpg
│
├── .venv/                   # Virtual environment
└── README.md

🛠️ Requirements

Python 3.10.x (Recommended)

Windows OS

📦 Required Python Libraries
pip install numpy==1.24.4
pip install opencv-python
pip install face-recognition
pip install customtkinter
pip install pillow


⚠️ Important:
NumPy 2.x is not compatible with dlib and face_recognition.
Always use NumPy 1.24.4.

🔧 Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/aadityasinhaa/face-recognition-attendance.git
cd face-recognition-attendance

2️⃣ Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate

3️⃣ Install Dependencies
pip install numpy==1.24.4 opencv-python face-recognition customtkinter pillow

▶️ How to Run
🔐 Start Login System
python login.py

🔑 Sample Login Credentials
Username: admin
Password: admin123

And you can also add your login credentials in elif tree.

📝 Attendance CSV Format
Name,Date,Time
aadi,2025-12-21,10:32:15
rishi,2025-12-21,10:33:02


✔ One entry per student
✔ No duplicate attendance

🎥 Camera Backend

The project uses DirectShow backend for Windows:

cv2.VideoCapture(0, cv2.CAP_DSHOW)


To test webcam:

python camera_test.py

🎓 Academic Use

This project is suitable for:

College mini projects

AI / ML practicals

Computer Vision demonstrations

Viva & project evaluations

🧑‍💻 Developer

Aaditya Raj
🎓 Student | Python & AI Enthusiast

⭐ Future Enhancements

Date-wise duplicate prevention

Excel export

Voice / sound confirmation

Admin dashboard

Convert to .exe

Database integration

📜 License

This project is free for educational use.
Feel free to fork, modify, and improve.