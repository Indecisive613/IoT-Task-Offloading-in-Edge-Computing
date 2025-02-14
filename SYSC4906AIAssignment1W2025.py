import math
import random
import matplotlib.pyplot as plt

# Use ggplot style for plotting
plt.style.use("ggplot")

##############################
# GLOBAL PARAMETERS
##############################

alpha = 0.5  # weighting for cost = alpha*delay + (1-alpha)*energy
NUM_STEPS = 120

##############################
# 1. DEFINE 20 TASKS
##############################

PREDEFINED_20 = [
    {
        "Tlocal": 5.0,  "Elocal": 6.0,
        "Tcomm": 1.0,   "Tedge": 1.0,
        "Ecomm": 1.0
    },
    {
        "Tlocal": 6.0,  "Elocal": 5.5,
        "Tcomm": 1.2,   "Tedge": 1.0,
        "Ecomm": 1.0
    },
    {
        "Tlocal": 5.0,  "Elocal": 6.0,
        "Tcomm": 0.8,   "Tedge": 1.0,
        "Ecomm": 1.2
    },
    {
        "Tlocal": 5.5,  "Elocal": 5.0,
        "Tcomm": 1.0,   "Tedge": 0.8,
        "Ecomm": 1.0
    },
    {
        "Tlocal": 6.0,  "Elocal": 7.0,
        "Tcomm": 1.0,   "Tedge": 1.0,
        "Ecomm": 1.0
    },
    {
        "Tlocal": 10,  "Elocal": 1.1,
        "Tcomm": 0.1,   "Tedge": 0.9,
        "Ecomm": 11.1
    },
    {
        "Tlocal": 11.8,  "Elocal": 1.2,
        "Tcomm": 0.5,   "Tedge": 0.5,
        "Ecomm": 11.3
    },
    {
        "Tlocal": 11.5,  "Elocal": 2.0,
        "Tcomm": 1.0,   "Tedge": 1.0,
        "Ecomm": 13.0
    },
    {
        "Tlocal": 11.2,  "Elocal": 1.5,
        "Tcomm": 1.0,   "Tedge": 1.0,
        "Ecomm": 13.4
    },
    {
        "Tlocal": 11.6,  "Elocal": 2.0,
        "Tcomm": 1.1,   "Tedge": 1.0,
        "Ecomm": 13.1
    },
    {
        "Tlocal": 1.0,  "Elocal": 10.5,
        "Tcomm": 11.5,   "Tedge": 0.5,
        "Ecomm": 1.0
    },
    {
        "Tlocal": 1.0,  "Elocal": 10.2,
        "Tcomm": 11.0,   "Tedge": 0.1,
        "Ecomm": 1.0
    },
    {
        "Tlocal": 1.5,  "Elocal": 10.0,
        "Tcomm": 10.5,   "Tedge": 1.0,
        "Ecomm": 1.5
    },
    {
        "Tlocal": 1.5,  "Elocal": 11.0,
        "Tcomm": 11.0,   "Tedge": 0.5,
        "Ecomm": 1.2
    },
    {
        "Tlocal": 1.3,  "Elocal": 9.3,
        "Tcomm": 11.2,   "Tedge": 0.1,
        "Ecomm": 1.4
    },
    {
        "Tlocal": 2.0,  "Elocal": 2.0,
        "Tcomm": 2.2,   "Tedge": 9.0,
        "Ecomm": 9.5
    },
    {
        "Tlocal": 2.2,  "Elocal": 2.5,
        "Tcomm": 2.2,   "Tedge": 9.0,
        "Ecomm": 9.8
    },
    {
        "Tlocal": 2.0,  "Elocal": 2.5,
        "Tcomm": 2.0,   "Tedge": 9.0,
        "Ecomm": 9.0
    },
    {
        "Tlocal": 2.5,  "Elocal": 2.5,
        "Tcomm": 2.8,   "Tedge": 9.0,
        "Ecomm": 9.4
    },
    {
        "Tlocal": 2.1,  "Elocal": 2.3,
        "Tcomm": 2.2,   "Tedge": 9.0,
        "Ecomm": 9.3
    }
]

##############################
# 2. Weighted Cost for local/offload
##############################

def cost_local(task):
    return alpha*task["Tlocal"] + (1-alpha)*task["Elocal"]

def cost_offload(task):
    return alpha*(task["Tcomm"] + task["Tedge"]) + (1-alpha)*task["Ecomm"]

##############################
# 3. 4-step feasibility for local/offload
##############################

def valid_move_p1(last_moves, new_move):
    """
    - No more than 2 'local' in any 4 consecutive
    - No more than 3 'offload' in any 4 consecutive
    """
    window = (last_moves[-3:] + [new_move])
    if window.count("local") > 2:
        return False
    if window.count("offload") > 3:
        return False
    return True

##############################
# 4. Generate the 120-step scenario
##############################

def generate_scenario_120():
    """
    Creates a list of 120 tasks, each a random pick from PREDEFINED_20.
    """
    tasks = []
    for _ in range(NUM_STEPS):
        task_dict = random.choice(PREDEFINED_20)
        tasks.append(task_dict)
    return tasks

##############################
# 5. Minimax & Random approaches
##############################

def run_minimax(tasks):
##############################
# Add your Player code here. The code should return two values: moves, total_cost
##############################
    return ["local"] * len(tasks), 1000 # Pick all local for now
    
def run_random_player(tasks):
    """
    For each task, pick local/offload at random if feasible,
    else default to local with cost=0 if no feasible moves.
    Return (moves, totalCost).
    """
    last3moves = []
    moves = []
    total_cost = 0.0
    for tdict in tasks:
        c_loc = cost_local(tdict)
        c_off= cost_offload(tdict)
        feasible=[]
        if valid_move_p1(last3moves, "local"):
            feasible.append(("local", c_loc))
        if valid_move_p1(last3moves, "offload"):
            feasible.append(("offload", c_off))

        if not feasible:
            chosen = "local"
            step_cost = 0.0
        else:
            chosen, step_cost = random.choice(feasible)
        moves.append(chosen)
        last3moves.append(chosen)
        total_cost += step_cost

    return moves, total_cost

##############################
# 6. Stepwise evaluation
##############################

def evaluate_stepwise(tasks, moves):
    """
    Return stepwise cumulative delay, energy, cost arrays for plotting.
    """
    delay_arr = []
    energy_arr= []
    cost_arr  = []
    cum_delay=0.0
    cum_energy=0.0
    cum_cost=0.0

    for i, tdict in enumerate(tasks):
        if moves[i]=="local":
            step_delay = tdict["Tlocal"]
            step_energy= tdict["Elocal"]
        else: # offload
            step_delay= tdict["Tcomm"]+ tdict["Tedge"]
            step_energy= tdict["Ecomm"]
        cum_delay += step_delay
        cum_energy+= step_energy
        step_cost = alpha*step_delay + (1-alpha)*step_energy
        cum_cost += step_cost

        delay_arr.append(cum_delay)
        energy_arr.append(cum_energy)
        cost_arr.append(cum_cost)

    return delay_arr, energy_arr, cost_arr

##############################
# 7. Plot
##############################

def plot_results(dG, eG, cG, dR, eR, cR):
    steps = range(1, NUM_STEPS+1)

    # 1) Delay
    plt.figure(figsize=(8,5))
    plt.plot(steps, dG, label="Minimax")
    plt.plot(steps, dR, label="Random")
    plt.title("Cumulative Delay (120 steps)")
    plt.xlabel("Step")
    plt.ylabel("Delay")
    plt.legend()
    plt.show()

    # 2) Energy
    plt.figure(figsize=(8,5))
    plt.plot(steps, eG, label="Minimax")
    plt.plot(steps, eR, label="Random")
    plt.title("Cumulative Energy (120 steps)")
    plt.xlabel("Step")
    plt.ylabel("Energy")
    plt.legend()
    plt.show()

    # 3) Cost
    plt.figure(figsize=(8,5))
    plt.plot(steps, cG, label="Minimax")
    plt.plot(steps, cR, label="Random")
    plt.title(f"Cumulative Cost (alpha={alpha})")
    plt.xlabel("Step")
    plt.ylabel("Cost")
    plt.legend()
    plt.show()

##############################
# 8. Print table
##############################

def print_3row_table(tasks, movesG, movesR):
    """
    Row 0 => The index of each task in PREDEFINED_20
    Row 1 => Minimax's local/off decisions
    Row 2 => Random's local/off decisions
    """
    print("\nTABLE (3 rows => tasks, minimax, random):\n")

    # tasks row
    print("Tasks:    ", end="")
    for tdict in tasks:
        idx = PREDEFINED_20.index(tdict)
        print(f"T{idx:2}", end=" ")
    print()

    # Minimax row
    print("Minimax:   ", end="")
    for mv in movesG:
        print(f"{mv:6}", end=" ")
    print()

    # Random row
    print("Random:   ", end="")
    for mv in movesR:
        print(f"{mv:6}", end=" ")
    print("\n")

##############################
# MAIN
##############################

def main():
    random.seed(42)

    # 1) Generate scenario of 120 tasks
    tasks_120 = generate_scenario_120()

    # 2) Minimax approach
    movesMinimax, costMinimax = run_minimax(tasks_120)
    print(f"Minimax final cost: {costMinimax:.2f}")

    # 3) Random approach
    movesRandom, costRandom = run_random_player(tasks_120)
    print(f"Random final cost: {costRandom:.2f}")

    # 4) Evaluate stepwise
    dG, eG, cG = evaluate_stepwise(tasks_120, movesMinimax)
    dR, eR, cR = evaluate_stepwise(tasks_120, movesRandom)

    # 5) Print table
    print_3row_table(tasks_120, movesMinimax, movesRandom)

    # 6) Plot
    plot_results(dG, eG, cG, dR, eR, cR)

if __name__=="__main__":
    main()