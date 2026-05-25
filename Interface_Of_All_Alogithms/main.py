import customtkinter as ctk
import copy
import random
from collections import deque
import heapq

GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, '.']
]

def state_to_string(state):
    return ''.join(str(x) for row in state for x in row)

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
    moves = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
    dx, dy = moves[action]
    new_x, new_y = x + dx, y + dy
    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    return new_state

def is_goal(state):
    return state == GOAL_STATE

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

    def to_string(self):
        state_str = '\n'.join(str(row) for row in self.state)
        return f"State:\n{state_str}\nAction: {self.action}, Depth: {self.depth}"

def get_solution(node):
    result = []
    while node is not None:
        result.append(node)
        node = node.parent
    return result[::-1]

class StepBasedSolver:
    def __init__(self):
        self.steps = []
        self.solution = []

    def generate_steps_bfs(self, start):
        self.steps = []
        step = 1
        queue = deque()
        visited = set()
        
        start_node = Node(start, depth=0)
        queue.append(start_node)
        visited.add(state_to_string(start))
        
        self.steps.append({
            "step": step,
            "node": None,
            "state": start,
            "frontier": [start_node],
            "action": "START",
            "message": "Bắt đầu BFS",
            "depth": "-"
        })
        step += 1
        
        nodes_expanded = 0
        while queue:
            node = queue.popleft()
            nodes_expanded += 1
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": list(queue),
                "action": "POP",
                "message": f"Lấy node từ queue",
                "depth": node.depth
            })
            step += 1
            
            if is_goal(node.state):
                self.solution = get_solution(node)
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": node.state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tìm thấy goal!",
                    "depth": node.depth,
                    "solution": self.solution
                })
                return
            
            children = []
            for action in get_actions(node.state):
                child_state = execute_action(node.state, action)
                child_key = state_to_string(child_state)
                
                if child_key not in visited:
                    visited.add(child_key)
                    child = Node(child_state, parent=node, action=action, depth=node.depth + 1, path=node.path)
                    children.append(child)
                    queue.append(child)
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": list(queue),
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "depth": node.depth
            })
            step += 1

    def generate_steps_dfs(self, start):
        self.steps = []
        step = 1
        stack = []
        visited = set()
        
        start_node = Node(start, depth=0)
        stack.append(start_node)
        
        self.steps.append({
            "step": step,
            "node": None,
            "state": start,
            "frontier": [start_node],
            "action": "START",
            "message": "Bắt đầu DFS",
            "depth": "-"
        })
        step += 1
        
        while stack:
            node = stack.pop()
            state_str = state_to_string(node.state)
            
            if state_str in visited:
                continue
            
            visited.add(state_str)
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": list(stack),
                "action": "POP",
                "message": f"Lấy node từ stack",
                "depth": node.depth
            })
            step += 1
            
            if is_goal(node.state):
                self.solution = get_solution(node)
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": node.state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tìm thấy goal!",
                    "depth": node.depth,
                    "solution": self.solution
                })
                return
            
            children = []
            for action in reversed(get_actions(node.state)):
                child_state = execute_action(node.state, action)
                child = Node(child_state, parent=node, action=action, depth=node.depth + 1, path=node.path)
                children.append(child)
                stack.append(child)
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": list(stack),
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "depth": node.depth
            })
            step += 1

    def generate_steps_ids(self, start):
        self.steps = []
        step = 1
        
        for limit in range(30):
            start_node = Node(start, depth=0)
            frontier = [start_node]
            
            self.steps.append({
                "step": step,
                "node": None,
                "state": start,
                "frontier": frontier.copy(),
                "action": "START",
                "message": f"Bắt đầu với I = {limit}",
                "limit": limit,
                "depth": "-"
            })
            step += 1
            
            while frontier:
                node = frontier.pop()
                
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": node.state,
                    "frontier": frontier.copy(),
                    "action": "POP",
                    "message": "Lấy node từ frontier",
                    "limit": limit,
                    "depth": node.depth
                })
                step += 1
                
                if is_goal(node.state):
                    self.solution = get_solution(node)
                    self.steps.append({
                        "step": step,
                        "node": node,
                        "state": node.state,
                        "frontier": frontier.copy(),
                        "action": "GOAL",
                        "message": "Tìm thấy goal!",
                        "limit": limit,
                        "depth": node.depth,
                        "solution": self.solution
                    })
                    return
                
                if node.depth >= limit:
                    self.steps.append({
                        "step": step,
                        "node": node,
                        "state": node.state,
                        "frontier": frontier.copy(),
                        "action": "CUTOFF",
                        "message": "DEPTH >= I (cắt)",
                        "limit": limit,
                        "depth": node.depth
                    })
                    step += 1
                else:
                    children = []
                    for action in get_actions(node.state):
                        child_state = execute_action(node.state, action)
                        child_key = state_to_string(child_state)
                        
                        if child_key not in node.path:
                            child = Node(child_state, parent=node, action=action, depth=node.depth + 1, path=node.path)
                            children.append(child)
                    
                    for child in reversed(children):
                        frontier.append(child)
                    
                    self.steps.append({
                        "step": step,
                        "node": node,
                        "state": node.state,
                        "frontier": frontier.copy(),
                        "action": "EXPAND",
                        "message": f"Sinh {len(children)} node con",
                        "limit": limit,
                        "depth": node.depth
                    })
                    step += 1
            
            self.steps.append({
                "step": step,
                "node": None,
                "state": start,
                "frontier": [],
                "action": "NEXT I",
                "message": f"Tăng I từ {limit} lên {limit+1}",
                "limit": limit,
                "depth": "-"
            })
            step += 1

    def calculate_cost(self, state):
        cost = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != GOAL_STATE[i][j]:
                    cost += 1
        return cost

    def generate_steps_ucs(self, start):
        self.steps = []
        step = 1
        heap = []
        visited = set()
        counter = 0
        
        start_cost = self.calculate_cost(start)
        start_node = Node(start, depth=0)
        heapq.heappush(heap, (start_cost, counter, state_to_string(start), start_node))
        visited.add(state_to_string(start))
        
        self.steps.append({
            "step": step,
            "node": None,
            "state": start,
            "frontier": [start_node],
            "action": "START",
            "message": "Bắt đầu UCS",
            "cost": start_cost,
            "depth": "-"
        })
        step += 1
        
        while heap:
            _, _, _, node = heapq.heappop(heap)
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "POP",
                "message": "Lấy node với cost thấp nhất",
                "cost": self.calculate_cost(node.state),
                "depth": node.depth
            })
            step += 1
            
            if is_goal(node.state):
                self.solution = get_solution(node)
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": node.state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tìm thấy goal!",
                    "cost": self.calculate_cost(node.state),
                    "depth": node.depth,
                    "solution": self.solution
                })
                return
            
            children = []
            for action in get_actions(node.state):
                child_state = execute_action(node.state, action)
                child_key = state_to_string(child_state)
                
                if child_key not in visited:
                    visited.add(child_key)
                    child = Node(child_state, parent=node, action=action, depth=node.depth + 1)
                    children.append(child)
                    child_cost = self.calculate_cost(child_state)
                    counter += 1
                    heapq.heappush(heap, (child_cost, counter, child_key, child))
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "cost": self.calculate_cost(node.state),
                "depth": node.depth
            })
            step += 1

class PuzzleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("8 Puzzle - Tất Cả Thuật Toán")
        self.geometry("1300x750")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.initial_state = random_initial_state()
        self.current_step = 0
        self.auto_running = False
        self.auto_delay = 500
        self.cells = []
        self.solver = StepBasedSolver()
        self.algorithm = "BFS"

        self.build_ui()
        self.update_board(self.initial_state)

    def build_ui(self):
        self.main = ctk.CTkFrame(self, fg_color="#020617", corner_radius=0)
        self.main.pack(fill="both", expand=True)

        ctk.CTkLabel(self.main, text="8 Puzzle", font=("Arial", 34, "bold"), text_color="#60a5fa").pack(pady=(20, 10))

        content = ctk.CTkFrame(self.main, fg_color="#020617", corner_radius=0)
        content.pack(fill="both", expand=True, padx=20, pady=15)

        self.left = ctk.CTkFrame(content, width=450, fg_color="#0f172a", corner_radius=20)
        self.left.pack(side="left", fill="both", padx=(0, 12))
        self.left.pack_propagate(False)

        self.right = ctk.CTkFrame(content, width=750, fg_color="#0f172a", corner_radius=20)
        self.right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        self.build_left()
        self.build_right()

    def build_left(self):
        board_frame = ctk.CTkFrame(self.left, fg_color="#1e293b", corner_radius=22)
        board_frame.pack(pady=(35, 20))

        for i in range(3):
            row = []
            for j in range(3):
                cell = ctk.CTkLabel(board_frame, text="", width=88, height=88, corner_radius=17,
                    fg_color="#2563eb", text_color="white", font=("Arial", 34, "bold"))
                cell.grid(row=i, column=j, padx=7, pady=7)
                row.append(cell)
            self.cells.append(row)

        algo_frame = ctk.CTkFrame(self.left, fg_color="transparent")
        algo_frame.pack(pady=10)

        ctk.CTkLabel(algo_frame, text="Thuật toán:", font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))

        self.algo_menu = ctk.CTkComboBox(algo_frame, values=["BFS", "DFS", "IDS", "UCS"],
            command=self.change_algorithm, width=150, height=32)
        self.algo_menu.set("BFS")
        self.algo_menu.pack(side="left")

        button_frame = ctk.CTkFrame(self.left, fg_color="transparent")
        button_frame.pack(pady=15)

        ctk.CTkButton(button_frame, text="Random", width=135, height=42, fg_color="#9333ea",
            hover_color="#7e22ce", font=("Arial", 14, "bold"), command=self.random_new).grid(row=0, column=0, padx=7, pady=7)

        ctk.CTkButton(button_frame, text="Giải", width=135, height=42, font=("Arial", 14, "bold"),
            command=self.solve).grid(row=0, column=1, padx=7, pady=7)

        ctk.CTkButton(button_frame, text="Bước tiếp", width=135, height=42, fg_color="#16a34a",
            hover_color="#15803d", font=("Arial", 14, "bold"), command=self.next_step).grid(row=1, column=0, padx=7, pady=7)

        self.auto_button = ctk.CTkButton(button_frame, text="Chạy auto", width=135, height=42, fg_color="#f59e0b",
            hover_color="#d97706", font=("Arial", 14, "bold"), command=self.auto_run)
        self.auto_button.grid(row=1, column=1, padx=7, pady=7)

        ctk.CTkButton(button_frame, text="Reset", width=285, height=40, fg_color="#dc2626",
            hover_color="#b91c1c", font=("Arial", 14, "bold"), command=self.reset_view).grid(row=2, column=0, columnspan=2, padx=7, pady=7)

    def build_right(self):
        ctk.CTkLabel(self.right, text="Bảng thông tin", font=("Arial", 25, "bold"), text_color="#93c5fd").pack(pady=(25, 12))

        top = ctk.CTkFrame(self.right, fg_color="#111827", corner_radius=18)
        top.pack(fill="x", padx=25, pady=(0, 15))

        self.step_label = ctk.CTkLabel(top, text="Step: -", font=("Arial", 14, "bold"), text_color="#38bdf8")
        self.step_label.grid(row=0, column=0, padx=20, pady=12)

        self.algo_label = ctk.CTkLabel(top, text="Thuật toán: BFS", font=("Arial", 14, "bold"), text_color="#facc15")
        self.algo_label.grid(row=0, column=1, padx=20, pady=12)

        self.depth_label = ctk.CTkLabel(top, text="Depth: -", font=("Arial", 14, "bold"), text_color="#4ade80")
        self.depth_label.grid(row=0, column=2, padx=20, pady=12)

        self.log_box = ctk.CTkTextbox(self.right, width=700, height=260, fg_color="#020617",
            text_color="#e5e7eb", font=("Consolas", 11), corner_radius=16)
        self.log_box.pack(padx=25, pady=(0, 15))
        self.log_box.insert("end", "Logs...\n")
        self.log_box.configure(state="disabled")

        bottom = ctk.CTkFrame(self.right, fg_color="transparent")
        bottom.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.frontier_box = ctk.CTkTextbox(bottom, width=340, height=140, fg_color="#1e1b4b",
            text_color="#e0e7ff", font=("Consolas", 9), corner_radius=16)
        self.frontier_box.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.frontier_box.insert("end", "Frontier...")
        self.frontier_box.configure(state="disabled")

        self.solution_box = ctk.CTkTextbox(bottom, width=340, height=140, fg_color="#172554",
            text_color="#e0f2fe", font=("Consolas", 9), corner_radius=16)
        self.solution_box.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.solution_box.insert("end", "Lời giải...")
        self.solution_box.configure(state="disabled")

    def change_algorithm(self, value):
        self.algorithm = value
        self.algo_label.configure(text=f"Thuật toán: {value}")

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                text = "" if val == "." else str(val)
                color = "#1f2937" if val == "." else "#2563eb"
                self.cells[i][j].configure(text=text, fg_color=color)

    def random_new(self):
        self.initial_state = random_initial_state()
        self.current_step = 0
        self.solver.steps = []
        self.update_board(self.initial_state)
        self.reset_logs()
        self.step_label.configure(text="Step: -")

    def solve(self):
        self.auto_running = False
        self.auto_button.configure(text="Chạy auto")
        self.current_step = 0
        self.reset_logs()
        
        if self.algorithm == "BFS":
            self.solver.generate_steps_bfs(self.initial_state)
        elif self.algorithm == "DFS":
            self.solver.generate_steps_dfs(self.initial_state)
        elif self.algorithm == "IDS":
            self.solver.generate_steps_ids(self.initial_state)
        else:
            self.solver.generate_steps_ucs(self.initial_state)
        
        if self.solver.steps:
            self.log_message(f"Đã tạo {len(self.solver.steps)} bước cho {self.algorithm}")

    def next_step(self):
        if not self.solver.steps:
            return

        if self.current_step >= len(self.solver.steps):
            self.log_message("Đã hết các bước!")
            return

        data = self.solver.steps[self.current_step]
        self.current_step += 1

        self.update_board(data["state"])
        self.update_info(data)
        self.log_message(f"[Step {data['step']}] {data['message']}")
        self.update_frontier(data)
        
        if "solution" in data:
            self.show_solution(data["solution"])

    def update_info(self, data):
        self.step_label.configure(text=f"Step: {data['step']}")
        self.depth_label.configure(text=f"Depth: {data['depth']}")

    def update_frontier(self, data):
        frontier_text = ""
        for i, node in enumerate(data.get("frontier", [])):
            state_str = str(node.state).replace(", ", ",")
            frontier_text += f"{i+1}. {state_str} (d={node.depth})\n"
        
        self.frontier_box.configure(state="normal")
        self.frontier_box.delete("1.0", "end")
        self.frontier_box.insert("end", frontier_text if frontier_text else "Frontier rỗng")
        self.frontier_box.configure(state="disabled")

    def show_solution(self, solution):
        moves_text = ""
        for i, node in enumerate(solution):
            if node.action:
                moves_text += f"{i}. {node.action}\n"
        
        self.solution_box.configure(state="normal")
        self.solution_box.delete("1.0", "end")
        self.solution_box.insert("end", "Lời giải:\n" + moves_text)
        self.solution_box.configure(state="disabled")

    def auto_run(self):
        if not self.solver.steps:
            return

        if self.auto_running:
            self.auto_running = False
            self.auto_button.configure(text="Chạy auto")
        else:
            self.auto_running = True
            self.auto_button.configure(text="Dừng")
            self.run_auto_step()

    def run_auto_step(self):
        if not self.auto_running or self.current_step >= len(self.solver.steps):
            self.auto_running = False
            self.auto_button.configure(text="Chạy auto")
            return

        self.next_step()
        self.after(self.auto_delay, self.run_auto_step)

    def reset_view(self):
        self.auto_running = False
        self.auto_button.configure(text="Chạy auto")
        self.current_step = 0
        self.solver.steps = []
        self.update_board(self.initial_state)
        self.reset_logs()
        self.step_label.configure(text="Step: -")

    def reset_logs(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.insert("end", "Logs...\n")
        self.log_box.configure(state="disabled")

        self.frontier_box.configure(state="normal")
        self.frontier_box.delete("1.0", "end")
        self.frontier_box.insert("end", "Frontier...")
        self.frontier_box.configure(state="disabled")

        self.solution_box.configure(state="normal")
        self.solution_box.delete("1.0", "end")
        self.solution_box.insert("end", "Lời giải...")
        self.solution_box.configure(state="disabled")

    def log_message(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

if __name__ == "__main__":
    app = PuzzleApp()
    app.mainloop()
