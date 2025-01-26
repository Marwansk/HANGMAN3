# Importa le librerie necessarie
import tkinter as tk
from tkinter import messagebox  # Per i popup di vittoria/sconfitta
import random  # Per la selezione casuale della parola


class HangmanGUI:
    def __init__(self, master):
        # Inizializzazione della finestra principale
        self.master = master
        self.master.title("Hangman Game - Marchi Auto")  # Titolo applicazione

        # Lista personalizzata di marchi automobilistici (30 elementi)
        # Mix tra marchi italiani e internazionali
        self.words = [
            "ferrari", "lamborghini", "alfaromeo", "fiat", "maserati",
            "lancia", "iveco", "pagani", "ducati", "aprilia",
            "toyota", "ford", "honda", "bmw", "mercedes",
            "volkswagen", "hyundai", "tesla", "nissan", "chevrolet",
            "peugeot", "renault", "volvo", "audi", "subaru",
            "mazda", "porsche", "bentley", "rollsroyce", "cadillac"
        ]

        # Selezione casuale e conversione in maiuscolo per uniformità
        self.secret_word = random.choice(self.words).upper()

        # Configurazione tentativi
        self.max_attempts = 600  # Corrisponde alle 600 parti del corpo
        self.remaining_attempts = self.max_attempts  # Contatore decrementabile

        # Lista per tracciare le lettere già provate
        self.guessed_letters = []  # Utilizza una lista per mantenere l'ordine

        # --- Inizializzazione componenti grafici ---
        # Canvas per disegnare l'impiccato (400x300 pixel, sfondo bianco)
        self.canvas = tk.Canvas(master, width=400, height=300, bg='white')
        self.canvas.pack(pady=20)  # Padding verticale 20px

        # Label per visualizzare la parola nascosta (font grande, colore blu scuro)
        self.word_display = tk.Label(master, font=('Helvetica', 24), fg='navy')
        self.word_display.pack(pady=10)  # Padding verticale 10px

        # Frame contenitore per i pulsanti delle lettere
        self.buttons_frame = tk.Frame(master)  # Contenitore flessibile
        self.buttons_frame.pack(pady=20)  # Padding verticale 20px

        # Label per informazioni di gioco (font piccolo, colore rosso scuro)
        self.info_label = tk.Label(master, font=('Helvetica', 12), fg='darkred')
        self.info_label.pack()  # Posizionamento automatico

        # --- Setup iniziale del gioco ---
        self.draw_hangman_base()  # Disegna struttura fissa della forca
        self.create_letter_buttons()  # Genera la tastiera alfabetica
        self.update_word_display()  # Mostra gli underscore iniziali
        self.update_info()  # Aggiorna contatore tentativi

    def draw_hangman_base(self):
        """
        Disegna la struttura base della forca usando coordinate fisse.
        Le coordinate (x,y) sono state calcolate per un disegno bilanciato.
        """
        # Base orizzontale (da 50,280 a 150,280)
        self.canvas.create_line(50, 280, 150, 280, width=3)
        # Palo verticale (da 100,280 a 100,50)
        self.canvas.create_line(100, 280, 100, 50, width=3)
        # Traversa superiore (da 100,50 a 200,50)
        self.canvas.create_line(100, 50, 200, 50, width=3)
        # Corda (linea verticale corta da 200,50 a 200,80)
        self.canvas.create_line(200, 50, 200, 80, width=3)

    def draw_hangman_part(self, part_number):
        """
        Aggiunge progressivamente le parti del corpo usando un sistema a indice.
        Ogni indice corrisponde a una parte specifica:
        0: testa, 1: corpo, 2: braccio sx, 3: braccio dx, 4: gamba sx, 5: gamba dx
        """
        parts = [
            # Testa (cerchio da 180,80 a 220,120)
            lambda: self.canvas.create_oval(180, 80, 220, 120, width=3),
            # Corpo (linea verticale da 200,120 a 200,180)
            lambda: self.canvas.create_line(200, 120, 200, 180, width=3),
            # Braccio sinistro (linea diagonale da 200,130 a 170,150)
            lambda: self.canvas.create_line(200, 130, 170, 150, width=3),
            # Braccio destro (linea diagonale da 200,130 a 230,150)
            lambda: self.canvas.create_line(200, 130, 230, 150, width=3),
            # Gamba sinistra (linea diagonale da 200,180 a 170,220)
            lambda: self.canvas.create_line(200, 180, 170, 220, width=3),
            # Gamba destra (linea diagonale da 200,180 a 230,220)
            lambda: self.canvas.create_line(200, 180, 230, 220, width=3)
        ]
        # Esegue la funzione corrispondente all'indice se valida
        if part_number < len(parts):
            parts[part_number]()

    def create_letter_buttons(self):
        """
        Crea una griglia di pulsanti per tutte le lettere dell'alfabeto.
        Disposizione: 4 righe (26 lettere / 7 colonne = circa 4 righe)
        """
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Stringa di riferimento
        for i, letter in enumerate(letters):  # Loop su ogni lettera
            # Crea pulsante con caratteristiche visive
            btn = tk.Button(
                self.buttons_frame,
                text=letter,
                width=3,  # Larghezza fissa
                height=2,  # Altezza fissa
                command=lambda l=letter: self.guess_letter(l),  # Binding dinamico
                bg='lightblue',  # Colore di sfondo
                activebackground='deepskyblue',  # Colore al click
                font=('Arial', 10)  # Tipo e dimensione font
            )
            # Posiziona in griglia: row=i//7 (divisione intera), column=i%7 (resto)
            btn.grid(row=i // 7, column=i % 7, padx=2, pady=2)  # Spaziatura tra pulsanti

    def guess_letter(self, letter):
        """
        Gestisce la logica principale del gioco quando viene selezionata una lettera.
        - letter: carattere maiuscolo (A-Z) selezionato dall'utente
        """
        if letter not in self.guessed_letters:  # Evita ripetizioni
            self.guessed_letters.append(letter)  # Registra tentativo

            if letter not in self.secret_word:  # Lettera non presente
                self.remaining_attempts -= 1  # Decrementa tentativi
                # Disegna parte del corpo: calcola l'indice in base agli errori
                self.draw_hangman_part(self.max_attempts - self.remaining_attempts)

            # Disabilita il pulsante e cambia colore
            for child in self.buttons_frame.winfo_children():  # Loop su tutti i pulsanti
                if child['text'] == letter:  # Trova il pulsante cliccato
                    # Cambia colore: verde se corretta, grigio se errata
                    bg_color = 'lightgreen' if letter in self.secret_word else 'lightgray'
                    child.config(
                        state=tk.DISABLED,  # Disabilita ulteriori click
                        bg=bg_color  # Imposta nuovo colore di sfondo
                    )

            # Aggiorna interfaccia
            self.update_word_display()  # Mostra lettere indovinate
            self.update_info()  # Aggiorna contatore
            self.check_game_over()  # Verifica condizioni di fine gioco

    def update_word_display(self):
        """Costruisce e aggiorna la visualizzazione della parola nascosta"""
        # List comprehension: mostra lettera se indovinata, altrimenti '_'
        displayed_word = [char if char in self.guessed_letters else '_' for char in self.secret_word]
        # Unisce le lettere con spazi e aggiorna la Label
        self.word_display.config(text=' '.join(displayed_word))

    def update_info(self):
        """Aggiorna il pannello informativo con lo stato attuale del gioco"""
        # Formatta stringa con tentativi rimasti e lettere usate
        info_text = (
            f"Tentativi rimasti: {self.remaining_attempts} | "
            f"Lettere usate: {', '.join(self.guessed_letters)}"
        )
        self.info_label.config(text=info_text)  # Aggiorna testo Label

    def check_game_over(self):
        """Verifica le condizioni di vittoria o sconfitta"""
        # Vittoria: tutte le lettere sono state indovinate
        if all(char in self.guessed_letters for char in self.secret_word):
            messagebox.showinfo(
                "Vittoria!",
                f"Complimenti! Hai indovinato: {self.secret_word}"
            )
            self.master.destroy()  # Chiude l'applicazione

        # Sconfitta: esauriti i tentativi disponibili
        elif self.remaining_attempts <= 0:
            messagebox.showinfo(
                "Game Over",
                f"Hai perso! La parola era: {self.secret_word}"
            )
            self.master.destroy()  # Chiude l'applicazione


# Blocco main: punto di ingresso dell'applicazione
if __name__ == "__main__":
    root = tk.Tk()  # Crea istanza principale di Tk
    root.geometry("650x650")  # Dimensioni finestra (larghezza x altezza)
    root.resizable(False, False)  # Blocca ridimensionamento finestra
    game = HangmanGUI(root)  # Istanzia la classe del gioco
    root.mainloop()  # Avvia il loop principale degli eventi