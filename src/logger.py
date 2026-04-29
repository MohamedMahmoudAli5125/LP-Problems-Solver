import numpy as np

class SimplexLogger:
    def __init__(self, solver):
        self.solver = solver
        
    def to_string(self) -> str:
        s, sol = self.solver, self.solver.solution
        lines = ["="*31, "  SIMPLEX METHOD – FULL TRACE", "="*31]
        lines += [f"  Objective : {s.model.obj_type.upper()}", f"  Status    : {s.status}", ""]

        # Render Tableaux
        for i, (tab, lbl) in enumerate(zip(s.steps, s.step_labels)):
            lines += ["-"*31, f"  Step {i+1}  |  {lbl}", "-"*31]
            lines += self._format_tableau(tab, lbl)
            lines.append("")

        # Render Final Result
        lines += ["="*10, "  RESULT", "="*10]
        if s.status == "Optimal":
            lines += [f"  Status: Optimal ✓", f"  Objective: {sol.get('objective_value', 'N/A')}", "\n  Variables:"]
            lines += [f"    {k:>10} = {v}" for k, v in sol.items() if k != 'objective_value']
        else:
            lines.append(f"  Status: {s.status}")
            
        return "\n".join(lines)

    def _format_tableau(self, tab, label) -> list[str]:
        # Phase 2 drops artificials (starts with 'a')
        meta = list(self.solver.std_output.col_metaData)
        if "Phase 2" in label:
            meta = [m for m in meta if not m.startswith("a")]
        
        if len(meta) != tab.shape[1] - 1:
            headers = [f"x{i+1}" for i in range(tab.shape[1]-1)] + ["RHS"]
        else:
            headers = meta + ["RHS"]

        # Build Table
        res = ["        " + "".join(h.rjust(10) for h in headers), "-" * (10 * len(headers) + 8)]
        for r in range(tab.shape[0]):
            if r == tab.shape[0] - 1: res.append("-" * len(res[-1])) 
            row_lbl = "Z" if r == tab.shape[0]-1 else f"R{r+1}"
            cells = [f"{v:g}" if abs(v-round(v))<1e-9 else f"{v:.4f}" for v in tab[r]]
            res.append(row_lbl.ljust(8) + "".join(c.rjust(10) for c in cells))
        return res

    def write(self, filepath: str = "simplex_steps.txt"):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_string())