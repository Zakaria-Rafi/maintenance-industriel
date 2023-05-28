import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import os


class DetailsPanneWindow(tk.Toplevel):
    def __init__(self, parent, panne_id, conn):
        super().__init__(parent)
        self.title("Détails de la Panne")
        self.parent = parent
        self.panne_id = panne_id
        self.conn = conn

        self.description_entry = None
        self.photo_label = None

        self.configurer_widgets()
        self.afficher_photos()

    def configurer_widgets(self):
        description_label = ttk.Label(self, text="Description:")
        description_label.pack(padx=10, pady=10)

        self.description_entry = ttk.Entry(self)
        self.description_entry.pack(padx=10, pady=5)

        enregistrer_button = ttk.Button(self, text="Enregistrer", command=self.enregistrer_description)
        enregistrer_button.pack(padx=10, pady=5)

        ajouter_photo_button = ttk.Button(self, text="Ajouter une photo", command=self.ajouter_photo)
        ajouter_photo_button.pack(padx=10, pady=5)

    def ajouter_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            new_dir = "photos"
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            new_path = os.path.join(new_dir, f"{self.panne_id}.png")
            Image.open(file_path).save(new_path)
            c = self.conn.cursor()
            c.execute("INSERT INTO photos (panne_id, path) VALUES (?, ?)", (self.panne_id, new_path))
            self.conn.commit()
            messagebox.showinfo("Ajout de photo", "La photo a été ajoutée avec succès.")

    def enregistrer_description(self):
        nouvelle_description = self.description_entry.get()
        c = self.conn.cursor()
        c.execute("UPDATE pannes SET description=? WHERE id=?", (nouvelle_description, self.panne_id))
        self.conn.commit()
        messagebox.showinfo("Sauvegarde réussie", "La description a été mise à jour avec succès.")
