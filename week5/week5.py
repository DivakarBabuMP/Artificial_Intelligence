import random
import math

def calculate_cost(state):
    attacking_pairs = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacking_pairs += 1
    return attacking_pairs

def generate_neighbor(state):
    neighbor = state[:]
    column = random.randint(0, len(state) - 1)
    new_row = random.randint(0, len(state) - 1)
    while new_row == state[column]:
        new_row = random.randint(0, len(state) - 1)
    neighbor[column] = new_row
    return neighbor

def simulated_annealing(n, initial_temperature, cooling_factor, max_iterations):
    current_state = [random.randint(0, n-1) for _ in range(n)]
    current_cost = calculate_cost(current_state)
    best_state = current_state
    best_cost = current_cost
    temperature = initial_temperature

    print(f"Initial state: {current_state} with cost: {current_cost}")

    iteration = 0
    while iteration < max_iterations and temperature > 0:
        neighbor_state = generate_neighbor(current_state)
        neighbor_cost = calculate_cost(neighbor_state)

        delta_cost = neighbor_cost - current_cost

        if delta_cost < 0:
            current_state = neighbor_state
            current_cost = neighbor_cost
        else:
            acceptance_probability = math.exp(-delta_cost / temperature)
            if random.random() < acceptance_probability:
                current_state = neighbor_state
                current_cost = neighbor_cost

        if current_cost < best_cost:
            best_state = current_state
            best_cost = current_cost

        print(f"Iteration {iteration+1}: {current_state} with cost: {current_cost}")

        temperature *= cooling_factor
        iteration += 1

    return best_state, best_cost

if __name__ == "__main__":
    N = 4
    initial_temperature = 100
    cooling_factor = 0.95
    max_iterations = 1000

    best_state, best_cost = simulated_annealing(N, initial_temperature, cooling_factor, max_iterations)

    print(f"\nFinal solution: {best_state} with cost: {best_cost}")