import customtkinter as ctk
import copy
import random


GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, '.']
]


def state_to_string(state):
    return ''.join(str(x) for row in state for x in row)


def state_to_pretty_string(state):
    return '\n'.join(' '.join(str(x) for x in row) for row in state)


def find_empty(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == '.':
                return i, j


def get_actions(state):
    x, y = find_empty(state)
    actions = []

    if x > 0:
        actions.append("UP")
    if x < 2:
        actions.append("DOWN")
    if y > 0:
        actions.append("LEFT")
    if y < 2:
        actions.append("RIGHT")

    return actions


def execute_action(state, action):
    new_state = copy.deepcopy(state)
    x, y = find_empty(new_state)

    if action == "UP":
        nx, ny = x - 1, y
    elif action == "DOWN":
        nx, ny = x + 1, y
    elif action == "LEFT":
        nx, ny = x, y - 1
    else:
        nx, ny = x, y + 1

    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
    return new_state


def random_initial_state():
    state = copy.deepcopy(GOAL_STATE)
    old_action = None

    for _ in range(random.randint(8, 16)):
        actions = get_actions(state)

        if old_action == "UP" and "DOWN" in actions:
            actions.remove("DOWN")
        elif old_action == "DOWN" and "UP" in actions:
            actions.remove("UP")
        elif old_action == "LEFT" and "RIGHT" in actions:
            actions.remove("RIGHT")
        elif old_action == "RIGHT" and "LEFT" in actions:
            actions.remove("LEFT")

        action = random.choice(actions)
        state = execute_action(state, action)
        old_action = action

    return state


def is_goal(state):
    return state == GOAL_STATE


class Node:
    def __init__(self, state, parent=None, action=None, depth=0, path=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth

        if path is None:
            self.path = set()
        else:
            self.path = set(path)

        self.path.add(state_to_string(state))


def get_solution(node):
    result = []

    while node is not None:
        result.append(node)
        node = node.parent

    return result[::-1]


class IDS8PuzzleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("8 Puzzle")
        self.geometry("1150x700")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.initial_state = random_initial_state()
        self.steps = []
        self.solution = []
        self.current_step = 0
        self.auto_running = False
        self.auto_delay = 500
        self.cells = []

        self.build_ui()
        self.update_board(self.initial_state)

    def build_ui(self):
        self.main = ctk.CTkFrame(self, fg_color="#020617", corner_radius=0)
        self.main.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.main,
            text="8 Puzzle",
            font=("Arial", 34, "bold"),
            text_color="#60a5fa"
        ).pack(pady=(20, 10))

        content = ctk.CTkFrame(self.main, fg_color="#020617", corner_radius=0)
        content.pack(fill="both", expand=True, padx=20, pady=15)

        self.left = ctk.CTkFrame(content, width=400, fg_color="#0f172a", corner_radius=20)
        self.left.pack(side="left", fill="both", padx=(0, 12))
        self.left.pack_propagate(False)

        self.right = ctk.CTkFrame(content, width=700, fg_color="#0f172a", corner_radius=20)
        self.right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        self.build_left()
        self.build_right()

    def build_left(self):
        board_frame = ctk.CTkFrame(self.left, fg_color="#1e293b", corner_radius=22)
        board_frame.pack(pady=(35, 20))

        for i in range(3):
            row = []
            for j in range(3):
                cell = ctk.CTkLabel(
                    board_frame,
                    text="",
                    width=88,
                    height=88,
                    corner_radius=17,
                    fg_color="#2563eb",
                    text_color="white",
                    font=("Arial", 34, "bold")
                )
                cell.grid(row=i, column=j, padx=7, pady=7)
                row.append(cell)
            self.cells.append(row)

        button_frame = ctk.CTkFrame(self.left, fg_color="transparent")
        button_frame.pack(pady=15)

        ctk.CTkButton(
            button_frame,
            text="Random",
            width=135,
            height=42,
            fg_color="#9333ea",
            hover_color="#7e22ce",
            font=("Arial", 14, "bold"),
            command=self.random_new
        ).grid(row=0, column=0, padx=7, pady=7)

        ctk.CTkButton(
            button_frame,
            text="Tìm IDS",
            width=135,
            height=42,
            font=("Arial", 14, "bold"),
            command=self.find_ids
        ).grid(row=0, column=1, padx=7, pady=7)

        ctk.CTkButton(
            button_frame,
            text="Chạy từng lượt",
            width=135,
            height=42,
            fg_color="#16a34a",
            hover_color="#15803d",
            font=("Arial", 14, "bold"),
            command=self.next_ids_step
        ).grid(row=1, column=0, padx=7, pady=7)

        self.auto_button = ctk.CTkButton(
            button_frame,
            text="Chạy tự động",
            width=135,
            height=42,
            fg_color="#f59e0b",
            hover_color="#d97706",
            font=("Arial", 14, "bold"),
            command=self.auto_run
        )
        self.auto_button.grid(row=1, column=1, padx=7, pady=7)

        ctk.CTkButton(
            button_frame,
            text="Reset",
            width=285,
            height=40,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=("Arial", 14, "bold"),
            command=self.reset_view
        ).grid(row=2, column=0, columnspan=2, padx=7, pady=7)

    def build_right(self):
        ctk.CTkLabel(
            self.right,
            text="Bảng trạng thái IDS",
            font=("Arial", 25, "bold"),
            text_color="#93c5fd"
        ).pack(pady=(25, 12))

        top = ctk.CTkFrame(self.right, fg_color="#111827", corner_radius=18)
        top.pack(fill="x", padx=25, pady=(0, 15))

        self.step_label = ctk.CTkLabel(
            top,
            text="Step: -",
            font=("Arial", 17, "bold"),
            text_color="#38bdf8"
        )
        self.step_label.grid(row=0, column=0, padx=55, pady=14)

        self.limit_label = ctk.CTkLabel(
            top,
            text="I: -",
            font=("Arial", 17, "bold"),
            text_color="#facc15"
        )
        self.limit_label.grid(row=0, column=1, padx=55, pady=14)

        self.depth_label = ctk.CTkLabel(
            top,
            text="Depth: -",
            font=("Arial", 17, "bold"),
            text_color="#4ade80"
        )
        self.depth_label.grid(row=0, column=2, padx=55, pady=14)

        self.log_box = ctk.CTkTextbox(
            self.right,
            width=640,
            height=285,
            fg_color="#020617",
            text_color="#e5e7eb",
            font=("Consolas", 12),
            corner_radius=16
        )
        self.log_box.pack(padx=25, pady=(0, 15))
        self.write_log_header()

        bottom = ctk.CTkFrame(self.right, fg_color="transparent")
        bottom.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.frontier_box = ctk.CTkTextbox(
            bottom,
            width=310,
            height=210,
            fg_color="#1e1b4b",
            text_color="#e0e7ff",
            font=("Consolas", 12),
            corner_radius=16
        )
        self.frontier_box.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.frontier_box.insert("end", "Frontier sẽ hiện ở đây...")
        self.frontier_box.configure(state="disabled")

        self.solution_box = ctk.CTkTextbox(
            bottom,
            width=310,
            height=210,
            fg_color="#172554",
            text_color="#e0f2fe",
            font=("Consolas", 12),
            corner_radius=16
        )
        self.solution_box.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.solution_box.insert("end", "Solution sẽ hiện ở đây...")
        self.solution_box.configure(state="disabled")

    def generate_steps(self):
        self.steps = []
        self.solution = []
        step = 1

        for limit in range(40):
            start = Node(self.initial_state, depth=0)
            frontier = [start]
            result = "failure"

            self.steps.append({
                "step": step,
                "limit": limit,
                "node": None,
                "depth": "-",
                "state": self.initial_state,
                "frontier": frontier.copy(),
                "action": "START",
                "message": f"Bắt đầu với I = {limit}",
                "solution": None
            })
            step += 1

            while frontier:
                node = frontier.pop()

                self.steps.append({
                    "step": step,
                    "limit": limit,
                    "node": node,
                    "depth": node.depth,
                    "state": node.state,
                    "frontier": frontier.copy(),
                    "action": "POP",
                    "message": "Lấy node từ frontier",
                    "solution": None
                })
                step += 1

                if is_goal(node.state):
                    self.solution = get_solution(node)

                    self.steps.append({
                        "step": step,
                        "limit": limit,
                        "node": node,
                        "depth": node.depth,
                        "state": node.state,
                        "frontier": frontier.copy(),
                        "action": "GOAL",
                        "message": "Tìm thấy goal 12345678.",
                        "solution": self.solution
                    })
                    return

                if node.depth >= limit:
                    result = "cutoff"

                    self.steps.append({
                        "step": step,
                        "limit": limit,
                        "node": node,
                        "depth": node.depth,
                        "state": node.state,
                        "frontier": frontier.copy(),
                        "action": "CUTOFF",
                        "message": "DEPTH(node) >= I",
                        "solution": None
                    })
                    step += 1

                else:
                    children = []

                    for action in get_actions(node.state):
                        child_state = execute_action(node.state, action)
                        child_key = state_to_string(child_state)

                        if child_key not in node.path:
                            child = Node(
                                state=child_state,
                                parent=node,
                                action=action,
                                depth=node.depth + 1,
                                path=node.path
                            )
                            children.append(child)

                    for child in reversed(children):
                        frontier.append(child)

                    self.steps.append({
                        "step": step,
                        "limit": limit,
                        "node": node,
                        "depth": node.depth,
                        "state": node.state,
                        "frontier": frontier.copy(),
                        "action": "EXPAND",
                        "message": f"Sinh {len(children)} node con",
                        "solution": None
                    })
                    step += 1

            if result == "cutoff":
                self.steps.append({
                    "step": step,
                    "limit": limit,
                    "node": None,
                    "depth": "-",
                    "state": self.initial_state,
                    "frontier": [],
                    "action": "NEXT I",
                    "message": "Tăng giới hạn I",
                    "solution": None
                })
                step += 1

    def random_new(self):
        self.auto_running = False
        self.auto_button.configure(text="Chạy tự động")
        self.initial_state = random_initial_state()
        self.reset_all()
        self.update_board(self.initial_state)

    def find_ids(self):
        self.auto_running = False
        self.auto_button.configure(text="Chạy tự động")
        self.reset_all()
        self.generate_steps()
        self.show_solution_summary()

    def next_ids_step(self):
        if not self.steps:
            return

        if self.current_step >= len(self.steps):
            self.auto_running = False
            self.auto_button.configure(text="Chạy tự động")
            return

        data = self.steps[self.current_step]
        self.current_step += 1

        self.update_board(data["state"])
        self.update_status(data)
        self.append_log(data)
        self.update_frontier(data["frontier"])

        if data.get("solution") is not None:
            self.show_solution_summary()

    def auto_run(self):
        if not self.steps:
            self.find_ids()

        if not self.steps:
            return

        self.auto_running = not self.auto_running

        if self.auto_running:
            self.auto_button.configure(text="Dừng")
            self.run_auto_step()
        else:
            self.auto_button.configure(text="Chạy tự động")

    def run_auto_step(self):
        if not self.auto_running:
            return

        if self.current_step >= len(self.steps):
            self.auto_running = False
            self.auto_button.configure(text="Chạy tự động")
            return

        self.next_ids_step()
        self.after(self.auto_delay, self.run_auto_step)

    def reset_view(self):
        self.auto_running = False
        self.auto_button.configure(text="Chạy tự động")
        self.current_step = 0
        self.update_board(self.initial_state)
        self.clear_boxes()

    def reset_all(self):
        self.auto_running = False
        self.steps = []
        self.solution = []
        self.current_step = 0
        self.update_board(self.initial_state)
        self.clear_boxes()

        if hasattr(self, "auto_button"):
            self.auto_button.configure(text="Chạy tự động")

    def clear_boxes(self):
        self.step_label.configure(text="Step: -")
        self.limit_label.configure(text="I: -")
        self.depth_label.configure(text="Depth: -")

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.write_log_header()

        self.frontier_box.configure(state="normal")
        self.frontier_box.delete("1.0", "end")
        self.frontier_box.insert("end", "Frontier sẽ hiện ở đây...")
        self.frontier_box.configure(state="disabled")

        self.solution_box.configure(state="normal")
        self.solution_box.delete("1.0", "end")
        self.solution_box.insert("end", "Solution sẽ hiện ở đây...")
        self.solution_box.configure(state="disabled")

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                value = state[i][j]

                if value == '.':
                    self.cells[i][j].configure(text="", fg_color="#334155")
                else:
                    self.cells[i][j].configure(text=str(value), fg_color="#2563eb")

        if state == GOAL_STATE:
            for i in range(3):
                for j in range(3):
                    self.cells[i][j].configure(fg_color="#16a34a")

    def update_status(self, data):
        self.step_label.configure(text=f"Step: {data['step']}")
        self.limit_label.configure(text=f"I: {data['limit']}")
        self.depth_label.configure(text=f"Depth: {data['depth']}")

    def write_log_header(self):
        self.log_box.insert(
            "end",
            f"{'Step':<6}{'I':<4}{'Depth':<8}{'Action':<10}Message\n"
        )
        self.log_box.insert("end", "-" * 75 + "\n")
        self.log_box.configure(state="disabled")

    def append_log(self, data):
        self.log_box.configure(state="normal")

        line = (
            f"{data['step']:<6}"
            f"{data['limit']:<4}"
            f"{str(data['depth']):<8}"
            f"{data['action']:<10}"
            f"{data['message']}\n"
        )

        self.log_box.insert("end", line)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_frontier(self, frontier):
        self.frontier_box.configure(state="normal")
        self.frontier_box.delete("1.0", "end")

        self.frontier_box.insert("end", "FRONTIER\n")
        self.frontier_box.insert("end", "-" * 35 + "\n")

        if not frontier:
            self.frontier_box.insert("end", "Frontier rỗng\n")
        else:
            for i, node in enumerate(reversed(frontier), start=1):
                self.frontier_box.insert(
                    "end",
                    f"{i}. {state_to_string(node.state)} | depth={node.depth}\n"
                )

        self.frontier_box.configure(state="disabled")

    def show_solution_summary(self):
        self.solution_box.configure(state="normal")
        self.solution_box.delete("1.0", "end")

        if not self.solution:
            self.solution_box.insert("end", "Chưa có solution.")
        else:
            self.solution_box.insert("end", "SOLUTION\n")
            self.solution_box.insert("end", "=" * 32 + "\n\n")

            for i, node in enumerate(self.solution):
                if node.action is None:
                    self.solution_box.insert("end", f"Bước {i}: Initial\n")
                else:
                    self.solution_box.insert("end", f"Bước {i}: {node.action}\n")

                self.solution_box.insert("end", state_to_pretty_string(node.state))
                self.solution_box.insert("end", "\n\n")

        self.solution_box.configure(state="disabled")


if __name__ == "__main__":
    app = IDS8PuzzleApp()
    app.mainloop()