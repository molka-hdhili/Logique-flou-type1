import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Canvas
from PIL import Image, ImageTk

# Univers de discours
tc_range = np.arange(20, 81, 1)  # Technologie
nc_range = np.arange(9, 71, 1)   # Normes
pi_range = np.arange(5, 51, 1)   # Portée
rc_range = np.arange(-80, 71, 1)  # Risque

# Définir les fonctions d'appartenance floues de type 2
def create_type2_membership_functions():
    def trimf(x, a, b, c):
        return np.maximum(0, np.minimum((x-a)/(b-a), (c-x)/(c-b)))

    # Type 2 : Chaque fonction a une incertitude définie par deux bandes : inférieur et supérieur
    def interval_type2(mf_lower, mf_upper):
        return {"lower": mf_lower, "upper": mf_upper}

    # Membership functions avec incertitude (bandes supérieure et inférieure)
    rc_mf = {
        "Très faible": interval_type2(
            trimf(rc_range, -80, -60, -40),  # Bande inférieure
            trimf(rc_range, -70, -50, -30)  # Bande supérieure
        ),
        "Faible": interval_type2(
            trimf(rc_range, -40, -10, 20),
            trimf(rc_range, -30, 0, 30)
        ),
        "Moyen": interval_type2(
            trimf(rc_range, 10, 30, 50),
            trimf(rc_range, 20, 40, 60)
        ),
        "Élevé": interval_type2(
            trimf(rc_range, 40, 60, 80),
            trimf(rc_range, 50, 70, 90)
        )
    }

    return rc_mf

# Initialiser les fonctions d'appartenance de type 2
membership_functions = create_type2_membership_functions()

# Calcul des degrés d'appartenance pour les ensembles de type 2
def calculate_type2_membership(value, interval):
    lower_degree = np.interp(value, rc_range, interval["lower"])
    upper_degree = np.interp(value, rc_range, interval["upper"])
    return lower_degree, upper_degree

# Interface utilisateur avec calcul de type 2
def interactive_fuzzy_system_type2():
    root = Tk()
    root.title("Système Flou Type 2")
    root.geometry("800x600")

    # Charger l'image de fond
    bg_image_path = r"C:\Users\user\Desktop\capture\Capture.png"
    try:
        bg_image = ImageTk.PhotoImage(Image.open(bg_image_path).resize((800, 600)))
        canvas = Canvas(root, width=800, height=600)
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.pack(fill="both", expand=True)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        bg_image = None

    # Ajout des widgets
    Label(canvas, text="Technologie (20-80):", bg="white").place(x=50, y=50)
    tc_entry = Entry(canvas)
    tc_entry.place(x=200, y=50)

    Label(canvas, text="Normes (9-70):", bg="white").place(x=50, y=100)
    nc_entry = Entry(canvas)
    nc_entry.place(x=200, y=100)

    Label(canvas, text="Portée (5-50):", bg="white").place(x=50, y=150)
    pi_entry = Entry(canvas)
    pi_entry.place(x=200, y=150)

    result_label = Label(canvas, text="Risque estimé:", bg="white")
    result_label.place(x=50, y=250)

    risk_label = Label(canvas, text="Niveau de risque:", bg="white")
    risk_label.place(x=50, y=300)

    def plot_membership_type2(risk_value):
        plt.figure(figsize=(12, 6))

        for label, mf in membership_functions.items():
            plt.fill_between(rc_range, mf["lower"], mf["upper"], alpha=0.3, label=f"{label} (Incertitude)")
            plt.plot(rc_range, mf["lower"], '--', label=f"{label} - Bande inférieure")
            plt.plot(rc_range, mf["upper"], '-', label=f"{label} - Bande supérieure")

        plt.axvline(risk_value, color="red", linestyle="--", label=f"Risque: {risk_value:.2f}")
        plt.title("Fonctions d'appartenance - Type 2")
        plt.xlabel("Valeur de risque")
        plt.ylabel("Degré d'appartenance")
        plt.legend()
        plt.grid()
        plt.show()

    def on_submit():
        try:
            # Lire les entrées
            tc_value = float(tc_entry.get())
            nc_value = float(nc_entry.get())
            pi_value = float(pi_entry.get())

            # Vérification des limites
            if not (20 <= tc_value <= 80):
                result_label.config(text="Erreur: Technologie hors limites")
                return
            if not (9 <= nc_value <= 70):
                result_label.config(text="Erreur: Normes hors limites")
                return
            if not (5 <= pi_value <= 50):
                result_label.config(text="Erreur: Portée hors limites")
                return

            # Calcul du risque (exemple simplifié)
            risk_value = (tc_value + nc_value + pi_value) / 3

            # Calcul des degrés d'appartenance flous de type 2
            memberships = {
                label: calculate_type2_membership(risk_value, mf)
                for label, mf in membership_functions.items()
            }

            # Identifier le niveau de risque dominant (en fonction des bandes supérieures)
            dominant_label = max(memberships, key=lambda label: memberships[label][1])
            lower, upper = memberships[dominant_label]

            # Afficher les résultats
            result_label.config(text=f"Risque estimé: {risk_value:.2f}")
            risk_label.config(text=f"Niveau de risque: {dominant_label}\n"
                                   f"Incertitude: [{lower:.2f}, {upper:.2f}]")

            # Afficher les courbes de type 2
            plot_membership_type2(risk_value)

        except ValueError:
            result_label.config(text="Erreur: Entrée invalide")

    Button(canvas, text="Calculer", command=on_submit, bg="lightblue").place(x=50, y=200)

    root.mainloop()

# Lancer l'interface utilisateur
interactive_fuzzy_system_type2()
