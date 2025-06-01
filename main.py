import tkinter as tk
from tkinter import messagebox
import random
import json


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kvíz játék")
        self.root.geometry("500x400")

        f = open("kerdesek.json", "r", encoding="utf-8")
        self.questions = json.load(f)["kerdesek"]
        f.close()
        for question in self.questions:
            print(question)
            self.shuffle_asnwers(question)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.question_label = tk.Label(self.main_frame, text="", wraplength=480, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack()
        
        self.answer_buttons = []
        self.selected_buttons = []

        self.valaszok = []
        
        self.submit_btn = tk.Button(self.main_frame, text="Válasz beküldése", command=self.check_answer)
        self.submit_btn.pack(pady=10)

        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.result_label.pack()

        self.next_btn = tk.Button(self.main_frame, text="Következő kérdés", command=self.load_next_question, state="disabled")
        self.next_btn.pack(pady=10)

        self.load_next_question()

    def load_next_question(self):
        self.result_label.config(text="")
        self.next_btn.config(state="disabled")

        self.current_question = random.choice(self.questions)
        self.question_label.config(text=self.current_question["kerdes"])

        for btn in self.answer_buttons:
            btn.destroy()
        self.answer_buttons.clear()
        self.valaszok = []
        
        for i in range(len(self.current_question["valaszlehetosegek"])):
            btn = tk.Button(self.options_frame, 
                            text = self.current_question["valaszlehetosegek"][i],
                            command = lambda x = i: self.set_valasz(x) )
            btn.config(bg="lightgray")
            btn.pack()
            self.answer_buttons.append(btn)

        self.submit_btn.config(state="normal")

    def shuffle_asnwers(self, question):
        correct = question["helyes_valasz"]
        correct_text = [question["valaszlehetosegek"][i] for i in correct]
        random.shuffle(question["valaszlehetosegek"])
        new_correct = []
        for i in range(len(question["valaszlehetosegek"])):
            if question["valaszlehetosegek"][i] in correct_text:
                new_correct.append(i)
        question["helyes_valasz"] = new_correct

    def set_valasz(self, x):
        if (x not in self.valaszok):
            self.valaszok.append(x)
        else:
            self.valaszok.remove(x)
        for i in range(len(self.answer_buttons)):
            if i in self.valaszok:
                self.answer_buttons[i].config(bg="green")
            else:
                self.answer_buttons[i].config(bg="lightgray")
        
    def check_answer(self):
        correct = set(self.current_question["helyes_valasz"])

        if set(self.valaszok) == correct:
            self.result_label.config(text="✅ Helyes válasz!", fg="green")
        else:
            helyes_szöveg = ", ".join(
                [self.current_question["valaszlehetosegek"][i] for i in correct]
            )
            self.result_label.config(
                text=f"❌ Hibás válasz!\n👉 Helyes(ek): {helyes_szöveg}", fg="red"
            )

        self.submit_btn.config(state="disabled")
        self.next_btn.config(state="normal")

# Ablak indítása
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
