# tkinter_ui.py
import tkinter as tk
import requests

# Fonction pour récupérer les abonnés via l'API Flask
def afficher_abonnes():
    response = requests.get("http://127.0.0.1:5000/abonnee/get_abonnes")
    if response.status_code == 200:
        abonnes = response
        breakpoint()
        # Effacer les anciennes données
        for widget in frame_abonnes.winfo_children():
            widget.destroy()
        # Afficher les abonnés dans l'interface
        for abonne in abonnes:
            label = tk.Label(frame_abonnes, text=f"{abonne['nom']} {abonne['prenom']}")
            label.pack()

# Interface Tkinter
root = tk.Tk()
root.title("Gestion des Abonnés")

frame_abonnes = tk.Frame(root)
frame_abonnes.pack()

button = tk.Button(root, text="Afficher les abonnés", command=afficher_abonnes)
button.pack()

root.mainloop()
