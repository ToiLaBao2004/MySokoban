import pygame
import assets
from game import Game
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Hàm để tải bản đồ (ma trận) của level được chọn
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

# Hàm hiển thị cảnh báo "deadlock" bằng pygame
def show_deadlock_warning(screen):
    font = pygame.font.SysFont("Arial", 24)
    warning_text = font.render("You're stuck! Press 'Z' to undo.", True, (255, 0, 0))  # Text màu đỏ
    text_rect = warning_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Đặt ở giữa màn hình
    screen.blit(warning_text, text_rect)
    pygame.display.flip()

# Hàm hiển thị cảnh báo "You Win!" bằng pygame
def show_win_game(screen):
    font = pygame.font.SysFont("Arial", 36)
    win_text = font.render("You Win!", True, (0, 255, 0))  # Text màu xanh lá cây
    text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Đặt ở giữa màn hình
    screen.blit(win_text, text_rect)
    pygame.display.flip()

# Hàm khởi động trò chơi
def start_game():
    select_level = combobox.get().lower().replace(" ", "")  # Lấy level được chọn từ combobox
    if select_level == "chooselevel":  # Kiểm tra nếu chưa chọn level
        messagebox.showinfo("Choose a level", "Please choose a level")  # Hiển thị thông báo yêu cầu chọn level
        return

    matrix = load_map(select_level)  # Tải ma trận của level được chọn

    # Tải các sprite từ assets
    assets.load_sprites()

    # Khởi tạo pygame và tạo đối tượng LayeredUpdates cho các sprite
    pygame.init()
    sprites = pygame.sprite.LayeredUpdates()

    # Đặt tiêu đề cho cửa sổ trò chơi
    pygame.display.set_caption("Sokoban")

    # Khởi tạo đối tượng Game với ma trận đã tạo
    gameSokoban = Game(matrix, [])

    # Tính toán kích thước màn hình và tạo cửa sổ
    size = gameSokoban.load_size()
    screen = pygame.display.set_mode(size)

    # Điền nền sàn vào cửa sổ vừa tạo
    Game.fill_screen_with_floor(size, screen)

    # Biến điều kiện vòng lặp chạy trò chơi
    running = True
    list_dock = gameSokoban.listDock()

    # Vòng lặp chính của trò chơi
    while running:
        # Vẽ trò chơi lên màn hình
        gameSokoban.fill_screen_with_floor(size, screen)
        gameSokoban.print_game(screen)

        # Cập nhật màn hình
        pygame.display.flip()

        # Xử lý các sự kiện từ pygame
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if gameSokoban.stack_matrix:  # Kiểm tra nếu có bước trước đó để quay lại
                        prev_matrix = gameSokoban.stack_matrix.pop()  # Lấy ma trận trước đó
                        gameSokoban.matrix = prev_matrix  # Cập nhật ma trận
                elif event.key == pygame.K_UP:
                    gameSokoban.move(-1, 0, list_dock)  # Di chuyển lên
                elif event.key == pygame.K_DOWN:
                    gameSokoban.move(1, 0, list_dock)  # Di chuyển xuống
                elif event.key == pygame.K_LEFT:
                    gameSokoban.move(0, -1, list_dock)  # Di chuyển sang trái
                elif event.key == pygame.K_RIGHT:
                    gameSokoban.move(0, 1, list_dock)  # Di chuyển sang phải
            if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ
                running = False  # Kết thúc vòng lặp

        # Kiểm tra deadlock sau mỗi lần di chuyển
        if gameSokoban.check_all_boxes_for_deadlock():
            show_deadlock_warning(screen)  # Hiển thị cảnh báo deadlock

        gameSokoban.print_game(screen)
        pygame.display.update()

        # Kiểm tra xem người chơi đã hoàn thành trò chơi chưa
        if gameSokoban.is_completed(list_dock):
            show_win_game(screen)


    # Thoát khỏi pygame khi trò chơi kết thúc
    pygame.quit()

# Khởi tạo giao diện Tkinter
root = tk.Tk()
root.title("My Sokoban")

# Lấy kích thước màn hình và đặt vị trí của cửa sổ giữa màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width // 2 - 500 // 2
y = screen_height // 2 - 300 // 2
root.geometry(f"500x300+{x}+{y}")

# Đặt weight cho các hàng và cột để chúng có thể mở rộng
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Hàm để tải hình ảnh của bản đồ dựa vào level được chọn
def load_img_map():
    select_level = combobox.get().lower().replace(" ", "")  # Lấy level được chọn từ combobox
    img_path = f"img_map\\{select_level}.png"  # Tạo đường dẫn đến hình ảnh bản đồ
    try:
        img = Image.open(img_path)  # Mở hình ảnh
        img = img.resize((250, 200))  # Thay đổi kích thước hình ảnh
        img_tk = ImageTk.PhotoImage(img)  # Tạo đối tượng PhotoImage từ hình ảnh đã thay đổi kích thước

        image_label.config(image=img_tk)  # Hiển thị hình ảnh lên label
        image_label.image = img_tk  # Giữ tham chiếu đến hình ảnh để không bị thu hồi bộ nhớ
    except FileNotFoundError:
        print(f"Không tìm thấy file {img_path}")  # Thông báo nếu không tìm thấy hình ảnh

# Tạo và đặt các widget cho giao diện Tkinter
label = tk.Label(root, text="Select Level:", font=("Arial", 14))
label.grid(row=0, column=0, padx=10, pady=10)

# Tạo combobox để chọn level
options = ['Choose Level', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5',
           'Level 6', 'Level 7', 'Level 8', 'Level 9', 'Level 10']
combobox = ttk.Combobox(root, values=options, width=13, font=("Arial", 12))
combobox.current(0)
combobox.grid(row=0, column=1, padx=10, pady=10)

# Nút bắt đầu trò chơi
button_start = tk.Button(root, text="Start", command=start_game, font=("Arial", 10), width=12)
button_start.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Hiển thị hình ảnh bản đồ mặc định khi chưa chọn level
img_path_default = f"img_map\\chooselevel.png"
try:
    img = Image.open(img_path_default)  # Mở hình ảnh mặc định
    img = img.resize((250, 200))  # Thay đổi kích thước hình ảnh
    img_tk = ImageTk.PhotoImage(img)  # Tạo đối tượng PhotoImage từ hình ảnh đã thay đổi kích thước
except FileNotFoundError:
    print(f"Không tìm thấy file {img_path_default}")

image_label = tk.Label(root, image=img_tk)  # Hiển thị hình ảnh mặc định lên label
image_label.grid(row=1, rowspan=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Nút giải bài bằng thuật toán BFS
button_bfs = tk.Button(root, text="Solve with\n BFS", command="", font=("Arial", 10), width=12, height=4)
button_bfs.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# Nút giải bài bằng thuật toán DFS
button_dfs = tk.Button(root, text="Solve with\n DFS", command="", font=("Arial", 10), width=12, height=4)
button_dfs.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

# Sự kiện khi người dùng chọn level trong combobox, sẽ tải bản đồ hình ảnh
combobox.bind("<<ComboboxSelected>>", lambda event: load_img_map())

# Bắt đầu vòng lặp giao diện Tkinter
root.mainloop()