import customtkinter as ctk
from GomokuGame import *
import threading
import winsound
import time

class CustomAlert(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        winsound.MessageBeep()
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        ctk.CTkLabel(self, text=message, font=("Pixelify Sans Bold", 24)).pack(pady=20)

        ctk.CTkButton(
            self,
            text="OK",
            command=self.destroy,
            font=("Pixelify Sans SemiBold", 20),
            fg_color="#FFD600",
            hover_color="#C7AE00",
            text_color="#2D2D2D",
            corner_radius=10
        ).pack(pady=10)

        self.attributes('-topmost', True)
        self.withdraw()
        self.update_idletasks()

        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()

        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.geometry(f"+{x}+{y}")
        self.deiconify()
        self.focus_set()
        self.grab_set()
        self.wait_window()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gomoku")
        self.geometry("1000x700")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        home = HomePage(parent=self.container, controller=self)
        self.frames["HomePage"] = home
        home.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def start_game(self, page_name, board_size, depth_limit):
        if page_name in self.frames:
            self.frames[page_name].destroy()
            del self.frames[page_name]

        if page_name == "PageOne":
            new_frame = PageOne(parent=self.container, controller=self, board_size=board_size, depth_limit=depth_limit)
        elif page_name == "PageTwo":
            new_frame = PageTwo(parent=self.container, controller=self, board_size=board_size, depth_limit=depth_limit)
        else:
            raise ValueError(f"Unknown page_name: {page_name}")

        self.frames[page_name] = new_frame
        new_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(page_name)

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        main_frame = ctk.CTkFrame(self, corner_radius=30)
        main_frame.pack(fill="both", expand=True, pady=20, padx=20)

        title_label = ctk.CTkLabel(
            main_frame, text="Gomoku", font=("Comic Sans MS", 110 , "bold"), text_color="#FFD700"
        )
        title_label.pack(pady=(20, 10))

        section_width = 450

        section1_frame = ctk.CTkFrame(main_frame, corner_radius=15, width=section_width, height=120)
        section1_frame.pack(pady=20)
        section1_frame.pack_propagate(False)

        section1_inner = ctk.CTkFrame(section1_frame, fg_color="transparent")
        section1_inner.pack(expand=True)

        ctk.CTkLabel(section1_inner, text="Board Size ", font=("Anta", 24)).grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.board_size_entry = ctk.CTkEntry(
            section1_inner,
            width=120,
            font=("Anta", 24),
            placeholder_text="5 ~ 19"
        )
        self.board_size_entry.grid(row=0, column=1, padx=10, pady=10)
        self.board_size_entry.insert(0, "6")

        ctk.CTkLabel(section1_inner, text="AI Depth     ", font=("Anta", 24)).grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.depth_entry = ctk.CTkEntry(
            section1_inner,
            width=120,
            font=("Anta", 24),
            placeholder_text="1 ~ 5"
        )
        self.depth_entry.grid(row=1, column=1, padx=10, pady=10)
        self.depth_entry.insert(0, "2")

        section2_frame = ctk.CTkFrame(main_frame, corner_radius=15, width=section_width, height=180)
        section2_frame.pack(pady=10)
        section2_frame.pack_propagate(False)

        btn1 = ctk.CTkButton(
            section2_frame, text="Human VS MiniMax",
            font=("Pixelify Sans SemiBold", 28), corner_radius=10,
            fg_color="#1467C2",
            hover_color="#003DA6",
            width=350, height=60,
            command=lambda: controller.start_game("PageOne", self.get_board_size(), self.get_depth())
        )
        btn1.pack(pady=(20, 10), anchor="center")

        btn2 = ctk.CTkButton(
            section2_frame, text="MiniMax VS Alpha-Beta",
            font=("Pixelify Sans SemiBold", 28), corner_radius=10,
            fg_color="#1467C2",
            hover_color="#003DA6",
            width=350, height=60,
            command=lambda: controller.start_game("PageTwo", self.get_board_size(), self.get_depth())
        )
        btn2.pack(pady=(0, 20), anchor="center")

    def get_board_size(self):
        try:
            size = int(self.board_size_entry.get())
            if size < 5:
                size = 5
            elif size > 19:
                size = 15
        except ValueError:
            size = 6
        return size

    def get_depth(self):
        try:
            d = int(self.depth_entry.get())
            if d < 1:
                d = 1
        except ValueError:
            d = 2
        return d

# Human VS MiniMax
class PageOne(ctk.CTkFrame):
    def __init__(self, parent, controller, board_size=6, cell_size=40, depth_limit=2):
        super().__init__(parent)
        self.controller = controller
        self.board_size = board_size
        self.cell_size = cell_size
        self.depth_limit = depth_limit
        self.canvas_size = (board_size - 1) * cell_size + 2 * cell_size

        self.active = True

        main_frame = ctk.CTkFrame(self , corner_radius=30)
        main_frame.pack(fill="both", expand=True , pady=20 , padx=20)

        section_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=20,
            fg_color="#ffc18c",
            width = self.canvas_size,
            height = self.canvas_size
        )
        section_frame.pack(pady=20, padx=40)
        section_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(pady=20)

        self.gomoku = Gomoku(board_size)
        self.turn = PLAYER

        self.canvas = ctk.CTkCanvas(
            section_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            highlightbackground="black",
            bg="#ffc18c",
            highlightthickness=0
        )
        self.canvas.pack(pady=10 , padx=10)
        self.draw_grid()
        self.draw_all_pieces()

        self.canvas.bind("<Button-1>", self.on_click)

        back_button = ctk.CTkButton(
            btn_container,
            text="Back to Home",
            width=200,
            height=50,
            font=("Pixelify Sans SemiBold", 24),
            fg_color="#FFD600",
            hover_color="#C7AE00",
            text_color="#2D2D2D",
            command=self.on_back
        )
        back_button.pack(side="left", padx=10)

        restart_button = ctk.CTkButton(
            btn_container,
            text="Restart",
            width=200,
            height=50,
            font=("Pixelify Sans SemiBold", 24),
            fg_color="#1467C2",
            hover_color="#003DA6",
            command=self.restart_game
        )
        restart_button.pack(side="left", padx=10)

    def restart_game(self):
        self.active = True

        self.gomoku = Gomoku(self.board_size)
        self.turn = PLAYER

        self.canvas.delete("pieces")
        self.canvas.delete("grid")
        self.draw_grid()
        self.draw_all_pieces()

        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.on_click)

    def on_back(self):
        self.active = False
        self.canvas.unbind("<Button-1>")
        self.controller.show_frame("HomePage")

    def draw_grid(self):
        self.canvas.delete("grid")
        for i in range(self.board_size):
            x = y = self.cell_size + i * self.cell_size
            self.canvas.create_line(x, self.cell_size, x, self.canvas_size - self.cell_size, fill="black", tags="grid" , width=2)
            self.canvas.create_line(self.cell_size, y, self.canvas_size - self.cell_size, y, fill="black", tags="grid" , width=2)

    def draw_piece(self, x, y, color):
        cx = self.cell_size + x * self.cell_size
        cy = self.cell_size + y * self.cell_size
        r = self.cell_size // 2 - 3
        fill = "black" if color == "black" else "white"
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=fill, outline="black", tags="pieces")

    def draw_all_pieces(self):
        self.canvas.delete("pieces")
        for y in range(self.board_size):
            for x in range(self.board_size):
                val = self.gomoku.board[y][x]
                if val == PLAYER:
                    self.draw_piece(x, y, "black")
                elif val == miniMaxAI:
                    self.draw_piece(x, y, "white")

    def on_click(self, event):
        if not self.active or self.turn != PLAYER:
            return

        x = round((event.x - self.cell_size) / self.cell_size)
        y = round((event.y - self.cell_size) / self.cell_size)
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            if self.gomoku.isValidMove(y, x):
                self.gomoku.makeMove(y, x, PLAYER)
                self.draw_all_pieces()
                if self.gomoku.checkWinner(PLAYER):
                    self.after(0, lambda: CustomAlert(self, "Game Over", "You win!"))
                    self.turn = None
                    return
                elif self.gomoku.isDraw():
                    self.after(0, lambda: CustomAlert(self, "Game Over", "Draw!"))
                    self.turn = None
                    return

                self.turn = miniMaxAI
                threading.Thread(target=self.ai_move, daemon=True).start()


    def ai_move(self):
        if not self.active:
            return

        _ , movee = self.gomoku.minimax(depth=0, isMaximizing=True, depthLimit=self.depth_limit)

        if not self.active:
            return

        if movee:
            self.gomoku.makeMove(movee[0], movee[1], miniMaxAI)
        self.draw_all_pieces()
        if self.gomoku.checkWinner(miniMaxAI):
            self.after(0, lambda: CustomAlert(self, "Game Over", "AI wins!"))
            self.turn = None
            return
        elif self.gomoku.isDraw():
            self.after(0, lambda: CustomAlert(self, "Game Over", "Draw!"))
            self.turn = None
            return
        self.turn = PLAYER

# MiniMax vs AlphaBeta
class PageTwo(ctk.CTkFrame):
    def __init__(self, parent, controller, board_size=6, cell_size=40, depth_limit=2):
        super().__init__(parent)
        self.current_ai = None

        self.controller = controller
        self.board_size = board_size
        self.cell_size = cell_size
        self.depth_limit = depth_limit
        self.canvas_size = (board_size - 1) * cell_size + 2 * cell_size

        self.run_id = 0
        self._start_new_game()

        main_frame = ctk.CTkFrame(self, corner_radius=30)
        main_frame.pack(fill="both", expand=True, pady=20, padx=20)

        section_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=20,
            fg_color="#ffc18c",
            width=self.canvas_size,
            height=self.canvas_size
        )
        section_frame.pack(pady=20, padx=40)
        section_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas = ctk.CTkCanvas(
            section_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            highlightbackground="black",
            bg="#ffc18c",
            highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=10)
        self.draw_grid()
        self.draw_all_pieces()

        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(pady=20)

        back_button = ctk.CTkButton(
            btn_container,
            text="Back to Home",
            width=200,
            height=50,
            font=("Pixelify Sans SemiBold", 24),
            fg_color="#FFD600",
            hover_color="#C7AE00",
            text_color="#2D2D2D",
            command=self.on_back
        )
        back_button.pack(side="left", padx=10)

        restart_button = ctk.CTkButton(
            btn_container,
            text="Restart",
            width=200,
            height=50,
            font=("Pixelify Sans SemiBold", 24),
            fg_color="#1467C2",
            hover_color="#003DA6",
            command=self.restart_game
        )
        restart_button.pack(side="left", padx=10)

        threading.Thread(target=self.ai_vs_ai_loop, args=(self.run_id,), daemon=True).start()

    def _start_new_game(self):
        self.run_id += 1
        self.gomoku = Gomoku(self.board_size)
        self.current_ai = miniMaxAI

    def restart_game(self):
        self._start_new_game()

        self.canvas.delete("pieces")
        self.canvas.delete("grid")
        self.draw_grid()
        self.draw_all_pieces()

        threading.Thread(target=self.ai_vs_ai_loop, args=(self.run_id,), daemon=True).start()

    def on_back(self):
        self.run_id += 1
        self.controller.show_frame("HomePage")

    def draw_grid(self):
        self.canvas.delete("grid")
        for i in range(self.board_size):
            x = y = self.cell_size + i * self.cell_size
            self.canvas.create_line(x, self.cell_size, x, self.canvas_size - self.cell_size,
                                     fill="black", tags="grid", width=2)
            self.canvas.create_line(self.cell_size, y, self.canvas_size - self.cell_size, y,
                                     fill="black", tags="grid", width=2)

    def draw_piece(self, x, y, color):
        cx = self.cell_size + x * self.cell_size
        cy = self.cell_size + y * self.cell_size
        r = self.cell_size // 2 - 3
        fill = "white" if color == "white" else "black"
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                 fill=fill, outline="black", tags="pieces")

    def draw_all_pieces(self):
        self.canvas.delete("pieces")
        for y in range(self.board_size):
            for x in range(self.board_size):
                val = self.gomoku.board[y][x]
                if val == miniMaxAI:
                    self.draw_piece(x, y, "black")
                elif val == AlphaBetaAI:
                    self.draw_piece(x, y, "white")

    def ai_vs_ai_loop(self, run_id):
        while self.run_id == run_id:
            if self.gomoku.isDraw():
                self.after(0, lambda: CustomAlert(self, "Game Over", "Draw!"))
                break

            if self.current_ai == miniMaxAI:
                _, movee = self.gomoku.minimax(0, True, self.depth_limit)
                ai_player = miniMaxAI
                tagg = "Minimax AI"
            else:
                _, movee = self.gomoku.alphaBeta(self.depth_limit, True)
                ai_player = AlphaBetaAI
                tagg = "AlphaBeta AI"

            if self.run_id != run_id:
                break

            if movee:
                self.gomoku.makeMove(movee[0], movee[1], ai_player)
                self.after(0, self.draw_all_pieces)
                if self.gomoku.checkWinner(ai_player):
                    self.after(0, lambda: CustomAlert(self, "Game Over", f"{tagg} wins!"))
                    break

            self.current_ai = AlphaBetaAI if self.current_ai == miniMaxAI else miniMaxAI
            time.sleep(0.5)

if __name__ == "__main__":
    app = App()
    app.mainloop()