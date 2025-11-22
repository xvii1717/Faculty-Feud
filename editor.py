import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox


DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "questions.json")


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_round(root):
    q = simpledialog.askstring("Question", "Enter the question text:", parent=root)
    if not q:
        return
    answers = []
    while True:
        text = simpledialog.askstring("Answer", "Enter an answer (leave blank to finish):", parent=root)
        if not text:
            break
        points = simpledialog.askinteger("Points", "Points for this answer:", parent=root, minvalue=0, initialvalue=10)
        answers.append({"text": text, "points": points or 0, "revealed": False})

    if not answers:
        messagebox.showinfo("No answers", "No answers added; round will not be saved.")
        return

    data = load_data()
    data.setdefault("rounds", []).append({"question": q, "answers": answers})
    save_data(data)
    messagebox.showinfo("Saved", "Round added to questions.json")


def main():
    root = tk.Tk()
    root.title("Faculty Feud - Question Editor")
    root.geometry("400x200")

    add_btn = tk.Button(root, text="Add Round", command=lambda: add_round(root))
    add_btn.pack(pady=12)

    root.mainloop()


if __name__ == "__main__":
    main()
