"""Run from any directory after installing matplotlib; all times are seconds."""
import json
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from queue_model import SystemMG1
from own import SystemMG1 as LCGSystem

dest = Path(__file__).resolve().parent
sizes = [1000, 3000, 10000, 30000, 100000]
series = {}
for label, cls in [("Python random", SystemMG1), ("32-bit LCG", LCGSystem)]:
    series[label] = [cls(seed=42).symuluj(n, "staly", warmup=1000) for n in sizes]
(dest / "queue-example.json").write_text(json.dumps({"seed":42,"warmup":1000,"observations":sizes,"mean_system_seconds":series,"analytical_seconds":90}, indent=2)+"\n")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.hashsalt":"queue-example"})
fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
for label, values in series.items():
    ax.plot(sizes, values, marker="o", label=label)
ax.axhline(90, color="#475569", linestyle="--", label="M/D/1 analytical: 90 s")
ax.set(xscale="log", xlabel="Measured arrivals after warm-up", ylabel="Mean system time (s)", title="FCFS queue: fixed 60 s service, mean arrival interval 120 s")
ax.grid(alpha=.2); ax.legend()
fig.savefig(dest / "queue-example.svg", metadata={"Date":None})

# Normalize generated XML whitespace for clean source diffs.
svg = dest / 'queue-example.svg'
svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
