import tkinter as tk

window = tk.Tk()
window.title("Pong")
canvas1 = tk.Canvas(window, bg="black", width=500, height=500)

balle = canvas1.create_oval(40, 40, 0, 0, fill="red")
canvas1.move(balle, 480, 400)
canvas1.pack()

line1 = canvas1.create_line(250, 500, 250, 2, fill="white", dash=(5, 2))

racleft = canvas1.create_rectangle(2, 2, 10, 100, fill="green")
canvas1.move(racleft, 10, 200)

racright = canvas1.create_rectangle(2, 2, 10, 100, fill="green")
canvas1.move(racright, 480, 200)

button1 = tk.Button(window, text="rejouer", command=window.destroy)
button1.pack()
button2 = tk.Button(window, text="quitter", command=window.destroy)
button2.pack()

x = 0
y = 0
balleX = 300
balleY = 300
dirX = 10
dirY = 7

score_gauche = 0
score_droite = 0

texte_score_gauche = canvas1.create_text(120, 20, text="Joueur Gauche : 0", fill="white", font=("Arial", 12))
texte_score_droite = canvas1.create_text(380, 20, text="Joueur Droit : 0", fill="white", font=("Arial", 12))

def haut_droite(evt):
    canvas1.move(racright, 0, -20)

def bas_droite(evt):
    canvas1.move(racright, 0, 20)

def ia_deplace_raquette():
    coords_balle = canvas1.coords(balle)
    coords_rac = canvas1.coords(racright)
    centre_balle = (coords_balle[1] + coords_balle[3]) / 2
    centre_rac = (coords_rac[1] + coords_rac[3]) / 2

    if centre_balle < centre_rac and coords_rac[1] > 0:
        canvas1.move(racright, 0, -8)  # vitesse IA vers le haut
    elif centre_balle > centre_rac and coords_rac[3] < 500:
        canvas1.move(racright, 0, 8)   # vitesse IA vers le bas

def haut_gauche(evt):
    canvas1.move(racleft, 0, -20)

def bas_gauche(evt):
    canvas1.move(racleft, 0, 20)

canvas1.bind_all("<KeyPress-Up>", haut_gauche)
canvas1.bind_all("<KeyPress-Down>", bas_gauche)

def mouvballe():
    global balleX, balleY, dirX, dirY, score_gauche, score_droite

    balleX = balleX + dirX
    balleY = balleY + dirY

    canvas1.coords(balle, balleX, balleY, balleX + 10, balleY + 10)

    if balleY < 10 or balleY > 465:
        dirY = -dirY

    if balleX > 490:
        score_gauche += 1
        canvas1.itemconfig(texte_score_gauche, text=f"Joueur Gauche : {score_gauche}")
        balleX = 250
        balleY = 250
        dirX = -10

    if balleX < 0:
        score_droite += 1
        canvas1.itemconfig(texte_score_droite, text=f"Joueur Droit : {score_droite}")
        balleX = 250
        balleY = 250
        dirX = 10

    coords_balle = canvas1.coords(balle)
    coords_racright = canvas1.coords(racright)
    if coords_balle[2] >= coords_racright[0] and coords_balle[0] <= coords_racright[2]:
        if coords_balle[3] >= coords_racright[1] and coords_balle[1] <= coords_racright[3]:
            dirX = -dirX

    coords_racleft = canvas1.coords(racleft)
    if coords_balle[0] <= coords_racleft[2] and coords_balle[2] >= coords_racleft[0]:
        if coords_balle[3] >= coords_racleft[1] and coords_balle[1] <= coords_racleft[3]:
            dirX = -dirX

    ia_deplace_raquette()

    canvas1.after(50, mouvballe)
mouvballe()
window.mainloop()
