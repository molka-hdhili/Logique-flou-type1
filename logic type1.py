import numpy as np
import skfuzzy as fuzz
from skfuzzy.control import Antecedent, Consequent, Rule, ControlSystem, ControlSystemSimulation
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Scrollbar, Text
from PIL import Image, ImageTk

# Définir les univers de discours
tc_range = np.arange(20, 81, 1)   # technologies (20 à 80)
nc_range = np.arange(9, 71, 1)    # normes (9 à 70)
pi_range = np.arange(5, 51, 1)    # porté de l’information  (5 à 50)
rc_range = np.arange(-80, 71, 1)  # Risque (-80 à 70)

# Définir les fonctions d'appartenance
tc = Antecedent(tc_range, 'Technology')
tc['AV'] = fuzz.trimf(tc_range, [20, 35, 45])  # avancé
tc['AC'] = fuzz.trimf(tc_range, [35, 45, 60])  # acceptable
tc['IN'] = fuzz.trimf(tc_range, [45, 60, 80])  # insuffisante

nc = Antecedent(nc_range, 'Norms')
nc['DN'] = fuzz.trapmf(nc_range, [9, 24, 40, 55])  # DN (Dans les Normes)
nc['HN'] = fuzz.trapmf(nc_range, [40, 55, 60, 70])  # HN (Hors des Normes)

pi = Antecedent(pi_range, 'Scope')
pi['TG'] = fuzz.trapmf(pi_range, [5, 10, 15, 20])  # tres grande
pi['GR'] = fuzz.trapmf(pi_range, [15, 20, 25, 30])  # grande
pi['MO'] = fuzz.trapmf(pi_range, [25, 30, 35, 40])  # moyenne
pi['FA'] = fuzz.trapmf(pi_range, [35, 40, 45, 50])  # faible

rc = Consequent(rc_range, 'Risk')
rc['TF'] = fuzz.trimf(rc_range, [-80, -50, -10])  # très forte
rc['FO'] = fuzz.trimf(rc_range, [-50, -10, 10])   # forte
rc['MO'] = fuzz.trimf(rc_range, [-10, 10, 40])    # moyenne
rc['FA'] = fuzz.trimf(rc_range, [10, 40, 70])     # faible

# Définir les règles basées sur les conditions fournies
rules = [
    Rule(nc['DN'] & tc['AV'] & pi['TG'], rc['FA']),
    Rule(nc['DN'] & tc['AV'] & pi['GR'], rc['FA']),
    Rule(nc['DN'] & tc['AV'] & pi['MO'], rc['MO']),
    Rule(nc['DN'] & tc['AV'] & pi['FA'], rc['FO']),
    Rule(nc['DN'] & tc['AC'] & pi['TG'], rc['FA']),
    Rule(nc['DN'] & tc['AC'] & pi['GR'], rc['MO']),
    Rule(nc['DN'] & tc['AC'] & pi['MO'], rc['MO']),
    Rule(nc['DN'] & tc['AC'] & pi['FA'], rc['FO']),
    Rule(nc['DN'] & tc['IN'] & pi['TG'], rc['FA']),
    Rule(nc['DN'] & tc['IN'] & pi['GR'], rc['MO']),
    Rule(nc['DN'] & tc['IN'] & pi['MO'], rc['MO']),
    Rule(nc['DN'] & tc['IN'] & pi['FA'], rc['FO']),
    Rule(nc['HN'] & tc['AV'] & pi['TG'], rc['MO']),
    Rule(nc['HN'] & tc['AV'] & pi['GR'], rc['MO']),
    Rule(nc['HN'] & tc['AV'] & pi['MO'], rc['FO']),
    Rule(nc['HN'] & tc['AV'] & pi['FA'], rc['TF']),
    Rule(nc['HN'] & tc['AC'] & pi['TG'], rc['MO']),
    Rule(nc['HN'] & tc['AC'] & pi['GR'], rc['FO']),
    Rule(nc['HN'] & tc['AC'] & pi['MO'], rc['FO']),
    Rule(nc['HN'] & tc['AC'] & pi['FA'], rc['TF']),
    Rule(nc['HN'] & tc['IN'] & pi['TG'], rc['MO']),
    Rule(nc['HN'] & tc['IN'] & pi['GR'], rc['FO']),
    Rule(nc['HN'] & tc['IN'] & pi['MO'], rc['TF']),
    Rule(nc['HN'] & tc['IN'] & pi['FA'], rc['TF']),
]

# Construire et simuler le système d'inférence flou
control_system = ControlSystem(rules)
simulation = ControlSystemSimulation(control_system)

# Fonction pour afficher les courbes des fonctions d'appartenance
def plot_membership_functions():
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Plot des fonctions d'appartenance pour Technology
    axs[0, 0].plot(tc_range, tc['AV'].mf, label="Avancée (AV)")
    axs[0, 0].plot(tc_range, tc['AC'].mf, label="Acceptable (AC)")
    axs[0, 0].plot(tc_range, tc['IN'].mf, label="Insuffisante (IN)")
    axs[0, 0].set_title("Technology")
    axs[0, 0].legend()
    axs[0, 0].grid()

    # Plot des fonctions d'appartenance pour Norms
    axs[0, 1].plot(nc_range, nc['DN'].mf, label="Dans les Normes (DN)")
    axs[0, 1].plot(nc_range, nc['HN'].mf, label="Hors des Normes (HN)")
    axs[0, 1].set_title("Norms")
    axs[0, 1].legend()
    axs[0, 1].grid()

    # Plot des fonctions d'appartenance pour Scope
    axs[1, 0].plot(pi_range, pi['TG'].mf, label="Très Grande (TG)")
    axs[1, 0].plot(pi_range, pi['GR'].mf, label="Grande (GR)")
    axs[1, 0].plot(pi_range, pi['MO'].mf, label="Moyenne (MO)")
    axs[1, 0].plot(pi_range, pi['FA'].mf, label="Faible (FA)")
    axs[1, 0].set_title("Scope")
    axs[1, 0].legend()
    axs[1, 0].grid()

    # Plot des fonctions d'appartenance pour Risk
    axs[1, 1].plot(rc_range, rc['TF'].mf, label="Très Forte (TF)")
    axs[1, 1].plot(rc_range, rc['FO'].mf, label="Forte (FO)")
    axs[1, 1].plot(rc_range, rc['MO'].mf, label="Moyenne (MO)")
    axs[1, 1].plot(rc_range, rc['FA'].mf, label="Faible (FA)")
    axs[1, 1].set_title("Risk")
    axs[1, 1].legend()
    axs[1, 1].grid()

    plt.tight_layout()
    plt.show()

# Fonction pour créer l'interface graphique
def interactive_fuzzy_system():
    root = Tk()
    root.title("Système d'Inférence Floue")

    # Image de fond
    background_image = Image.open(r"C:\Users\user\Desktop\capture\Capture.PNG")
    background_image = background_image.resize((600, 600), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Affichage de l'image
    background_label = Label(root, image=background_photo)
    background_label.place(x=0, y=0)

    # Entrée pour Technology
    Label(root, text=" Technologie (20-80):", font=('Arial', 12), bg="sky blue").place(x=30, y=30)
    tc_entry = Entry(root, font=('Arial', 12), width=20, bd=0, bg="white", highlightthickness=1)
    tc_entry.place(x=250, y=30)

    # Entrée pour Norms
    Label(root, text="Normes (9-70):", font=('Arial', 12), bg="sky blue").place(x=30, y=70)
    nc_entry = Entry(root, font=('Arial', 12), bd=0 , bg="white", width=20, highlightthickness=1)
    nc_entry.place(x=250, y=70)

    # Entrée pour Scope
    Label(root, text="Porté d'information (5-50):", font=('Arial', 12), bg="sky blue").place(x=30, y=110)
    pi_entry = Entry(root, font=('Arial', 12), width=20, bd=0, bg="white", highlightthickness=1)
    pi_entry.place(x=250, y=110)

    # Bouton pour soumettre les valeurs
    def on_submit():
        try:
            # Récupérer les valeurs
            tc_input = float(tc_entry.get())
            nc_input = float(nc_entry.get())
            pi_input = float(pi_entry.get())

            # Validation des entrées
            if not (20 <= tc_input <= 80):
                print("Entrée invalide pour la Technologie. Elle doit être entre 20 et 80.")
                return
            if not (9 <= nc_input <= 70):
                print("Entrée invalide pour les Normes. Elles doivent être entre 9 et 70.")
                return
            if not (5 <= pi_input <= 50):
                print("Entrée invalide pour la Portée de l'information. Elle doit être entre 5 et 50.")
                return

            # Entrer les valeurs dans la simulation
            simulation.input['Technology'] = tc_input
            simulation.input['Norms'] = nc_input
            simulation.input['Scope'] = pi_input

            # Calculer la sortie
            simulation.compute()

            # Afficher la sortie
            result = simulation.output['Risk']
            print(f"Risque de cybercriminalité calculé : {result:.2f}")

            # Déterminer le niveau de risque
            deg_TF = fuzz.interp_membership(rc_range, rc['TF'].mf, result)
            deg_FO = fuzz.interp_membership(rc_range, rc['FO'].mf, result)
            deg_MO = fuzz.interp_membership(rc_range, rc['MO'].mf, result)
            deg_FA = fuzz.interp_membership(rc_range, rc['FA'].mf, result)

            print(f"Analyse détaillée pour une valeur de risque de {result:.2f}:")
            print(f"- Degré d'appartenance à 'Très Forte' : {deg_TF:.2f}")
            print(f"- Degré d'appartenance à 'Forte'      : {deg_FO:.2f}")
            print(f"- Degré d'appartenance à 'Moyenne'    : {deg_MO:.2f}")
            print(f"- Degré d'appartenance à 'Faible'     : {deg_FA:.2f}")

            # Déterminer le niveau de risque
            if deg_TF > max(deg_FO, deg_MO, deg_FA):
                risk_level = "très forte"
            elif deg_FO > max(deg_MO, deg_FA):
                risk_level = "forte"
            elif deg_MO > deg_FA:
                risk_level = "moyenne"
            else:
                risk_level = "faible"

            # Mettre à jour l'affichage du niveau de risque sur l'interface
            risk_label.config(text=f"Niveau de risque: {risk_level.capitalize()}")

            # Mettre à jour l'affichage de l'analyse détaillée
            analysis_text = (f"Analyse détaillée pour une valeur de risque de {result:.2f}:\n"
                             f"- Degré d'appartenance à 'Très Forte' : {deg_TF:.2f}\n"
                             f"- Degré d'appartenance à 'Forte'      : {deg_FO:.2f}\n"
                             f"- Degré d'appartenance à 'Moyenne'    : {deg_MO:.2f}\n"
                             f"- Degré d'appartenance à 'Faible'     : {deg_FA:.2f}")
            analysis_label.config(text=analysis_text)

            # Affichage graphique des fonctions d'appartenance
            rc.view(sim=simulation)
            plot_membership_functions()

        except ValueError:
            print("Entrée invalide!")

    submit_button = Button(root, text="Calculer", command=on_submit, bg="sky blue", fg="lavender", font=('Arial', 12, 'bold'))
    submit_button.place(x=250, y=150)

    # Affichage du niveau de risque
    risk_label = Label(root, text="Niveau de risque:", font=('Arial', 12), bg="lavender")
    risk_label.place(x=30, y=190)

    # Affichage de l'analyse détaillée
    analysis_label = Label(root, text="Analyse détaillée:", font=('Arial', 10), bg="light cyan", justify="left")
    analysis_label.place(x=30, y=220)

    root.mainloop()

# Lancer l'interface
interactive_fuzzy_system()
