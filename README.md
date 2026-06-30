# 🤖 AI Algorithms – 8-Puzzle

## 📁 Cấu trúc dự án

```
AI/
├── Interface_Of_All_Alogithms/   # Giao diện tổng hợp tất cả thuật toán (main.py)
├── Week2/                        # Agent phản xạ đơn giản
├── Week3/                        # Mô hình agent & agent phản xạ có trạng thái
├── Week4/                        # Tìm kiếm mù (BFS, DFS)
├── Week5/                        # Tìm kiếm có thông tin (UCS, IDS, A*, Greedy)
├── Week6/                        # Tìm kiếm cục bộ (Hill Climbing, Simulated Annealing, Local Beam)
├── Week7/                        # Tìm kiếm trong môi trường không xác định
└── Week8/                        # CSP & Game Search (Minimax, Alpha-Beta, Expectimax)
```

## 📚 Chi tiết từng tuần

### Week 2

| File | Mô tả |
|------|-------|
| `simplereflex.py` | Simple Reflex Agent – chọn hành động tốt nhất theo điểm greedy |
| `solve.py` | Phiên bản giải đơn giản hỗ trợ |

---

### Week 3 – Model-Based Agent
| File | Mô tả |
|------|-------|
| `base/model-8puzzle.py` | Model-Based Agent cho bài toán 8-Puzzle |
| `base/model-mayhutbui.py` | Model-Based Agent cho bài toán máy hút bụi |
| `simple/simple-mayhutbui.py` | Simple Reflex Agent cho máy hút bụi |

---

### Week 4 – Blind Search (Tìm kiếm mù)
| File | Mô tả |
|------|-------|
| `B1/solveBFS.py` | **BFS** – Breadth-First Search (tìm kiếm theo chiều rộng) |
| `B1/solveDFS.py` | **DFS** – Depth-First Search (tìm kiếm theo chiều sâu) |
| `B2/IDS_8puzzle.py` | **IDS** – Iterative Deepening Search |
| `B2/UCS_8puzzle.py` | **UCS** – Uniform Cost Search |

---

### Week 5 – Informed Search (Tìm kiếm có thông tin)
| File | Mô tả |
|------|-------|
| `B1/AStar_8puzzle.py` | **A*** – A-Star Search với heuristic Manhattan Distance |
| `B1/Greedy_8puzzle.py` | **Greedy Best-First Search** |
| `B2/HillClimbing_8puzzle.py` | **Hill Climbing** – Leo đồi cơ bản |
| `B2/IDA_8puzzle.py` | **IDA*** – Iterative Deepening A* |

---

### Week 6 – Local Search (Tìm kiếm cục bộ)
| File | Mô tả |
|------|-------|
| `B1/LocalBeamSearch_8puzzle.py` | **Local Beam Search** – Giữ k trạng thái tốt nhất |
| `B1/LocalBeamSearchWithHillClimbing_8puzzle.py` | **Local Beam + Hill Climbing** kết hợp |
| `B1/RandomRestart_8puzzle.py` | **Random Restart Hill Climbing** |
| `B1/SteepestAscent_8puzzle.py` | **Steepest-Ascent Hill Climbing** |
| `B1/Stochastic_8puzzle.py` | **Stochastic Hill Climbing** |
| `B2/BeliefState_8puzzle.py` | **Belief State Search** – Tìm kiếm trạng thái niềm tin |
| `B2/SimulatedAnnealing_8puzzle.py` | **Simulated Annealing** – Luyện kim mô phỏng |

---

### Week 7 – Nondeterministic & Partial Observation Search
| File | Mô tả |
|------|-------|
| `and-or-graph-search.py` | **AND-OR Graph Search** – Tìm kiếm trong môi trường không xác định |
| `belief-state-bs-bg.py` | **Belief State Search** với BFS/BG |
| `nondeterministic-heuristic-search.py` | Tìm kiếm heuristic không xác định |

---

### Week 8 – CSP & Game Search
| File | Mô tả |
|------|-------|
| `B1/BacktrackingSearch_8puzzle.py` | **Backtracking Search** – Tìm kiếm quay lui |
| `B1/ForwardChecking_8puzzle.py` | **Forward Checking** – Kiểm tra trước |
| `B1/ArcConsistency_8puzzle.py` | **Arc Consistency (AC-3)** |
| `B1/MinConflicts_8puzzle.py` | **Min-Conflicts** – Giải CSP bằng leo đồi |
| `B2/Minimax.py` | **Minimax** – Tìm kiếm trong game 2 người |
| `B2/AlphaBeta.py` | **Alpha-Beta Pruning** – Cắt tỉa alpha-beta |
| `B2/Expectimax.py` | **Expectimax** – Minimax cho môi trường ngẫu nhiên |

---

## 🎯 Bài toán chính – 8-Puzzle

Bài toán 8 ô trượt trên lưới 3×3:

```
Ví dụ:

Trạng thái ban đầu:    Trạng thái đích:
┌───┬───┬───┐          ┌───┬───┬───┐
│ 2 │ 8 │ 3 │          │ 1 │ 2 │ 3 │
├───┼───┼───┤    →     ├───┼───┼───┤
│ 1 │   │ 4 │          │ 4 │ 5 │ 6 │
├───┼───┼───┤          ├───┼───┼───┤
│ 7 │ 6 │ 5 │          │ 7 │ 8 │   │
└───┴───┴───┘          └───┴───┴───┘
```

Ô trống có thể di chuyển: **UP | DOWN | LEFT | RIGHT**

## 🚀 Yêu cầu

- **Python** 3.8+
- Không cần thư viện ngoài (chỉ dùng thư viện chuẩn: `copy`, `random`, `heapq`, `collections`)

---

## ▶️ Cách chạy

```bash
# Chạy từng file thuật toán cụ thể
python Week4/B1/solveBFS.py
python Week5/B1/AStar_8puzzle.py
python Week6/B1/LocalBeamSearch_8puzzle.py
python Week8/B2/Minimax.py

# Chạy giao diện tổng hợp tất cả thuật toán
python Interface_Of_All_Alogithms/main.py
```

---

## 📊 So sánh thuật toán

| Thuật toán | Hoàn chỉnh | Tối ưu | Độ phức tạp | Ghi chú |
|------------|:----------:|:------:|-------------|---------|
| BFS | ✅ | ✅ | O(b^d) | Bộ nhớ lớn |
| DFS | ✅ | ❌ | O(b^m) | Có thể lặp vô hạn |
| UCS | ✅ | ✅ | O(b^d) | Xét chi phí đường đi |
| IDS | ✅ | ✅ | O(b^d) | Tiết kiệm bộ nhớ |
| Greedy | ❌ | ❌ | O(b^m) | Nhanh nhưng không chắc tối ưu |
| A* | ✅ | ✅ | O(b^d) | Tốt nhất có thông tin |
| IDA* | ✅ | ✅ | O(b^d) | A* tiết kiệm bộ nhớ |
| Hill Climbing | ❌ | ❌ | O(∞) | Có thể kẹt cực trị địa phương |
| Simulated Annealing | ❌ | ❌ | O(∞) | Thoát cực trị địa phương |
| Minimax | ✅ | ✅ | O(b^m) | Cho game 2 người |
| Alpha-Beta | ✅ | ✅ | O(b^(m/2)) | Tối ưu hóa Minimax |
| Expectimax | ✅ | ❌ | O(b^m) | Cho môi trường ngẫu nhiên |

---

## 👤 Tác giả

**Nguyen Quang Vinh**  
Môn học: Trí tuệ Nhân tạo

---

*Dự án được tổ chức theo từng tuần học, mỗi tuần tập trung vào một nhóm thuật toán AI.*
