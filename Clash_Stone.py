# Importation de tout les modules necessaires
import random as rd
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, Tk, Button
from PIL import Image, ImageTk
import sys, time, random, os, threading


fenetre = tk.Tk()
fenetre.title("Clash Stones")
fenetre.geometry("{0}x{1}+0+0".format(fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()))
fenetre.resizable(False, False) # ne pas pouvoir redimensionner

# Définition des caractéristiques des cartes
class Carte():
    """Chaques carte est une instance de cette class"""
    __slots__ = ['nom', 'vie', 'attaque', 'effet_attaque', 'faiblesse', 'image', 'vie_initiale'] 
    def __init__(self, nom, vie, attaque, effet_attaque, image):
        # attribuer les caracteristiques des cartes = nom, vie, attaque, faiblesse...
        dico_faiblesse = {"plante": "feu", "feu": "eau", "eau": "electricite", "electricite": "roche", "roche": "plante"}
        self.nom, self.vie, self.attaque, self.effet_attaque, self.image, self.vie_initiale, self.faiblesse = nom, vie, attaque, effet_attaque, image, vie, dico_faiblesse[self.effet_attaque]   
        
    def Attaquer(self, carte_attaquee):
        multiplicateur = 1.5 if carte_attaquee.faiblesse == self.effet_attaque else 1
        carte_attaquee.vie -= int(self.attaque * multiplicateur) 
        if carte_attaquee.vie < 0:
            carte_attaquee.vie = 0 # ne pas aller dans les negatifs
        
    def reset(self):
        self.vie = self.vie_initiale            
    

# Dimensions des images et des boutons
largeur = 90
hauteur = 130

# Fonction pour charger une image
def image(chemin):
    return ImageTk.PhotoImage(Image.open(chemin).resize((largeur, hauteur)))

# charger les images : logo, 1Joueur, 2Joueur, Dos des cartes et fleche verte indiquant qui doit jouer
image_dos_carte, image_fleche_verte, image_logo_jeu, image_1joueur, image_2joueur = image("Images_annexes/dosCarte.png"), image("Images_annexes/fleche verte.png"), ImageTk.PhotoImage(Image.open("Images_annexes/Logo_jeu.png").resize((1210, 1010))), ImageTk.PhotoImage(Image.open("Images_annexes/1joueur.png").resize((300, 150))), ImageTk.PhotoImage(Image.open("Images_annexes/2joueur.png").resize((300, 150)))

# Charger toutes les cartes, leur caracteristique et leur image dans un dictionnaire
dictionnaire_cartes = {
"carte_nain_de_feu" : Carte("Nain de Flammes", 150, 40, "feu", image('Images/Nain_de_feu.png')),
"carte_chauve_souris_feu" : Carte("Chauve-souris Incandescente", 120, 30, "feu", image('Images/Chauve_souris_feu.png')),
"carte_serpent_de_feu" : Carte("Serpent de Braises", 130, 35, "feu", image('Images/Serpent_de_braise.png')),
"carte_phoenix_de_feu" : Carte("Phoenix Cendre", 200, 50, "feu", image('Images/Phoenix_ardent.png')),
"carte_scorpion_de_feu" : Carte("Scorpion de Feu", 140, 45, "feu", image('Images/Scorpion_brulant.png')),
"carte_fantome_de_feu" : Carte("Fantome de Feu", 110, 35, "feu", image('Images/Phantom_de_feu.png')),
"carte_golem_de_feu" : Carte("Golem de Lave", 180, 55, "feu", image('Images/Golem_de_lave.png')),
"carte_golem_vegetal" : Carte("Golem Sylvestre", 200, 45, "plante", image('Images/Golem_vegetal.png')),
"carte_plante_carnivore" : Carte("Plante Carnivore Geante", 160, 40, "plante", image('Images/Plante_carnivore.png')),
"carte_dragon_vegetal" : Carte("Dragon des Ronces", 220, 60, "plante", image('Images/Dragon_naturel.png')),
"carte_araigne_vegetale" : Carte("Araignee Sylvestre", 120, 35, "plante", image('Images/Araignee_de_foret.png')),
"carte_menthe_religieuse" : Carte("Menthe Religieuse", 140, 30, "plante", image('Images/Menthe_geante.png')),
"carte_ours_vegetal" : Carte("Ours des Forets", 180, 50, "plante", image('Images/Roi_ours.png')),
"carte_loup_vegetal" : Carte("Loup des Clairieres", 150, 45, "plante", image('Images/Loup_empereur.png')),
"carte_dragon_eau" : Carte("Dragon des Mers", 220, 55, "eau", image('Images/Dragon_aquatique.png')),
"carte_elfe_eau" : Carte("Elfe des Marees", 160, 35, "eau", image('Images/Elfe_des_mers.png')),
"carte_gorille_glace" : Carte("Gorille des Neiges", 190, 50, "eau", image('Images/Gorille_de_glace.png')),
"carte_colibri_glace" : Carte("Colibri Gele", 110, 25, "eau", image('Images/Colibri_des_neiges.png')),
"carte_poisson_globe" : Carte("Poisson-Globe Geant", 140, 35, "eau", image('Images/Poisson_globe_geant.png')),
"carte_sorcier_glace" : Carte("Sorcier du Givre", 170, 45, "eau", image('Images/Sorcier_du_blizzard.png')),
"carte_hiboux_glace" : Carte("Hibou de Givre", 150, 40, "eau", image('Images/Hiboux_du_froid.png')),
"carte_seiche_malefique" : Carte("Seiche Malefique", 150, 40, "eau", image('Images/Seiche_oceanique.png')),
"carte_dragon_foudre" : Carte("Dragon Orageux", 210, 60, "electricite", image('Images/Lezard_de_foudre.png')),
"carte_scorpion_foudre" : Carte("Scorpion Fulgurant", 140, 40, "electricite", image('Images/Insecte_electrique.png')),
"carte_chevalier_foudre" : Carte("Chevalier de Tonnerre", 180, 50, "electricite", image('Images/Chevalier_des_tempetes.png')),
"carte_taureau_foudre" : Carte("Taureau de Foudre", 190, 55, "electricite", image('Images/Taureau_eclair.png')),
"carte_anguille_foudre" : Carte("Anguille Lumineuse", 130, 35, "electricite", image('Images/Anguille_geante.png')),
"carte_aigle_foudre" : Carte("Aigle Foudroyant", 160, 45, "electricite", image('Images/Aigle_des_orages.png')),
"carte_golem_pierre" : Carte("Golem de Granite", 230, 55, "roche", image('Images/Golem_de_pierre.png')),
"carte_gargouille_pierre" : Carte("Gargouille de Roche", 180, 45, "roche", image('Images/Gargouille_de_roche.png')),
"carte_serpent_pierre" : Carte("Serpent de Poussiere", 140, 35, "roche", image('Images/Serpent_totem.png')),
"carte_lezard_pierre" : Carte("Lezard de Sable", 120, 30, "roche", image('Images/Lezard_des_cavernes.png')),
"carte_boeuf_pierre" : Carte("Boeuf de Roche", 200, 50, "roche", image('Images/Boeuf_des_montagnes.png')),
"carte_rhinoceros_pierre" : Carte("Rhinoceros du Canyon", 210, 55, "roche", image('Images/Rhinoceros_terrestres.png')),
}

def choisir_un_mode():
    fond_logo = tk.Label(fenetre, image = image_logo_jeu, width=1200, height=1000).place(x = 0, y = 0)
    mode_1_joueur = tk.Button(fenetre, image = image_1joueur, width=300, height=150, command=lambda:lancer_le_jeu(True), highlightthickness=0, relief="flat", bg = "#000000").place(x=80, y=820)
    mode_2_joueur = tk.Button(fenetre, image = image_2joueur, width=300, height=150, command=lambda:lancer_le_jeu(False), highlightthickness=0, relief="flat", bg = "#000000").place(x=800, y=820)

def lancer_le_jeu(bot_present):
    global liste_bouton_deck1, liste_bouton_deck2, bouton_attaquer1, bouton_attaquer2, bouton_carte9, bouton_carte10, p1_peut_jouer, p2_peut_jouer, icone_qui_joue, presence_du_bot, liste_carte1_affichees, liste_carte2_affichees, liste_carte1, liste_carte2, comteur_p1, comteur_p2, stats9, stats10, compteur_pour_attaquer, bouton_exclu
    for carte in liste_cartes:
        carte.reset()                           # Réinitialiser toutes les vies des cartes
    random.shuffle(liste_cartes)                # Mélanger la liste des cartes afin de ne jamais avoir les memes entre plusieurs parties
    icone_qui_joue = None                       # Initialisation vide de l'icone indiquant qui doit jouer
    compteur_pour_attaquer = 0                  # empecher d'attaquer avant que les 2 joueurs ai choisi une carte (mettre en commentaire pour tester d'attaquer directement)
    comteur_p1, comteur_p2 = 0, 0               # les comteurs servent a empeche d'afficher les stats des cartes avant d'en avoir placee une au milieu du terrain
    p1_peut_jouer, p2_peut_jouer = True, False 
    bouton_exclu = [] 
    presence_du_bot = bot_present
    # Chemins relatifs pour les images
    bg_path = os.path.join("Images", "arriere_plan2.webp")
    jeu_path = os.path.join("Images", "Arriere_plan.png")

    # Vérification de l'existence des fichiers
    if os.path.exists(bg_path):
        print("Le fichier de fond existe.")
    else:
        print("Le fichier de fond n'existe pas.")

    if os.path.exists(jeu_path):
        print("Le fichier de jeu existe.")
    else:
        print("Le fichier de jeu n'existe pas.")

    # Charger l'image de fond
    try:
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((1210, 1000), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(fenetre, image=bg_photo)
        bg_label.image = bg_photo  # Garder une référence
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image de fond : {e}")

    # Cadre pour la zone de jeu 
    cadre_jeu = tk.Frame(fenetre, bg="#FFFFFF", width=880, height=980, bd=3, relief="ridge")
    cadre_jeu.place(x=160, y=10)

    # Charger et afficher l'image de jeu comme arrière-plan du cadre
    try:
        image_jeu = Image.open(jeu_path)
        image_jeu = image_jeu.resize((875, 975), Image.LANCZOS)
        image_jeu_photo = ImageTk.PhotoImage(image_jeu)
        image_label = tk.Label(cadre_jeu, image=image_jeu_photo, bg="#FFFFFF")
        image_label.image = image_jeu_photo  # Garder une référence
        image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    except Exception as e:
        print(f"Erreur lors du chargement de l'image de jeu : {e}")

    # Liste des cartes en evitant les doublons en parcourant la liste des cartes de 2 sens differents 
    # et en separant les cartes affichees (=cartes en bas) aux cartes en fond (=cartes entrain de cycler)
    liste_carte1 = [liste_cartes[carte] for carte in range(1, 5)]
    liste_carte1_affichees = [liste_cartes[carte] for carte in range(5, 9)]

    liste_carte2 = [liste_cartes[-carte] for carte in range(1, 5)]
    liste_carte2_affichees = [liste_cartes[-carte] for carte in range(5, 9)]

    # initialiser les label des cadres des stats et les bouton attaquer
    stats9 = tk.Label(fenetre, font=("Arial", 20), fg="#0000B0", width=30, height=10, anchor="w", justify="left",)
    stats10 = tk.Label(fenetre, font=("Arial", 20), fg="#0000B0", width=30, height=10, anchor="w", justify="left",)
    bouton_attaquer1 = tk.Button(fenetre, text="Attaquer !!!", font=("Arial", 16), bg="#6da715", fg="white", bd=2, highlightbackground="#000000", highlightthickness=2, state="disabled")
    bouton_attaquer2 = tk.Button(fenetre, text="Attaquer !!!", font=("Arial", 16), bg="#6da715", fg="white", bd=2, highlightbackground="#000000", highlightthickness=2, state="disabled")


    #################################### Tout ce qui concerne les boutons du haut est ici (Alias deck 1)####################################
    bouton_carte1 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(1,0), bd=0, highlightthickness=0, relief="flat")
    bouton_carte1.place(x=220, y=70)
    bouton_carte2 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(1,1), bd=0, highlightthickness=0, relief="flat")
    bouton_carte2.place(x=340, y=70)
    bouton_carte3 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(1,2), bd=0, highlightthickness=0, relief="flat")
    bouton_carte3.place(x=460, y=70)
    bouton_carte4 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(1,3), bd=0, highlightthickness=0, relief="flat")
    bouton_carte4.place(x=580, y=70)
    # Carte au milieu du terrain
    bouton_carte9 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur,command=afficher_stats(9), bd=0, highlightthickness=0, relief="flat")
    bouton_carte9.place(x=400, y=270)


    #################################### Tout ce qui concerne les boutons du bas est ici (Alias deck 2) ####################################
    bouton_carte5 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(2,0), bd=0, highlightthickness=0, relief="flat")
    bouton_carte5.place(x=220, y=780)
    bouton_carte6 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(2,1), bd=0, highlightthickness=0, relief="flat")
    bouton_carte6.place(x=340, y=780)
    bouton_carte7 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(2,2), bd=0, highlightthickness=0, relief="flat")
    bouton_carte7.place(x=460, y=780)
    bouton_carte8 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=lambda:bouton_clique(2,3), bd=0, highlightthickness=0, relief="flat")
    bouton_carte8.place(x=580, y=780)
    # Carte au milieu du terrain
    bouton_carte10 = tk.Button(cadre_jeu, image=None, width=largeur, height=hauteur, command=afficher_stats(10), bd=0, highlightthickness=0, relief="flat") 
    bouton_carte10.place(x=400, y=580)



    # Ranger les boutons dans 2 listes (= bdd des boutons)
    liste_bouton_deck1 = [bouton_carte1, bouton_carte2, bouton_carte3, bouton_carte4]
    liste_bouton_deck2 = [bouton_carte5, bouton_carte6, bouton_carte7, bouton_carte8]



    for i in range(4):
        """
        simuler un clique de chaque carte pour activer les emplacements
        """ 
        for j in range(2):
            bouton_clique(j+1, i) 

    if rd.randint(1,2) == 1:                            # Definie qui joue en 1er
        p1_peut_jouer, p2_peut_jouer = True, False
    else :
        p1_peut_jouer, p2_peut_jouer = False,  True
        

    # arranger quelque truc par exemple, l'image des cartes du milieu qui doivent etre vide ou barree au commencement
    bouton_carte10.config(image = image_dos_carte)
    bouton_carte9.config(image = image_dos_carte)
    stats9.destroy()
    stats9 = tk.Label(fenetre)
    stats10.destroy()
    stats10 = tk.Label(fenetre)
    bouton_attaquer2.place(x=400, y=650)  # Positionner les bouton attaquer
    bouton_attaquer1.place(x=400, y=350)  
    icone_indique_joueur()
    
    def action_bot():
        """
        Fonction regroupant les variables et initialisations du jeu
        """
        global liste_bouton_deck1, bouton_attaquer1, liste_commande_bot, liste_commande_bot
        liste_commande_bot = [
                    lambda: bouton_clique(1, 0),
                    lambda: bouton_clique(1, 1),
                    lambda: bouton_clique(1, 2),
                    lambda: bouton_clique(1, 3)]
        liste_attaque_bot = [   
                    lambda: commande_attaquer(9),
                    lambda: commande_attaquer(9),
                    lambda: commande_attaquer(9),
                    lambda: commande_attaquer(9)]
        listes_bot = liste_attaque_bot + liste_commande_bot
        if bot_present:
            for bouton in liste_bouton_deck1:
                bouton.config(command = lambda:None)
            bouton_attaquer1.config(command = lambda:None)
        
        
            while bot_present:  # Boucle pour gérer le bot
                time.sleep(1)
                commande = rd.choice(listes_bot)
                try :
                    commande()
                except :
                    pass
                print("Commande exécutée.")
    
    # Si bot_present est actif, lancer le bot dans un thread séparé
    if bot_present:
        bot_thread = threading.Thread(target=action_bot, daemon=True)
        bot_thread.start()


def changer_de_tour():
    global p1_peut_jouer, p2_peut_jouer
    p1_peut_jouer, p2_peut_jouer = not p1_peut_jouer, not p2_peut_jouer
    icone_indique_joueur()


def icone_indique_joueur():
    global icone_qui_joue
    if icone_qui_joue:
            icone_qui_joue.destroy()
    if p1_peut_jouer == True:
        icone_qui_joue = tk.Label(fenetre, image=image_fleche_verte, font=("Arial", 14), fg="green")
        icone_qui_joue.place(x=180, y=100) 
    else:
        icone_qui_joue = tk.Label(fenetre, image=image_fleche_verte, font=("Arial", 14), fg="blue")
        icone_qui_joue.place(x=180, y=820)  


def commande_attaquer(id_bouton):
    global compteur_pour_attaquer
    """
    fonction prenant en parametre le bouton 9 ou 10
    ayant pour but d'attaquer la carte adverse (celle au milieu)
    + systeme de tour par tour
    """
    if compteur_pour_attaquer < 10 :
        return
    if id_bouton == 9 :
        carte_attaquante, carte_attaquee, liste_bouton_opposant  = liste_carte1[-1], liste_carte2[-1], liste_bouton_deck2
        autre_bouton, joueur = 10, "Joueur 1"
        if not p1_peut_jouer:
            return 
    else :
        carte_attaquante, carte_attaquee, liste_bouton_opposant = liste_carte2[-1], liste_carte1[-1], liste_bouton_deck1
        autre_bouton, joueur = 9, "Joueur 2"
        if not p2_peut_jouer:
            return
    compteur = 0
    for bouton in liste_bouton_opposant :               # compter le nombre d'emplacement mort de l'adversaire
        if bouton.cget("state") == "disabled" :
            compteur += 1
    
    if carte_attaquante.vie > 0 :
        carte_attaquante.Attaquer(carte_attaquee)
        afficher_stats(autre_bouton)
        changer_de_tour()

    if compteur == 4 and carte_attaquee.vie <= 0 :      # verifier si l'adversaire a 4 emplacement mort et si sa derniere carte (au milieu) est morte
        choisir_un_mode()                          
        



def afficher_stats(bouton):
    """
    Fonction qui affiche les statistiques de la carte sur les boutons 9 ou 10 avec un affichage esth��tique am��lior��.
    """
    global comteur_p1, comteur_p2, stats9, stats10

    # Choisir la carte et les variables en fonction du bouton cliqu��
    if bouton == 9:
        carte = liste_carte1[-1]
        comteur = comteur_p1
        stats = stats9
        y = 300
        couleur_fond = "#D2B48C"  
        couleur_texte = "#4E3629"  
    elif bouton == 10:
        carte = liste_carte2[-1]
        comteur = comteur_p2
        stats = stats10
        y = 595
        couleur_fond = "#D2B48C"  
        couleur_texte = "#4E3629"  

    # V��rifier si le compteur d��passe 4 pour afficher les stats
    if comteur > 4:
        # Mise �� jour du texte avec les statistiques de la carte (nom et PV)
        stats.config(
            text=f"{carte.nom}\nPV : {carte.vie}",
            font=("Verdana", 16, "bold"),  # Police et taille 
            fg=couleur_texte,  # Couleur du texte
            bg=couleur_fond,  # Couleur de fond 
            width=12,  # Largeur 
            height=4,  # Hauteur ajust��e pour inclure le nom et les PV
            anchor="center",
            justify="center",
            relief="solid",  # Bordure 
            bd=2,  # Largeur de la bordure
            padx=10,  # Espacement int��rieur horizontal
            pady=5,  # Espacement int��rieur vertical
            wraplength=180  # Limiter la largeur du texte et effectuer un retour �� la ligne
        )
        stats.place(x=670, y=y)  # Positionnement du label sur l'��cran


    
def bouton_clique(numero_de_deck, numero_du_bouton):
    """
    Fonction prenant en parametre le numero du bouton et le numero de deck. Elle a pour fonction de 
    faire le systeme de file dans la liste_carte et de verifier la nouvelle carte qui lui est attribué 
    dans la liste_deck puis après elle donne la reference de l'ancienne carte au bouton du milieu afin
    de pouvoir afficher les bonnes stats de la bonne carte
    """
    global comteur_p1, comteur_p2, liste_carte1, liste_carte2, compteur_pour_attaquer, liste_commande_bot, bouton_exclu, presence_du_bot
    
    # verifier si c'est au tour du joueur
    if numero_de_deck == 1 and not p1_peut_jouer:
        return
    elif numero_de_deck == 2 and not p2_peut_jouer:
        return
    
    if numero_du_bouton in bouton_exclu and numero_de_deck == 1 and presence_du_bot == True:
        return
    compteur_pour_attaquer += 1  
    # Defini les variables en fonction du deck (si c'est le joueur ou le bot)
    if numero_de_deck == 1 :
        bouton_attaquer = bouton_attaquer1
        comteur_p1 += 1
        liste_deck = liste_carte1_affichees
        liste_carte = liste_carte1
        liste_bouton = liste_bouton_deck1  
        bouton_milieu = bouton_carte9 
    else:
        bouton_attaquer = bouton_attaquer2
        comteur_p2 += 1
        liste_deck = liste_carte2_affichees
        liste_carte = liste_carte2
        liste_bouton = liste_bouton_deck2
        bouton_milieu = bouton_carte10
    
    bouton = liste_bouton[numero_du_bouton]                                                             # quel est le bouton concerne ?
    ancienne_carte = liste_deck[numero_du_bouton]                                                       # quel est l'ancienne carte qui va aller au milieu ?
    
    if liste_carte[-1].vie <= 0 :                                                                  # Cas lorsque la carte du milieu est morte = pareille que le else
        del liste_carte[-1]                                                                             # sauf qu'on ne declenche pas le cycle de carte
        liste_carte.append(ancienne_carte)
        bouton.config(image = image_dos_carte, state="disabled") 
        bouton_exclu.append(numero_du_bouton)
    else :                                      
        nouvelle_carte_a_supprimer = liste_carte.pop(0)                                                 # supprimer et stocker la prochaine carte du cycle 
        liste_deck[numero_du_bouton] = nouvelle_carte_a_supprimer                                       # remplacer l'ancienne carte par la nouvelle
        liste_carte.append(ancienne_carte)                                                              # deplacer l'ancienne carte a la fin de la liste_carte = carte du milieu
        bouton.config(image=nouvelle_carte_a_supprimer.image)                                           # mettre a jour l'image du bouton clique
        bouton.image = nouvelle_carte_a_supprimer.image                                                 # Cette ligne sert a garder l'image en memoire en lien avec le garbage collector
    bouton_attaquer.config(state="normal", command=lambda:commande_attaquer(numero_de_deck+8))                          # mettre a jour la commande du bouton attaquer
    bouton_milieu.config(image=ancienne_carte.image, command=lambda: afficher_stats(numero_de_deck+8))  # mettre a jour la commande et l'image du bouton du milieu
    afficher_stats(numero_de_deck+8)                                                                   # mettre a jour les stats de la carte du milieu
    changer_de_tour()  
                    


choisir_un_mode()

# Lancer la boucle principale
fenetre.mainloop()
