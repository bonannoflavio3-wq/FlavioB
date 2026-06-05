import tkinter as tk

# Fenêtre principale
window = tk.Tk()
window.title("Pong")
canvas1 = tk.Canvas(window, bg="black", width=500, height=500)
canvas1.pack()

balleX = 250
balleY = 250
dirX = 10
dirY = 7
score_gauche = 0
score_droite = 0

balle = canvas1.create_oval(balleX, balleY, balleX + 10, balleY + 10, fill="red")

canvas1.create_line(250, 0, 250, 500, fill="white", dash=(5, 2))

racleft = canvas1.create_rectangle(10, 200, 20, 300, fill="green")
racright = canvas1.create_rectangle(480, 200, 490, 300, fill="green")

texte_score_gauche = canvas1.create_text(120, 20, text="Joueur Gauche : 0", fill="white", font=("Arial", 12))
texte_score_droite = canvas1.create_text(380, 20, text="Joueur Droit : 0", fill="white", font=("Arial", 12))

def haut_droite(evt): canvas1.move(racright, 0, -20)
def bas_droite(evt): canvas1.move(racright, 0, 20)
def haut_gauche(evt): canvas1.move(racleft, 0, -20)
def bas_gauche(evt): canvas1.move(racleft, 0, 20)

canvas1.bind_all("<KeyPress-Up>", haut_droite)
canvas1.bind_all("<KeyPress-Down>", bas_droite)
canvas1.bind_all("<KeyPress-a>", haut_gauche)
canvas1.bind_all("<KeyPress-q>", bas_gauche)

def restart_game():
    global balleX, balleY, dirX, dirY, score_gauche, score_droite
    balleX = 250
    balleY = 250
    dirX = 10
    dirY = 7
    score_gauche = 0
    score_droite = 0

    canvas1.coords(balle, balleX, balleY, balleX + 10, balleY + 10)
    canvas1.itemconfig(texte_score_gauche, text="Joueur Gauche : 0")
    canvas1.itemconfig(texte_score_droite, text="Joueur Droit : 0")

tk.Button(window, text="Rejouer", command=restart_game).pack()
tk.Button(window, text="Quitter", command=window.destroy).pack()

def mouvballe():
    global balleX, balleY, dirX, dirY, score_gauche, score_droite

    balleX += dirX
    balleY += dirY
    canvas1.coords(balle, balleX, balleY, balleX + 10, balleY + 10)

    if balleY < 0 or balleY > 490:
        dirY = -dirY

    coords_balle = canvas1.coords(balle)
    coords_racright = canvas1.coords(racright)
    coords_racleft = canvas1.coords(racleft)

    if coords_balle[2] >= coords_racright[0] and coords_balle[0] <= coords_racright[2]:
        if coords_balle[3] >= coords_racright[1] and coords_balle[1] <= coords_racright[3]:
            dirX = -dirX

    if coords_balle[0] <= coords_racleft[2] and coords_balle[2] >= coords_racleft[0]:
        if coords_balle[3] >= coords_racleft[1] and coords_balle[1] <= coords_racleft[3]:
            dirX = -dirX

    if balleX > 490:
        score_gauche += 1
        canvas1.itemconfig(texte_score_gauche, text=f"Joueur Gauche : {score_gauche}")
        balleX, balleY = 250, 250
        dirX = -10

    if balleX < 0:
        score_droite += 1
        canvas1.itemconfig(texte_score_droite, text=f"Joueur Droit : {score_droite}")
        balleX, balleY = 250, 250
        dirX = 10

    canvas1.after(50, mouvballe)

mouvballe()
window.mainloop()
