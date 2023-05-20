import tkinter as tk
import sqlite3
from tkinter import ttk

# Connexion à la base de données
conn = sqlite3.connect("maintenance.db")
c = conn.cursor()

# Création de la table pour les pannes
c.execute('''CREATE TABLE IF NOT EXISTS pannes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             description TEXT,
             date TEXT)''')

# Création de la table pour les maintenances en cours
c.execute('''CREATE TABLE IF NOT EXISTS maintenances
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             panne_id INTEGER,
             description TEXT,
             etat TEXT,
             FOREIGN KEY (panne_id) REFERENCES pannes(id))''')

# Fonction pour ajouter une panne à la base de données
def ajouter_panne():
    description = panne_entry.get()
    c.execute("INSERT INTO pannes (description, date) VALUES (?, date('now'))", (description,))
    conn.commit()
    panne_entry.delete(0, tk.END)
    rafraichir_liste_pannes()

# Fonction pour supprimer une panne de la base de données
def supprimer_panne():
    selected_item = liste_pannes.selection()
    if selected_item:
        panne_id = liste_pannes.item(selected_item)['values'][0]
        c.execute("DELETE FROM pannes WHERE id=?", (panne_id,))
        conn.commit()
        rafraichir_liste_pannes()

# Fonction pour ajouter une maintenance en cours à la base de données
def ajouter_maintenance():
    description = maintenance_entry.get()
    selected_item = liste_pannes.focus()  # Get the ID of the selected item
    if selected_item:
        panne_id = liste_pannes.item(selected_item)['values'][0]
        c.execute("INSERT INTO maintenances (panne_id, description, etat) VALUES (?, ?, 'En cours')", (panne_id, description))
        conn.commit()
        maintenance_entry.delete(0, tk.END)
        rafraichir_liste_maintenances()

# Fonction pour supprimer une maintenance de la base de données
def supprimer_maintenance():
    selected_item = liste_maintenances.selection()
    if selected_item:
        maintenance_id = liste_maintenances.item(selected_item)['values'][0]
        c.execute("DELETE FROM maintenances WHERE id=?", (maintenance_id,))
        conn.commit()
        rafraichir_liste_maintenances()

# Fonction pour terminer une maintenance
def terminer_maintenance():
    selected_item = liste_maintenances.selection()
    if selected_item:
        maintenance_id = liste_maintenances.item(selected_item)['values'][0]
        c.execute("UPDATE maintenances SET etat='Terminée' WHERE id=?", (maintenance_id,))
        conn.commit()
        rafraichir_liste_maintenances()

# Fonction pour mettre à jour la liste des pannes
def rafraichir_liste_pannes():
    liste_pannes.delete(*liste_pannes.get_children())
    c.execute("SELECT id, description FROM pannes")
    pannes = c.fetchall()
    for panne in pannes:
        liste_pannes.insert('', tk.END, values=panne)

# Fonction pour mettre à jour la liste des maintenances
def rafraichir_liste_maintenances():
    liste_maintenances.delete(*liste_maintenances.get_children())
    c.execute("SELECT maintenances.id, pannes.description, maintenances.description, maintenances.etat FROM maintenances INNER JOIN pannes ON maintenances.panne_id = pannes.id")
    maintenances = c.fetchall()
    for maintenance in maintenances:
        liste_maintenances.insert('', tk.END, values=maintenance)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Logiciel de Maintenance Industrielle")

# Style
style = ttk.Style()
style.theme_use('clam')

# Cadre pour les pannes
cadre_pannes = ttk.Frame(fenetre, padding=10)
cadre_pannes.pack(side=tk.LEFT, padx=10)

pannes_label = ttk.Label(cadre_pannes, text="Pannes", font=("Arial", 14))
pannes_label.pack(pady=10)

# Liste des pannes existantes
liste_pannes = ttk.Treeview(cadre_pannes, columns=("ID", "Description"), show="headings")
liste_pannes.heading("ID", text="ID")
liste_pannes.heading("Description", text="Description")
liste_pannes.pack()

# Défilement vertical pour la liste des pannes
scrollbar_pannes = ttk.Scrollbar(cadre_pannes, orient=tk.VERTICAL, command=liste_pannes.yview)
scrollbar_pannes.pack(side=tk.RIGHT, fill=tk.Y)
liste_pannes.configure(yscroll=scrollbar_pannes.set)

# Boutons pour les pannes
boutons_pannes_frame = ttk.Frame(cadre_pannes)
boutons_pannes_frame.pack(pady=10)

bouton_ajouter_panne = ttk.Button(boutons_pannes_frame, text="Ajouter Panne", command=ajouter_panne)
bouton_ajouter_panne.pack(side=tk.LEFT, padx=5)

bouton_supprimer_panne = ttk.Button(boutons_pannes_frame, text="Supprimer Panne", command=supprimer_panne)
bouton_supprimer_panne.pack(side=tk.LEFT, padx=5)

# Cadre pour les maintenances
cadre_maintenances = ttk.Frame(fenetre, padding=10)
cadre_maintenances.pack(side=tk.RIGHT, padx=10)

maintenances_label = ttk.Label(cadre_maintenances, text="Maintenances en cours", font=("Arial", 14))
maintenances_label.pack(pady=10)


# Liste des maintenances en cours
liste_maintenances = ttk.Treeview(cadre_maintenances, columns=("ID", "Panne", "Description", "État"), show="headings")
liste_maintenances.heading("ID", text="ID")
liste_maintenances.heading("Panne", text="Panne")
liste_maintenances.heading("Description", text="Description")
liste_maintenances.heading("État", text="État")
liste_maintenances.pack()

# Défilement vertical pour la liste des maintenances
scrollbar_maintenances = ttk.Scrollbar(cadre_maintenances, orient=tk.VERTICAL, command=liste_maintenances.yview)
scrollbar_maintenances.pack(side=tk.RIGHT, fill=tk.Y)
liste_maintenances.configure(yscroll=scrollbar_maintenances.set)

# Boutons pour les maintenances
boutons_maintenances_frame = ttk.Frame(cadre_maintenances)
boutons_maintenances_frame.pack(pady=10)

bouton_ajouter_maintenance = ttk.Button(boutons_maintenances_frame, text="Ajouter Maintenance", command=ajouter_maintenance)
bouton_ajouter_maintenance.pack(side=tk.LEFT, padx=5)

bouton_supprimer_maintenance = ttk.Button(boutons_maintenances_frame, text="Supprimer Maintenance", command=supprimer_maintenance)
bouton_supprimer_maintenance.pack(side=tk.LEFT, padx=5)

bouton_terminer_maintenance = ttk.Button(boutons_maintenances_frame, text="Terminer Maintenance", command=terminer_maintenance)
bouton_terminer_maintenance.pack(side=tk.LEFT, padx=5)

# Entry widget for maintenance descriptions
maintenance_entry = ttk.Entry(cadre_maintenances)
maintenance_entry.pack()

# Entry widget for issue descriptions
panne_entry = ttk.Entry(cadre_pannes)
panne_entry.pack()
# Récupération des pannes et des maintenances depuis la base de données
rafraichir_liste_pannes()
rafraichir_liste_maintenances()

# Fermeture de la connexion à la base de données lors de la fermeture de la fenêtre
def fermer_fenetre():
    conn.close()
    fenetre.destroy()

fenetre.protocol("WM_DELETE_WINDOW", fermer_fenetre)
fenetre.mainloop()
