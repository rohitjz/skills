#!/usr/bin/env python3
"""Exercise the repo tooling end to end: validator, installer, and the analog-ui scripts
(chart in every mode, CSV and XLSX input, email export, asset inlining)."""
import csv, datetime as dt, math, pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SK = ROOT / "skills/design/analog-ui"
SB = SK / "mediums/sketchbook"
PY = sys.executable
results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail and not ok else ''}")


def run(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def main():
    tmp = pathlib.Path(tempfile.mkdtemp())

    r = run(PY, str(ROOT / "scripts/validate.py"))
    check("validate.py passes", r.returncode == 0, r.stdout[-300:])

    r = run("bash", str(ROOT / "install.sh"), "--list")
    n = len([l for l in r.stdout.splitlines() if l.strip()])
    check("install.sh --list lists every skill", r.returncode == 0 and n == len(list(ROOT.glob("skills/*/*/SKILL.md"))), f"{n} listed")
    r = run("bash", str(ROOT / "install.sh"), "--target", str(tmp / "inst"), "--category", "design")
    check("install.sh installs a category flat", (tmp / "inst/analog-ui/SKILL.md").exists() and (tmp / "inst/analog-ui/mediums/sketchbook/assets/sketchbook.css").exists() and not (tmp / "inst/sketchbook-ui").exists(), r.stderr)
    r = run("bash", str(ROOT / "install.sh"), "--target", str(tmp / "lnk"), "--link", "council")
    check("install.sh --link makes a symlink", (tmp / "lnk/council").is_symlink(), r.stderr)
    r = run("bash", str(ROOT / "install.sh"), "--target", str(tmp / "x"), "does-not-exist")
    check("install.sh fails on unknown skill", r.returncode != 0)

    data = tmp / "d.csv"
    with open(data, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date", "users", "share", "pct", "count"])
        for i in range(200):
            day = dt.date(2025, 1, 1) + dt.timedelta(days=i * 5)
            w.writerow([day.isoformat(), 1000 + i * 40 + 80 * math.sin(i / 4), 0.03 + i / 9000, 3 + i / 90, 5000 + i * 300])
    chart = SB / "scripts/sketch_chart.py"
    cases = {
        "primary only": [],
        "ratio secondary": ["--secondary", "share", "--secondary-label", "share"],
        "pct secondary": ["--secondary", "pct", "--secondary-format", "pct"],
        "count secondary": ["--secondary", "count", "--secondary-format", "count"],
        "smoothing + thinning": ["--smooth", "7", "--every", "3"],
        "milestone marks": ["--mark", "2025-03-01|launch", "--mark", "2027-06-01|v2", "--primary-label", "users"],
    }
    for label, extra in cases.items():
        slug = re.sub(r"\W+", "-", label)
        out = tmp / f"c-{slug}.png"
        r = run(PY, str(chart), str(data), "--date", "date", "--primary", "users", "--out", str(out), *extra)
        check(f"sketch_chart: {label}", r.returncode == 0 and out.exists() and out.stat().st_size > 5000, r.stderr[-300:])

    try:
        import openpyxl
        wb = openpyxl.Workbook(); ws = wb.active; ws.append(["date", "users"])
        for i in range(60):
            ws.append([dt.datetime(2026, 1, 1) + dt.timedelta(days=i), 500 + i * 7])
        x = tmp / "d.xlsx"; wb.save(x)
        out = tmp / "xlsx.png"
        r = run(PY, str(chart), str(x), "--date", "date", "--primary", "users", "--out", str(out))
        check("sketch_chart: xlsx input, month ticks", r.returncode == 0 and out.exists(), r.stderr[-300:])
    except ImportError:
        check("sketch_chart: xlsx input", False, "openpyxl missing")

    from PIL import Image
    im = Image.open(tmp / "c-primary-only.png")
    check("sketch_chart: output is transparent and trimmed", im.mode == "RGBA" and im.getchannel("A").getextrema()[0] == 0)

    sample = SB / "examples/lets-encrypt-10-years/index.html"
    single = tmp / "single.html"
    r = run(PY, str(SK / "scripts/inline_assets.py"), str(sample), "-o", str(single))
    html = single.read_text() if single.exists() else ""
    local = re.findall(r'(?:href|src)="(?!https?:|data:|#|//)[^"]+\.(?:css|png|jpg|svg)"', html)
    check("inline_assets: no local css/img references left", r.returncode == 0 and html and not local, str(local[:3]))

    out = tmp / "email"
    r = run(PY, str(SK / "scripts/export_email.py"), str(sample), "--slices", "4", "--out", str(out))
    parts = sorted(out.glob("part-*.png"))
    widths = {Image.open(p).width for p in parts}
    total = sum(Image.open(p).height for p in parts)
    full = Image.open(out / "full.png").height if (out / "full.png").exists() else -1
    check("export_email: 4 slices, same width, no lost rows", r.returncode == 0 and len(parts) == 4 and len(widths) == 1 and total == full, r.stderr[-300:] or f"{len(parts)} parts, {total} vs {full}")
    check("export_email: paste page references every slice", all(p.name in (out / "paste-into-email.html").read_text() for p in parts))

    fails = [r for r in results if not r[1]]
    print(f"\n{len(results)} tool checks, {len(fails)} failures")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
