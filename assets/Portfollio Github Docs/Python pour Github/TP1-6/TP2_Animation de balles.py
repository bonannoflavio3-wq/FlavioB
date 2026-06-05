from tkinter import *
import tkinter as tk
import random

def move():
    global flag
    for balle in balles:
        if balle['x'] > largeur - 20 or balle['x'] < 20:
            balle['dx'] = -balle['dx']
        balle['x'] += balle['dx']

        balle['v'] += balle['dv']
        balle['y'] += balle['v']

        if balle['y'] > hauteur - 20:
            balle['y'] = hauteur - 20
            balle['v'] = -balle['v']

        if balle['y'] < 20:
            balle['y'] = 20
            balle['v'] = -balle['v']

        canva1.coords(balle['id'], balle['x'] - 15, balle['y'] - 15, balle['x'] + 15, balle['y'] + 15)

    if flag > 0:
        window.after(50, move)

def stop_it():
    global flag
    if flag == 1:
        flag=0
    else:
        flag=1
        move()

def ajouter_balle():
    """Ajoute une nouvelle balle sur le canevas"""
    x = random.randint(30, largeur - 30)
    y = random.randint(30, hauteur - 30)
    dx = random.choice([-5, -4, 4, 5])
    dv = random.randint(1, 3)
    v = 0
    balle_id = canva1.create_oval(x - 15, y - 15, x + 15, y + 15, width=2, fill="red")
    balles.append({'id': balle_id, 'x': x, 'y': y, 'dx': dx, 'dv': dv, 'v': v})

balles = []
flag = 0

hauteur = 300
largeur = 300

window = tk.Tk()
window.title("TP2: animation balles")

canva1 = Canvas(window, bg='black', height=hauteur, width=largeur)
canva1.grid(row=1, column=1, columnspan=4, padx=5, pady=5)

tk.Button(window, text='Stop /start', width=8, command=stop_it).grid(row=2, column=2)
tk.Button(window, text='Quitter', width=8, command=window.quit).grid(row=2, column=3)
tk.Button(window, text='Ajouter balle', width=12, command=ajouter_balle).grid(row=2, column=4)

ajouter_balle()

window.mainloop()
