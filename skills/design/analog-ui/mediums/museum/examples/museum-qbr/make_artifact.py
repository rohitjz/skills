"""Draws the framed 'artefact' chart for the museum QBR sample (illustrative data)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

weeks = list(range(1, 40))
searchers = [41 + 0.9 * w + (3 if w > 26 else 0) + (2.5 if w > 30 else 0) + (0.8 if w % 3 == 0 else -0.4) for w in weeks]
plt.rcParams.update({"font.family": "serif", "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"]})
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=220)
fig.patch.set_facecolor("#FBFAF7"); ax.set_facecolor("#FBFAF7")
ax.plot(weeks, searchers, color="#2B2A27", lw=1.6)
ax.fill_between(weeks, searchers, color="#2B2A27", alpha=.05)
ax.axvspan(27, 39, color="#B4552D", alpha=.07, lw=0)
ax.text(27.4, 47, "Q3: learned ranking\nships to all users", fontsize=9, color="#B4552D", style="italic", va="bottom")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#8C877D")
ax.tick_params(colors="#6B665D", labelsize=8.5, length=3)
ax.set_xticks([1, 13, 26, 39]); ax.set_xticklabels(["Jan", "Apr", "Jul", "Sep"])
ax.set_ylim(0, 90); ax.set_yticks([0, 30, 60, 90]); ax.set_yticklabels(["0", "30K", "60K", "90K"])
ax.annotate(f"{searchers[-1]:.0f}K", (39, searchers[-1]), xytext=(6, -3), textcoords="offset points", fontsize=10, color="#2B2A27")
ax.annotate(f"{searchers[0]:.0f}K", (1, searchers[0]), xytext=(4, -14), textcoords="offset points", fontsize=10, color="#6B665D")
fig.tight_layout(); fig.savefig("artifact.png", facecolor=fig.get_facecolor())
print(round(searchers[0]), round(searchers[-1]))
