'''
Created on 10.09.2024

@author: Ayyoub
'''
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk

# Funktion, um Artikel (Produkte) aus der MySQL-Datenbank zu holen
def get_artikel():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            database='gruppenarbeit',
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produkte")
        artikel_liste = cursor.fetchall()
        conn.close()
        return artikel_liste
    except mysql.connector.Error as err:
        messagebox.showerror("Fehler", f"Fehler bei der Datenbankverbindung: {err}")
        return []

# Funktion, um Bestellungen zur MySQL-Datenbank hinzuzufügen
def add_bestellung(produkt_id, menge):
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            database='gruppenarbeit',
            port=3306
        )
        cursor = conn.cursor()
        # Hier fügen wir eine Bestellung für Max Mustermann hinzu (kunde_id = 1)
        cursor.execute("INSERT INTO bestellungen (produkt_id, menge, kunde_id) VALUES (%s, %s, 1)", (produkt_id, menge))
        conn.commit()
        conn.close()
        messagebox.showinfo("Erfolg", "Der Artikel wurde zu den Bestellungen hinzugefügt.")
    except mysql.connector.Error as err:
        messagebox.showerror("Fehler", f"Fehler bei der Bestellung: {err}")

# Funktion zum Öffnen eines neuen Fensters, um die Artikel anzuzeigen und Bestellungen hinzuzufügen
def show_artikel():
    artikel_window = tk.Toplevel(window)
    artikel_window.title("Alle Artikel")
    artikel_window.geometry("600x400")
    
    tree = ttk.Treeview(artikel_window, columns=("ID", "Name", "Preis"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Preis", text="Preis (€)")
    tree.column("ID", width=50)
    tree.column("Name", width=250)
    tree.column("Preis", width=100)
    
    artikel_liste = get_artikel()

    if artikel_liste:
        for artikel in artikel_liste:
            tree.insert("", "end", values=(artikel[0], artikel[1], artikel[2]))
    else:
        messagebox.showinfo("Information", "Keine Artikel in der Datenbank.")
    
    tree.pack(fill="both", expand=True)

    # Funktion, die beim Klick auf einen Artikel ausgeführt wird
    def on_article_click(event):
        selected_item = tree.focus()  # Ausgewähltes Element holen
        artikel_id = tree.item(selected_item)['values'][0]  # Artikel-ID extrahieren
        artikel_name = tree.item(selected_item)['values'][1]  # Artikel-Name extrahieren

        # Eingabeaufforderung für die Menge
        menge_window = tk.Toplevel(artikel_window)
        menge_window.title("Menge eingeben")
        menge_window.geometry("300x150")
        
        menge_label = tk.Label(menge_window, text=f"Wähle die Menge für {artikel_name}:")
        menge_label.pack(pady=10)
        
        menge_entry = tk.Entry(menge_window)
        menge_entry.pack(pady=10)
        
        def submit_menge():
            menge = menge_entry.get()
            if menge.isdigit():
                add_bestellung(artikel_id, menge)
                menge_window.destroy()
            else:
                messagebox.showerror("Fehler", "Bitte eine gültige Menge eingeben.")
        
        submit_button = tk.Button(menge_window, text="Bestellen", command=submit_menge)
        submit_button.pack(pady=10)
    
    # Ereignisbindung für den Klick auf einen Artikel
    tree.bind("<Double-1>", on_article_click)

# Funktion, um Kundendaten (Max Mustermann) aus der MySQL-Datenbank zu holen
def get_kundendaten():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            database='gruppenarbeit',
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kunden WHERE name = 'Max Mustermann'")
        kundendaten = cursor.fetchone()  # Nur einen Datensatz abrufen
        conn.close()
        return kundendaten
    except mysql.connector.Error as err:
        messagebox.showerror("Fehler", f"Fehler bei der Datenbankverbindung: {err}")
        return None

# Funktion zum Öffnen des Konto-Fensters (zeigt Daten von Max Mustermann)
def show_konto():
    konto_window = tk.Toplevel(window)
    konto_window.title("Konto - Max Mustermann")
    konto_window.geometry("400x200")

    kundendaten = get_kundendaten()
    
    if kundendaten:
        name_label = tk.Label(konto_window, text=f"Name: {kundendaten[1]}", font=("Arial", 14))
        name_label.pack(pady=10)
        
        email_label = tk.Label(konto_window, text=f"E-Mail: {kundendaten[2]}", font=("Arial", 14))
        email_label.pack(pady=10)
        
        adresse_label = tk.Label(konto_window, text=f"Adresse: {kundendaten[3]}", font=("Arial", 14))
        adresse_label.pack(pady=10)
    else:
        messagebox.showinfo("Information", "Kunde Max Mustermann nicht gefunden.")

# Funktion, um Bestellungen von Max Mustermann anzuzeigen
def show_bestellungen():
    bestellungen_window = tk.Toplevel(window)
    bestellungen_window.title("Bestellungen - Max Mustermann")
    bestellungen_window.geometry("600x400")
    
    tree = ttk.Treeview(bestellungen_window, columns=("BestellID", "Produkt", "Menge"), show='headings')
    tree.heading("BestellID", text="Bestell-ID")
    tree.heading("Produkt", text="Produkt")
    tree.heading("Menge", text="Menge")
    tree.column("BestellID", width=80)
    tree.column("Produkt", width=200)
    tree.column("Menge", width=100)

    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            database='gruppenarbeit',
            port=3306
        )
        cursor = conn.cursor()
        # Bestellungen von Max Mustermann (kunde_id = 1) anzeigen
        cursor.execute("""
            SELECT bestellungen.id, produkte.name, bestellungen.menge
            FROM bestellungen
            JOIN produkte ON bestellungen.produkt_id = produkte.id
            WHERE bestellungen.kunde_id = 1
        """)
        bestellungen_liste = cursor.fetchall()
        conn.close()

        if bestellungen_liste:
            for bestellung in bestellungen_liste:
                tree.insert("", "end", values=(bestellung[0], bestellung[1], bestellung[2]))
        else:
            messagebox.showinfo("Information", "Keine Bestellungen für Max Mustermann gefunden.")
    except mysql.connector.Error as err:
        messagebox.showerror("Fehler", f"Fehler bei der Datenbankverbindung: {err}")
    
    tree.pack(fill="both", expand=True)

# Hauptfenster erstellen
window = tk.Tk()
window.title("Shop")
window.geometry("1280x720")
window.configure(bg="white")

# Bilder laden und auf die richtige Größe skalieren
image = Image.open("WK.png")
image = image.resize((50, 50))  
photo = ImageTk.PhotoImage(image)

image2 = Image.open("KNT.png")
image2 = image2.resize((50, 50))  
photo2 = ImageTk.PhotoImage(image2)

image3 = Image.open("AAT.png")
image3 = image3.resize((50, 50))  
photo3 = ImageTk.PhotoImage(image3)

# Grid-Konfiguration
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)

# Titel-Label
titel = tk.Label(window, text="Willkommen im Online-Shop", font=("Arial", 24))
titel.grid(row=0, column=0, pady=20)
titel.configure(bg="white")

# Button "Alle Artikel" - öffnet das Artikel-Fenster
button1 = tk.Button(window, image=photo3, compound="top", text="Alle Artikel", font=("Arial", 16), command=show_artikel)
button1.grid(row=1, column=0, padx=50, pady=10, sticky="nsew")
button1.configure(bg="white")

# Button "Bestellungen" - öffnet das Bestellungen-Fenster
button2 = tk.Button(window, text="Bestellungen", image=photo, compound="top", font=("Arial", 16), command=show_bestellungen)
button2.grid(row=2, column=0, padx=50, pady=10, sticky="nsew")
button2.configure(bg="white")

# Button "Konto" - öffnet das Konto-Fenster
button3 = tk.Button(window, image=photo2, compound="top", text="Konto", font=("Arial", 16), command=show_konto)
button3.grid(row=3, column=0, padx=50, pady=10, sticky="nsew")
button3.configure(bg="white")

# Hauptschleife starten
window.mainloop()
