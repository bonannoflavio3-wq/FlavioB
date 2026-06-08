import tkinter as tk
import random

# Paramètres du jeu
largeur = 1000
hauteur = 500
SPACE_SIZE = 20

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu Snake")
        self.root.resizable(False, False)

        self.score = 0
        self.running = True
        self.paused = False
        self.direction = 'Right'

        self.label = tk.Label(root, text=f"Score : {self.score}", font=('Arial', 14))
        self.label.pack()

        self.canvas = tk.Canvas(root, bg="black", width=largeur, height=hauteur)
        self.canvas.pack()

        self.pause_button = tk.Button(root, text="Pause", font=('Arial', 12), command=self.toggle_pause)
        self.pause_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Quitter", font=('Arial', 12), command=root.quit)
        self.quit_button.pack(pady=5)

        self.replay_button = tk.Button(root, text="Rejouer", font=('Arial', 20), command=self.restart_game)

        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.snake_squares = []
        for x, y in self.snake:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="yellow")
            self.snake_squares.append(square)

        self.food = self.create_food()

        self.root.bind("<Left>", self.go_left)
        self.root.bind("<Right>", self.go_right)
        self.root.bind("<Up>", self.go_up)
        self.root.bind("<Down>", self.go_down)

        self.next_turn()

    def create_food(self):
        while True:
            x = random.randint(0, (largeur - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            y = random.randint(0, (hauteur - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            if [x, y] not in self.snake:
                break
        return self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red")
    
    def next_turn(self):
        if not self.running:
            return

        if self.paused:
            self.root.after(100, self.next_turn)
            return
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= SPACE_SIZE
        elif self.direction == "Down":
            head_y += SPACE_SIZE
        elif self.direction == "Left":
            head_x -= SPACE_SIZE
        elif self.direction == "Right":
            head_x += SPACE_SIZE

        head_x %= largeur
        head_y %= hauteur

        new_head = [head_x, head_y]

        if self.check_collision(new_head):
            self.game_over()
            return

        self.snake.insert(0, new_head)
        square = self.canvas.create_rectangle(head_x, head_y, head_x + SPACE_SIZE, head_y + SPACE_SIZE, fill="yellow")
        self.snake_squares.insert(0, square)

        food_coords = self.canvas.coords(self.food)
        if head_x == int(food_coords[0]) and head_y == int(food_coords[1]):
            self.score += 1
            self.label.config(text=f"Score : {self.score}")
            self.canvas.delete(self.food)
            self.food = self.create_food()
        else:
            self.canvas.delete(self.snake_squares.pop())
            self.snake.pop()

        self.root.after(100, self.next_turn)

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Reprendre" if self.paused else "Pause")

    def check_collision(self, head):
        return head in self.snake[1:]

    def game_over(self):
        self.running = False
        self.canvas.create_text(largeur / 2, hauteur / 2, text="Game Over", fill="red", font=("Arial", 32))
        self.replay_button.pack(pady=5)

    def restart_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.label.config(text=f"Score : {self.score}")
        self.direction = 'Right'
        self.running = True
        self.paused = False

        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.snake_squares = []

        for x, y in self.snake:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="yellow")
            self.snake_squares.append(square)

        self.food = self.create_food()
        self.replay_button.pack_forget()
        self.next_turn()

    def change_direction(self, new_direction):
        opposites = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if not self.paused and self.running and self.direction != opposites[new_direction]:
            self.direction = new_direction

    def go_left(self, event): self.change_direction("Left")
    def go_right(self, event): self.change_direction("Right")
    def go_up(self, event): self.change_direction("Up")
    def go_down(self, event): self.change_direction("Down")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
