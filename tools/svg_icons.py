#!/usr/bin/env python3
"""Flatten the studio's stroke icons (assets/icons/lucide + assets/icons/custom,
24x24, 2px stroke) into Elisa line segments: build/generated/studio_icon_paths.elisa.

elisa-ui draws strokes, not SVG, so every path/circle/rect/line/polyline is
flattened to short segments in the 24-unit box. Curves get few segments
(about one per 3 units of arc length) to stay inside UiCore::MAX_COMMANDS.

    python3 tools/svg_icons.py [out.elisa]
"""
import math, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Studio icon name -> source SVG (relative to assets/icons). Order = icon codes.
ICONS = [
    ("PLAY", "lucide/play.svg"), ("PAUSE", "lucide/pause.svg"),
    ("BACK", "lucide/skip-back.svg"), ("FORWARD", "lucide/skip-forward.svg"),
    ("LOOP", "lucide/repeat.svg"), ("UNDO", "lucide/undo-2.svg"), ("REDO", "lucide/redo-2.svg"),
    ("TRAILS", "custom/trails.svg"), ("CONTACTS", "custom/contacts.svg"),
    ("HEAT", "lucide/flame.svg"), ("ONION", "lucide/layers.svg"), ("GHOST", "lucide/ghost.svg"),
    ("XRAY", "lucide/scan-eye.svg"), ("MESH", "lucide/box.svg"), ("EXPORT", "lucide/download.svg"),
    ("FRAME", "lucide/scan.svg"), ("EYE", "lucide/eye.svg"), ("EYE_OFF", "lucide/eye-off.svg"),
    ("UP", "lucide/chevron-up.svg"), ("DOWN", "lucide/chevron-down.svg"),
    ("TRASH", "lucide/trash-2.svg"), ("PLUS", "lucide/plus.svg"), ("BALANCE", "lucide/scale.svg"),
    ("CLEAN", "lucide/sparkles.svg"), ("OPEN", "lucide/folder-open.svg"), ("SAVE", "lucide/save.svg"),
    ("FOOT_FIX", "custom/foot-fix.svg"), ("PIVOT", "custom/pivot.svg"),
    ("SPIKE", "custom/spike.svg"), ("RETIME", "custom/retime.svg"),
]


def steps(length):
    return max(2, min(6, int(math.ceil(length / 4.0))))


def arc_points(x1, y1, rx, ry, phi, large, sweep, x2, y2):
    # SVG endpoint arc -> centre parameterisation (SVG 1.1 appendix F.6).
    if rx == 0 or ry == 0:
        return [(x2, y2)]
    rx, ry = abs(rx), abs(ry)
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    xp, yp = c * dx + s * dy, -s * dx + c * dy
    lam = xp * xp / (rx * rx) + yp * yp / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * yp * yp - ry * ry * xp * xp
    den = rx * rx * yp * yp + ry * ry * xp * xp
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        co = -co
    cxp, cyp = co * rx * yp / ry, -co * ry * xp / rx
    cx = c * cxp - s * cyp + (x1 + x2) / 2
    cy = s * cxp + c * cyp + (y1 + y2) / 2
    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a
    t1 = ang(1, 0, (xp - cxp) / rx, (yp - cyp) / ry)
    dt = ang((xp - cxp) / rx, (yp - cyp) / ry, (-xp - cxp) / rx, (-yp - cyp) / ry)
    if not sweep and dt > 0:
        dt -= 2 * math.pi
    elif sweep and dt < 0:
        dt += 2 * math.pi
    n = steps(abs(dt) * max(rx, ry))
    pts = []
    for i in range(1, n + 1):
        t = t1 + dt * i / n
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        pts.append((c * ex - s * ey + cx, s * ex + c * ey + cy))
    return pts


def path_polylines(d):
    toks = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?", d)
    i, cmd = 0, None
    x = y = sx = sy = 0.0
    last_ctrl = None
    lines, cur = [], []
    def num():
        nonlocal i
        v = float(toks[i]); i += 1
        return v
    def flag():
        # Arc flags may be packed against the next number ("011.5").
        nonlocal i
        t = toks[i]
        if len(t) > 1 and t[0] in "01":
            toks[i] = t[1:]
            return int(t[0])
        i += 1
        return int(float(t))
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
        rel = cmd.islower()
        C = cmd.upper()
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if C == "M":
            if len(cur) > 1:
                lines.append(cur)
            x, y = ox + num(), oy + num()
            sx, sy = x, y
            cur = [(x, y)]
            cmd = "l" if rel else "L"
            last_ctrl = None
        elif C == "L":
            x, y = ox + num(), oy + num(); cur.append((x, y)); last_ctrl = None
        elif C == "H":
            x = ox + num(); cur.append((x, y)); last_ctrl = None
        elif C == "V":
            y = (y if rel else 0.0) + num(); cur.append((x, y)); last_ctrl = None
        elif C in "CS":
            if C == "C":
                x1, y1 = ox + num(), oy + num()
            else:
                x1, y1 = (2 * x - last_ctrl[0], 2 * y - last_ctrl[1]) if last_ctrl else (x, y)
            x2, y2 = ox + num(), oy + num()
            ex, ey = ox + num(), oy + num()
            n = steps(math.dist((x, y), (x1, y1)) + math.dist((x1, y1), (x2, y2)) + math.dist((x2, y2), (ex, ey)))
            for k in range(1, n + 1):
                t = k / n; u = 1 - t
                cur.append((u**3 * x + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * ex,
                            u**3 * y + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * ey))
            last_ctrl = (x2, y2); x, y = ex, ey
        elif C in "QT":
            if C == "Q":
                x1, y1 = ox + num(), oy + num()
            else:
                x1, y1 = (2 * x - last_ctrl[0], 2 * y - last_ctrl[1]) if last_ctrl else (x, y)
            ex, ey = ox + num(), oy + num()
            n = steps(math.dist((x, y), (x1, y1)) + math.dist((x1, y1), (ex, ey)))
            for k in range(1, n + 1):
                t = k / n; u = 1 - t
                cur.append((u * u * x + 2 * u * t * x1 + t * t * ex, u * u * y + 2 * u * t * y1 + t * t * ey))
            last_ctrl = (x1, y1); x, y = ex, ey
        elif C == "A":
            rx, ry, phi = num(), num(), num()
            large = flag(); sweep = flag()
            ex, ey = ox + num(), oy + num()
            cur.extend(arc_points(x, y, rx, ry, phi, large, sweep, ex, ey))
            x, y = ex, ey; last_ctrl = None
        elif C == "Z":
            cur.append((sx, sy)); x, y = sx, sy; last_ctrl = None
            lines.append(cur); cur = [(x, y)]
    if len(cur) > 1:
        lines.append(cur)
    return lines


def ellipse(cx, cy, rx, ry):
    n = max(6, min(10, int(math.ceil(2 * math.pi * max(rx, ry) / 4.0))))
    return [[(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]]


MAX_SEGMENTS = 20  # per icon: 18 toolbar icons stay ~360 of 1024 commands


def simplify(pts, tol):
    # Douglas-Peucker on one polyline.
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    L = math.dist(pts[0], pts[-1])
    def dist(p):
        if L < 1e-9:
            return math.dist(p, pts[0])
        return abs((bx - ax) * (ay - p[1]) - (ax - p[0]) * (by - ay)) / L
    k, d = max(((i, dist(p)) for i, p in enumerate(pts[1:-1], 1)), key=lambda t: t[1])
    if d <= tol:
        return [pts[0], pts[-1]]
    return simplify(pts[:k + 1], tol)[:-1] + simplify(pts[k:], tol)


def icon_segments(path):
    polys = icon_polylines(path)
    tol = 0.0
    while True:
        segs = []
        for p in polys:
            q = simplify(p, tol) if tol > 0 else p
            for (x1, y1), (x2, y2) in zip(q, q[1:]):
                if math.dist((x1, y1), (x2, y2)) > 1e-3:
                    segs.append((x1, y1, x2, y2))
        if len(segs) <= MAX_SEGMENTS or tol > 3.0:
            return segs
        tol += 0.15


def icon_polylines(path):
    tree = ET.parse(path)
    out = []
    for el in tree.iter():
        tag = el.tag.split("}")[-1]
        a = {k: el.get(k) for k in el.keys()}
        f = lambda k, dflt=0.0: float(a.get(k, dflt))
        if tag == "path":
            polys = path_polylines(a["d"])
        elif tag == "circle":
            polys = ellipse(f("cx"), f("cy"), f("r"), f("r"))
        elif tag == "ellipse":
            polys = ellipse(f("cx"), f("cy"), f("rx"), f("ry"))
        elif tag == "line":
            polys = [[(f("x1"), f("y1")), (f("x2"), f("y2"))]]
        elif tag in ("polyline", "polygon"):
            nums = [float(v) for v in re.findall(r"-?\d*\.?\d+", a["points"])]
            pts = list(zip(nums[0::2], nums[1::2]))
            polys = [pts + ([pts[0]] if tag == "polygon" else [])]
        elif tag == "rect":
            x, y, w, h, r = f("x"), f("y"), f("width"), f("height"), f("rx", a.get("ry", 0))
            if r > 0:
                d = (f"M{x+r} {y}h{w-2*r}a{r} {r} 0 0 1 {r} {r}v{h-2*r}a{r} {r} 0 0 1 {-r} {r}"
                     f"h{-(w-2*r)}a{r} {r} 0 0 1 {-r} {-r}v{-(h-2*r)}a{r} {r} 0 0 1 {r} {-r}z")
                polys = path_polylines(d)
            else:
                polys = [[(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]]
        else:
            continue
        out.extend(polys)
    return out


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "build", "generated", "studio_icon_paths.elisa")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    lines = ["# GENERATED by tools/svg_icons.py from assets/icons (Lucide ISC + custom). Do not edit.",
             "module StudioIconPaths:", "    public:"]
    lines.append("        const enum Icon of i64:")
    for code, (name, _) in enumerate(ICONS):
        variant = "".join(part.title() for part in name.lower().split("_"))
        lines.append(f"            {variant} = {code}")
    lines.append(f"        const COUNT: i64 = {len(ICONS)}")
    lines += ["",
              "        # Strokes icon `icon` into the s x s box at (x, y); 24 SVG units span s.",
              "        def draw(icon: Icon, x: f32, y: f32, s: f32, w: f32, c: UiCore::Color) -> void can[Global{Read, Write}]:",
              "            k: f32 = s / 24.0"]
    total = 0
    for code, (name, src) in enumerate(ICONS):
        segs = icon_segments(os.path.join(ROOT, "assets", "icons", src))
        total += len(segs)
        variant = "".join(part.title() for part in name.lower().split("_"))
        lines.append(f"            {'if' if code == 0 else 'elif'} icon == Icon.{variant}:")
        for x1, y1, x2, y2 in segs:
            lines.append(f"                StudioDraw::segment(x + {x1:.2f} * k, y + {y1:.2f} * k, x + {x2:.2f} * k, y + {y2:.2f} * k, w, c)")
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {out}: {len(ICONS)} icons, {total} segments")


if __name__ == "__main__":
    main()
