import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# Funzione per connettersi al database SQLite
def connect_db():
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS strumenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantita INTEGER NOT NULL,
            descrizione TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reattivi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            formula TEXT NOT NULL,
            quantita INTEGER NOT NULL,
            descrizione TEXT
        )
    ''')
    conn.commit()
    return conn


# Funzione per aggiungere un nuovo strumento
def aggiungi_strumento():
    nome = entry_nome_strumento.get()
    categoria = entry_categoria_strumento.get()
    quantita = entry_quantita_strumento.get()
    descrizione = entry_descrizione_strumento.get()

    if nome and categoria and quantita:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO strumenti (nome, categoria, quantita, descrizione)
            VALUES (?, ?, ?, ?)
        ''', (nome, categoria, quantita, descrizione))
        conn.commit()
        conn.close()
        messagebox.showinfo("Successo", "Strumento aggiunto con successo!")
        entry_nome_strumento.delete(0, tk.END)
        entry_categoria_strumento.delete(0, tk.END)
        entry_quantita_strumento.delete(0, tk.END)
        entry_descrizione_strumento.delete(0, tk.END)
        leggi_strumenti()
    else:
        messagebox.showerror("Errore", "Tutti i campi devono essere compilati!")


# Funzione per aggiungere un nuovo reattivo
def aggiungi_reattivo():
    nome = entry_nome_reattivo.get()
    formula = entry_formula_reattivo.get()
    quantita = entry_quantita_reattivo.get()
    descrizione = entry_descrizione_reattivo.get()

    if nome and formula and quantita:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reattivi (nome, formula, quantita, descrizione)
            VALUES (?, ?, ?, ?)
        ''', (nome, formula, quantita, descrizione))
        conn.commit()
        conn.close()
        messagebox.showinfo("Successo", "Reattivo aggiunto con successo!")
        entry_nome_reattivo.delete(0, tk.END)
        entry_formula_reattivo.delete(0, tk.END)
        entry_quantita_reattivo.delete(0, tk.END)
        entry_descrizione_reattivo.delete(0, tk.END)
        leggi_reattivi()
    else:
        messagebox.showerror("Errore", "Tutti i campi devono essere compilati!")


# Funzione per modificare uno strumento
def modifica_strumento():
    try:
        selected_item = tree_strumenti.selection()[0]
        item = tree_strumenti.item(selected_item)
        id_strumento = item['values'][0]

        nome = entry_nome_strumento.get()
        categoria = entry_categoria_strumento.get()
        quantita = entry_quantita_strumento.get()
        descrizione = entry_descrizione_strumento.get()

        if nome and categoria and quantita:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE strumenti 
                SET nome = ?, categoria = ?, quantita = ?, descrizione = ?
                WHERE id = ?
            ''', (nome, categoria, quantita, descrizione, id_strumento))
            conn.commit()
            conn.close()
            messagebox.showinfo("Successo", "Strumento modificato con successo!")
            leggi_strumenti()
        else:
            messagebox.showerror("Errore", "Tutti i campi devono essere compilati!")
    except IndexError:
        messagebox.showerror("Errore", "Seleziona uno strumento da modificare.")


# Funzione per modificare un reattivo
def modifica_reattivo():
    try:
        selected_item = tree_reattivi.selection()[0]
        item = tree_reattivi.item(selected_item)
        id_reattivo = item['values'][0]

        nome = entry_nome_reattivo.get()
        formula = entry_formula_reattivo.get()
        quantita = entry_quantita_reattivo.get()
        descrizione = entry_descrizione_reattivo.get()

        if nome and formula and quantita:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE reattivi 
                SET nome = ?, formula = ?, quantita = ?, descrizione = ?
                WHERE id = ?
            ''', (nome, formula, quantita, descrizione, id_reattivo))
            conn.commit()
            conn.close()
            messagebox.showinfo("Successo", "Reattivo modificato con successo!")
            leggi_reattivi()
        else:
            messagebox.showerror("Errore", "Tutti i campi devono essere compilati!")
    except IndexError:
        messagebox.showerror("Errore", "Seleziona un reattivo da modificare.")


# Funzione per eliminare uno strumento
def elimina_strumento():
    try:
        selected_item = tree_strumenti.selection()[0]
        item = tree_strumenti.item(selected_item)
        id_strumento = item['values'][0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM strumenti WHERE id = ?', (id_strumento,))
        conn.commit()
        conn.close()
        tree_strumenti.delete(selected_item)
        messagebox.showinfo("Successo", "Strumento eliminato con successo!")
    except IndexError:
        messagebox.showerror("Errore", "Seleziona uno strumento da eliminare.")


# Funzione per eliminare un reattivo
def elimina_reattivo():
    try:
        selected_item = tree_reattivi.selection()[0]
        item = tree_reattivi.item(selected_item)
        id_reattivo = item['values'][0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reattivi WHERE id = ?', (id_reattivo,))
        conn.commit()
        conn.close()
        tree_reattivi.delete(selected_item)
        messagebox.showinfo("Successo", "Reattivo eliminato con successo!")
    except IndexError:
        messagebox.showerror("Errore", "Seleziona un reattivo da eliminare.")


# Funzione per leggere e visualizzare gli strumenti dal database
def leggi_strumenti():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM strumenti')
    rows = cursor.fetchall()
    conn.close()

    for row in tree_strumenti.get_children():
        tree_strumenti.delete(row)
    for row in rows:
        tree_strumenti.insert('', 'end', values=row)


# Funzione per leggere e visualizzare i reattivi dal database
def leggi_reattivi():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reattivi')
    rows = cursor.fetchall()
    conn.close()

    for row in tree_reattivi.get_children():
        tree_reattivi.delete(row)
    for row in rows:
        tree_reattivi.insert('', 'end', values=row)


# Creazione della finestra principale
root = tk.Tk()
root.title("Gestione Strumenti e Reattivi di Laboratorio by Antonio Cufari ver. 1.1")

# Creazione dei widget per gli strumenti
frame_strumenti = tk.LabelFrame(root, text="Strumenti")
frame_strumenti.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(frame_strumenti, text="Nome:").grid(row=0, column=0)
entry_nome_strumento = tk.Entry(frame_strumenti)
entry_nome_strumento.grid(row=0, column=1)

tk.Label(frame_strumenti, text="Categoria:").grid(row=1, column=0)
entry_categoria_strumento = tk.Entry(frame_strumenti)
entry_categoria_strumento.grid(row=1, column=1)

tk.Label(frame_strumenti, text="Quantità:").grid(row=2, column=0)
entry_quantita_strumento = tk.Entry(frame_strumenti)
entry_quantita_strumento.grid(row=2, column=1)

tk.Label(frame_strumenti, text="Descrizione:").grid(row=3, column=0)
entry_descrizione_strumento = tk.Entry(frame_strumenti)
entry_descrizione_strumento.grid(row=3, column=1)

tk.Button(frame_strumenti, text="Aggiungi Strumento", command=aggiungi_strumento).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(frame_strumenti, text="Modifica Strumento", command=modifica_strumento).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(frame_strumenti, text="Elimina Strumento", command=elimina_strumento).grid(row=3, column=0, columnspan=2, pady=5)

columns = ("id", "nome", "categoria", "quantita", "descrizione")
tree_strumenti = ttk.Treeview(frame_strumenti, columns=columns, show='headings')
for col in columns:
    tree_strumenti.heading(col, text=col)
tree_strumenti.grid(row=7, column=0, columnspan=2, pady=5)

# Creazione dei widget per i reattivi
frame_reattivi = tk.LabelFrame(root, text="Reattivi")
frame_reattivi.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(frame_reattivi, text="Nome:").grid(row=0, column=0)
entry_nome_reattivo = tk.Entry(frame_reattivi)
entry_nome_reattivo.grid(row=0, column=1)

tk.Label(frame_reattivi, text="Formula:").grid(row=1, column=0)
entry_formula_reattivo = tk.Entry(frame_reattivi)
entry_formula_reattivo.grid(row=1, column=1)

tk.Label(frame_reattivi, text="Quantità:").grid(row=2, column=0)
entry_quantita_reattivo = tk.Entry(frame_reattivi)
entry_quantita_reattivo.grid(row=2, column=1)

tk.Label(frame_reattivi, text="Descrizione:").grid(row=3, column=0)
entry_descrizione_reattivo = tk.Entry(frame_reattivi)
entry_descrizione_reattivo.grid(row=3, column=1)

tk.Button(frame_reattivi, text="Aggiungi Reattivo", command=aggiungi_reattivo).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(frame_reattivi, text="Modifica Reattivo", command=modifica_reattivo).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(frame_reattivi, text="Elimina Reattivo", command=elimina_reattivo).grid(row=3, column=0, columnspan=2, pady=5)

columns = ("id", "nome", "formula", "quantita", "descrizione")
tree_reattivi = ttk.Treeview(frame_reattivi, columns=columns, show='headings')
for col in columns:
    tree_reattivi.heading(col, text=col)
tree_reattivi.grid(row=7, column=0, columnspan=2, pady=5)

# Funzione per inizializzare la visualizzazione dei dati
def inizializza_dati():
    leggi_strumenti()
    leggi_reattivi()

# Popolamento iniziale dei dati nelle tabelle
inizializza_dati()

# Avvio del loop principale dell'interfaccia
root.mainloop()
