from BankersAlgorithm import (
    CalculateNeed,
    AvailableResources,
    isSafeState,
    checkRequest,
    fmt,
)


def read_int(prompt, minimum=0, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if value < minimum or (maximum is not None and value > maximum):
            if maximum is not None:
                print(f"  Value must be between {minimum} and {maximum}.")
            else:
                print(f"  Value must be {minimum} or more.")
            continue
        return value


def read_vector(prompt, length):
    while True:
        parts = input(prompt).split()
        try:
            vec = [int(x) for x in parts]
        except ValueError:
            print("  Enter whole numbers separated by spaces.")
            continue
        if len(vec) != length:
            print(f"  Expected {length} values, got {len(vec)}.")
            continue
        if any(v < 0 for v in vec):
            print("  Values cannot be negative.")
            continue
        return vec


def print_vector(title, vec):
    print(f"{title} = {fmt(vec)}")


def print_matrix(title, matrix):
    print(f"\n{title}:")
    print("      " + "".join(f"R{j:<4}" for j in range(len(matrix[0]))))
    for i, row in enumerate(matrix):
        print(f"P{i:<4} " + "".join(f"{v:<5}" for v in row))


def validate(total, allocation, maximum, available):
    for i in range(len(allocation)):
        for j in range(len(total)):
            if allocation[i][j] > maximum[i][j]:
                print(f"Input error: Allocation[P{i}][R{j}] exceeds Max[P{i}][R{j}].")
                return False
    if any(a < 0 for a in available):
        print("Input error: Allocation column sums exceed Total.")
        return False
    return True


def main():
    print("=== Banker's Algorithm ===")
    n = read_int("Number of processes: ", minimum=1)
    m = read_int("Number of resource types: ", minimum=1)
    total = read_vector(f"Total vector ({m} values): ", m)

    print(f"\nEnter Allocation rows ({m} values each):")
    allocation = [read_vector(f"  Allocation P{i}: ", m) for i in range(n)]
    print(f"\nEnter Max rows ({m} values each):")
    maximum = [read_vector(f"  Max P{i}: ", m) for i in range(n)]

    need = CalculateNeed(allocation, maximum)
    available = AvailableResources(total, allocation)

    if not validate(total, allocation, maximum, available):
        return

    print("\n--- Initial State ---")
    print_vector("Total", total)
    print_matrix("Allocation", allocation)
    print_matrix("Max", maximum)
    print_matrix("Need", need)
    print_vector("\nAvailable", available)

    print("\n--- Safety Algorithm ---")
    log = []
    isSafeState(need, available, allocation, log)
    print("\n".join(log))

    choice = input("\nCheck a resource request? (y/n): ").strip().lower()
    if choice == "y":
        p = read_int(f"Requesting process (0-{n - 1}): ", minimum=0, maximum=n - 1)
        request = read_vector(f"Request vector ({m} values): ", m)
        print("\n--- Request Check ---")
        log = []
        checkRequest(p, request, need, available, allocation, log)
        print("\n".join(log))


if __name__ == "__main__":
    main()
