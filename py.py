import copy
import heapq
import time


# Manhattan distance heuristic
def manhattan_distance(state, goal):
    # map value to its target coordinate in goal state
    goal_pos = {}
    for r in range(3):
        for c in range(3):
            goal_pos[goal[r][c]] = (r, c)

    dist = 0
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:
                target_r, target_c = goal_pos[val]
                dist += abs(r - target_r) + abs(c - target_c)
    return dist


# find row and col of the blank tile (0)
def find_blank(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c
    return None


# generate all valid adjacent moves
def get_neighbors(state):
    neighbors = []
    blank_r, blank_c = find_blank(state)

    # up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_r, new_c = blank_r + dr, blank_c + dc

        if 0 <= new_r < 3 and 0 <= new_c < 3:
            # create new board and swap blank with target cell
            new_state = [row[:] for row in state]
            new_state[blank_r][blank_c], new_state[new_r][new_c] = (
                new_state[new_r][new_c],
                new_state[blank_r][blank_c],
            )
            neighbors.append(new_state)

    return neighbors


# display board state
def print_state(state, step_num=None, heuristic=None):
    if step_num is not None:
        print(f"\nStep {step_num}:")
        print("-" * 12)

    for row in state:
        print(" ".join(str(val) if val != 0 else "_" for val in row))

    if heuristic is not None:
        print(f"h(n) = {heuristic}")


# check if 8-puzzle configuration is solvable using inversion count
def is_solvable(state):
    flat = [val for row in state for val in row if val != 0]

    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1

    return inversions % 2 == 0


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


# greedy best-first search algorithm
def greedy_best_first_search(initial_state, goal_state):
    print("\nRunning Greedy Best-First Search...")
    print("-" * 40)

    if not is_solvable(initial_state):
        print("Error: Initial state is not solvable.")
        return None

    if initial_state == goal_state:
        print("Already at goal state.")
        return [initial_state]

    counter = 0
    init_h = manhattan_distance(initial_state, goal_state)
    # pq entry: (heuristic, tie_breaker_counter, state, path)
    pq = [(init_h, counter, initial_state, [initial_state])]
    counter += 1

    visited = set()
    visited.add(state_to_tuple(initial_state))

    explored_count = 0

    while pq:
        _, _, current, path = heapq.heappop(pq)
        explored_count += 1

        if current == goal_state:
            print(f"Goal reached! Total states expanded: {explored_count}")
            return path

        for neighbor in get_neighbors(current):
            neighbor_key = state_to_tuple(neighbor)

            if neighbor_key not in visited:
                visited.add(neighbor_key)
                h = manhattan_distance(neighbor, goal_state)
                heapq.heappush(pq, (h, counter, neighbor, path + [neighbor]))
                counter += 1

    print("No solution path found.")
    return None


# prompt user for grid values
def get_user_input():
    print("\nEnter initial board row by row (use 0 for blank space):")
    print("Example format: '1 2 3'")
    print("-" * 40)

    state = []
    for i in range(3):
        while True:
            try:
                line = input(f"Row {i + 1}: ").strip()
                row = [int(x) for x in line.split()]

                if len(row) != 3:
                    print("Error: Each row must contain exactly 3 numbers.")
                    continue

                if not all(0 <= x <= 8 for x in row):
                    print("Error: Values must be in range [0, 8].")
                    continue

                state.append(row)
                break
            except ValueError:
                print("Error: Invalid input. Enter integers only.")

    flat = [num for row in state for num in row]
    if sorted(flat) != list(range(9)):
        print("\nError: Board must contain unique numbers from 0 to 8.")
        return None

    return state


def main():
    print("=" * 40)
    print("       8-PUZZLE SOLVER (GBFS)")
    print("=" * 40)

    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("\nTarget Goal:")
    print_state(goal_state)

    initial_state = get_user_input()
    if initial_state is None:
        return

    print("\nInitial State:")
    print_state(initial_state)

    start_time = time.time()
    solution_path = greedy_best_first_search(initial_state, goal_state)
    exec_time = time.time() - start_time

    if solution_path:
        print("\n" + "=" * 40)
        print("            SOLUTION PATH")
        print("=" * 40)

        for step, state in enumerate(solution_path):
            h = manhattan_distance(state, goal_state)
            print_state(state, step, h)
            time.sleep(0.3)

        print("-" * 40)
        print(f"Total steps: {len(solution_path) - 1}")
        print(f"Time elapsed: {exec_time:.4f} seconds")
        print("-" * 40)
    else:
        print("\nCould not find a valid solution.")


if __name__ == "__main__":
    main()