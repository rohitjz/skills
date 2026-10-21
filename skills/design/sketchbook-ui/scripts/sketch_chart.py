#!/usr/bin/env python3
"""Draw a pencil-sketch line chart (optionally dual-axis) (transparent PNG) from a CSV or XLSX.

Primary series: graphite line with hatched fill (left axis).
Secondary series (optional): pencil-blue line (right axis, shown as %).

Example:
  python scripts/sketch_chart.py examples/lets-encrypt-10-years/data.csv --date date \
      --primary active_domains --every 3 \
      --mark "2018-09-15|1M certs a day" --mark "2020-02-27|1 billionth cert" \
      --out examples/lets-encrypt-10-years/chart.png
"""
import argparse, csv, datetime as dt, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib import font_manager as fm
from matplotlib.ticker import FuncFormatter

GRAPHITE, PENCIL = "#3A3A38", "#2F5BB7"
HAND_FONTS = [
    "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf",  # macOS
    "/Library/Fonts/Bradley Hand Bold.ttf",
    "C:/Windows/Fonts/segoepr.ttf",                               # Segoe Print
    "/usr/share/fonts/truetype/humor-sans/Humor-Sans.ttf",
]


def hand_font(user_path=None):
    for p in [user_path] + HAND_FONTS:
        if p and os.path.exists(p):
            fm.fontManager.addfont(p)
            return fm.FontProperties(fname=p).get_name()
    return None  # matplotlib's xkcd mode still gives the wobble


def read_rows(path, date_col, cols):
    if path.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(path, data_only=True).active
        it = ws.iter_rows(values_only=True)
        head = [str(h) for h in next(it)]
        recs = [dict(zip(head, r)) for r in it]
    else:
        with open(path, newline="") as f:
            recs = list(csv.DictReader(f))
    out = []
    for r in recs:
        d = r.get(date_col)
        if d in (None, ""):
            continue
        if not isinstance(d, (dt.date, dt.datetime)):
            d = dt.datetime.fromisoformat(str(d)[:10])
        out.append([d] + [float(r[c]) if c and r.get(c) not in (None, "") else None for c in cols])
    return out


def compact(v):
    if v == 0:
        return "0"
    if v >= 1e9:
        return f"{v/1e9:.1f}".rstrip("0").rstrip(".") + "B"
    if v >= 1e8:
        return f"{v/1e6:.0f}M"
    if v >= 1e6:
        return f"{v/1e6:.2f}".rstrip("0").rstrip(".") + "M"
    if v >= 1e3:
        return f"{v/1e3:.0f}K"
    return f"{v:.0f}"


def main():
    a = argparse.ArgumentParser()
    a.add_argument("data")
    a.add_argument("--date", required=True)
    a.add_argument("--primary", required=True)
    a.add_argument("--secondary")
    a.add_argument("--primary-label", default="")
    a.add_argument("--secondary-label", default="")
    a.add_argument("--secondary-format", choices=["ratio", "pct", "count"], default="ratio",
                   help="ratio: 0-1 shown as %%; pct: already a percent; count: compact K/M/B")
    a.add_argument("--smooth", type=int, default=1, help="rolling mean window in rows (e.g. 7)")
    a.add_argument("--every", type=int, default=1, help="keep every Nth row after smoothing")
    a.add_argument("--mark", action="append", default=[],
                   help='callout on the primary line: "YYYY-MM-DD|label" (repeatable)')
    a.add_argument("--font", help="path to a handwriting .ttf")
    a.add_argument("--out", required=True)
    a.add_argument("--size", default="8.6x4.6", help="inches WxH")
    o = a.parse_args()

    rows = read_rows(o.data, o.date, [o.primary, o.secondary])
    def roll(v):
        if o.smooth <= 1:
            return v
        out = []
        for i in range(len(v)):
            win = [x for x in v[max(0, i - o.smooth + 1):i + 1] if x is not None]
            out.append(sum(win) / len(win) if win else None)
        return out
    rows = [r for r in rows if r[1] is not None]
    d = [r[0] for r in rows]
    p = roll([r[1] for r in rows])
    s = roll([r[2] * (100 if o.secondary_format == "ratio" else 1) for r in rows]) if o.secondary else None
    keep = list(range(0, len(d), o.every))
    if keep[-1] != len(d) - 1:
        keep.append(len(d) - 1)
    d = [d[i] for i in keep]; p = [p[i] for i in keep]
    if s:
        s = [s[i] for i in keep]
    pct = o.secondary_format != "count"
    sfmt = (lambda v: f"{v:.1f}%") if pct else compact
    W, H = (float(x) for x in o.size.split("x"))
    name = hand_font(o.font)

    with plt.xkcd(scale=0.7, length=120, randomness=2):
        plt.rcParams.update({"path.effects": []})
        if name:
            plt.rcParams["font.family"] = name
        fig, ax = plt.subplots(figsize=(W, H), dpi=200)
        fig.patch.set_alpha(0); ax.patch.set_alpha(0)
        ax.fill_between(d, p, facecolor="none", edgecolor=GRAPHITE, hatch="////", lw=0, alpha=.22)
        ax.plot(d, p, color=GRAPHITE, lw=2.4)
        top = max(p) * 1.27
        ax.set_ylim(0, top)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: compact(v)))
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.tick_params(labelsize=13, colors=GRAPHITE)
        span = (d[-1] - d[0]).days
        ax.set_xlim(d[0] - dt.timedelta(days=2), d[-1] + dt.timedelta(days=max(10, span // 5)))
        loc = md.YearLocator() if span > 900 else md.MonthLocator()
        ax.xaxis.set_major_formatter(md.DateFormatter("%Y" if span > 900 else "%b"))
        ticks = [m for m in md.num2date(loc.tick_values(d[0], d[-1]))]
        ax.set_xticks([m for m in ticks if d[0] <= m.replace(tzinfo=None) <= d[-1]])
        ax.scatter([d[0], d[-1]], [p[0], p[-1]], color=GRAPHITE, s=30, zorder=5)
        if p[0] > top * .04:  # skip a start label that would sit on the x-axis
            ax.annotate(compact(p[0]), (d[0], p[0]), xytext=(8, -22), textcoords="offset points", color=GRAPHITE, fontsize=17)
        ax.annotate(compact(p[-1]), (d[-1], p[-1]), xytext=(8, -14), textcoords="offset points", color=GRAPHITE, fontsize=19)
        for k, m in enumerate(o.mark):
            when, label = m.split("|", 1)
            when = dt.datetime.fromisoformat(when)
            i = min(range(len(d)), key=lambda j: abs((d[j] - when).days))
            dy = top * (0.30 + 0.16 * (k % 3))
            ax.annotate(label, xy=(d[i], p[i]), xytext=(d[i], min(top * .93, p[i] + dy)),
                        ha="left" if i < len(d) * .12 else "right" if i > len(d) * .88 else "center", color=PENCIL, fontsize=15,
                        arrowprops=dict(arrowstyle="->", color=PENCIL, lw=1.1, shrinkB=4,
                                        connectionstyle="arc3,rad=.15"))
            ax.scatter([d[i]], [p[i]], s=26, facecolor="white", edgecolor=PENCIL, linewidth=1.6, zorder=6)
        mid = int(len(d) * .55)
        if o.primary_label:
            ax.annotate(o.primary_label, xy=(d[mid], p[mid]), xytext=(d[int(len(d) * .5)], top * .12),
                        color=GRAPHITE, fontsize=17,
                        arrowprops=dict(arrowstyle="->", color=GRAPHITE, lw=1.2, connectionstyle="arc3,rad=-.25"))
        if s:
            ax2 = ax.twinx(); ax2.patch.set_alpha(0)
            ax2.plot(d, s, color=PENCIL, lw=1.8)
            ax2.set_ylim(0, max(s) * 1.16)
            ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%" if pct else compact(v)))
            for k in ("top", "left", "bottom"):
                ax2.spines[k].set_visible(False)
            ax2.spines["right"].set_color(PENCIL)
            ax2.tick_params(labelsize=13, colors=PENCIL)
            ax2.scatter([d[0], d[-1]], [s[0], s[-1]], color=PENCIL, s=24, zorder=5)
            ax2.annotate(sfmt(s[0]), (d[0], s[0]), xytext=(6, -34), textcoords="offset points", color=PENCIL, fontsize=17)
            ax2.annotate(sfmt(s[-1]), (d[-1], s[-1]), xytext=(8, 4), textcoords="offset points", color=PENCIL, fontsize=17)
            if o.secondary_label:
                q = int(len(d) * .25)
                ax2.annotate(o.secondary_label, xy=(d[q], s[q]), xytext=(d[2], max(s) * 1.1),
                             color=PENCIL, fontsize=17,
                             arrowprops=dict(arrowstyle="->", color=PENCIL, lw=1.2, connectionstyle="arc3,rad=.3"))
        fig.tight_layout()
        fig.savefig(o.out, transparent=True)

    # trim transparent margins so the chart fills its taped card
    from PIL import Image
    im = Image.open(o.out); bb = im.getchannel("A").getbbox()
    if bb:
        pad = 12
        im.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad))).save(o.out, optimize=True)
    print("wrote", o.out)


if __name__ == "__main__":
    main()
