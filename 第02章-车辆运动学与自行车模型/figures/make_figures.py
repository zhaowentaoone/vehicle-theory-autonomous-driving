"""Generate textbook figures for Chapter 02 (bicycle kinematics, ICR, Ackermann)."""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent

INK = "#1f2937"
MUTED = "#6b7280"
BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#15803d"
RED = "#dc2626"
FILL = "#e5e7eb"
STROKE = "#374151"
PANEL = "#f8fafc"
WHITE = "#ffffff"
FONT = "Segoe UI, Microsoft YaHei, PingFang SC, sans-serif"

L = 2.8
LF, LR = 1.2, 1.6
TRACK = 1.5


def rot(psi: float, x: float, y: float) -> tuple[float, float]:
    c, s = math.cos(psi), math.sin(psi)
    return c * x - s * y, s * x + c * y


class Frame:
    def __init__(self, ox: float, oy: float, scale: float):
        self.ox, self.oy, self.s = ox, oy, scale

    def p(self, x: float, y: float) -> tuple[float, float]:
        return self.ox + self.s * x, self.oy - self.s * y


CURRENT_MARKER = "arr"


def header(w: int, h: int, marker_id: str) -> list[str]:
    global CURRENT_MARKER
    CURRENT_MARKER = marker_id
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'<rect width="{w}" height="{h}" fill="{WHITE}"/>',
        f'<defs><marker id="{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
        f'<path d="M 0 1.2 L 9 5 L 0 8.8 z" fill="#1f2937"/></marker></defs>',
    ]


def text(x, y, s, *, size=14, fill=INK, anchor="start", weight="500") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'
    )


def line(x1, y1, x2, y2, color, sw=1.6, dash=None, marker=True) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{CURRENT_MARKER})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" fill="none"{dash_attr}{mk}/>'
    )


def poly(pts, fill, stroke, sw=1.8) -> str:
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def circle(x, y, r, fill, stroke=None, sw=1.2) -> str:
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{st}/>'


def caption_bar(w, title: str) -> list[str]:
    return [
        f'<rect x="0" y="0" width="{w}" height="36" fill="{PANEL}"/>',
        text(20, 24, title, size=15, fill=INK, weight="600"),
    ]


def wheel(fr: Frame, cx, cy, heading, length=0.55, width=0.2):
    pts = []
    for x, y in [(length, width), (length, -width), (-length, -width), (-length, width)]:
        rx, ry = rot(heading, x, y)
        pts.append(fr.p(cx + rx, cy + ry))
    return poly(pts, "#bbf7d0", GREEN, 1.4)


def bicycle_body(fr: Frame, rear, psi, length=4.2, width=1.5):
    # rear axle center is origin of this drawing
    hx, hy = rot(psi, length / 2 + 0.15, 0)
    cx, cy = rear[0] + hx, rear[1] + hy  # roughly geometric center
    pts = []
    for x, y in [
        (length * 0.62, width / 2),
        (length * 0.62, -width / 2),
        (-length * 0.38, -width / 2),
        (-length * 0.38, width / 2),
    ]:
        rx, ry = rot(psi, x, y)
        pts.append(fr.p(rear[0] + rx, rear[1] + ry))
    return [poly(pts, FILL, STROKE, 1.7)]


def fig01_icr() -> str:
    w, h = 860, 520
    out = header(w, h, "arr-c2-1")
    out += caption_bar(w, "图 2-1　转前轮，整车绕地面上一个点转：这个点叫瞬时转动中心 ICR")
    fr = Frame(90, 455, 46)
    psi = 0.0
    rear = (4.2, 2.4)
    R = 5.4
    icr = (rear[0], rear[1] + R)
    out += bicycle_body(fr, rear, psi)
    # rear / front axle
    fx, fy = rot(psi, L, 0)
    front = (rear[0] + fx, rear[1] + fy)
    out.append(circle(*fr.p(*rear), 5, BLUE, INK, 1))
    out.append(circle(*fr.p(*front), 5, RED, INK, 1))
    out.append(text(fr.p(*rear)[0] - 8, fr.p(*rear)[1] + 18, "后轴中心", size=12, fill=BLUE, anchor="end"))
    out.append(text(fr.p(*front)[0] + 10, fr.p(*front)[1] + 4, "前轴中心", size=12, fill=RED))
    out.append(wheel(fr, rear[0], rear[1], 0.0, 0.5, 0.18))
    dlt = math.atan(L / R)
    out.append(wheel(fr, front[0], front[1], dlt, 0.5, 0.18))
    # ICR and radii
    out.append(circle(*fr.p(*icr), 6, WHITE, RED, 1.6))
    out.append(text(fr.p(*icr)[0] - 10, fr.p(*icr)[1] - 12, "ICR", size=16, fill=RED, weight="700", anchor="end"))
    out.append(line(*fr.p(*rear), *fr.p(*icr), MUTED, 1.3, "5 4", marker=False))
    out.append(line(*fr.p(*front), *fr.p(*icr), MUTED, 1.3, "5 4", marker=False))
    mid_r = fr.p(rear[0] + 0.28, rear[1] + R / 2)
    out.append(text(mid_r[0], mid_r[1], "R", size=16, fill=BLUE, weight="700"))
    # circular arc through rear
    pts = []
    for k in range(28):
        a = -0.35 + 1.05 * k / 27
        pts.append(f"{fr.p(icr[0] + R * math.sin(a), icr[1] - R * math.cos(a))[0]:.1f},{fr.p(icr[0] + R * math.sin(a), icr[1] - R * math.cos(a))[1]:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 4"/>')
    # velocity at rear: along +x
    out.append(line(*fr.p(*rear), *fr.p(rear[0] + 1.7, rear[1]), GREEN, 2.4))
    out.append(text(fr.p(rear[0] + 1.85, rear[1] - 0.15)[0], fr.p(rear[0] + 1.85, rear[1] - 0.15)[1], "速度 v 沿车头", size=13, fill=GREEN))
    # notes
    out.append(text(70, 490, "车速 v 只决定绕圈有多快；圆的半径 R 由转角几何决定，与 v 无关。这就是「运动学」：还没有力。", size=13, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig02_ackermann() -> str:
    w, h = 860, 540
    out = header(w, h, "arr-c2-2")
    out += caption_bar(w, "图 2-2　Ackermann：每个轮的轴线都穿过 ICR，内侧前轮转得更大")
    fr = Frame(80, 500, 42)
    rear = (5.6, 3.15)
    t = TRACK
    R = 6.2
    icr = (rear[0], rear[1] + R)
    psi = 0.0
    out += bicycle_body(fr, rear, psi, 4.4, 1.85)
    # four wheels
    fl = (rear[0] + L, rear[1] + t / 2)
    frw = (rear[0] + L, rear[1] - t / 2)
    rl = (rear[0], rear[1] + t / 2)
    rr = (rear[0], rear[1] - t / 2)
    d_in = math.atan(L / (R - t / 2))
    d_out = math.atan(L / (R + t / 2))
    out.append(wheel(fr, *fl, d_in, 0.48, 0.17))
    out.append(wheel(fr, *frw, d_out, 0.48, 0.17))
    out.append(wheel(fr, *rl, 0.0, 0.48, 0.17))
    out.append(wheel(fr, *rr, 0.0, 0.48, 0.17))
    out.append(circle(*fr.p(*icr), 6.5, WHITE, RED, 1.7))
    out.append(text(fr.p(*icr)[0], fr.p(*icr)[1] - 14, "ICR", size=16, fill=RED, weight="700", anchor="middle"))
    # axle lines to ICR
    for p in (fl, frw, rl, rr, rear):
        out.append(line(*fr.p(*p), *fr.p(*icr), MUTED, 1.05, "4 3", marker=False))
    out.append(line(*fr.p(*rl), *fr.p(*rr), BLUE, 1.6, marker=False))
    out.append(line(*fr.p(*fl), *fr.p(*frw), ORANGE, 1.6, marker=False))
    # labels
    out.append(text(fr.p(fl[0] + 0.55, fl[1] + 0.55)[0], fr.p(fl[0] + 0.55, fl[1] + 0.55)[1], "δ_内（更大）", size=13, fill=GREEN))
    out.append(text(fr.p(frw[0] + 0.55, frw[1] - 0.15)[0], fr.p(frw[0] + 0.55, frw[1] - 0.15)[1], "δ_外", size=13, fill=GREEN))
    out.append(text(70, 44, "后轮转角 = 0，所以 ICR 只能落在后轴延长线上。", size=13, fill=MUTED))
    out.append(text(70, 520, "tan δ_内 = L / (R − t/2)，tan δ_外 = L / (R + t/2)。轮距 t 远小于 R 时，两者几乎相等。", size=13, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig03_bicycle() -> str:
    w, h = 860, 430
    out = header(w, h, "arr-c2-3")
    out += caption_bar(w, "图 2-3　自行车模型：左右收到中轴，只用一个等效转角 δ")
    # left
    out.append(f'<rect x="20" y="52" width="400" height="350" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(220, 78, "四轮（Ackermann）", size=14, fill=INK, weight="700", anchor="middle"))
    fr = Frame(70, 360, 40)
    rear = (3.6, 2.2)
    out += bicycle_body(fr, rear, 0.0, 4.2, 1.7)
    t = 1.35
    R = 5.6
    d_in = math.atan(L / (R - t / 2))
    d_out = math.atan(L / (R + t / 2))
    out.append(wheel(fr, rear[0] + L, rear[1] + t / 2, d_in, 0.42, 0.15))
    out.append(wheel(fr, rear[0] + L, rear[1] - t / 2, d_out, 0.42, 0.15))
    out.append(wheel(fr, rear[0], rear[1] + t / 2, 0, 0.42, 0.15))
    out.append(wheel(fr, rear[0], rear[1] - t / 2, 0, 0.42, 0.15))
    out.append(text(220, 380, "内侧更大，对准同一个 ICR", size=12, fill=MUTED, anchor="middle"))
    # right
    out.append(f'<rect x="440" y="52" width="400" height="350" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(640, 78, "中轴两轮（自行车）", size=14, fill=INK, weight="700", anchor="middle"))
    fr2 = Frame(500, 360, 40)
    rear2 = (3.3, 2.2)
    out += bicycle_body(fr2, rear2, 0.0, 4.2, 1.5)
    dlt = math.atan(L / R)
    out.append(wheel(fr2, rear2[0] + L, rear2[1], dlt, 0.5, 0.18))
    out.append(wheel(fr2, rear2[0], rear2[1], 0, 0.5, 0.18))
    out.append(circle(*fr2.p(rear2[0], rear2[1]), 5, BLUE, INK, 1))
    out.append(circle(*fr2.p(rear2[0] + L, rear2[1]), 5, RED, INK, 1))
    out.append(text(fr2.p(rear2[0] + L + 0.7, rear2[1] + 1.0)[0], fr2.p(rear2[0] + L + 0.7, rear2[1] + 1.0)[1], "一个 δ", size=14, fill=GREEN, weight="700"))
    out.append(text(640, 380, "车道保持（小转角）足够；大转角泊车要想想 Ackermann", size=12, fill=MUTED, anchor="middle"))
    out.append("</svg>")
    return "\n".join(out)


def fig04_rear_vel() -> str:
    w, h = 860, 500
    out = header(w, h, "arr-c2-4")
    out += caption_bar(w, "图 2-4　后轴无侧滑：速度只能沿车头，再投影到地面")
    for i, (ox, title, psi_deg) in enumerate([(16, "第一步：在车上写速度", 0), (444, "第二步：变到地面", 32)]):
        out.append(f'<rect x="{ox}" y="52" width="400" height="400" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
        out.append(text(ox + 20, 78, title, size=14, fill=INK, weight="700"))
        fr = Frame(ox + 78, 385, 38)
        psi = math.radians(0 if i == 0 else 26)
        rear = (2.7, 2.05)
        out += bicycle_body(fr, rear, psi, 3.6, 1.45)
        out.append(wheel(fr, *rear, psi, 0.42, 0.16))
        fx, fy = rot(psi, L * 0.85, 0)
        out.append(wheel(fr, rear[0] + fx, rear[1] + fy, psi + math.radians(18), 0.42, 0.16))
        # body x velocity
        hx, hy = rot(psi, 1.8, 0)
        out.append(line(*fr.p(*rear), *fr.p(rear[0] + hx, rear[1] + hy), ORANGE, 2.4))
        out.append(text(fr.p(rear[0] + hx * 0.62, rear[1] + hy * 0.62 - 0.32)[0],
                        fr.p(rear[0] + hx * 0.62, rear[1] + hy * 0.62 - 0.32)[1], "v", size=14, fill=ORANGE, weight="700"))
        # forbidden vy
        sx, sy = rot(psi, 0, 1.15)
        out.append(line(*fr.p(*rear), *fr.p(rear[0] + sx, rear[1] + sy), RED, 1.8))
        pno = fr.p(rear[0] + sx, rear[1] + sy)
        out.append(line(pno[0] - 7, pno[1] - 7, pno[0] + 7, pno[1] + 7, RED, 2.2, marker=False))
        out.append(line(pno[0] - 7, pno[1] + 7, pno[0] + 7, pno[1] - 7, RED, 2.2, marker=False))
        if i == 0:
            out.append(text(ox + 20, 420, "无侧滑：后轴不能有车体 y 方向速度。", size=13, fill=MUTED))
        else:
            out += [
                line(*fr.p(0.2, 0.3), *fr.p(1.7, 0.3), BLUE, 2.0),
                line(*fr.p(0.2, 0.3), *fr.p(0.2, 1.8), BLUE, 2.0),
                text(fr.p(1.85, 0.3)[0], fr.p(1.85, 0.3)[1] + 4, "X", size=13, fill=BLUE),
                text(fr.p(0.2, 1.95)[0], fr.p(0.2, 1.95)[1], "Y", size=13, fill=BLUE),
            ]
            # inertial components
            out.append(line(*fr.p(*rear), *fr.p(rear[0] + hx, rear[1]), BLUE, 1.3, "4 3", marker=False))
            out.append(line(*fr.p(rear[0] + hx, rear[1]), *fr.p(rear[0] + hx, rear[1] + hy), BLUE, 1.3, "4 3", marker=False))
            out.append(text(ox + 20, 408, "Ẋ = v cosψ", size=14, fill=INK, weight="600"))
            out.append(text(ox + 20, 430, "Ẏ = v sinψ", size=14, fill=INK, weight="600"))
            out.append(text(ox + 20, 448, "这就是第 01 章 R(ψ) 乘 (v, 0)。", size=12, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig05_triangle() -> str:
    w, h = 860, 520
    out = header(w, h, "arr-c2-5")
    out += caption_bar(w, "图 2-5　前轮对准 ICR：直角三角形给出 R = L / tanδ，再得到 ψ̇")
    fr = Frame(90, 470, 52)
    rear = (3.4, 2.2)
    R = 5.0
    icr = (rear[0], rear[1] + R)
    dlt = math.atan(L / R)
    front = (rear[0] + L, rear[1])
    out += bicycle_body(fr, rear, 0.0, 4.0, 1.35)
    out.append(wheel(fr, *rear, 0.0, 0.48, 0.17))
    out.append(wheel(fr, *front, dlt, 0.48, 0.17))
    out.append(circle(*fr.p(*rear), 5.5, BLUE, INK, 1))
    out.append(circle(*fr.p(*front), 5.5, RED, INK, 1))
    out.append(circle(*fr.p(*icr), 6.5, WHITE, RED, 1.7))
    out.append(text(fr.p(*icr)[0] - 12, fr.p(*icr)[1] - 10, "ICR", size=16, fill=RED, weight="700", anchor="end"))
    # triangle
    out.append(line(*fr.p(*rear), *fr.p(*front), ORANGE, 2.2, marker=False))
    out.append(line(*fr.p(*rear), *fr.p(*icr), BLUE, 2.2, marker=False))
    out.append(line(*fr.p(*front), *fr.p(*icr), GREEN, 2.0, marker=False))
    # right angle mark
    ra = 0.35
    out.append(line(*fr.p(rear[0] + ra, rear[1]), *fr.p(rear[0] + ra, rear[1] + ra), INK, 1.2, marker=False))
    out.append(line(*fr.p(rear[0], rear[1] + ra), *fr.p(rear[0] + ra, rear[1] + ra), INK, 1.2, marker=False))
    out.append(text(fr.p((rear[0] + front[0]) / 2, rear[1] - 0.32)[0],
                    fr.p((rear[0] + front[0]) / 2, rear[1] - 0.32)[1], "轴距 L", size=14, fill=ORANGE, anchor="middle", weight="700"))
    out.append(text(fr.p(rear[0] - 0.55, rear[1] + R / 2)[0],
                    fr.p(rear[0] - 0.55, rear[1] + R / 2)[1], "R", size=16, fill=BLUE, weight="700", anchor="end"))
    # delta arc at front
    out.append(text(fr.p(front[0] + 0.25, front[1] + 1.15)[0],
                    fr.p(front[0] + 0.25, front[1] + 1.15)[1], "δ", size=18, fill=GREEN, weight="700"))
    # panel
    out.append(f'<rect x="560" y="70" width="280" height="390" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    lines = [
        ("对直角三角形：", INK, "700"),
        ("对边 L，邻边 R", MUTED, "500"),
        ("tan δ = L / R", GREEN, "700"),
        ("于是  R = L / tanδ", BLUE, "700"),
        ("刚体绕 ICR 转：", INK, "700"),
        ("后轴线速度 v = ω R", MUTED, "500"),
        ("ω 就是横摆角速度 ψ̇", MUTED, "500"),
        ("所以  ψ̇ = v / R", ORANGE, "700"),
        ("代入 R：", INK, "700"),
        ("ψ̇ = (v / L) tanδ", RED, "700"),
    ]
    y = 100
    for s, c, wt in lines:
        out.append(text(578, y, s, size=14, fill=c, weight=wt))
        y += 32
    out.append("</svg>")
    return "\n".join(out)


def fig06_small_angle() -> str:
    w, h = 860, 460
    out = header(w, h, "arr-c2-6")
    out += caption_bar(w, "图 2-6　小转角：tanδ ≈ δ（弧度）。车道保持常用；泊车不要用")
    # plot tan vs delta
    left, top, pw, ph = 70, 70, 420, 320
    out.append(f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="{PANEL}" stroke="#e5e7eb"/>')
    # axes
    ox, oy = left + 50, top + ph - 40
    axw, axh = 330, 250
    out.append(line(ox, oy, ox + axw, oy, INK, 1.4))
    out.append(line(ox, oy, ox, oy - axh, INK, 1.4))
    out.append(text(ox + axw - 10, oy + 22, "δ (deg)", size=12, fill=MUTED, anchor="end"))
    out.append(text(ox - 8, oy - axh + 8, "tanδ 与 δ(rad)", size=12, fill=MUTED, anchor="end"))
    dmax = 40.0
    def px(deg):
        return ox + axw * deg / dmax
    def py(val):  # val in rad-like 0..0.84
        return oy - axh * val / 0.90
    # identity
    p1 = []
    p2 = []
    for d in range(0, 41):
        rad = math.radians(d)
        p1.append(f"{px(d):.1f},{py(rad):.1f}")
        p2.append(f"{px(d):.1f},{py(math.tan(rad)):.1f}")
    out.append(f'<polyline points="{" ".join(p1)}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    out.append(f'<polyline points="{" ".join(p2)}" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
    # 5 deg marker
    out.append(line(px(5), oy, px(5), py(math.tan(math.radians(5))), MUTED, 1.1, "3 3", marker=False))
    out.append(text(px(5), oy + 22, "5°", size=12, fill=MUTED, anchor="middle"))
    out.append(text(px(32), py(math.radians(32)) + 14, "δ（弧度）", size=13, fill=BLUE))
    out.append(text(px(32), py(math.tan(math.radians(32))) - 8, "tanδ", size=13, fill=ORANGE))
    # right notes
    out.append(f'<rect x="520" y="70" width="320" height="340" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    notes = [
        (94, "车道保持 |δ| 多半 < 5°", INK),
        (128, "5° 时 tanδ 与 δ 相差约 0.3%", MUTED),
        (162, "于是 ψ̇ ≈ v δ / L", GREEN),
        (206, "这是第 09 章线性化的起点。", MUTED),
        (250, "泊车 |δ| 可达 30°+", RED),
        (284, "30° 时 tanδ / δ ≈ 1.21", RED),
        (318, "误差超过 20%，不要用小角度。", RED),
        (360, "公式里的 δ 必须是弧度。", INK),
    ]
    for y, s, c in notes:
        out.append(text(538, y, s, size=14, fill=c, weight="600" if c != MUTED else "500"))
    out.append("</svg>")
    return "\n".join(out)


def fig07_cg_beta() -> str:
    w, h = 860, 520
    out = header(w, h, "arr-c2-7")
    out += caption_bar(w, "图 2-7　参考点改到质心：后轴仍无侧滑，但质心速度偏一个几何角 β")
    fr = Frame(80, 470, 50)
    rear = (3.6, 2.15)
    R = 5.2
    icr = (rear[0], rear[1] + R)
    dlt = math.atan(L / R)
    cg = (rear[0] + LR, rear[1])
    front = (rear[0] + L, rear[1])
    out += bicycle_body(fr, rear, 0.0, 4.1, 1.4)
    out.append(wheel(fr, *rear, 0.0, 0.45, 0.16))
    out.append(wheel(fr, *front, dlt, 0.45, 0.16))
    out.append(circle(*fr.p(*rear), 5, BLUE, INK, 1))
    out.append(circle(*fr.p(*cg), 6, ORANGE, INK, 1.1))
    out.append(circle(*fr.p(*icr), 6, WHITE, RED, 1.6))
    out.append(text(fr.p(*rear)[0], fr.p(*rear)[1] + 20, "后轴", size=12, fill=BLUE, anchor="middle"))
    out.append(text(fr.p(*cg)[0], fr.p(*cg)[1] + 20, "质心", size=12, fill=ORANGE, anchor="middle"))
    out.append(text(fr.p(*icr)[0] - 10, fr.p(*icr)[1] - 10, "ICR", size=14, fill=RED, weight="700", anchor="end"))
    out.append(line(*fr.p(*rear), *fr.p(*icr), MUTED, 1.2, "4 3", marker=False))
    out.append(line(*fr.p(*cg), *fr.p(*icr), ORANGE, 1.5, "4 3", marker=False))
    # velocity at CG: perpendicular to ICR-CG
    # from ICR to CG: (LR, -R), 90 CCW: (R, LR)
    hx, hy = R, LR
    n = math.hypot(hx, hy)
    hx, hy = 1.8 * hx / n, 1.8 * hy / n
    out.append(line(*fr.p(*cg), *fr.p(cg[0] + hx, cg[1] + hy), RED, 2.4))
    out.append(text(fr.p(cg[0] + hx + 0.15, cg[1] + hy)[0],
                    fr.p(cg[0] + hx + 0.15, cg[1] + hy)[1], "质心速度", size=13, fill=RED))
    # heading vs velocity = beta
    out.append(line(*fr.p(*cg), *fr.p(cg[0] + 1.6, cg[1]), ORANGE, 1.5, marker=False))
    out.append(text(fr.p(cg[0] + 0.7, cg[1] + 0.55)[0],
                    fr.p(cg[0] + 0.7, cg[1] + 0.55)[1], "β", size=16, fill=RED, weight="700"))
    out.append(text(70, 500, "tanβ = l_r / R = l_r tanδ / L。这个 β 是几何量，不是第 05 章由侧向力产生的动力学侧偏角。", size=13, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig08_curvature() -> str:
    w, h = 860, 460
    out = header(w, h, "arr-c2-8")
    out += caption_bar(w, "图 2-8　路径曲率 κ = dψ/ds；自行车把它变成转角 δ = arctan(κ L)")
    # path
    out.append(f'<rect x="30" y="56" width="500" height="370" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    # clothoid-like arc
    pts = []
    for i in range(40):
        t = i / 39
        x = 70 + 430 * t
        y = 330 - 180 * (t * t)
        pts.append(f"{x:.1f},{y:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
    # two nearby tangents
    def pos(t):
        x = 70 + 430 * t
        y = 330 - 180 * (t * t)
        # dy/dt = -360 t, dx/dt = 430
        ang = math.atan2(360 * t, 430)  # heading of path in screen (y down so flip)
        return x, y, math.atan2(-360 * t, 430)
    x1, y1, a1 = pos(0.35)
    x2, y2, a2 = pos(0.55)
    out.append(line(x1, y1, x1 + 70 * math.cos(a1), y1 + 70 * math.sin(a1), ORANGE, 2.0))
    out.append(line(x2, y2, x2 + 70 * math.cos(a2), y2 + 70 * math.sin(a2), ORANGE, 2.0))
    out.append(circle(x1, y1, 4.5, ORANGE, INK, 1))
    out.append(circle(x2, y2, 4.5, ORANGE, INK, 1))
    out.append(text(x1 - 4, y1 + 22, "ψ", size=13, fill=ORANGE))
    out.append(text(x2 + 8, y2 + 22, "ψ+dψ", size=13, fill=ORANGE))
    out.append(text( (x1+x2)/2, (y1+y2)/2 + 28, "ds", size=13, fill=BLUE, anchor="middle"))
    out.append(text(50, 400, "沿路径走一小段弧长 ds，航向增加 dψ，则 κ = dψ / ds。", size=13, fill=MUTED))
    # right panel
    out.append(f'<rect x="550" y="56" width="290" height="370" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    box = [
        (90, "ds = v dt", MUTED),
        (128, "dψ = ψ̇ dt", MUTED),
        (166, "κ = dψ/ds = ψ̇ / v", INK),
        (214, "代入自行车 ψ̇：", MUTED),
        (252, "κ = tanδ / L", GREEN),
        (300, "反过来给规划器用：", MUTED),
        (338, "δ = arctan(κ L)", BLUE),
        (380, "闭环还要改误差（第 08 章）", MUTED),
    ]
    for y, s, c in box:
        out.append(text(568, y, s, size=14, fill=c, weight="700" if c != MUTED else "500"))
    out.append("</svg>")
    return "\n".join(out)


def fig09_euler() -> str:
    w, h = 860, 470
    out = header(w, h, "arr-c2-9")
    out += caption_bar(w, "图 2-9　常转角本应走圆弧；欧拉用切线弦代替弧，步长大了圆会裂开")
    # true circle
    cx, cy, rad = 250, 270, 140
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    out.append(text(cx, cy - rad - 12, "真实圆弧", size=13, fill=BLUE, anchor="middle"))
    # start point at right
    ang0 = 0.15
    x0 = cx + rad * math.cos(ang0)
    y0 = cy + rad * math.sin(ang0)
    # tangent Euler steps
    dpsi = 0.42
    x, y, a = x0, y0, ang0 + math.pi / 2  # heading tangent CCW
    out.append(circle(x0, y0, 5, GREEN, INK, 1))
    px, py = x0, y0
    for i in range(5):
        step = 48
        nx = px + step * math.cos(a)
        ny = py + step * math.sin(a)
        out.append(line(px, py, nx, ny, ORANGE, 2.2, marker=(i == 4)))
        a += dpsi
        px, py = nx, ny
        out.append(circle(px, py, 3.5, ORANGE))
    out.append(text(px + 8, py + 4, "欧拉折线", size=13, fill=ORANGE))
    # right notes
    out.append(f'<rect x="500" y="60" width="340" height="370" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    notes = [
        (90, "前向欧拉在想什么", INK),
        (122, "用此刻的速度直线冲 Δt", MUTED),
        (148, "X ← X + Δt v cosψ", BLUE),
        (174, "Y ← Y + Δt v sinψ", BLUE),
        (200, "ψ ← ψ + Δt (v/L) tanδ", BLUE),
        (240, "Δt 很小：折线贴着圆", GREEN),
        (266, "Δt 很大：一步切出去", RED),
        (304, "常 v、δ 时有精确圆弧公式", INK),
        (330, "一步转 Δψ = v Δt / R", MUTED),
        (356, "几何上没有局部截断误差。", MUTED),
        (392, "本课程仿真默认 Δt = 0.01 s。", MUTED),
    ]
    for y, s, c in notes:
        out.append(text(518, y, s, size=14, fill=c, weight="600" if c in (INK, BLUE, GREEN, RED) else "500"))
    out.append("</svg>")
    return "\n".join(out)


def fig10_fail() -> str:
    w, h = 860, 430
    out = header(w, h, "arr-c2-10")
    out += caption_bar(w, "图 2-10　运动学何时定性错：侧向加速度大、轮胎要侧偏角才能提供力")
    # left ok
    out.append(f'<rect x="20" y="52" width="400" height="340" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(220, 80, "低速 / 小曲率：运动学够用", size=14, fill=GREEN, weight="700", anchor="middle"))
    out.append(text(40, 120, "几何要求的向心加速度", size=13, fill=MUTED))
    out.append(text(40, 148, "a_y ≈ v² κ = v² tanδ / L", size=15, fill=INK, weight="700"))
    out.append(text(40, 186, "若 a_y 只有 0.1 g 量级，", size=14, fill=INK))
    out.append(text(40, 214, "轮胎几乎不用侧偏就能提供力，", size=14, fill=INK))
    out.append(text(40, 242, "车真的按几何圆走。", size=14, fill=INK))
    out.append(text(40, 286, "停车场、低速跟线、教学仿真", size=13, fill=GREEN))
    out.append(text(40, 314, "→ 用本章模型。", size=13, fill=GREEN))
    # right fail
    out.append(f'<rect x="440" y="52" width="400" height="340" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(640, 80, "高速 / 大曲率：必须上动力学", size=14, fill=RED, weight="700", anchor="middle"))
    out.append(text(460, 120, "粗判：v² κ > 0.3 g", size=15, fill=RED, weight="700"))
    out.append(text(460, 156, "轮胎要先有侧偏角才有侧向力，", size=14, fill=INK))
    out.append(text(460, 184, "实际曲率小于几何 tanδ/L", size=14, fill=INK))
    out.append(text(460, 212, "（不足转向：你打了方向，弯没那么急）。", size=14, fill=INK))
    out.append(text(460, 250, "冰雪、甩尾、ESP：几何约束先破。", size=14, fill=INK))
    out.append(text(460, 286, "这些现象第 03、05 章才解释。", size=13, fill=MUTED))
    out.append(text(460, 318, "现在先把几何模型写对。", size=13, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    figs = {
        "fig01-icr.svg": fig01_icr(),
        "fig02-ackermann.svg": fig02_ackermann(),
        "fig03-bicycle.svg": fig03_bicycle(),
        "fig04-rear-velocity.svg": fig04_rear_vel(),
        "fig05-triangle.svg": fig05_triangle(),
        "fig06-small-angle.svg": fig06_small_angle(),
        "fig07-cg-beta.svg": fig07_cg_beta(),
        "fig08-curvature.svg": fig08_curvature(),
        "fig09-euler.svg": fig09_euler(),
        "fig10-when-fails.svg": fig10_fail(),
    }
    for name, svg in figs.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
