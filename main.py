import time
import pygame
import assets
from game import Game
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from solver import bfs, dfs, astar, Solve

def load_map(level):
    list_map = []
    path = f"levels\\{level}.txt"
    if not os.path.exists(path):
        print(f"Thư mục {path} không tồn tại.")
        return
    else:
        with open(path, "r") as file:
            for line in file:
                row = [char for char in line.rstrip('\n')]
                list_map.append(row)
    return list_map

def show_deadlock_warning(screen):
    font = pygame.font.SysFont("Arial", 24)
    warning_text = font.render("You're stuck! Press 'Z' to undo.", True, (255, 0, 0))
    text_rect = warning_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(warning_text, text_rect)
    pygame.display.flip()

def show_win_game(screen):
    font = pygame.font.SysFont("Arial", 36)
    win_text = font.render("You Win!", True, (0, 255, 0))
    text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(win_text, text_rect)
    pygame.display.flip()

def start_game():
    select_level = combobox.get().lower().replace(" ", "")
    if select_level == "chooselevel":
        messagebox.showinfo("Choose a level", "Please choose a level")
        return

    matrix = load_map(select_level)

    assets.load_sprites()

    pygame.init()
    sprites = pygame.sprite.LayeredUpdates()

    pygame.display.set_caption("Sokoban")

    gameSokoban = Game(matrix, [])

    size = gameSokoban.load_size()
    screen = pygame.display.set_mode(size)

    Game.fill_screen_with_floor(size, screen)

    running = True
    list_dock = gameSokoban.listDock()

    machinePlay = False
    path = ""
    solve = Solve(matrix)
    lenPath = 0
    i = 0

    while running:
        gameSokoban.fill_screen_with_floor(size, screen)
        gameSokoban.print_game(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if gameSokoban.stack_matrix:
                        prev_matrix = gameSokoban.stack_matrix.pop()
                        gameSokoban.matrix = prev_matrix
                elif event.key == pygame.K_UP:
                    gameSokoban.move(-1, 0, list_dock)
                elif event.key == pygame.K_DOWN:
                    gameSokoban.move(1, 0, list_dock)
                elif event.key == pygame.K_LEFT:
                    gameSokoban.move(0, -1, list_dock)
                elif event.key == pygame.K_RIGHT:
                    gameSokoban.move(0, 1, list_dock)
                elif event.key == pygame.K_b:
                    solve.matrix = gameSokoban.matrix
                    path = bfs(solve)
                    lenPath = len(path)
                    machinePlay = True
                elif event.key == pygame.K_d:
                    solve.matrix = gameSokoban.matrix
                    path = dfs(solve)
                    lenPath = len(path)
                    machinePlay = True
                elif event.key ==pygame.K_a:
                    solve.matrix=gameSokoban.matrix
                    path=astar(solve)
                    lenPath=len(path)
                    machinePlay= True
            if event.type == pygame.QUIT:
                running = False

        if machinePlay:
            if i == lenPath:
                machinePlay = False
            elif i < lenPath:
                move = path[i]
                if move == 'U':
                    solve.move(-1, 0)
                elif move == 'D':
                    solve.move(1, 0)
                elif move == 'L':
                    solve.move(0, -1)
                elif move == 'R':
                    solve.move(0, 1)
            i += 1
            time.sleep(0.1)

        if not machinePlay:
            if gameSokoban.check_all_boxes_for_deadlock():
                show_deadlock_warning(screen)

        gameSokoban.print_game(screen)
        pygame.display.update()

        if gameSokoban.is_completed(list_dock):
            show_win_game(screen)

    pygame.quit()



root = tk.Tk()
root.title("My Sokoban")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width // 2 - 500 // 2
y = screen_height // 2 - 300 // 2
root.geometry(f"500x300+{x}+{y}")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

img_tk_level = None

def load_img_map():
    global img_tk_level  # Khai báo img_tk_level là biến toàn cục
    select_level = combobox.get().lower().replace(" ", "")
    img_path = f"img_map\\{select_level}.png"
    try:
        imageLevel = Image.open(img_path)
        imageLevel = imageLevel.resize((250, 200))
        img_tk_level = ImageTk.PhotoImage(imageLevel)

        image_label.config(image=img_tk_level)
        image_label.image = img_tk_level
    except FileNotFoundError:
        print(f"Không tìm thấy file {img_path}")

label = tk.Label(root, text="Select Level:", font=("Arial", 14))
label.grid(row=0, column=0, padx=10, pady=10)

options = ['Choose Level', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5',
           'Level 6', 'Level 7', 'Level 8', 'Level 9', 'Level 10']
combobox = ttk.Combobox(root, values=options, width=13, font=("Arial", 12))
combobox.current(0)
combobox.grid(row=0, column=1, padx=10, pady=10)

button_start = tk.Button(root, text="Start", command=start_game, font=("Arial", 10), width=12)
button_start.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

img_tk = None

img_path_default = f"img_map\\chooselevel.png"
try:
    img = Image.open(img_path_default)
    img = img.resize((250, 200))
    img_tk = ImageTk.PhotoImage(img)
except FileNotFoundError:
    print(f"Không tìm thấy file {img_path_default}")

image_label = tk.Label(root, image=img_tk)
image_label.grid(row=1, rowspan=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

combobox.bind("<<ComboboxSelected>>", lambda event: load_img_map())

root.mainloop()