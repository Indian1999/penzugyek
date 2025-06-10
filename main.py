import tkinter as tk
from tkinter import font
from tkinter import messagebox
import random
import json
import os


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kvíz játék")
        
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.questions = {}

        self.checkbox_vars = {}
        self.q_list_checkboxes = []
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        
        self.questions_frame = tk.Frame(self.main_frame, width=self.screen_width*0.8, height = self.screen_height)
        self.questions_frame.grid(row=0, column=1, pady = 10)
        self.questions_frame.grid_propagate(False)
        self.questions_frame.columnconfigure(0, weight=1)
        
        self.questions_list_frame = tk.Frame(self.main_frame,width=self.screen_width*0.2, height = self.screen_height)
        self.questions_list_frame.grid(row=0, column=0, padx = 20)
        self.questions_list_frame.grid_propagate(False)
        self.questions_list_frame.columnconfigure(0, weight=1)
        
        tk.Label(self.questions_list_frame, text="Aktív kérdések")
        
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith(".json"):
                f = open(file, "r", encoding="utf-8")
                self.questions[file] = json.load(f)["kerdesek"]
                self.checkbox_vars[file] = tk.BooleanVar(value = True)
                self.q_list_checkboxes.append(
                    tk.Checkbutton(
                                    self.questions_list_frame, 
                                    text = file.replace(".json",""),
                                    variable= self.checkbox_vars[file],
                                    font = font.Font(size=15)
                                   )
                    )
                self.q_list_checkboxes[-1].pack()
                f.close()
        for key in self.questions.keys():   
            for question in self.questions[key]:
                self.shuffle_asnwers(question)
        
        self.question_label = tk.Label(self.questions_frame, text="", wraplength=480, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.questions_frame)
        self.options_frame.pack()
        
        self.answer_buttons = []
        self.selected_buttons = []

        self.valaszok = []
        
        self.submit_btn = tk.Button(self.questions_frame, text="Válasz beküldése", command=self.check_answer)
        self.submit_btn.pack(pady=10)

        self.result_label = tk.Label(self.questions_frame, text="", font=("Arial", 12))
        self.result_label.pack()

        self.next_btn = tk.Button(self.questions_frame, text="Következő kérdés", command=self.load_next_question, state="disabled")
        self.next_btn.pack(pady=10)

        self.load_next_question()
    
    def set_current_question(self):
        good_keys = [key for key in self.questions.keys() if self.checkbox_vars[key].get()]
        if len(good_keys) != 0:
            self.current_question = random.choice(list(good_keys))
            self.current_question = random.choice(self.questions[self.current_question])
        else:
            self.current_question = {"kerdes": "Válassz ki legalább egy témakört!", "valaszlehetosegek": ["Jólvan tesa"], "helyes_valasz":[0]}
        
    def load_next_question(self):
        self.result_label.config(text="")
        self.next_btn.config(state="disabled")

        self.set_current_question()
        self.question_label.config(text=self.current_question["kerdes"])

        for btn in self.answer_buttons:
            btn.destroy()
        self.answer_buttons.clear()
        self.valaszok = []
        
        for i in range(len(self.current_question["valaszlehetosegek"])):
            btn = tk.Button(self.options_frame, 
                            text = self.current_question["valaszlehetosegek"][i],
                            command = lambda x = i: self.set_valasz(x))
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
