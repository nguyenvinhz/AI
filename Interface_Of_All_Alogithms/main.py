import customtkinter as ctk
import copy
import math
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

    def manhattan_distance(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == '.':
                    return abs(i - 2) + abs(j - 2)
        return 0

    def tile_manhattan_distance(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != '.':
                    goal_i = (value - 1) // 3
                    goal_j = (value - 1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def all_actions(self):
        return ["UP", "DOWN", "LEFT", "RIGHT"]

    def opposite_action(self, action):
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        return opposites[action]

    def execute_action_with_wall(self, state, action):
        if action in get_actions(state):
            return execute_action(state, action)
        return copy.deepcopy(state)

    def belief_to_string(self, belief_state):
        return "|".join(state_to_string(state) for state in belief_state)

    def belief_cost(self, belief_state):
        return sum(self.tile_manhattan_distance(state) for state in belief_state)

    def is_belief_goal(self, belief_state):
        return all(is_goal(state) for state in belief_state)

    def execute_belief_action(self, belief_state, action):
        return [
            self.execute_action_with_wall(state, action)
            for state in belief_state
        ]

    def predecessor_states(self, state, action):
        predecessors = []
        if action not in get_actions(state):
            predecessors.append(copy.deepcopy(state))

        reverse_action = self.opposite_action(action)
        if reverse_action in get_actions(state):
            predecessors.append(execute_action(state, reverse_action))

        return predecessors

    def random_plan(self, length=7):
        actions_from_goal = []
        state = copy.deepcopy(GOAL_STATE)

        for _ in range(length):
            choices = [
                action
                for action in self.all_actions()
                if self.predecessor_states(state, action)
            ]
            action = random.choice(choices)
            state = random.choice(self.predecessor_states(state, action))
            actions_from_goal.append(action)

        return list(reversed(actions_from_goal))

    def make_state_from_plan(self, plan):
        state = copy.deepcopy(GOAL_STATE)

        for action in reversed(plan):
            choices = self.predecessor_states(state, action)
            if not choices:
                return None
            state = random.choice(choices)

        return state

    def run_plan(self, state, plan):
        current = copy.deepcopy(state)
        for action in plan:
            current = self.execute_action_with_wall(current, action)
        return current

    def belief_greedy_result(self, initial_belief, max_expansions=1000):
        counter = 0
        start = copy.deepcopy(initial_belief)
        frontier = [(self.belief_cost(start), counter, start, [])]
        visited = {self.belief_to_string(start)}
        expansions = 0

        while frontier and expansions < max_expansions:
            _, _, belief_state, actions_taken = heapq.heappop(frontier)
            expansions += 1

            if self.is_belief_goal(belief_state):
                return {
                    "success": True,
                    "actions": actions_taken,
                    "final_belief": belief_state
                }

            for action in self.all_actions():
                next_belief = self.execute_belief_action(belief_state, action)
                next_key = self.belief_to_string(next_belief)
                if next_key in visited:
                    continue

                visited.add(next_key)
                counter += 1
                heapq.heappush(frontier, (
                    self.belief_cost(next_belief),
                    counter,
                    next_belief,
                    actions_taken + [action]
                ))

        return {"success": False, "actions": [], "final_belief": None}

    def random_belief_state(self, size=3, plan_length=7, max_attempts=1000, min_solution_steps=4):
        for _ in range(max_attempts):
            plan = self.random_plan(plan_length)
            belief_state = []
            seen = set()
            state_attempts = 0

            while len(belief_state) < size and state_attempts < 100:
                state_attempts += 1
                state = self.make_state_from_plan(plan)
                if state is None:
                    break

                key = state_to_string(state)
                if key not in seen and state != GOAL_STATE and self.run_plan(state, plan) == GOAL_STATE:
                    belief_state.append(state)
                    seen.add(key)

            if len(belief_state) == size and self.belief_cost(belief_state) >= plan_length:
                if min_solution_steps <= 0:
                    return belief_state

                result = self.belief_greedy_result(belief_state)
                if result["success"] and len(result["actions"]) >= min_solution_steps:
                    return belief_state

        return self.random_belief_state(size, plan_length, max_attempts, min_solution_steps - 1)

    def count_inversions(self, state):
        tiles = []
        for i in range(3):
            for j in range(3):
                if state[i][j] != '.':
                    tiles.append(state[i][j])
        
        inversions = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1
        return inversions

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

    def generate_steps_greedy(self, start):
        self.steps = []
        step = 1
        heap = []
        visited = set()
        counter = 0
        
        start_heuristic = self.manhattan_distance(start)
        start_node = Node(start, depth=0)
        heapq.heappush(heap, (start_heuristic, counter, state_to_string(start), start_node))
        visited.add(state_to_string(start))
        
        self.steps.append({
            "step": step,
            "node": None,
            "state": start,
            "frontier": [start_node],
            "action": "START",
            "message": "Bắt đầu Greedy",
            "heuristic": start_heuristic,
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
                "message": "Lấy node với h(n) thấp nhất",
                "heuristic": self.manhattan_distance(node.state),
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
                    "heuristic": self.manhattan_distance(node.state),
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
                    child_heuristic = self.manhattan_distance(child_state)
                    counter += 1
                    heapq.heappush(heap, (child_heuristic, counter, child_key, child))
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "heuristic": self.manhattan_distance(node.state),
                "depth": node.depth
            })
            step += 1

    def generate_steps_astar(self, start):
        self.steps = []
        step = 1
        heap = []
        visited = set()
        counter = 0
        
        start_h = self.count_inversions(start)
        start_g = 0
        start_f = start_g + start_h
        start_node = Node(start, depth=0)
        heapq.heappush(heap, (start_f, counter, state_to_string(start), start_node))
        visited.add(state_to_string(start))
        
        self.steps.append({
            "step": step,
            "node": None,
            "state": start,
            "frontier": [start_node],
            "action": "START",
            "message": "Bắt đầu A*",
            "f_n": start_f,
            "depth": "-"
        })
        step += 1
        
        while heap:
            _, _, _, node = heapq.heappop(heap)
            
            g_n = node.depth
            h_n = self.count_inversions(node.state)
            f_n = g_n + h_n
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "POP",
                "message": f"Lấy node với f(n)={f_n} thấp nhất",
                "f_n": f_n,
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
                    "f_n": f_n,
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
                    child_g = child.depth
                    child_h = self.count_inversions(child_state)
                    child_f = child_g + child_h
                    counter += 1
                    heapq.heappush(heap, (child_f, counter, child_key, child))
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "f_n": f_n,
                "depth": node.depth
            })
            step += 1

    def heuristic_ida_star(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == '.':
                    return abs(i - 2) + abs(j - 2)
        return 0

    def search_with_limit_ida(self, node, g_limit, visited):
        stack = [node]
        min_limit = float('inf')
        local_visited = set()
        local_visited.add(state_to_string(node.state))
        
        while stack:
            current = stack.pop()
            h_val = self.heuristic_ida_star(current.state)
            f_val = current.depth + h_val
            
            if f_val > g_limit:
                if f_val < min_limit:
                    min_limit = f_val
                continue
            
            if is_goal(current.state):
                return current, g_limit
            
            for action in get_actions(current.state):
                child_state = execute_action(current.state, action)
                child_key = state_to_string(child_state)
                
                if child_key not in local_visited:
                    local_visited.add(child_key)
                    child = Node(child_state, parent=current, action=action, depth=current.depth + 1)
                    stack.append(child)
        
        return None, min_limit

    def generate_steps_ida_star(self, start):
        self.steps = []
        step = 1
        
        for limit in range(50):
            start_node = Node(start, depth=0)
            visited = set()
            visited.add(state_to_string(start))
            
            self.steps.append({
                "step": step,
                "node": None,
                "state": start,
                "frontier": [start_node],
                "action": "START",
                "message": f"IDA* - Threshold = {limit}",
                "threshold": limit,
                "depth": "-"
            })
            step += 1
            
            result_node, new_threshold = self.search_with_limit_ida(start_node, limit, visited)
            
            if result_node is not None:
                self.solution = get_solution(result_node)
                self.steps.append({
                    "step": step,
                    "node": result_node,
                    "state": result_node.state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tìm thấy goal!",
                    "threshold": limit,
                    "depth": result_node.depth,
                    "solution": self.solution
                })
                return
            
            if new_threshold == float('inf'):
                return
            
            step += 1
            self.steps.append({
                "step": step,
                "node": None,
                "state": start,
                "frontier": [],
                "action": "NEXT_THRESHOLD",
                "message": f"Tăng threshold từ {limit} lên {new_threshold}",
                "threshold": limit,
                "depth": "-"
            })
            step += 1

    def generate_steps_hill_climbing(self, start):
        self.steps = []
        step = 1
        current = start
        current_value = self.manhattan_distance(current)
        current_node = Node(current, depth=0)
        iterations = 0
        
        self.steps.append({
            "step": step,
            "node": current_node,
            "state": current,
            "frontier": [current_node],
            "action": "START",
            "message": f"Bắt đầu Hill Climbing (h={current_value})",
            "heuristic": current_value,
            "depth": "-"
        })
        step += 1
        
        while iterations < 1000:
            iterations += 1
            
            if is_goal(current):
                self.solution = get_solution(current_node)
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tìm thấy goal!",
                    "heuristic": current_value,
                    "depth": current_node.depth,
                    "solution": self.solution
                })
                return
            
            rules = get_actions(current)
            best_neighbor = None
            best_value = current_value
            best_action = None
            neighbors = []
            
            for action in rules:
                neighbor = execute_action(current, action)
                value = self.manhattan_distance(neighbor)
                neighbor_node = Node(neighbor, parent=current_node, action=action, depth=current_node.depth + 1)
                neighbors.append((neighbor_node, value))
                
                if value < best_value:
                    best_value = value
                    best_neighbor = neighbor
                    best_action = action
            
            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": neighbors,
                "action": "EXPAND",
                "message": f"Sinh {len(neighbors)} neighbor",
                "heuristic": current_value,
                "depth": current_node.depth
            })
            step += 1

            if best_neighbor is None:
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "LOCAL_MAX",
                    "message": "Stuck tai local maximum!",
                    "heuristic": current_value,
                    "depth": current_node.depth
                })
                return

            current = best_neighbor
            current_value = best_value
            current_node = Node(current, parent=current_node, action=best_action, depth=current_node.depth + 1)

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": [current_node],
                "action": "MOVE",
                "message": f"Di chuyen: {best_action} (h={best_value})",
                "heuristic": best_value,
                "depth": current_node.depth
            })
            step += 1

    def generate_steps_steepest_ascent(self, start):
        self.steps = []
        step = 1
        current = start
        current_h = self.tile_manhattan_distance(current)
        current_node = Node(current, depth=0)
        iterations = 0

        self.steps.append({
            "step": step,
            "node": current_node,
            "state": current,
            "frontier": [current_node],
            "action": "START",
            "message": f"Bat dau Steepest Ascent Hill Climbing (h={current_h})",
            "heuristic": current_h,
            "depth": "-"
        })
        step += 1

        while iterations < 1000:
            if is_goal(current):
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                return

            neighbors = []
            best_node = None
            best_h = current_h

            for action in get_actions(current):
                neighbor = execute_action(current, action)
                h_val = self.tile_manhattan_distance(neighbor)
                neighbor_node = Node(neighbor, parent=current_node, action=action, depth=current_node.depth + 1)
                neighbors.append((neighbor_node, h_val))
                if h_val < best_h:
                    best_node = neighbor_node
                    best_h = h_val

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": neighbors,
                "action": "EXPAND",
                "message": f"Sinh {len(neighbors)} neighbor, chon h nho nhat",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1

            if best_node is None:
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "LOCAL_OPTIMUM",
                    "message": "Dung tai cuc tri cuc bo",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                return

            current_node = best_node
            current = current_node.state
            current_h = best_h
            iterations += 1

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": [current_node],
                "action": "MOVE",
                "message": f"Di chuyen: {current_node.action} (h={current_h})",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1

    def generate_steps_stochastic(self, start):
        self.steps = []
        step = 1
        current = start
        current_h = self.tile_manhattan_distance(current)
        current_node = Node(current, depth=0)
        iterations = 0

        self.steps.append({
            "step": step,
            "node": current_node,
            "state": current,
            "frontier": [current_node],
            "action": "START",
            "message": f"Bat dau Stochastic Hill Climbing (h={current_h})",
            "heuristic": current_h,
            "depth": "-"
        })
        step += 1

        while iterations < 1000:
            if is_goal(current):
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                return

            better_neighbors = []
            all_neighbors = []
            for action in get_actions(current):
                neighbor = execute_action(current, action)
                h_val = self.tile_manhattan_distance(neighbor)
                neighbor_node = Node(neighbor, parent=current_node, action=action, depth=current_node.depth + 1)
                all_neighbors.append((neighbor_node, h_val))
                if h_val < current_h:
                    better_neighbors.append((neighbor_node, h_val))

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": all_neighbors,
                "action": "EXPAND",
                "message": f"Sinh {len(all_neighbors)} neighbor, co {len(better_neighbors)} tot hon",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1

            if not better_neighbors:
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "LOCAL_OPTIMUM",
                    "message": "Khong co neighbor tot hon",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                return

            current_node, current_h = random.choice(better_neighbors)
            current = current_node.state
            iterations += 1

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": [current_node],
                "action": "MOVE",
                "message": f"Chon ngau nhien: {current_node.action} (h={current_h})",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1

    def append_hill_climbing_process(self, current_node, step, max_iterations=100, prefix="HC"):
        current = current_node.state
        current_h = self.tile_manhattan_distance(current)

        for iteration in range(max_iterations):
            best_node = None
            best_h = current_h
            neighbors = []

            for action in get_actions(current):
                neighbor = execute_action(current, action)
                h_val = self.tile_manhattan_distance(neighbor)
                neighbor_node = Node(neighbor, parent=current_node, action=action, depth=current_node.depth + 1)
                neighbors.append((neighbor_node, h_val))
                if h_val < best_h:
                    best_node = neighbor_node
                    best_h = h_val

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": neighbors,
                "action": f"{prefix}_EXPAND",
                "message": f"{prefix} lap {iteration + 1}: xet {len(neighbors)} neighbor",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1

            if best_node is None:
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": f"{prefix}_STOP",
                    "message": f"{prefix}: dung tai local optimum h={current_h}",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                step += 1
                break

            current_node = best_node
            current = current_node.state
            current_h = best_h

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": [current_node],
                "action": f"{prefix}_MOVE",
                "message": f"{prefix}: di chuyen {current_node.action}, h={current_h}",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1

            if is_goal(current):
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                step += 1
                break

        return current_node, current_h, step

    def generate_steps_random_restart(self, start):
        self.steps = []
        step = 1
        best_node = None
        best_h = float("inf")
        num_restarts = 10

        self.steps.append({
            "step": step,
            "node": None,
            "state": start,
            "frontier": [],
            "action": "START",
            "message": f"Bat dau Random Restart Hill Climbing ({num_restarts} lan)",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        for restart in range(num_restarts):
            restart_state = start if restart == 0 else random_initial_state()
            restart_node = Node(restart_state, depth=0)
            restart_h = self.tile_manhattan_distance(restart_state)

            self.steps.append({
                "step": step,
                "node": restart_node,
                "state": restart_state,
                "frontier": [restart_node],
                "action": "RESTART",
                "message": f"Restart #{restart + 1} (h={restart_h})",
                "heuristic": restart_h,
                "depth": "-"
            })
            step += 1

            result_node, result_h, step = self.append_hill_climbing_process(
                restart_node,
                step,
                max_iterations=100,
                prefix=f"R{restart + 1}"
            )
            if result_h < best_h:
                best_node = result_node
                best_h = result_h

            self.steps.append({
                "step": step,
                "node": result_node,
                "state": result_node.state,
                "frontier": [result_node],
                "action": "RESULT",
                "message": f"Ket qua restart #{restart + 1}: h={result_h}",
                "heuristic": result_h,
                "depth": result_node.depth
            })
            step += 1

            if is_goal(result_node.state):
                return

        self.steps.append({
            "step": step,
            "node": best_node,
            "state": best_node.state,
            "frontier": [],
            "action": "BEST",
            "message": f"Khong thay goal, trang thai tot nhat h={best_h}",
            "heuristic": best_h,
            "depth": best_node.depth
        })

    def generate_steps_local_beam(self, start, use_hill_climbing=False):
        self.steps = []
        step = 1
        k = 3
        max_iterations = 100
        start_node = Node(start, depth=0)
        beam = [start_node]
        name = "Local Beam + Hill Climbing" if use_hill_climbing else "Local Beam Search"

        self.steps.append({
            "step": step,
            "node": start_node,
            "state": start,
            "frontier": beam.copy(),
            "action": "START",
            "message": f"Bat dau {name} (k={k})",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        for iteration in range(max_iterations):
            for node in beam:
                if is_goal(node.state):
                    self.steps.append({
                        "step": step,
                        "node": node,
                        "state": node.state,
                        "frontier": [],
                        "action": "GOAL",
                        "message": "Tim thay goal!",
                        "heuristic": 0,
                        "depth": node.depth
                    })
                    return

            successors = []
            expanded = []
            seen = set(state_to_string(node.state) for node in beam)
            for node in beam:
                for action in get_actions(node.state):
                    child_state = execute_action(node.state, action)
                    child = Node(child_state, parent=node, action=action, depth=node.depth + 1)
                    h_val = self.tile_manhattan_distance(child_state)
                    expanded.append((child, h_val))
                    if use_hill_climbing:
                        self.steps.append({
                            "step": step,
                            "node": child,
                            "state": child.state,
                            "frontier": [child],
                            "action": "HC_START",
                            "message": f"Chay Hill Climbing cho successor {action} (h={h_val})",
                            "heuristic": h_val,
                            "depth": child.depth
                        })
                        step += 1
                        child, h_val, step = self.append_hill_climbing_process(
                            child,
                            step,
                            max_iterations=50,
                            prefix="BEAM_HC"
                        )
                    child_key = state_to_string(child.state)
                    if child_key not in seen:
                        successors.append((child, h_val))
                        seen.add(child_key)

            self.steps.append({
                "step": step,
                "node": beam[0] if beam else None,
                "state": beam[0].state if beam else start,
                "frontier": expanded,
                "action": "EXPAND",
                "message": f"Lap {iteration + 1}: mo rong {len(beam)} state, sinh {len(expanded)} successor",
                "heuristic": "-",
                "depth": beam[0].depth if beam else "-"
            })
            step += 1

            successors.sort(key=lambda item: item[1])
            beam = [node for node, _ in successors[:k]]

            self.steps.append({
                "step": step,
                "node": beam[0] if beam else None,
                "state": beam[0].state if beam else start,
                "frontier": [(node, h_val) for node, h_val in successors[:k]],
                "action": "ITERATION",
                "message": f"Lap {iteration + 1}: sinh {len(successors)} successor, giu {len(beam)} tot nhat",
                "heuristic": successors[0][1] if successors else "-",
                "depth": beam[0].depth if beam else "-"
            })
            step += 1

            if not successors or len(set(state_to_string(node.state) for node in beam)) <= 1:
                break

        best = beam[0] if beam else start_node
        best_h = self.tile_manhattan_distance(best.state)
        self.steps.append({
            "step": step,
            "node": best,
            "state": best.state,
            "frontier": [],
            "action": "BEST",
            "message": f"Khong thay goal, trang thai tot nhat h={best_h}",
            "heuristic": best_h,
            "depth": best.depth
        })

    def generate_steps_simulated_annealing(self, start):
        self.steps = []
        step = 1
        current = start
        current_h = self.tile_manhattan_distance(current)
        best = copy.deepcopy(current)
        best_h = current_h
        temperature = 100.0
        cooling_rate = 0.95
        min_temperature = 0.01
        max_iterations = 300
        current_node = Node(current, depth=0)

        self.steps.append({
            "step": step,
            "node": current_node,
            "state": current,
            "frontier": [current_node],
            "action": "START",
            "message": f"Bat dau Simulated Annealing (h={current_h}, T={temperature:.2f})",
            "heuristic": current_h,
            "depth": "-"
        })
        step += 1

        for iteration in range(1, max_iterations + 1):
            if is_goal(current):
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth
                })
                return

            if temperature < min_temperature:
                break

            action = random.choice(get_actions(current))
            next_state = execute_action(current, action)
            next_h = self.tile_manhattan_distance(next_state)
            delta = current_h - next_h

            if delta >= 0:
                accepted = True
                probability = 1.0
            else:
                probability = math.exp(delta / temperature)
                accepted = random.random() < probability

            next_node = Node(next_state, parent=current_node, action=action, depth=current_node.depth + 1)
            decision = "accepted" if accepted else "rejected"

            if accepted:
                current = next_state
                current_h = next_h
                current_node = next_node

                if current_h < best_h:
                    best = copy.deepcopy(current)
                    best_h = current_h

            self.steps.append({
                "step": step,
                "node": current_node,
                "state": current,
                "frontier": [(next_node, next_h)],
                "action": "ANNEAL",
                "message": f"Lap {iteration}: {action}, h {self.tile_manhattan_distance(next_node.parent.state)}->{next_h}, T={temperature:.2f}, P={probability:.3f}, {decision}",
                "heuristic": current_h,
                "depth": current_node.depth
            })
            step += 1
            temperature *= cooling_rate

        best_node = Node(best, depth=0)
        self.steps.append({
            "step": step,
            "node": best_node,
            "state": best,
            "frontier": [],
            "action": "BEST",
            "message": f"Khong thay goal, trang thai tot nhat h={best_h}",
            "heuristic": best_h,
            "depth": "-"
        })

    def generate_steps_belief_greedy(self):
        self.steps = []
        step = 1
        counter = 0
        start = self.random_belief_state(size=3)
        start_cost = self.belief_cost(start)
        frontier = [(start_cost, counter, start, [])]
        visited = {self.belief_to_string(start)}
        expansions = 0
        max_expansions = 5000

        self.steps.append({
            "step": step,
            "node": None,
            "state": start[0],
            "belief": start,
            "frontier": [{"belief": start, "cost": start_cost, "path": []}],
            "action": "START",
            "message": f"Bat dau Greedy Belief State, h(n)={start_cost}",
            "heuristic": start_cost,
            "depth": "-"
        })
        step += 1

        while frontier and expansions < max_expansions:
            cost, _, belief_state, actions_taken = heapq.heappop(frontier)
            expansions += 1

            self.steps.append({
                "step": step,
                "node": None,
                "state": belief_state[0],
                "belief": belief_state,
                "frontier": [{"belief": belief_state, "cost": cost, "path": actions_taken}],
                "action": "POP",
                "message": f"Mo rong belief #{expansions}, path={actions_taken if actions_taken else 'START'}, h(n)={cost}",
                "heuristic": cost,
                "depth": len(actions_taken)
            })
            step += 1

            if self.is_belief_goal(belief_state):
                self.steps.append({
                    "step": step,
                    "node": None,
                    "state": belief_state[0],
                    "belief": belief_state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Ca 3 trang thai deu ve goal. Path={actions_taken}",
                    "heuristic": 0,
                    "depth": len(actions_taken)
                })
                return

            candidates = []
            for action in self.all_actions():
                next_belief = self.execute_belief_action(belief_state, action)
                next_key = self.belief_to_string(next_belief)
                if next_key in visited:
                    continue

                visited.add(next_key)
                next_cost = self.belief_cost(next_belief)
                next_path = actions_taken + [action]
                counter += 1
                heapq.heappush(frontier, (next_cost, counter, next_belief, next_path))
                candidates.append({
                    "belief": next_belief,
                    "cost": next_cost,
                    "path": next_path,
                    "action": action
                })

            candidates.sort(key=lambda item: item["cost"])
            self.steps.append({
                "step": step,
                "node": None,
                "state": belief_state[0],
                "belief": belief_state,
                "frontier": candidates,
                "action": "EXPAND",
                "message": f"Sinh {len(candidates)} belief moi, chon theo h(n) nho nhat",
                "heuristic": cost,
                "depth": len(actions_taken)
            })
            step += 1

        self.steps.append({
            "step": step,
            "node": None,
            "state": start[0],
            "belief": start,
            "frontier": [],
            "action": "FAILED",
            "message": "Khong tim thay goal belief trong gioi han",
            "heuristic": "-",
            "depth": "-"
        })

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

        self.algo_menu = ctk.CTkComboBox(algo_frame, values=[
            "BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "IDA*", "Hill Climbing",
            "Steepest Ascent", "Stochastic", "Random Restart", "Local Beam", "Local Beam + HC",
            "Simulated Annealing", "Belief State"
        ],
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
        elif self.algorithm == "UCS":
            self.solver.generate_steps_ucs(self.initial_state)
        elif self.algorithm == "Greedy":
            self.solver.generate_steps_greedy(self.initial_state)
        elif self.algorithm == "A*":
            self.solver.generate_steps_astar(self.initial_state)
        elif self.algorithm == "IDA*":
            self.solver.generate_steps_ida_star(self.initial_state)
        elif self.algorithm == "Hill Climbing":
            self.solver.generate_steps_hill_climbing(self.initial_state)
        elif self.algorithm == "Steepest Ascent":
            self.solver.generate_steps_steepest_ascent(self.initial_state)
        elif self.algorithm == "Stochastic":
            self.solver.generate_steps_stochastic(self.initial_state)
        elif self.algorithm == "Random Restart":
            self.solver.generate_steps_random_restart(self.initial_state)
        elif self.algorithm == "Local Beam":
            self.solver.generate_steps_local_beam(self.initial_state)
        elif self.algorithm == "Local Beam + HC":
            self.solver.generate_steps_local_beam(self.initial_state, use_hill_climbing=True)
        elif self.algorithm == "Simulated Annealing":
            self.solver.generate_steps_simulated_annealing(self.initial_state)
        elif self.algorithm == "Belief State":
            self.solver.generate_steps_belief_greedy()
        
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
        for i, item in enumerate(data.get("frontier", [])):
            if isinstance(item, Node):
                node = item
                state_str = str(node.state).replace(", ", ",")
                frontier_text += f"{i+1}. {state_str} (d={node.depth})\n"
            elif isinstance(item, tuple):
                node, value = item
                state_str = str(node.state).replace(", ", ",")
                frontier_text += f"{i+1}. {state_str} (h={value})\n"
            elif isinstance(item, dict) and "belief" in item:
                frontier_text += f"{i+1}. h={item.get('cost')} path={item.get('path', [])}\n"
                for state_index, state in enumerate(item["belief"], start=1):
                    state_str = str(state).replace(", ", ",")
                    frontier_text += f"   State {state_index}: {state_str}\n"
                frontier_text += "\n"
        
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
