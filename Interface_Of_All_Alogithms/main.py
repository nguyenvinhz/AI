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
        
        start_cost = 0
        start_node = Node(start, depth=0)
        heapq.heappush(heap, (start_cost, counter, state_to_string(start), start_node))
        best_cost = {state_to_string(start): 0}
        
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
            cost, _, _, node = heapq.heappop(heap)
            node_key = state_to_string(node.state)
            if node_key in visited:
                continue
            visited.add(node_key)
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "POP",
                "message": "Lấy node với cost thấp nhất",
                "cost": cost,
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
                    "cost": cost,
                    "depth": node.depth,
                    "solution": self.solution
                })
                return
            
            children = []
            for action in get_actions(node.state):
                child_state = execute_action(node.state, action)
                child_key = state_to_string(child_state)
                
                child_cost = cost + 1
                if child_key not in visited and child_cost < best_cost.get(child_key, float("inf")):
                    best_cost[child_key] = child_cost
                    child = Node(child_state, parent=node, action=action, depth=node.depth + 1)
                    children.append(child)
                    counter += 1
                    heapq.heappush(heap, (child_cost, counter, child_key, child))
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "cost": cost,
                "depth": node.depth
            })
            step += 1

    def generate_steps_greedy(self, start):
        self.steps = []
        step = 1
        heap = []
        visited = set()
        counter = 0
        
        start_heuristic = self.tile_manhattan_distance(start)
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
                "heuristic": self.tile_manhattan_distance(node.state),
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
                    "heuristic": self.tile_manhattan_distance(node.state),
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
                    child_heuristic = self.tile_manhattan_distance(child_state)
                    counter += 1
                    heapq.heappush(heap, (child_heuristic, counter, child_key, child))
            
            self.steps.append({
                "step": step,
                "node": node,
                "state": node.state,
                "frontier": [n for _, _, _, n in heap],
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con",
                "heuristic": self.tile_manhattan_distance(node.state),
                "depth": node.depth
            })
            step += 1

    def generate_steps_astar(self, start):
        self.steps = []
        step = 1
        heap = []
        closed = set()
        best_g = {}
        counter = 0
        
        start_h = self.tile_manhattan_distance(start)
        start_g = 0
        start_f = start_g + start_h
        start_node = Node(start, depth=0)
        heapq.heappush(heap, (start_f, counter, state_to_string(start), start_node))
        best_g[state_to_string(start)] = 0
        
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
            node_key = state_to_string(node.state)
            if node_key in closed:
                continue
            closed.add(node_key)
            
            g_n = node.depth
            h_n = self.tile_manhattan_distance(node.state)
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
                
                child_g = node.depth + 1
                if child_key not in closed and child_g < best_g.get(child_key, float("inf")):
                    best_g[child_key] = child_g
                    child = Node(child_state, parent=node, action=action, depth=node.depth + 1)
                    children.append(child)
                    child_h = self.tile_manhattan_distance(child_state)
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
        return self.tile_manhattan_distance(state)

    def generate_steps_ida_star(self, start):
        self.steps = []
        self.solution = []
        step = 1
        limit = self.heuristic_ida_star(start)

        def dfs(current, path_keys, g_limit):
            nonlocal step
            h_val = self.heuristic_ida_star(current.state)
            f_val = current.depth + h_val

            self.steps.append({
                "step": step,
                "node": current,
                "state": current.state,
                "frontier": [current],
                "action": "POP",
                "message": f"Xét trạng thái: f(n) = g(n) + h(n) = {current.depth} + {h_val} = {f_val} | Threshold = {g_limit}",
                "threshold": g_limit,
                "depth": current.depth
            })
            step += 1

            if f_val > g_limit:
                self.steps.append({
                    "step": step,
                    "node": current,
                    "state": current.state,
                    "frontier": [],
                    "action": "CUTOFF",
                    "message": f"Vượt ngưỡng: f(n) = {f_val} > Threshold = {g_limit}. Quay lui!",
                    "threshold": g_limit,
                    "depth": current.depth
                })
                step += 1
                return None, f_val

            if is_goal(current.state):
                return current, f_val

            min_next_limit = float("inf")
            children = []
            for action in get_actions(current.state):
                child_state = execute_action(current.state, action)
                child_key = state_to_string(child_state)
                if child_key in path_keys:
                    continue
                child = Node(child_state, parent=current, action=action, depth=current.depth + 1)
                children.append(child)

            self.steps.append({
                "step": step,
                "node": current,
                "state": current.state,
                "frontier": children,
                "action": "EXPAND",
                "message": f"Sinh {len(children)} node con | Threshold = {g_limit}",
                "threshold": g_limit,
                "depth": current.depth
            })
            step += 1

            for child in children:
                result, next_limit = dfs(child, path_keys | {state_to_string(child.state)}, g_limit)
                if result is not None:
                    return result, next_limit
                min_next_limit = min(min_next_limit, next_limit)

            return None, min_next_limit

        while limit < 80:
            start_node = Node(start, depth=0)
            
            self.steps.append({
                "step": step,
                "node": None,
                "state": start,
                "frontier": [start_node],
                "action": "START",
                "message": f"IDA* - Bắt đầu Threshold = {limit}",
                "threshold": limit,
                "depth": "-"
            })
            step += 1
            
            result_node, new_threshold = dfs(start_node, {state_to_string(start)}, limit)
            
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
            limit = new_threshold

    def generate_steps_hill_climbing(self, start):
        self.steps = []
        step = 1
        current = start
        current_value = self.tile_manhattan_distance(current)
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
                value = self.tile_manhattan_distance(neighbor)
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
                self.solution = get_solution(current_node)
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth,
                    "solution": self.solution
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
                self.solution = get_solution(current_node)
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth,
                    "solution": self.solution
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
                self.solution = get_solution(current_node)
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth,
                    "solution": self.solution
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
                self.solution = get_solution(result_node)
                self.steps.append({
                    "step": step,
                    "node": result_node,
                    "state": result_node.state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tim thay goal o restart #{restart + 1}",
                    "heuristic": 0,
                    "depth": result_node.depth,
                    "solution": self.solution
                })
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
                    self.solution = get_solution(node)
                    self.steps.append({
                        "step": step,
                        "node": node,
                        "state": node.state,
                        "frontier": [],
                        "action": "GOAL",
                        "message": "Tim thay goal!",
                        "heuristic": 0,
                        "depth": node.depth,
                        "solution": self.solution
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
                self.solution = get_solution(current_node)
                self.steps.append({
                    "step": step,
                    "node": current_node,
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": "Tim thay goal!",
                    "heuristic": current_h,
                    "depth": current_node.depth,
                    "solution": self.solution
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
                    "depth": len(actions_taken),
                    "solution": actions_taken
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

    def run_belief_plan(self, belief_state, plan):
        current = copy.deepcopy(belief_state)
        trace = [self.belief_to_string(current)]

        for action in plan:
            current = self.execute_belief_action(current, action)
            trace.append(self.belief_to_string(current))

        return current, trace

    def random_belief_state(self, size=3, plan_length=7, max_attempts=1000):
        for _ in range(max_attempts):
            plan = self.random_plan(plan_length)
            belief_state = []
            seen = set()

            while len(belief_state) < size:
                state = self.make_state_from_plan(plan)
                if state is None:
                    break

                key = state_to_string(state)
                if key not in seen and state != GOAL_STATE and self.run_plan(state, plan) == GOAL_STATE:
                    belief_state.append(state)
                    seen.add(key)

            if len(belief_state) == size:
                final_belief, trace = self.run_belief_plan(belief_state, plan)
                if self.is_belief_goal(final_belief) and len(trace) == len(set(trace)):
                    return belief_state

        return self.random_belief_state(size, max(3, plan_length - 1), max_attempts)

    def generate_steps_belief_bs_bg_dfs(self):
        self.steps = []
        step = 1
        start = self.random_belief_state(size=3)
        stack = [(start, [])]
        explored = set()
        max_depth = 20
        max_nodes = 4000

        self.steps.append({
            "step": step,
            "node": None,
            "state": start[0],
            "belief": start,
            "frontier": [{"belief": start, "cost": self.belief_cost(start), "path": []}],
            "action": "START",
            "message": "Bat dau Belief State BS-BG DFS",
            "heuristic": self.belief_cost(start),
            "depth": "-"
        })
        step += 1

        while stack and len(explored) < max_nodes:
            belief_state, actions_taken = stack.pop()
            belief_key = self.belief_to_string(belief_state)
            if belief_key in explored:
                continue

            explored.add(belief_key)
            self.steps.append({
                "step": step,
                "node": None,
                "state": belief_state[0],
                "belief": belief_state,
                "frontier": [{"belief": belief_state, "cost": self.belief_cost(belief_state), "path": actions_taken}],
                "action": actions_taken[-1] if actions_taken else "POP",
                "message": f"Node {len(explored)} | Frontier={len(stack)} | Explored={len(explored)} | Path={actions_taken if actions_taken else 'START'}",
                "heuristic": self.belief_cost(belief_state),
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
                    "message": f"Ca 3 trang thai deu nam trong BG. Path={actions_taken}",
                    "heuristic": 0,
                    "depth": len(actions_taken),
                    "solution": actions_taken
                })
                return

            if len(actions_taken) < max_depth:
                actions = sorted(
                    self.all_actions(),
                    key=lambda action: self.belief_cost(self.execute_belief_action(belief_state, action))
                )
                for action in reversed(actions):
                    next_belief = self.execute_belief_action(belief_state, action)
                    next_key = self.belief_to_string(next_belief)
                    if next_key not in explored:
                        stack.append((next_belief, actions_taken + [action]))

        self.steps.append({
            "step": step,
            "node": None,
            "state": start[0],
            "belief": start,
            "frontier": [],
            "action": "FAILED",
            "message": "Khong tim thay BG trong gioi han DFS",
            "heuristic": "-",
            "depth": "-"
        })

    def generate_steps_nondeterministic_heuristic(self):
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
            "message": f"Bat dau tim kiem khong xac dinh theo heuristic, h(n)={start_cost}",
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
                "message": f"Mo rong belief #{expansions}, h(n)={cost}, path={actions_taken if actions_taken else 'START'}",
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
                    "message": f"Dat goal voi path={actions_taken}",
                    "heuristic": 0,
                    "depth": len(actions_taken),
                    "solution": actions_taken
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
                "message": f"Sinh {len(candidates)} ket qua, uu tien h(n) nho nhat",
                "heuristic": cost,
                "depth": len(actions_taken)
            })
            step += 1

    def random_and_or_initial_state(self, plan_length=5):
        state = copy.deepcopy(GOAL_STATE)
        scramble_actions = []
        previous_action = None

        while len(scramble_actions) < plan_length:
            choices = get_actions(state)
            if previous_action:
                reverse = self.opposite_action(previous_action)
                filtered = [action for action in choices if action != reverse]
                if filtered:
                    choices = filtered

            action = random.choice(choices)
            state = execute_action(state, action)
            scramble_actions.append(action)
            previous_action = action
        return state

    def generate_steps_and_or_graph_search(self):
        self.steps = []
        step = 1
        start = self.random_and_or_initial_state()
        max_depth = 15
        path_states = set()

        self.steps.append({
            "step": step,
            "node": Node(start, depth=0),
            "state": start,
            "frontier": [],
            "action": "START",
            "message": "Bat dau AND-OR Graph Search",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        def or_search(state, depth, path_actions):
            nonlocal step
            state_key = state_to_string(state)
            self.steps.append({
                "step": step,
                "node": Node(state, depth=depth),
                "state": state,
                "frontier": [],
                "action": "OR_SEARCH",
                "message": f"OR_SEARCH depth={depth}: state={state_key}",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": depth
            })
            step += 1

            if is_goal(state):
                return path_actions, state
            if depth >= max_depth or state_key in path_states:
                return None, state

            path_states.add(state_key)
            actions = sorted(
                get_actions(state),
                key=lambda action: self.tile_manhattan_distance(execute_action(state, action))
            )

            for action in actions:
                result = execute_action(state, action)
                self.steps.append({
                    "step": step,
                    "node": Node(result, depth=depth + 1),
                    "state": result,
                    "frontier": [{"state": result, "action": action}],
                    "action": "AND_SEARCH",
                    "message": f"AND_SEARCH: action={action}, result_states=1",
                    "heuristic": self.tile_manhattan_distance(result),
                    "depth": depth + 1
                })
                step += 1

                result_path, result_state = or_search(result, depth + 1, path_actions + [action])
                if result_path is not None:
                    return result_path, result_state

            path_states.remove(state_key)
            return None, state

        path, final_state = or_search(start, 0, [])
        final_action = "GOAL" if path is not None and is_goal(final_state) else "FAILED"
        final_message = f"Tim thay goal. Plan={path}" if final_action == "GOAL" else "AND-OR khong tim thay goal"
        self.steps.append({
            "step": step,
            "node": Node(final_state, depth=len(path) if path else 0),
            "state": final_state,
            "frontier": [],
            "action": final_action,
            "message": final_message,
            "heuristic": self.tile_manhattan_distance(final_state),
            "depth": len(path) if path else "-",
            "solution": path if path else []
        })

    def random_initial_state(self, depth=10):
        state = copy.deepcopy(GOAL_STATE)
        previous_action = None

        for _ in range(depth):
            actions = get_actions(state)
            if previous_action:
                reverse = self.opposite_action(previous_action)
                filtered = [action for action in actions if action != reverse]
                if filtered:
                    actions = filtered

            action = random.choice(actions)
            state = execute_action(state, action)
            previous_action = action
        return state

    def prioritized_actions(self, state, path):
        actions = get_actions(state)
        if path:
            reverse = self.opposite_action(path[-1])
            actions = [action for action in actions if action != reverse]

        return sorted(actions, key=lambda action: self.tile_manhattan_distance(execute_action(state, action)))

    def generate_steps_backtracking_csp(self):
        self.steps = []
        step = 1
        start = self.random_initial_state(depth=10)
        stack = [(start, [], {state_to_string(start)})]
        limit = 20

        self.steps.append({
            "step": step,
            "node": Node(start, depth=0),
            "state": start,
            "frontier": [Node(start, depth=0)],
            "action": "START",
            "message": "Bat dau Backtracking Search",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        while stack:
            state, path, visited = stack.pop()
            node = Node(state, action=path[-1] if path else None, depth=len(path))

            self.steps.append({
                "step": step,
                "node": node,
                "state": state,
                "frontier": [Node(item[0], depth=len(item[1])) for item in stack[-8:]],
                "action": "POP",
                "message": f"Xet node depth={len(path)}, h(n)={self.tile_manhattan_distance(state)}, path={path if path else 'START'}",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": len(path)
            })
            step += 1

            if is_goal(state):
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tim thay goal. Path={path}",
                    "heuristic": 0,
                    "depth": len(path),
                    "solution": path
                })
                return

            if len(path) >= limit:
                continue

            children = []
            for action in reversed(self.prioritized_actions(state, path)):
                next_state = execute_action(state, action)
                key = state_to_string(next_state)
                if key in visited:
                    continue
                children.append(Node(next_state, action=action, depth=len(path) + 1))
                stack.append((next_state, path + [action], visited | {key}))

            self.steps.append({
                "step": step,
                "node": node,
                "state": state,
                "frontier": children,
                "action": "EXPAND",
                "message": f"Thu cac phep gan hop le, sinh {len(children)} node con",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": len(path)
            })
            step += 1

    def generate_steps_forward_checking_csp(self):
        self.steps = []
        step = 1
        start = self.random_initial_state(depth=10)
        stack = [(start, [], {state_to_string(start)})]
        limit = 20

        self.steps.append({
            "step": step,
            "node": Node(start, depth=0),
            "state": start,
            "frontier": [Node(start, depth=0)],
            "action": "START",
            "message": "Bat dau Forward Checking",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        while stack:
            state, path, visited = stack.pop()
            node = Node(state, action=path[-1] if path else None, depth=len(path))

            self.steps.append({
                "step": step,
                "node": node,
                "state": state,
                "frontier": [Node(item[0], depth=len(item[1])) for item in stack[-8:]],
                "action": "POP",
                "message": f"Xet node depth={len(path)}, h(n)={self.tile_manhattan_distance(state)}",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": len(path)
            })
            step += 1

            if is_goal(state):
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tim thay goal. Path={path}",
                    "heuristic": 0,
                    "depth": len(path),
                    "solution": path
                })
                return

            if len(path) >= limit:
                continue

            candidates = []
            for action in self.prioritized_actions(state, path):
                next_state = execute_action(state, action)
                key = state_to_string(next_state)
                if key in visited:
                    continue

                next_domain = [
                    next_action
                    for next_action in get_actions(next_state)
                    if not path or next_action != self.opposite_action(action)
                ]
                if not next_domain and not is_goal(next_state):
                    continue

                candidates.append((action, next_state, key, next_domain))

            for action, next_state, key, _ in reversed(candidates):
                stack.append((next_state, path + [action], visited | {key}))

            self.steps.append({
                "step": step,
                "node": node,
                "state": state,
                "frontier": [(Node(item[1], action=item[0], depth=len(path) + 1), len(item[3])) for item in candidates],
                "action": "FORWARD_CHECK",
                "message": f"Kiem tra mien buoc ke, giu {len(candidates)} action hop le",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": len(path)
            })
            step += 1

    def ac3_action_domains(self, domains):
        queue = deque((index, index + 1) for index in range(len(domains) - 1))
        while queue:
            xi, xj = queue.popleft()
            revised = False
            for action in domains[xi][:]:
                supported = any(self.opposite_action(action) != other for other in domains[xj])
                if not supported:
                    domains[xi].remove(action)
                    revised = True
            if revised:
                if not domains[xi]:
                    return False
                if xi > 0:
                    queue.append((xi - 1, xi))
        return True

    def generate_steps_arc_consistency_csp(self):
        self.steps = []
        step = 1
        start = self.random_initial_state(depth=10)
        limit = 20
        base_domains = {index: self.all_actions()[:] for index in range(limit)}
        self.ac3_action_domains(base_domains)
        stack = [(start, [], {state_to_string(start)}, base_domains)]

        self.steps.append({
            "step": step,
            "node": Node(start, depth=0),
            "state": start,
            "frontier": [Node(start, depth=0)],
            "action": "START",
            "message": "Bat dau Arc Consistency AC-3",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        while stack:
            state, path, visited, domains = stack.pop()
            depth = len(path)
            node = Node(state, action=path[-1] if path else None, depth=depth)

            self.steps.append({
                "step": step,
                "node": node,
                "state": state,
                "frontier": [Node(item[0], depth=len(item[1])) for item in stack[-8:]],
                "action": "POP",
                "message": f"Xet X{depth}, domain={domains.get(depth, [])}, h(n)={self.tile_manhattan_distance(state)}",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": depth
            })
            step += 1

            if is_goal(state):
                self.steps.append({
                    "step": step,
                    "node": node,
                    "state": state,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tim thay goal. Path={path}",
                    "heuristic": 0,
                    "depth": depth,
                    "solution": path
                })
                return

            if depth >= limit:
                continue

            domain = [action for action in self.prioritized_actions(state, path) if action in domains[depth]]
            candidates = []
            for action in domain:
                next_state = execute_action(state, action)
                key = state_to_string(next_state)
                if key in visited:
                    continue

                next_domains = {index: values[:] for index, values in domains.items()}
                next_domains[depth] = [action]
                if depth + 1 < limit and self.opposite_action(action) in next_domains[depth + 1]:
                    next_domains[depth + 1].remove(self.opposite_action(action))
                if not self.ac3_action_domains(next_domains):
                    continue

                candidates.append((action, next_state, key, next_domains))

            for action, next_state, key, next_domains in reversed(candidates):
                stack.append((next_state, path + [action], visited | {key}, next_domains))

            self.steps.append({
                "step": step,
                "node": node,
                "state": state,
                "frontier": [Node(item[1], action=item[0], depth=depth + 1) for item in candidates],
                "action": "AC3",
                "message": f"Gan action va chay AC-3, con {len(candidates)} nhanh hop le",
                "heuristic": self.tile_manhattan_distance(state),
                "depth": depth
            })
            step += 1

    def score_action_plan(self, start, plan):
        state = copy.deepcopy(start)
        invalid = 0
        for index, action in enumerate(plan):
            if action not in get_actions(state):
                invalid += 5
                continue
            if index > 0 and action == self.opposite_action(plan[index - 1]):
                invalid += 1
            state = execute_action(state, action)
        return self.tile_manhattan_distance(state) + invalid, state

    def generate_steps_min_conflicts_csp(self):
        self.steps = []
        step = 1
        start = self.random_initial_state(depth=10)
        plan_length = 20
        max_steps = 120
        max_restarts = 6
        best_plan = None
        best_state = start
        best_score = float("inf")

        self.steps.append({
            "step": step,
            "node": Node(start, depth=0),
            "state": start,
            "frontier": [],
            "action": "START",
            "message": "Bat dau Min-Conflicts. Trang thai duoc tao tu xao tron",
            "heuristic": self.tile_manhattan_distance(start),
            "depth": "-"
        })
        step += 1

        for restart in range(1, max_restarts + 1):
            plan = [random.choice(self.all_actions()) for _ in range(plan_length)]
            self.steps.append({
                "step": step,
                "node": Node(start, depth=0),
                "state": start,
                "frontier": [],
                "action": "RESTART",
                "message": f"Khoi dong lai #{restart}, plan ngau nhien={plan}",
                "heuristic": self.tile_manhattan_distance(start),
                "depth": "-"
            })
            step += 1

            for iteration in range(1, max_steps + 1):
                score, current_state = self.score_action_plan(start, plan)
                if score < best_score:
                    best_score = score
                    best_plan = plan[:]
                    best_state = current_state

                self.steps.append({
                    "step": step,
                    "node": Node(current_state, depth=len(plan)),
                    "state": current_state,
                    "frontier": [],
                    "action": "EVALUATE",
                    "message": f"Restart {restart}, lap {iteration}: diem={score}, h(n)={self.tile_manhattan_distance(current_state)}",
                    "heuristic": self.tile_manhattan_distance(current_state),
                    "depth": iteration
                })
                step += 1

                if is_goal(current_state):
                    self.steps.append({
                        "step": step,
                        "node": Node(current_state, depth=len(plan)),
                        "state": current_state,
                        "frontier": [],
                        "action": "GOAL",
                        "message": f"Plan dat goal. Path={plan}",
                        "heuristic": 0,
                        "depth": iteration,
                        "solution": plan
                    })
                    return

                current_score = score
                conflict_indexes = []
                for index in range(len(plan)):
                    scores = []
                    for action in self.all_actions():
                        candidate_plan = plan[:]
                        candidate_plan[index] = action
                        candidate_score, _ = self.score_action_plan(start, candidate_plan)
                        scores.append(candidate_score)
                    if min(scores) < current_score:
                        conflict_indexes.append(index)

                index = random.choice(conflict_indexes) if conflict_indexes else random.randrange(len(plan))
                candidates = []
                for action in self.all_actions():
                    candidate_plan = plan[:]
                    candidate_plan[index] = action
                    candidate_score, candidate_state = self.score_action_plan(start, candidate_plan)
                    candidates.append((candidate_score, action, candidate_state))

                candidates.sort(key=lambda item: item[0])
                min_score = candidates[0][0]
                best = random.choice([item for item in candidates if item[0] == min_score])
                plan[index] = best[1]

                self.steps.append({
                    "step": step,
                    "node": Node(best[2], depth=len(plan)),
                    "state": best[2],
                    "frontier": [(Node(item[2], action=item[1], depth=len(plan)), item[0]) for item in candidates],
                    "action": "MIN_CONFLICT",
                    "message": f"Doi bien X{index} thanh {best[1]}, diem tot nhat={min_score}",
                    "heuristic": self.tile_manhattan_distance(best[2]),
                    "depth": iteration
                })
                step += 1

        self.steps.append({
            "step": step,
            "node": Node(best_state, depth=len(best_plan) if best_plan else 0),
            "state": best_state,
            "frontier": [],
            "action": "BEST",
            "message": f"Chua tim thay goal, plan tot nhat co diem={best_score}: {best_plan}",
            "heuristic": self.tile_manhattan_distance(best_state),
            "depth": "-"
        })

    def evaluate_state(self, state):
        if state == GOAL_STATE:
            return 100
        return -self.tile_manhattan_distance(state)

    def ordered_actions_local(self, state, previous_action=None):
        actions = get_actions(state)
        if previous_action:
            opp = self.opposite_action(previous_action)
            if opp in actions:
                actions.remove(opp)
        return sorted(actions, key=lambda action: self.tile_manhattan_distance(execute_action(state, action)))

    def minimax_search(self, state, depth, maximizing_player, visited, previous_action=None):
        if state == GOAL_STATE or depth == 0:
            return self.evaluate_state(state)

        actions = self.ordered_actions_local(state, previous_action)
        if not actions:
            return self.evaluate_state(state)

        if maximizing_player:
            best_value = -float("inf")
            for action in actions:
                next_state = execute_action(state, action)
                key = state_to_string(next_state)
                if key in visited:
                    continue
                visited.add(key)
                value = self.minimax_search(next_state, depth - 1, False, visited, action)
                visited.remove(key)
                best_value = max(best_value, value)
            return best_value if best_value != -float("inf") else self.evaluate_state(state)

        best_value = float("inf")
        for action in actions:
            next_state = execute_action(state, action)
            key = state_to_string(next_state)
            if key in visited:
                continue
            visited.add(key)
            value = self.minimax_search(next_state, depth - 1, True, visited, action)
            visited.remove(key)
            best_value = min(best_value, value)
        return best_value if best_value != float("inf") else self.evaluate_state(state)

    def alphabeta_search(self, state, depth, alpha, beta, visited, previous_action=None):
        if state == GOAL_STATE or depth == 0:
            return self.evaluate_state(state)

        actions = self.ordered_actions_local(state, previous_action)
        if not actions:
            return self.evaluate_state(state)

        best_value = -float("inf")
        for action in actions:
            next_state = execute_action(state, action)
            key = state_to_string(next_state)
            if key in visited:
                continue
            visited.add(key)
            value = self.alphabeta_search(next_state, depth - 1, alpha, beta, visited, action)
            visited.remove(key)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value if best_value != -float("inf") else self.evaluate_state(state)

    def expectimax_search(self, state, depth, maximizing_player, visited, previous_action=None):
        if state == GOAL_STATE or depth == 0:
            return self.evaluate_state(state)

        actions = self.ordered_actions_local(state, previous_action)
        if not actions:
            return self.evaluate_state(state)

        if maximizing_player:
            best_value = -float("inf")
            for action in actions:
                next_state = execute_action(state, action)
                key = state_to_string(next_state)
                if key in visited:
                    continue
                visited.add(key)
                value = self.expectimax_search(next_state, depth - 1, False, visited, action)
                visited.remove(key)
                best_value = max(best_value, value)
            return best_value if best_value != -float("inf") else self.evaluate_state(state)

        total = 0
        count = 0
        for action in actions:
            next_state = execute_action(state, action)
            key = state_to_string(next_state)
            if key in visited:
                continue
            visited.add(key)
            total += self.expectimax_search(next_state, depth - 1, True, visited, action)
            visited.remove(key)
            count += 1

        return total / count if count > 0 else self.evaluate_state(state)

    def generate_steps_minimax(self, start):
        self.steps = []
        self.solution = []
        step = 1
        current = copy.deepcopy(start)
        path = []
        previous_action = None
        visited = {state_to_string(current)}
        depth = 6
        max_steps = 30

        nodes_path = [Node(current, depth=0)]

        for step_idx in range(max_steps):
            self.steps.append({
                "step": step,
                "node": nodes_path[-1],
                "state": current,
                "frontier": [nodes_path[-1]],
                "action": previous_action if previous_action else "START",
                "message": f"Minimax - Bước {step_idx}: h(n)={self.tile_manhattan_distance(current)}, đường đi={path if path else 'START'}",
                "depth": len(path)
            })
            step += 1

            if is_goal(current):
                self.solution = nodes_path
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tìm thấy goal bằng Minimax! Số bước: {len(path)}",
                    "depth": len(path),
                    "solution": self.solution
                })
                return

            actions = self.ordered_actions_local(current, previous_action)
            best_action = None
            best_value = -float("inf")
            frontier_candidates = []

            for action in actions:
                next_state = execute_action(current, action)
                key = state_to_string(next_state)
                search_visited = visited.copy()
                search_visited.add(key)
                
                value = self.minimax_search(next_state, depth - 1, False, search_visited, action)
                neighbor_node = Node(next_state, parent=nodes_path[-1], action=action, depth=len(path) + 1)
                frontier_candidates.append((neighbor_node, value))

                if value > best_value:
                    best_value = value
                    best_action = action

            if best_action is None:
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "FAILED",
                    "message": "Không có nước đi khả thi (Thất bại)",
                    "depth": len(path)
                })
                return

            self.steps.append({
                "step": step,
                "node": nodes_path[-1],
                "state": current,
                "frontier": frontier_candidates,
                "action": "EVALUATE",
                "message": f"Thử các nước đi. Chọn {best_action} (value={best_value})",
                "depth": len(path)
            })
            step += 1

            next_state = execute_action(current, best_action)
            key = state_to_string(next_state)
            if key in visited:
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "FAILED",
                    "message": f"Trùng trạng thái đã đi qua khi chọn {best_action} (Thất bại)",
                    "depth": len(path)
                })
                return

            current = next_state
            visited.add(key)
            path.append(best_action)
            nodes_path.append(Node(current, parent=nodes_path[-1], action=best_action, depth=len(path)))
            previous_action = best_action

        self.steps.append({
            "step": step,
            "node": nodes_path[-1],
            "state": current,
            "frontier": [],
            "action": "FAILED",
            "message": "Đạt giới hạn bước đi tối đa mà không tìm thấy goal",
            "depth": len(path)
        })

    def generate_steps_alphabeta(self, start):
        self.steps = []
        self.solution = []
        step = 1
        current = copy.deepcopy(start)
        path = []
        previous_action = None
        visited = {state_to_string(current)}
        depth = 8
        max_steps = 30

        nodes_path = [Node(current, depth=0)]

        for step_idx in range(max_steps):
            self.steps.append({
                "step": step,
                "node": nodes_path[-1],
                "state": current,
                "frontier": [nodes_path[-1]],
                "action": previous_action if previous_action else "START",
                "message": f"Alpha-Beta - Bước {step_idx}: h(n)={self.tile_manhattan_distance(current)}, đường đi={path if path else 'START'}",
                "depth": len(path)
            })
            step += 1

            if is_goal(current):
                self.solution = nodes_path
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tìm thấy goal bằng Alpha-Beta! Số bước: {len(path)}",
                    "depth": len(path),
                    "solution": self.solution
                })
                return

            actions = self.ordered_actions_local(current, previous_action)
            best_action = None
            best_value = -float("inf")
            alpha = -float("inf")
            beta = float("inf")
            frontier_candidates = []

            for action in actions:
                next_state = execute_action(current, action)
                key = state_to_string(next_state)
                search_visited = visited.copy()
                search_visited.add(key)
                
                value = self.alphabeta_search(next_state, depth - 1, alpha, beta, search_visited, action)
                neighbor_node = Node(next_state, parent=nodes_path[-1], action=action, depth=len(path) + 1)
                frontier_candidates.append((neighbor_node, value))

                if value > best_value:
                    best_value = value
                    best_action = action
                alpha = max(alpha, best_value)

            if best_action is None:
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "FAILED",
                    "message": "Không có nước đi khả thi (Thất bại)",
                    "depth": len(path)
                })
                return

            self.steps.append({
                "step": step,
                "node": nodes_path[-1],
                "state": current,
                "frontier": frontier_candidates,
                "action": "EVALUATE",
                "message": f"Thử các nước đi. Chọn {best_action} (value={best_value})",
                "depth": len(path)
            })
            step += 1

            next_state = execute_action(current, best_action)
            key = state_to_string(next_state)
            if key in visited:
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "FAILED",
                    "message": f"Trùng trạng thái đã đi qua khi chọn {best_action} (Thất bại)",
                    "depth": len(path)
                })
                return

            current = next_state
            visited.add(key)
            path.append(best_action)
            nodes_path.append(Node(current, parent=nodes_path[-1], action=best_action, depth=len(path)))
            previous_action = best_action

        self.steps.append({
            "step": step,
            "node": nodes_path[-1],
            "state": current,
            "frontier": [],
            "action": "FAILED",
            "message": "Đạt giới hạn bước đi tối đa mà không tìm thấy goal",
            "depth": len(path)
        })

    def generate_steps_expectimax(self, start):
        self.steps = []
        self.solution = []
        step = 1
        current = copy.deepcopy(start)
        path = []
        previous_action = None
        visited = {state_to_string(current)}
        depth = 6
        max_steps = 30

        nodes_path = [Node(current, depth=0)]

        for step_idx in range(max_steps):
            self.steps.append({
                "step": step,
                "node": nodes_path[-1],
                "state": current,
                "frontier": [nodes_path[-1]],
                "action": previous_action if previous_action else "START",
                "message": f"Expectimax - Bước {step_idx}: h(n)={self.tile_manhattan_distance(current)}, đường đi={path if path else 'START'}",
                "depth": len(path)
            })
            step += 1

            if is_goal(current):
                self.solution = nodes_path
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "GOAL",
                    "message": f"Tìm thấy goal bằng Expectimax! Số bước: {len(path)}",
                    "depth": len(path),
                    "solution": self.solution
                })
                return

            actions = self.ordered_actions_local(current, previous_action)
            best_action = None
            best_value = -float("inf")
            frontier_candidates = []

            for action in actions:
                next_state = execute_action(current, action)
                key = state_to_string(next_state)
                search_visited = visited.copy()
                search_visited.add(key)
                
                value = self.expectimax_search(next_state, depth - 1, False, search_visited, action)
                neighbor_node = Node(next_state, parent=nodes_path[-1], action=action, depth=len(path) + 1)
                frontier_candidates.append((neighbor_node, value))

                if value > best_value:
                    best_value = value
                    best_action = action

            if best_action is None:
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "FAILED",
                    "message": "Không có nước đi khả thi (Thất bại)",
                    "depth": len(path)
                })
                return

            self.steps.append({
                "step": step,
                "node": nodes_path[-1],
                "state": current,
                "frontier": frontier_candidates,
                "action": "EVALUATE",
                "message": f"Thử các nước đi. Chọn {best_action} (value={best_value:.2f})",
                "depth": len(path)
            })
            step += 1

            next_state = execute_action(current, best_action)
            key = state_to_string(next_state)
            if key in visited:
                self.steps.append({
                    "step": step,
                    "node": nodes_path[-1],
                    "state": current,
                    "frontier": [],
                    "action": "FAILED",
                    "message": f"Trùng trạng thái đã đi qua khi chọn {best_action} (Thất bại)",
                    "depth": len(path)
                })
                return

            current = next_state
            visited.add(key)
            path.append(best_action)
            nodes_path.append(Node(current, parent=nodes_path[-1], action=best_action, depth=len(path)))
            previous_action = best_action

        self.steps.append({
            "step": step,
            "node": nodes_path[-1],
            "state": current,
            "frontier": [],
            "action": "FAILED",
            "message": "Đạt giới hạn bước đi tối đa mà không tìm thấy goal",
            "depth": len(path)
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
        self.algorithm_values = [
            "--- Uninformed Search ---",
            "BFS", "DFS", "IDS", "UCS",
            "--- Informed Search ---",
            "Greedy", "A*", "IDA*",
            "--- Local Search ---",
            "Hill Climbing", "Steepest Ascent", "Stochastic", "Random Restart",
            "Local Beam", "Local Beam + HC", "Simulated Annealing",
            "--- Belief / Nondeterministic ---",
            "Belief State Greedy", "Belief State (BS-BG DFS)",
            "Nondeterministic Heuristic", "AND-OR Graph Search",
            "--- Adversarial Search ---",
            "Minimax", "Alpha-Beta Pruning", "Expectimax",
            "--- CSP / Constraint Search ---",
            "Backtracking Search", "Forward Checking",
            "Arc Consistency", "Min-Conflicts"
        ]

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

        self.algo_menu = ctk.CTkComboBox(algo_frame, values=self.algorithm_values,
            command=self.change_algorithm, width=245, height=32)
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
        if value.startswith("---"):
            self.algo_menu.set(self.algorithm)
            return

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
        elif self.algorithm == "Belief State Greedy":
            self.solver.generate_steps_belief_greedy()
        elif self.algorithm == "Belief State (BS-BG DFS)":
            self.solver.generate_steps_belief_bs_bg_dfs()
        elif self.algorithm == "Nondeterministic Heuristic":
            self.solver.generate_steps_nondeterministic_heuristic()
        elif self.algorithm == "AND-OR Graph Search":
            self.solver.generate_steps_and_or_graph_search()
        elif self.algorithm == "Minimax":
            self.solver.generate_steps_minimax(self.initial_state)
        elif self.algorithm == "Alpha-Beta Pruning":
            self.solver.generate_steps_alphabeta(self.initial_state)
        elif self.algorithm == "Expectimax":
            self.solver.generate_steps_expectimax(self.initial_state)
        elif self.algorithm == "Backtracking Search":
            self.solver.generate_steps_backtracking_csp()
        elif self.algorithm == "Forward Checking":
            self.solver.generate_steps_forward_checking_csp()
        elif self.algorithm == "Arc Consistency":
            self.solver.generate_steps_arc_consistency_csp()
        elif self.algorithm == "Min-Conflicts":
            self.solver.generate_steps_min_conflicts_csp()
        
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
            elif isinstance(item, dict) and "state" in item:
                state_str = str(item["state"]).replace(", ", ",")
                frontier_text += f"{i+1}. {item.get('action', '')}: {state_str}\n"
        
        self.frontier_box.configure(state="normal")
        self.frontier_box.delete("1.0", "end")
        self.frontier_box.insert("end", frontier_text if frontier_text else "Frontier rỗng")
        self.frontier_box.configure(state="disabled")

    def show_solution(self, solution):
        moves_text = ""
        if solution and all(isinstance(action, str) for action in solution):
            for i, action in enumerate(solution, start=1):
                moves_text += f"{i}. {action}\n"
        else:
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
