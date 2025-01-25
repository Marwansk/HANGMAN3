# Importa il modulo per la generazione casuale
import random

# Lista di parole per il gioco
words = ['mercedes', 'kotlin', 'audi', 'java', 'swift']

# Selezione casuale della parola da indovinare
chosen_word = random.choice(words)

# Numero massimo di tentativi consentiti
attempts = 6

# Lista che mostra i caratteri indovinati (underscore = lettera nascosta)
display = ['_' for _ in chosen_word]

# Lista per tenere traccia delle lettere già provate
guessed_letters = []

# Messaggio di benvenuto
print('Welcome to Hangman!')

# Loop principale del gioco: continua finché ci sono tentativi e lettere da indovinare
while attempts > 0 and '_' in display:
    # Mostra lo stato attuale della parola
    print('\n' + ' '.join(display))
    # Mostra tentativi rimasti
    print(f"Tentativi rimasti: {attempts}")
    # Mostra lettere già provate
    print(f"Lettere provate: {', '.join(guessed_letters)}")

    # Input utente con conversione in minuscolo
    guess = input('Indovina una lettera: ').lower()

    # Validazione input:
    # 1. Deve essere un singolo carattere alfabetico
    if len(guess) != 1 or not guess.isalpha():
        print("Inserisci una singola lettera valida!")
        continue  # Torna all'inizio del loop

    # 2. Controlla se la lettera è già stata provata
    if guess in guessed_letters:
        print("Hai già provato questa lettera!")
        continue

    # Aggiunge la lettera alle tentate
    guessed_letters.append(guess)

    # Controlla se la lettera è nella parola
    if guess in chosen_word:
        # Rivelazione della lettera(indice per indice)
        for index, letter in enumerate(chosen_word):
            if letter == guess:
                display[index] = guess  # Sostituisce l'underscore
    else:
        # Lettera non trovata: decrementa i tentativi
        print("La lettera non è nella parola!")
        attempts -= 1

# Fuori dal loop principale - Controllo risultato finale
if '_' not in display:
    # Vittoria: tutte le lettere indovinate
    print('\nHai indovinato! La parola era:', chosen_word)
    print(' '.join(display))
    print('Hai vinto!')
else:
    # Sconfitta: esauriti i tentativi
    print('\nHai finito i tentativi! La parola era:', chosen_word)
    print('Hai perso!')