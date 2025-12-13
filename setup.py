import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import os
import shutil

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Always use a user-writable location for questions.json
def get_writable_questions_path():
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "questions.json")


def load_questions(file_path):
    writable_path = get_writable_questions_path()
    # If not present, copy from bundled resource
    if not os.path.exists(writable_path):
        bundled_path = resource_path(file_path)
        if os.path.exists(bundled_path):
            shutil.copy(bundled_path, writable_path)
        else:
            # If not found, create empty
            with open(writable_path, 'w') as f:
                json.dump({"rounds": []}, f, indent=4)
    try:
        with open(writable_path, 'r') as file:
            return json.load(file)
    except Exception:
        return {"rounds": []}

def save_questions(file_path, data):
    writable_path = get_writable_questions_path()
    with open(writable_path, 'w') as file:
        json.dump(data, file, indent=4)


class QuestionEditor(tk.Tk):
    def __init__(self, file_path):
        super().__init__()
        self.title("Faculty Feud Question Editor")
        self.geometry("500x600")
        self.file_path = file_path
        self.data = load_questions(file_path)

        self.question_var = tk.StringVar()
        self.multiplier_var = tk.StringVar(value="1")
        self.answers = []

        tk.Label(self, text="Enter Question:", font=(None, 14)).pack(pady=8)
        tk.Entry(self, textvariable=self.question_var, font=(None, 14), width=40).pack(pady=4)

        tk.Label(self, text="Multiplier (default 1):", font=(None, 12)).pack(pady=4)
        tk.Entry(self, textvariable=self.multiplier_var, font=(None, 12), width=10).pack(pady=2)

        self.answers_frame = tk.Frame(self)
        self.answers_frame.pack(pady=10)
        tk.Label(self.answers_frame, text="Answers:", font=(None, 13)).grid(row=0, column=0, columnspan=3)
        self.answer_entries = []

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=4)
        self.add_btn = tk.Button(btn_frame, text="Add Another Answer", command=self.add_answer_row)
        self.add_btn.pack(side=tk.LEFT, padx=4)
        self.remove_btn = tk.Button(btn_frame, text="Remove Last Answer", command=self.remove_answer_row)
        self.remove_btn.pack(side=tk.LEFT, padx=4)

        self.add_answer_row()  # Now safe: buttons exist
        self.update_remove_btn_state()

        tk.Button(self, text="Save Question", command=self.save_question).pack(pady=10)
        tk.Button(self, text="Exit", command=self.destroy).pack(pady=4)

        tk.Label(self, text="Instructions: Fill in the question, answers, and points. Click 'Save Question' to add it.", wraplength=480, font=(None, 10)).pack(pady=10)

    def add_answer_row(self):
        row = len(self.answer_entries) + 1
        ans_var = tk.StringVar()
        pts_var = tk.StringVar()
        ans_entry = tk.Entry(self.answers_frame, textvariable=ans_var, width=25)
        pts_entry = tk.Entry(self.answers_frame, textvariable=pts_var, width=8)
        ans_entry.grid(row=row, column=0, padx=2, pady=2)
        pts_entry.grid(row=row, column=1, padx=2, pady=2)
        tk.Label(self.answers_frame, text="Points").grid(row=row, column=2)
        self.answer_entries.append((ans_var, pts_var))
        self.update_remove_btn_state()

    def remove_answer_row(self):
        if len(self.answer_entries) > 1:
            ans_var, pts_var = self.answer_entries.pop()
            # Remove widgets from grid
            for widget in self.answers_frame.grid_slaves(row=len(self.answer_entries)+1):
                widget.destroy()
            self.update_remove_btn_state()

    def update_remove_btn_state(self):
        # Disable remove button if only one answer remains
        if len(self.answer_entries) <= 1:
            self.remove_btn.config(state=tk.DISABLED)
        else:
            self.remove_btn.config(state=tk.NORMAL)

    def save_question(self):
        question_text = self.question_var.get().strip()
        try:
            multiplier = int(self.multiplier_var.get())
        except ValueError:
            multiplier = 1
        answers = []
        for ans_var, pts_var in self.answer_entries:
            ans = ans_var.get().strip()
            try:
                pts = int(pts_var.get())
            except ValueError:
                pts = 0
            if ans:
                answers.append({"text": ans, "points": pts, "revealed": False})
        if not question_text or not answers:
            messagebox.showerror("Missing Info", "Please enter a question and at least one answer.")
            return
        # Sort answers by point value descending
        answers.sort(key=lambda a: a["points"], reverse=True)
        self.data["rounds"].append({
            "question": question_text,
            "answers": answers,
            "multiplier": multiplier
        })
        save_questions(self.file_path, self.data)
        messagebox.showinfo("Saved", "Question added!")
        self.question_var.set("")
        self.multiplier_var.set("1")
        for ans_var, pts_var in self.answer_entries:
            ans_var.set("")
            pts_var.set("")

def main():
    file_path = 'data/questions.json'
    # Clear questions.json on each run (in writable location)
    writable_path = get_writable_questions_path()
    with open(writable_path, 'w') as f:
        json.dump({"rounds": []}, f, indent=4)
    app = QuestionEditor(file_path)
    app.mainloop()

if __name__ == "__main__":
    main()