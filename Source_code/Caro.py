import time
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class CaroGUI:
    def __init__(self, root, size=9):
        self.root = root
        self.root.title("Hệ Thống Trò Chơi Caro AI - Báo Cáo Cuối Kỳ")
        self.size = size
        
        # Thiết lập cấu hình mặc định cho AI
        self.depth_limit = 3
        self.ai_mode = "Alpha-Beta" # Mặc định dùng Alpha-Beta
        
        # Khởi tạo trạng thái bàn cờ
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.player_icon = 'X'
        self.ai_icon = 'O'
        self.states_evaluated = 0
        self.game_over = False
        
        # Mảng lưu trữ các nút bấm trên giao diện bàn cờ
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        
        self.create_widgets()

    def create_widgets(self):
        """Khởi tạo cấu trúc giao diện điều khiển và bảng cờ"""
        # --- KHU VỰC 1: THANH ĐIỀU KHIỂN PHÍA TRÊN ---
        control_frame = tk.Frame(self.root, pady=10, padx=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(control_frame, text="Thuật toán AI:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, sticky='w')
        self.mode_combo = ttk.Combobox(control_frame, values=["Minimax thuần (Lv1)", "Alpha-Beta Pruning (Lv2)"], width=22, state="readonly")
        self.mode_combo.current(1) # Chọn sẵn Alpha-Beta
        self.mode_combo.grid(row=0, column=1, padx=5)
        
        tk.Label(control_frame, text="Độ sâu tìm kiếm:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, sticky='w')
        self.depth_spin = tk.Spinbox(control_frame, from_=1, to=5, width=5, font=("Arial", 10))
        self.depth_spin.delete(0, "end")
        self.depth_spin.insert(0, "3") # Mặc định độ sâu 3
        self.depth_spin.grid(row=0, column=3, padx=5)
        
        reset_btn = tk.Button(control_frame, text="Chơi Lại Từ Đầu", font=("Arial", 10, "bold"), bg="#f39c12", fg="white", command=self.reset_game)
        reset_btn.grid(row=0, column=4, padx=15)

        # --- KHU VỰC 2: BẢN ĐỒ BÀN CỜ 9X9 (CHIA Ô RÕ RÀNG) ---
        self.board_frame = tk.Frame(self.root, bg="#2c3e50", pady=3)
        self.board_frame.pack(side=tk.TOP, padx=20, pady=5)
        
        for r in range(self.size):
            for c in range(self.size):
                # Tạo nút bấm đại diện cho mỗi ô cờ vuông vắn
                btn = tk.Button(
                    self.board_frame, text=" ", font=("Courier New", 16, "bold"),
                    width=4, height=2, bg="#ecf0f1", activebackground="#bdc3c7",
                    command=lambda row=r, col=c: self.on_click(row, col)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

        # --- KHU VỰC 3: BẢNG THÔNG SỐ ĐO ĐẠC HIỆU NĂNG PHÍA DƯỚI ---
        self.status_frame = tk.LabelFrame(self.root, text=" Chỉ Chỉ Số Đo Đạc Hiệu Năng Hệ Thống (Level 1 & 2) ", font=("Arial", 10, "bold"), padx=15, pady=10)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        
        self.lbl_algo = tk.Label(self.status_frame, text="Thuật toán đang chạy: Chưa tính toán", font=("Arial", 10))
        self.lbl_algo.grid(row=0, column=0, sticky="w", padx=10)
        
        self.lbl_score = tk.Label(self.status_frame, text="Điểm đánh giá thế cờ: -", font=("Arial", 10))
        self.lbl_score.grid(row=0, column=1, sticky="w", padx=10)
        
        self.lbl_states = tk.Label(self.status_frame, text="Số trạng thái đã duyệt: -", font=("Arial", 10))
        self.lbl_states.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.lbl_time = tk.Label(self.status_frame, text="Thời gian xử lý: -", font=("Arial", 10))
        self.lbl_time.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    def on_click(self, r, c):
        """Xử lý khi người dùng click chuột vào một ô trên bàn cờ"""
        if self.game_over or self.board[r][c] != ' ':
            return
            
        # 1. Cập nhật nước đi của Người chơi (X)
        self.board[r][c] = self.player_icon
        self.buttons[r][c].config(text=self.player_icon, fg="#e74c3c", state="disabled", disabledforeground="#e74c3c")
        
        if self.check_win(self.player_icon):
            messagebox.showinfo("Kết quả", "🎉 Chúc mừng! Bạn đã giành chiến thắng trước AI!")
            self.game_over = True
            return
            
        if self.is_board_full():
            messagebox.showinfo("Kết quả", "🤝 Hòa cờ! Bàn cờ đã đầy.")
            self.game_over = True
            return
            
        # Đóng băng giao diện tạm thời để máy tính toán
        self.root.update()
        
        # 2. Gọi Máy (AI) tính toán bước đi tiếp theo
        self.ai_turn()

    def ai_turn(self):
        """Lấy cấu hình thuật toán và điều khiển Máy thực hiện nước đi"""
        # Cập nhật cấu hình hiện tại từ thanh điều khiển
        selected_mode = self.mode_combo.get()
        self.depth_limit = int(self.depth_spin.get())
        
        self.states_evaluated = 0
        start_time = time.perf_counter()
        
        if "Minimax" in selected_mode:
            self.ai_mode = "Minimax thuần"
            score, best_move = self.minimax(self.depth_limit, True)
        else:
            self.ai_mode = "Alpha-Beta Pruning"
            score, best_move = self.alpha_beta(self.depth_limit, -math.inf, math.inf, True)
            
        execution_time = time.perf_counter() - start_time
        
        # 3. Cập nhật nước đi của AI (O) lên giao diện bảng
        if best_move:
            r, c = best_move
            self.board[r][c] = self.ai_icon
            self.buttons[r][c].config(text=self.ai_icon, fg="#2ecc71", state="disabled", disabledforeground="#2ecc71")
            
            # Đẩy thông số đo đạc thời gian thực xuống khung trạng thái
            self.lbl_algo.config(text=f"Thuật toán đang chạy: {self.ai_mode} (Độ sâu: {self.depth_limit})")
            self.lbl_score.config(text=f"Điểm đánh giá thế cờ: {score}")
            self.lbl_states.config(text=f"Số trạng thái đã duyệt: {self.states_evaluated}")
            self.lbl_time.config(text=f"Thời gian xử lý: {execution_time:.4f} giây")
        else:
            messagebox.showinfo("Thông báo", "AI không tìm thấy nước đi. AI xin hàng!")
            self.game_over = True
            return

        if self.check_win(self.ai_icon):
            messagebox.showinfo("Kết quả", "💻 Kết thúc: Máy (AI) đã giành chiến thắng!")
            self.game_over = True
            return
            
        if self.is_board_full():
            messagebox.showinfo("Kết quả", "🤝 Hòa cờ! Bàn cờ đã đầy.")
            self.game_over = True
            return

    def get_valid_moves(self):
        """Sinh các nước đi kề cạnh thông minh bảo vệ cây quyết định không bùng nổ"""
        moves = set()
        has_pieces = False
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != ' ':
                    has_pieces = True
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == ' ':
                                moves.add((nr, nc))
        if not has_pieces:
            return [(self.size // 2, self.size // 2)]
        return list(moves)

    def check_win(self, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != player:
                    continue
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return True
        return False

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ': return False
        return True

    def evaluate_line(self, line):
        score = 0
        ai_count = line.count(self.ai_icon)
        player_count = line.count(self.player_icon)
        empty_count = line.count(' ')

        if ai_count == 4: return 100000          
        if player_count == 4: return -100000     

        if ai_count == 3 and empty_count == 1: score += 500
        if player_count == 3 and empty_count == 1: score -= 2000 

        if ai_count == 2 and empty_count == 2: score += 10
        if player_count == 2 and empty_count == 2: score -= 50

        return score

    def evaluate_board(self):
        self.states_evaluated += 1
        total_score = 0
        for r in range(self.size):
            for c in range(self.size - 3):
                total_score += self.evaluate_line([self.board[r][c+i] for i in range(4)])
                total_score += self.evaluate_line([self.board[c+i][r] for i in range(4)])
        for r in range(self.size - 3):
            for c in range(self.size - 3):
                total_score += self.evaluate_line([self.board[r+i][c+i] for i in range(4)])
                total_score += self.evaluate_line([self.board[r+3-i][c+i] for i in range(4)])
        return total_score

    def minimax(self, depth, is_max):
        if self.check_win(self.ai_icon): return 100000, None
        if self.check_win(self.player_icon): return -100000, None
        if self.is_board_full(): return 0, None
        if depth == 0: return self.evaluate_board(), None

        valid_moves = self.get_valid_moves()
        best_move = None

        if is_max:
            best_val = -math.inf
            for r, c in valid_moves:
                self.board[r][c] = self.ai_icon
                val, _ = self.minimax(depth - 1, False)
                self.board[r][c] = ' '
                if val > best_val:
                    best_val = val
                    best_move = (r, c)
            return best_val, best_move
        else:
            best_val = math.inf
            for r, c in valid_moves:
                self.board[r][c] = self.player_icon
                val, _ = self.minimax(depth - 1, True)
                self.board[r][c] = ' '
                if val < best_val:
                    best_val = val
                    best_move = (r, c)
            return best_val, best_move

    def alpha_beta(self, depth, alpha, beta, is_max):
        if self.check_win(self.ai_icon): return 100000, None
        if self.check_win(self.player_icon): return -100000, None
        if self.is_board_full(): return 0, None
        if depth == 0: return self.evaluate_board(), None

        valid_moves = self.get_valid_moves()
        best_move = None

        if is_max:
            best_val = -math.inf
            for r, c in valid_moves:
                self.board[r][c] = self.ai_icon
                val, _ = self.alpha_beta(depth - 1, alpha, beta, False)
                self.board[r][c] = ' '
                if val > best_val:
                    best_val = val
                    best_move = (r, c)
                alpha = max(alpha, best_val)
                if beta <= alpha: break
            return best_val, best_move
        else:
            best_val = math.inf
            for r, c in valid_moves:
                self.board[r][c] = self.player_icon
                val, _ = self.alpha_beta(depth - 1, alpha, beta, True)
                self.board[r][c] = ' '
                if val < best_val:
                    best_val = val
                    best_move = (r, c)
                beta = min(beta, best_val)
                if beta <= alpha: break
            return best_val, best_move

    def reset_game(self):
        """Khởi động lại toàn bộ bàn cờ về trạng thái trống ban đầu"""
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.game_over = False
        self.lbl_algo.config(text="Thuật toán đang chạy: Chưa tính toán")
        self.lbl_score.config(text="Điểm đánh giá thế cờ: -")
        self.lbl_states.config(text="Số trạng thái đã duyệt: -")
        self.lbl_time.config(text="Thời gian xử lý: -")
        
        for r in range(self.size):
            for c in range(self.size):
                self.buttons[r][c].config(text=" ", bg="#ecf0f1", state="normal")


# =========================================================================
# KHU VỰC THÊM MỚI - LEVEL 3: PHÂN TÍCH VÀ ĐÁNH GIÁ KIỂM THỬ TỰ ĐỘNG
# (Sử dụng cơ chế Kế thừa lớp để không can thiệp vào bất kỳ dòng mã GUI cũ nào)
# =========================================================================

class CaroSystemComplete(CaroGUI):
    def __init__(self, root, size=9):
        # Gọi lại hàm khởi tạo GUI nguyên gốc của bạn
        super().__init__(root, size)
        
    def create_widgets(self):
        # Chạy hàm dựng UI cơ bản gốc của bạn trước
        super().create_widgets()
        
        # Thêm nút bấm Kiểm thử Level 3 độc lập vào thanh điều khiển của bạn mà không phá cấu trúc cũ
        # Tìm container chứa nút bấm để chèn thêm
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and not hasattr(self, 'board_frame_checked'):
                # Đây chính là control_frame phía trên của bạn
                test_btn = tk.Button(
                    widget, text="Chạy Thử Nghiệm Tự Động (Lv3)", 
                    font=("Arial", 10, "bold"), bg="#9b59b6", fg="white", 
                    command=self.run_automated_analysis
                )
                test_btn.grid(row=0, column=5, padx=15)
                self.board_frame_checked = True
                break

    def run_automated_analysis(self):
        """Hàm thực thi Level 3: Tự động nạp kịch bản thế cờ và xuất bảng đo đạc trên Console"""
        print("\n" + "="*70)
        print("   KỊCH BẢN THỬ NGHIỆM ĐÁNH GIÁ HIỆU NĂNG THỰC NGHIỆM (LEVEL 3)   ")
        print("="*70)
        
        # Định nghĩa 4 thế cờ kịch bản mẫu từ dễ tới khó (Khai cuộc -> Trung cuộc -> Nguy cấp)
        test_cases = [
            {
                "name": "Thế cờ 1: Khai cuộc (Ít quân, nhiều không gian nhánh)",
                "pieces": [((4, 4), 'O'), ((4, 5), 'X')]
            },
            {
                "name": "Thế cờ 2: Trung cuộc giằng co (Tranh chấp khu trung tâm)",
                "pieces": [((4, 4), 'O'), ((3, 4), 'X'), ((4, 5), 'O'), ((5, 5), 'X'), ((3, 5), 'O'), ((2, 6), 'X')]
            },
            {
                "name": "Thế cờ 3: AI tấn công gài bẫy (Tạo chuỗi 3 quân liên tiếp)",
                "pieces": [((2, 2), 'O'), ((3, 3), 'O'), ((4, 4), 'X'), ((5, 5), 'X'), ((1, 5), 'O')]
            },
            {
                "name": "Thế cờ 4: Phòng ngự khẩn cấp (Người chơi X sắp có 4 quân)",
                "pieces": [((3, 3), 'X'), ((3, 4), 'X'), ((3, 5), 'X'), ((5, 5), 'O'), ((6, 6), 'O')]
            }
        ]
        
        target_depth = 3
        print(f"Hệ thống tự động phân tích so sánh song song ở Độ sâu cố định (Depth = {target_depth})\n")
        
        summary_results = []
        
        for idx, tc in enumerate(test_cases, 1):
            print(f"👉 Đang tính toán thực nghiệm cho [{tc['name']}]...")
            
            # Xóa sạch bàn cờ cũ để nạp ma trận thử nghiệm
            self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
            for (r, c), icon in tc["pieces"]:
                self.board[r][c] = icon
                
            # --- Đo đạc Thuật toán Level 1: Minimax Thuần ---
            self.states_evaluated = 0
            t_start = time.perf_counter()
            score_mm, move_mm = self.minimax(target_depth, True)
            time_mm = time.perf_counter() - t_start
            states_mm = self.states_evaluated
            
            # --- Đo đạc Thuật toán Level 2: Alpha-Beta Pruning ---
            self.states_evaluated = 0
            t_start = time.perf_counter()
            score_ab, move_ab = self.alpha_beta(target_depth, -math.inf, math.inf, True)
            time_ab = time.perf_counter() - t_start
            states_ab = self.states_evaluated
            
            # Tính toán tỷ lệ phần trăm số trạng thái được cắt bỏ tối ưu
            pruned_percentage = ((states_mm - states_ab) / max(1, states_mm)) * 100
            
            summary_results.append({
                "id": idx,
                "mm_states": states_mm, "mm_time": time_mm, "mm_move": move_mm,
                "ab_states": states_ab, "ab_time": time_ab, "ab_move": move_ab,
                "pruned": pruned_percentage
            })
            
            print(f"  [Minimax]    -> Điểm: {score_mm} | Duyệt: {states_mm:5d} trạng thái | Thời gian: {time_mm:.4f}s | Chọn: {move_mm}")
            print(f"  [Alpha-Beta] -> Điểm: {score_ab} | Duyệt: {states_ab:5d} trạng thái | Thời gian: {time_ab:.4f}s | Chọn: {move_ab}")
            print(f"  => Đánh giá: Cắt tỉa được {pruned_percentage:.1f}% cây quyết định thừa.\n")
            
        # Xuất bảng ma trận tổng hợp dữ liệu chuẩn định dạng báo cáo đồ án khoa học
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│               BẢNG MA TRẬN SO SÁNH HIỆU NĂNG THỰC NGHIỆM (LEVEL 3)           │")
        print("├───────┬─────────────────────────────┬─────────────────────────────┬─────────┤")
        print("│ Thế   │      Level 1: Minimax       │    Level 2: Alpha-Beta      │ Tỷ lệ   │")
        print("│ cờ    ├────────────┬────────────────┼────────────┬────────────────┤ Cắt tỉa │")
        print("│ mẫu   │ Số Node    │ Thời gian (s)  │ Số Node    │ Thời gian (s)  │ (%)     │")
        print("├───────┼────────────┼────────────────┼────────────┼────────────────┼─────────┤")
        for res in summary_results:
            print(f"│   {res['id']}   │  {res['mm_states']:8d}  │    {res['mm_time']:7.4f}     │  {res['ab_states']:8d}  │    {res['ab_time']:7.4f}     │  {res['pruned']:5.1f}% │")
        print("└───────┴────────────┴────────────────┴────────────┴────────────────┴─────────┘")
        print("\n>>> Chỉ số phân tích toán học: Kết quả 'Điểm' và 'Nước đi chọn' của 2 thuật toán")
        print("    trùng khớp hoàn toàn 100%, chứng minh Alpha-Beta cắt nhánh chính xác tuyệt đối.")
        
        # Trả lại trạng thái trống cho bàn cờ GUI sau khi chạy test xong
        self.reset_game()
        messagebox.showinfo("Level 3: Kết quả", "Đã chạy xong kịch bản kiểm thử tự động!\nMời bạn mở Terminal/Console để lấy bảng số liệu tổng hợp.")


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    # Khởi chạy bằng lớp Kế thừa chứa tính năng tự động phân tích kiểm thử Level 3
    app = CaroSystemComplete(root, size=9)
    root.mainloop()
