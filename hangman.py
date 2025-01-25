# Importazione delle librerie necessarie
import tkinter as tk
from tkinter import messagebox
import random


class HangmanGUI:
    def __init__(self, master):
        # Inizializzazione della finestra principale
        self.master = master
        self.master.title("Hangman Game")

        # --- CONFIGURAZIONE DEL GIOCO ---
        self.words = [
            # Marchi italiani
            "ferrari", "lamborghini", "alfaromeo", "fiat", "maserati", "lancia",
            "iveco", "pagani", "ducati", "aprilia",

            # Marchi internazionali
            "toyota", "ford", "honda", "bmw", "mercedes", "volkswagen",
            "hyundai", "tesla", "nissan", "chevrolet", "peugeot", "renault",
            "volvo", "audi", "subaru", "mazda", "porsche", "bentley",
            "rollsroyce", "cadillac", "jeep", "dodge", "chrysler", "bugatti",
            "mclaren", "lotus"]
        self.secret_word = random.choice(self.words).upper()  # Parola casuale in maiuscolo
        self.max_attempts = 3000  # Numero massimo di errori consentiti
        self.remaining_attempts = self.max_attempts  # Contatore tentativi rimasti
        self.guessed_letters = []  # Lista lettere indovinate

        # --- ELEMENTI GRAFICI PRINCIPALI ---
        # Canvas per disegnare l'impiccato
        self.canvas = tk.Canvas(master, width=400, height=300, bg='white')
        self.canvas.pack(pady=20)

        # Label per visualizzare la parola nascosta
        self.word_display = tk.Label(master, font=('Helvetica', 24), fg='navy')
        self.word_display.pack(pady=10)

        # Frame per contenere i pulsanti delle lettere
        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=20)

        # Label per le informazioni di gioco
        self.info_label = tk.Label(master, font=('Helvetica', 12), fg='darkred')
        self.info_label.pack()

        # --- INIZIALIZZAZIONE COMPONENTI ---
        self.draw_hangman_base()  # Disegna la struttura base
        self.create_letter_buttons()  # Crea la tastiera visiva
        self.update_word_display()  # Mostra gli underscore iniziali
        self.update_info()  # Aggiorna le info tentativi/lettere

    def draw_hangman_base(self):
        """Disegna la struttura fissa della forca"""
        # Base orizzontale
        self.canvas.create_line(50, 280, 150, 280, width=3)
        # Palo verticale
        self.canvas.create_line(100, 280, 100, 50, width=3)
        # Traversa superiore
        self.canvas.create_line(100, 50, 200, 50, width=3)
        # Corda (punto di attacco per il corpo)
        self.canvas.create_line(200, 50, 200, 80, width=3)

    def draw_hangman_part(self, part_number):
        """Aggiunge progressivamente le parti del corpo in base agli errori"""
        parts = [
            lambda: self.canvas.create_oval(180, 80, 220, 120, width=3),  # Testa
            lambda: self.canvas.create_line(200, 120, 200, 180, width=3),  # Corpo
            lambda: self.canvas.create_line(200, 130, 170, 150, width=3),  # Braccio sinistro
            lambda: self.canvas.create_line(200, 130, 230, 150, width=3),  # Braccio destro
            lambda: self.canvas.create_line(200, 180, 170, 220, width=3),  # Gamba sinistra
            lambda: self.canvas.create_line(200, 180, 230, 220, width=3)  # Gamba destra
        ]
        # Disegna solo se l'indice è valido
        if part_number < len(parts):
            parts[part_number]()

    def create_letter_buttons(self):
        """Crea la griglia di pulsanti per le lettere"""
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, letter in enumerate(letters):
            # Crea pulsante con lettera e azione associata
            btn = tk.Button(
                self.buttons_frame,
                text=letter,
                width=3,
                height=2,
                command=lambda l=letter: self.guess_letter(l),  # Binding dinamico
                bg='lightblue',
                activebackground='deepskyblue',
                font=('Arial', 10)
            )
            # Disposizione in griglia 4x7 (26 lettere)
            btn.grid(row=i // 7, column=i % 7, padx=2, pady=2)

    def guess_letter(self, letter):
        """Gestisce la logica quando viene selezionata una lettera"""
        if letter not in self.guessed_letters:
            self.guessed_letters.append(letter)

            if letter not in self.secret_word:
                # Lettera errata: decrementa tentativi e disegna parte corpo
                self.remaining_attempts -= 1
                self.draw_hangman_part(self.max_attempts - self.remaining_attempts)

            # Disabilita il pulsante e cambia colore
            for child in self.buttons_frame.winfo_children():
                if child['text'] == letter:
                    bg_color = 'lightgreen' if letter in self.secret_word else 'lightgray'
                    child.config(state=tk.DISABLED, bg=bg_color)

            # Aggiorna interfaccia
            self.update_word_display()
            self.update_info()
            self.check_game_over()

    def update_word_display(self):
        """Aggiorna la visualizzazione della parola con lettere indovinate"""
        displayed_word = [char if char in self.guessed_letters else '_' for char in self.secret_word]
        self.word_display.config(text=' '.join(displayed_word))

    def update_info(self):
        """Mostra tentativi rimasti e lettere già utilizzate"""
        info_text = f"Tentativi rimasti: {self.remaining_attempts} | Lettere usate: {', '.join(self.guessed_letters)}"
        self.info_label.config(text=info_text)

    def check_game_over(self):
        """Verifica condizioni di vittoria/sconfitta"""
        # Vittoria: tutte le lettere indovinate
        if all(char in self.guessed_letters for char in self.secret_word):
            messagebox.showinfo("Vittoria!", f"Complimenti! Hai indovinato: {self.secret_word}")
            self.master.destroy()

        # Sconfitta: tentativi esauriti
        elif self.remaining_attempts <= 0:
            messagebox.showinfo("Game Over", f"Hai perso! La parola era: {self.secret_word}")
            self.master.destroy()


# Avvio dell'applicazione
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x650")
    root.resizable(False, False)  # Blocca ridimensionamento finestra
    game = HangmanGUI(root)
    root.mainloop()