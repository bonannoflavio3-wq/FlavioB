import tkinter as tk
import random

# Paramètres du jeu
largeur = 1000
hauteur = 500
SPACE_SIZE = 20

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu Snake Duo")
        self.root.resizable(False, False)

        self.running = True
        self.paused = False

        self.score1 = 0
        self.score2 = 0

        self.direction1 = 'Right'
        self.direction2 = 'Left'

        self.label1 = tk.Label(root, text=f"Joueur 1 (Jaune) Score : {self.score1}", font=('Arial', 14), fg="yellow")
        self.label1.pack()
        self.label2 = tk.Label(root, text=f"Joueur 2 (Bleu) Score : {self.score2}", font=('Arial', 14), fg="cyan")
        self.label2.pack()

        self.canvas = tk.Canvas(root, bg="black", width=largeur, height=hauteur)
        self.canvas.pack()

        self.pause_button = tk.Button(root, text="Pause", font=('Arial', 12), command=self.toggle_pause)
        self.pause_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Quitter", font=('Arial', 12), command=root.quit)
        self.quit_button.pack(pady=5)

        self.replay_button = tk.Button(root, text="Rejouer", font=('Arial', 20), command=self.restart_game)

        self.snake1 = [[100, 100], [80, 100], [60, 100]]
        self.snake1_squares = []
        for x, y in self.snake1:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="yellow")
            self.snake1_squares.append(square)

        self.snake2 = [[900, 700], [920, 700], [940, 700]]
        self.snake2_squares = []
        for x, y in self.snake2:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="cyan")
            self.snake2_squares.append(square)

        self.food1 = self.create_food(self.snake1 + self.snake2)
        self.food2 = self.create_food(self.snake1 + self.snake2 + [self.canvas.coords(self.food1)[:2]])

        self.root.bind("<Left>", self.go_left_1)
        self.root.bind("<Right>", self.go_right_1)
        self.root.bind("<Up>", self.go_up_1)
        self.root.bind("<Down>", self.go_down_1)

        self.root.bind("z", self.go_up_2)
        self.root.bind("s", self.go_down_2)
        self.root.bind("q", self.go_left_2)
        self.root.bind("d", self.go_right_2)

        self.alive1 = True
        self.alive2 = True

        self.next_turn()

    def create_food(self, forbidden_positions):
        while True:
            x = random.randint(0, (largeur - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            y = random.randint(0, (hauteur - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            if [x, y] not in forbidden_positions:
                break
        return self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red")

    def create_food(self, forbidden_positions, color="red"):
        while True:
            x = random.randint(0, (largeur - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            y = random.randint(0, (hauteur - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            if [x, y] not in forbidden_positions:
                break
        return self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color)

    def next_turn(self):
        if not self.running:
            return

        if self.paused:
            self.root.after(100, self.next_turn)
            return

        if self.alive1:
            self.move_snake(1)
        if self.alive2:
            self.move_snake(2)

        if not self.alive1 or not self.alive2:
            self.game_over()
            return

        self.root.after(100, self.next_turn)

    def move_snake(self, player):
        if player == 1:
            direction = self.direction1
            snake = self.snake1
            snake_squares = self.snake1_squares
            food = self.food1
            score_label = self.label1
            score = self.score1
            color = "yellow"
        else:
            direction = self.direction2
            snake = self.snake2
            snake_squares = self.snake2_squares
            food = self.food2
            score_label = self.label2
            score = self.score2
            color = "cyan"

        head_x, head_y = snake[0]

        if direction == "Up":
            head_y -= SPACE_SIZE
        elif direction == "Down":
            head_y += SPACE_SIZE
        elif direction == "Left":
            head_x -= SPACE_SIZE
        elif direction == "Right":
            head_x += SPACE_SIZE

        head_x %= largeur
        head_y %= hauteur

        new_head = [head_x, head_y]

        if new_head in snake[1:]:
            if player == 1:
                self.alive1 = False
            else:
                self.alive2 = False
            return

        other_snake = self.snake2 if player == 1 else self.snake1
        if new_head in other_snake:
            if player == 1:
                self.alive1 = False
            else:
                self.alive2 = False
            return

        snake.insert(0, new_head)
        square = self.canvas.create_rectangle(head_x, head_y, head_x + SPACE_SIZE, head_y + SPACE_SIZE, fill=color)
        snake_squares.insert(0, square)

        food_coords = self.canvas.coords(food)
        if head_x == int(food_coords[0]) and head_y == int(food_coords[1]):
            if player == 1:
                self.score1 += 1
                score_label.config(text=f"Joueur 1 (Jaune) Score : {self.score1}")
                self.canvas.delete(food)
                self.food1 = self.create_food(self.snake1 + self.snake2, color="red")
            else:
                self.score2 += 1
                score_label.config(text=f"Joueur 2 (Bleu) Score : {self.score2}")
                self.canvas.delete(food)
                self.food2 = self.create_food(self.snake1 + self.snake2, color="cyan")
        else:
            tail = snake_squares.pop()
            self.canvas.delete(tail)
            snake.pop()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Reprendre" if self.paused else "Pause")

    def game_over(self):
        self.running = False
        msg = ""
        if not self.alive1 and not self.alive2:
            msg = "Match nul !"
        elif not self.alive1:
            msg = "Joueur 2 (Bleu) gagne !"
        elif not self.alive2:
            msg = "Joueur 1 (Jaune) gagne !"

        self.canvas.create_text(largeur / 2, hauteur / 2, text=f"Game Over\n{msg}", fill="red", font=("Arial", 32))
        self.replay_button.pack(pady=5)

    def restart_game(self):
        self.canvas.delete("all")
        self.score1 = 0
        self.score2 = 0
        self.label1.config(text=f"Joueur 1 (Jaune) Score : {self.score1}")
        self.label2.config(text=f"Joueur 2 (Bleu) Score : {self.score2}")

        self.direction1 = 'Right'
        self.direction2 = 'Left'

        self.running = True
        self.paused = False

        self.alive1 = True
        self.alive2 = True

        self.snake1 = [[100, 100], [80, 100], [60, 100]]
        self.snake1_squares = []
        for x, y in self.snake1:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="yellow")
            self.snake1_squares.append(square)

        self.snake2 = [[900, 700], [920, 700], [940, 700]]
        self.snake2_squares = []
        for x, y in self.snake2:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="cyan")
            self.snake2_squares.append(square)

        self.food1 = self.create_food(self.snake1 + self.snake2, color="red")
        self.food2 = self.create_food(self.snake1 + self.snake2 + [self.canvas.coords(self.food1)[:2]], color="cyan")

        self.replay_button.pack_forget()
        self.next_turn()

    def change_direction(self, player, new_direction):
        opposites = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if self.paused or not self.running:
            return
        if player == 1:
            if self.direction1 != opposites[new_direction]:
                self.direction1 = new_direction
        else:
            if self.direction2 != opposites[new_direction]:
                self.direction2 = new_direction

    def go_left_1(self, event): self.change_direction(1, "Left")
    def go_right_1(self, event): self.change_direction(1, "Right")
    def go_up_1(self, event): self.change_direction(1, "Up")
    def go_down_1(self, event): self.change_direction(1, "Down")

    def go_left_2(self, event): self.change_direction(2, "Left")
    def go_right_2(self, event): self.change_direction(2, "Right")
    def go_up_2(self, event): self.change_direction(2, "Up")
    def go_down_2(self, event): self.change_direction(2, "Down")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
