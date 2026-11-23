def fmt(vec):
    return "[" + ", ".join(str(x) for x in vec) + "]"


def CalculateNeed(Allocation, Max):
    """Need = Max - Allocation."""
    Need = []
    for i in range(len(Allocation)):
        row = []
        for j in range(len(Max[i])):
            row.append(Max[i][j] - Allocation[i][j])
        Need.append(row)
    return Need


def TotalAllocated(Allocation):
    """Column sums of the Allocation matrix."""
    total = [0] * len(Allocation[0])
    for i in range(len(Allocation)):
        for j in range(len(Allocation[i])):
            total[j] += Allocation[i][j]
    return total


def AvailableResources(TotalInstances, Allocation):
    """Available = Total - column sums of Allocation."""
    total_allocated = TotalAllocated(Allocation)
    available = []
    for i in range(len(TotalInstances)):
        available.append(TotalInstances[i] - total_allocated[i])
    return available


def isSafeState(Need, Available, Allocation, log=None):
    if log is None:
        log = []
    n = len(Need)
    m = len(Available)
    work = Available.copy()
    finish = [False] * n
    safe_sequence = []

    log.append(f"Work = Available = {fmt(work)}")
    log.append(f"Finish = {fmt(finish)}")

    progress = True
    while len(safe_sequence) < n and progress:
        progress = False
        for i in range(n):
            if finish[i]:
                continue
            fits = all(Need[i][j] <= work[j] for j in range(m))
            if fits:
                log.append(f"Check P{i}: Need {fmt(Need[i])} <= Work {fmt(work)}? YES")
                old_work = work.copy()
                for j in range(m):
                    work[j] += Allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                progress = True
                log.append(
                    f"  Work = {fmt(old_work)} + Allocation[P{i}] "
                    f"{fmt(Allocation[i])} = {fmt(work)}"
                )
                log.append(f"  Finish = {fmt(finish)}")
            else:
                j = next(j for j in range(m) if Need[i][j] > work[j])
                log.append(
                    f"Check P{i}: Need {fmt(Need[i])} <= Work {fmt(work)}? NO "
                    f"(R{j}: {Need[i][j]} > {work[j]})"
                )

    log.append(f"Final Finish = {fmt(finish)}")
    if len(safe_sequence) == n:
        log.append("Safe sequence: " + " -> ".join(f"P{i}" for i in safe_sequence))
        return True, safe_sequence
    log.append("UNSAFE STATE")
    return False, safe_sequence


def checkRequest(process, request, Need, Available, Allocation, log=None):
    """Resource-request check. Returns "GRANT", "WAIT", or "REJECTED".

    "REJECTED" is used only when Request > Need (process exceeded its
    maximum claim). The guideline lists only GRANT/WAIT. [uncertain]
    whether the instructor wants a different label for that case.
    """
    if log is None:
        log = []
    m = len(Available)
    p = process
    log.append(f"Request by P{p}: {fmt(request)}")

    # Step 1: Request <= Need
    ok_need = all(request[j] <= Need[p][j] for j in range(m))
    log.append(
        f"Step 1: Request {fmt(request)} <= Need[P{p}] {fmt(Need[p])}? "
        f"{'YES' if ok_need else 'NO'}"
    )
    if not ok_need:
        log.append("Request exceeds the process's maximum claim.")
        log.append("Decision: REJECTED")
        return "REJECTED"

    # Step 2: Request <= Available
    ok_avail = all(request[j] <= Available[j] for j in range(m))
    log.append(
        f"Step 2: Request {fmt(request)} <= Available {fmt(Available)}? "
        f"{'YES' if ok_avail else 'NO'}"
    )
    if not ok_avail:
        log.append("Resources not available now.")
        log.append("Decision: WAIT")
        return "WAIT"

    # Step 3: tentative state (work on copies; original state is untouched)
    new_available = [Available[j] - request[j] for j in range(m)]
    new_allocation = [row[:] for row in Allocation]
    new_need = [row[:] for row in Need]
    for j in range(m):
        new_allocation[p][j] += request[j]
        new_need[p][j] -= request[j]
    log.append("Step 3: Tentative state")
    log.append(f"  Available     = {fmt(new_available)}")
    log.append(f"  Allocation[P{p}] = {fmt(new_allocation[p])}")
    log.append(f"  Need[P{p}]       = {fmt(new_need[p])}")

    # Step 4: safety check on the tentative state
    log.append("Step 4: Safety check on tentative state")
    safe, _ = isSafeState(new_need, new_available, new_allocation, log)

    if safe:
        log.append("Decision: GRANT")
        return "GRANT"
    log.append("Tentative state is unsafe; request rolled back.")
    log.append("Decision: WAIT")
    return "WAIT"
