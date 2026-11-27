import tkinter as tk
from tkinter import ttk, messagebox


def fmt(v):
    return "[" + ", ".join(map(str, v)) + "]"


def calculate_need(alloc, maxm):
    return [
        [maxm[i][j] - alloc[i][j] for j in range(len(alloc[i]))]
        for i in range(len(alloc))
    ]


def available_resources(total, alloc):
    return [
        total[j] - sum(row[j] for row in alloc)
        for j in range(len(total))
    ]


def safe_state(need, available, alloc, log):

    work = available[:]
    finish = [False] * len(need)
    seq = []

    while len(seq) < len(need):

        found = False

        for i in range(len(need)):

            if finish[i]:
                continue

            if all(
                need[i][j] <= work[j]
                for j in range(len(work))
            ):

                work = [
                    work[j] + alloc[i][j]
                    for j in range(len(work))
                ]

                finish[i] = True
                seq.append(f"P{i}")

                log.append(
                    f"P{i} finished → Work = {fmt(work)}"
                )

                found = True

        if not found:
            log.append("Unsafe State")
            return False

    log.append(
        "Safe Sequence: " +
        " -> ".join(seq)
    )

    return True


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("Banker's Algorithm")
        self.root.geometry("900x700")

        setup = ttk.LabelFrame(
            root,
            text="System Setup"
        )

        setup.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Label(
            setup,
            text="Processes"
        ).grid(row=0, column=0)

        self.ent_n = ttk.Entry(
            setup,
            width=6
        )

        self.ent_n.grid(
            row=0,
            column=1
        )

        ttk.Label(
            setup,
            text="Resources"
        ).grid(row=0, column=2)

        self.ent_m = ttk.Entry(
            setup,
            width=6
        )

        self.ent_m.grid(
            row=0,
            column=3
        )

        ttk.Button(
            setup,
            text="Create Tables",
            command=self.create_tables
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.container = ttk.Frame(root)
        self.container.pack(
            fill="x",
            padx=10,
            pady=10
        )

        result_frame = ttk.LabelFrame(
            root,
            text="Results"
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table = ttk.Treeview(
            result_frame,
            columns=("Process", "Allocation", "Maximum", "Need"),
            show="headings",
            height=8
        )

        for col in ("Process", "Allocation", "Maximum", "Need"):
            self.table.heading(col, text=col)

        self.table.column("Process", width=100, anchor="center")
        self.table.column("Allocation", width=180, anchor="center")
        self.table.column("Maximum", width=180, anchor="center")
        self.table.column("Need", width=180, anchor="center")

        self.table.pack(fill="x", padx=10, pady=10)

        self.output = tk.Text(
            result_frame,
            height=10
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.alloc_entries = []
        self.max_entries = []

    def create_tables(self):

        for w in self.container.winfo_children():
            w.destroy()

        self.alloc_entries.clear()
        self.max_entries.clear()

        try:
            self.n = int(self.ent_n.get())
            self.m = int(self.ent_m.get())
        except:
            messagebox.showerror(
                "Error",
                "Enter valid numbers"
            )
            return

        ttk.Label(
            self.container,
            text="Total Resources"
        ).grid(row=0, column=0)

        self.total_entry = ttk.Entry(
            self.container,
            width=25
        )

        self.total_entry.grid(
            row=0,
            column=1,
            columnspan=self.m
        )

        ttk.Label(
            self.container,
            text="Allocation"
        ).grid(row=1, column=0)

        for i in range(self.n):

            row = []

            ttk.Label(
                self.container,
                text=f"P{i}"
            ).grid(
                row=i + 2,
                column=0
            )

            for j in range(self.m):

                e = ttk.Entry(
                    self.container,
                    width=5
                )

                e.grid(
                    row=i + 2,
                    column=j + 1
                )

                row.append(e)

            self.alloc_entries.append(row)

        offset = self.n + 3

        ttk.Label(
            self.container,
            text="Max"
        ).grid(
            row=offset,
            column=0
        )

        for i in range(self.n):

            row = []

            ttk.Label(
                self.container,
                text=f"P{i}"
            ).grid(
                row=offset + i + 1,
                column=0
            )

            for j in range(self.m):

                e = ttk.Entry(
                    self.container,
                    width=5
                )

                e.grid(
                    row=offset + i + 1,
                    column=j + 1
                )

                row.append(e)

            self.max_entries.append(row)

        ttk.Button(
            self.container,
            text="Compute",
            command=self.compute
        ).grid(
            row=offset + self.n + 2,
            column=0,
            pady=10
        )

    def compute(self):

        try:

            total = list(
                map(
                    int,
                    self.total_entry.get().split()
                )
            )

            alloc = [
                [
                    int(e.get())
                    for e in row
                ]
                for row in self.alloc_entries
            ]

            maxm = [
                [
                    int(e.get())
                    for e in row
                ]
                for row in self.max_entries
            ]

        except:
            messagebox.showerror(
                "Error",
                "Invalid Input"
            )
            return

        need = calculate_need(
            alloc,
            maxm
        )

        available = available_resources(
            total,
            alloc
        )
        for item in self.table.get_children():
            self.table.delete(item)

        for i in range(self.n):
            self.table.insert(
                "",
                "end",
                values=(
                    f"P{i}",
                    fmt(alloc[i]),
                    fmt(maxm[i]),
                    fmt(need[i])
                )
        )
        log = []

        safe_state(
            need,
            available,
            alloc,
            log
        )

        self.output.delete(
            "1.0",
            tk.END
        )

        self.output.insert(
            tk.END,
            f"Total = {fmt(total)}\n\n"
        )

        self.output.insert(
            tk.END,
            f"Available = {fmt(available)}\n\n"
        )

        self.output.insert(
            tk.END,
            "Need Matrix\n"
        )

        for i, row in enumerate(need):
            self.output.insert(
                tk.END,
                f"P{i}: {row}\n"
            )

        self.output.insert(
            tk.END,
            "\n\n" +
            "\n".join(log)
        )


root = tk.Tk()
App(root)
root.mainloop()
