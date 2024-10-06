import pygame
import assets
from game import Game
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def load_map(level):
    list_map = []  # Khởi tạo danh sách rỗng để lưu ma trận

    path = f"levels\\{level}.txt"  # Tạo đường dẫn đến file level

    if not os.path.exists(path):  # Kiểm tra xem file có tồn tại không
        print(f"Thư mục {path} không tồn tại.")  # Thông báo nếu file không tồn tại
        return
    else:
        with open(path, "r") as file:  # Mở file để đọc
            for line in file:  # Duyệt qua từng dòng trong file
                # Loại bỏ ký tự xuống dòng '\n' và giữ lại các ký tự khác (bao gồm cả khoảng trắng)
                row = [char for char in line.rstrip('\n')]
                list_map.append(row)  # Thêm dòng đã xử lý vào danh sách

    return list_map  # Trả về danh sách chứa ma trận của level

def start_game():
    select_level = combobox.get().lower().replace(" ", "")
    if select_level == "chooselevel":
        messagebox.showinfo("Choose a level", "Please choose a level")
        return

    matrix = load_map(select_level)

    # Tải các sprite từ assets
    assets.load_sprites()

    # Khởi tạo pygame và tạo đối tượng LayeredUpdates cho các sprite
    pygame.init()
    sprites = pygame.sprite.LayeredUpdates()

    # Đặt tiêu đề cho cửa sổ trò chơi
    pygame.display.set_caption("Sokoban")

    # Khởi tạo đối tượng Game với ma trận đã tạo
    gameSokoban = Game(matrix)

    # Tính toán kích thước màn hình và tạo cửa sổ
    size = gameSokoban.load_size()
    screen = pygame.display.set_mode(size)

    # Fill floor vào cửa sổ vừa tạo
    Game.fill_screen_with_floor(size, screen)

    # Biến running
    running = True

    # Vòng lặp chính của trò chơi
    while running:
        # Vẽ trò chơi lên màn hình
        gameSokoban.print_game(screen)

        # Cập nhật màn hình
        pygame.display.flip()

        # Xử lý các sự kiện từ pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ
                running = False  # Kết thúc vòng lặp

    # Thoát khỏi pygame khi trò chơi kết thúc
    pygame.quit()

root = tk.Tk()
root.title("My Sokoban")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width // 2 - 500 // 2
y = screen_height // 2 - 300 // 2
root.geometry(f"500x300+{x}+{y}")

def load_img_map():
    select_level = combobox.get().lower().replace(" ", "")
    img_path = f"img_map\\{select_level}.png"
    try:
        img = Image.open(img_path)
        img = img.resize((250, 200))
        img_tk = ImageTk.PhotoImage(img)

        image_label.config(image=img_tk)
        image_label.image = img_tk
    except FileNotFoundError:
        print(f"Không tìm thấy file {img_path}")

label = tk.Label(root, text="Select Level:", font=("Arial", 14))
label.grid(row=0, column=0, padx=10, pady=10)

options = ['Choose Level', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 9', 'Level 10']
combobox = ttk.Combobox(root, values=options, width=13, font=("Arial", 12))
combobox.current(0)
combobox.grid(row=0, column=1, padx=10, pady=10)

button_start = tk.Button(root, text="Start", command=start_game, font=("Arial", 10), width=12)
button_start.grid(row=0, column=2, padx=10, pady=10)

img_path_default = f"img_map\\chooselevel.png"
try:
    img = Image.open(img_path_default)
    img = img.resize((250, 200))
    img_tk = ImageTk.PhotoImage(img)
except FileNotFoundError:
    print(f"Không tìm thấy file {img_path_default}")
image_label = tk.Label(root, image=img_tk)
image_label.grid(row=1, rowspan=2, column=0, columnspan=2, padx=10, pady=10)

button_bfs = tk.Button(root, text="Solve with\n BFS", command="", font=("Arial", 10), width=12, height=4)
button_bfs.grid(row=1, column=2, padx=10, pady=10)

button_dfs = tk.Button(root, text="Solve with\n DFS", command="", font=("Arial", 10), width=12, height=4)
button_dfs.grid(row=2, column=2, padx=10, pady=10)

combobox.bind("<<ComboboxSelected>>", lambda event: load_img_map())

root.mainloop()