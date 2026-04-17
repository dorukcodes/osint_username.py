import tkinter as tk
from tkinter import scrolledtext
import subprocess

def scan():
    username = entry.get().strip()
    output_box.delete(1.0, tk.END)

    if not username:
        output_box.insert(tk.END, "Username gir bro\n")
        return

    try:
        result = subprocess.run(
            ["python", "osint_username.py", "-u", username],
            capture_output=True,
            text=True
        )

        output_box.insert(tk.END, result.stdout)

    except Exception as e:
        output_box.insert(tk.END, f"Error: {e}")


app = tk.Tk()
app.title("Doruk OSINT Tool")
app.geometry("700x500")
app.configure(bg="#0f0f0f")

# başlık
title = tk.Label(app, text="DORUK OSINT PANEL", fg="lime", bg="#0f0f0f", font=("Courier", 16))
title.pack(pady=10)

# input
entry = tk.Entry(app, width=40, bg="black", fg="lime", insertbackground="lime")
entry.pack(pady=10)

# buton
btn = tk.Button(app, text="SCAN", command=scan, bg="black", fg="lime")
btn.pack()

# output
output_box = scrolledtext.ScrolledText(app, width=85, height=20, bg="black", fg="lime")
output_box.pack(pady=10)

app.mainloop()
