import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- LOGIN FUNCTION ----------------
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Successful", "Welcome!")
        app.destroy()
        subprocess.Popen([sys.executable, "gui_attendance.py"])

    elif username == "aaditya" and password == "aaditya123":
        messagebox.showinfo("Login Successful", "Welcome!")
        app.destroy()
        subprocess.Popen([sys.executable, "gui_attendance.py"])
        
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# ---------------- GUI WINDOW ----------------
app = ctk.CTk()
app.geometry("420x420")
app.title("Login | Attendance System")

frame = ctk.CTkFrame(app, corner_radius=20)
frame.pack(padx=20, pady=20, fill="both", expand=True)

title = ctk.CTkLabel(
    frame,
    text="🔐 Login",
    font=ctk.CTkFont(size=26, weight="bold")
)
title.pack(pady=(40, 10))

subtitle = ctk.CTkLabel(
    frame,
    text="Face Recognition Attendance System",
    font=ctk.CTkFont(size=13)
)
subtitle.pack(pady=(0, 30))

username_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Username",
    width=260,
    height=40
)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Password",
    show="*",
    width=260,
    height=40
)
password_entry.pack(pady=10)

login_btn = ctk.CTkButton(
    frame,
    text="Login",
    width=260,
    height=42,
    font=ctk.CTkFont(size=15),
    command=login
)
login_btn.pack(pady=25)

footer = ctk.CTkLabel(
    frame,
    text="Developed by Aaditya Raj",
    font=ctk.CTkFont(size=11),
    text_color="gray"
)
footer.pack(side="bottom", pady=15)

app.mainloop()
