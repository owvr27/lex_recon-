import customtkinter as ctk
from core.engine import run

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("LexRecon")

domain = ctk.CTkEntry(app, placeholder_text="example.com")
domain.pack(pady=10)

def start(mode):
    run(domain.get(), mode, {})

ctk.CTkButton(app, text="FAST", command=lambda: start("fast")).pack()
ctk.CTkButton(app, text="DEEP", command=lambda: start("deep")).pack()
ctk.CTkButton(app, text="SMART", command=lambda: start("smart")).pack()

app.mainloop()
