# **BANKER'S ALGORITHM**

### Deadlock Avoidance — Banker's Algorithm

---

## **I. PROJECT OVERVIEW**

The **Banker's Algorithm**, an operating system deadlock-avoidance algorithm, is simulated by this program. By looking for a safe sequence, it determines whether a system is in a safe state and whether a resource request should be granted  without leading to an unsafe state.

In this project, Python is used to implement the Banker's Safety Algorithm. It determines the safe sequence, assesses whether processes can run safely, and computes the need and available resources. In order to decide whether a request should be granted or delayed, it also has an optional resource-request checking function.

---

## **II. SYSTEM FEATURES**

- **Resource Input:** Accepts the number of processes, resource types, Total vector, Allocation matrix, and Max matrix.
- **Need Calculation:** Automatically calculates the remaining resources required by each process.
- **Available Resources:** Determines the remaining available resources.
- **Safety Algorithm:** Checks whether the system is in a safe or unsafe state.
- **Safe Sequence:** Displays the order in which processes can safely execute.
- **Resource Request Checking:** Checks whether a process's resource request can be granted.
- **Input Validation:** Prevents invalid inputs, negative values, and allocations exceeding maximum requirements.

---

## **III. SYSTEM ARCHITECTURE** 
- **User Input** – process count, resources, allocation, max.
- **main.py** – reads and validates input, prints tables and the final result.
- **BankersAlgorithm.py** – Calculates Need and Available; performs safety and request checking.
- **Output** – matrices, work updates, finish flags, and safe sequence or unsafe state.

---

## **IV. PROGRAM EXECUTION INSTRUCTIONS**
1. Open Comman Prompt or VS Code terminal.
2. Clone the Github repository 
   ```bash
   git clone https://github.com/<username>/Bankers-Algorithm.git
   ```
3. Navigate to the project folder
   ```bash   
   cd Bankers-Algorithm
   ```
5. Run the program
   ```bash
   python main.py
   ```
---
      
## **V. INPUT REQUIREMENTS**

| Input |	Description |
|---|---|
| Number of processes |	n ≥ 1 |
| Number of resource types |	m ≥ 1 |
| Total vector | Total instances per resource (m values) |
| Allocation Matrix |	Resources currently assigned to each process |
| Max Matrix |	Maximum resources required by each process |
| Resource Request | Additional resources requested by a process |

---

## **VI. ALGORITHM IMPLEMENTATION AND PROCESS**
1. **Need** = Max − Allocation
2. **Available** = Total − column sums of Allocation
3. **Safety Algorithm:** set Work = Available and Finish[i] = False for all processes. Find an unfinished Pi with Need[i] ≤ Work (component-wise).
   Then Work = Work + Allocation[i] and Finish[i] = True. Repeat until none is found. If all Finish are True → **safe sequence**; otherwise → **UNSAFE STATE**.
4. **Resource-Request Algorithm** (process Pi, vector Request):
   - If Request ≤ Need[i] is false → REJECTED (exceeds maximum claim)
   - If Request ≤ Available is false → WAIT
   - Build a tentative state: Available −= Request, Allocation[i] += Request, Need[i] −= Request
   - Run the Safety Algorithm on it: safe → GRANT; unsafe → WAIT (rolled back)

---

## **VII. OUTPUT INTERPRETATION**

| Output | Meaning |
|---|---|
| Total, Allocation, Max, Need, Available |	Initial state (rows = processes, columns = R0, R1, …) | 
| Check Pi: Need [...] <= Work [...]? YES/NO | Whether Pi can finish with the current Work (for NO, the failing resource is shown) |
| Work = old + Allocation[Pi] = new | Resources returned when Pi finishes |
| Finish = [...] |	Which processes have finished so far |
| Safe sequence: P1 -> P3 -> ... |	Valid completion order → SAFE |
| UNSAFE STATE	| No safe sequence exists |
| Decision: GRANT |	Request is safe to grant |
| Decision: WAIT |	Not enough resources, or granting would be unsafe |
| Decision: REJECTED |	Request exceeds the process's maximum need |

---

## **VIII. GROUP MEMBERS**
- De Leon, Marriel N.
- Fernandez, John Ulrich P.
- Villanueva, Aldrich Miguel D.
- Yamson, Christian S.

---

## **IX. PROJECT DETAILS**
- **Group 4** | **Topic 5: Deadlock Avoidance — Banker's Algorithm**
- **Course:** PT 101 – Platform Technologies
- **Language:** Python 3
