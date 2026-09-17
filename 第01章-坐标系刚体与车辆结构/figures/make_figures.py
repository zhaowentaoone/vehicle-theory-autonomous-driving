"""Generate textbook figures for Chapter 01 (right-hand, y-left, yaw CCW+)."""

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


def rot(psi: float, x: float, y: float) -> tuple[float, float]:
    c, s = math.cos(psi), math.sin(psi)
    return c * x - s * y, s * x + c * y


class Frame:
    """Math y-up → SVG y-down."""

    def __init__(self, ox: float, oy: float, scale: float):
        self.ox, self.oy, self.s = ox, oy, scale

    def p(self, x: float, y: float) -> tuple[float, float]:
        return self.ox + self.s * x, self.oy - self.s * y

    def xy(self, x: float, y: float) -> str:
        px, py = self.p(x, y)
        return f"{px:.2f},{py:.2f}"


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


def text(x: float, y: float, s: str, *, size: int = 14, fill: str = INK, anchor: str = "start", weight: str = "500") -> str:
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


def poly(pts: list[tuple[float, float]], fill, stroke, sw=1.8) -> str:
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def circle(x, y, r, fill, stroke=None, sw=1.2) -> str:
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{st}/>'


def axis_pair(fr: Frame, origin, ex, ey, len_m, c_x, c_y, lx, ly, *, size=13):
    ox, oy = origin
    x2 = (ox + ex[0] * len_m, oy + ex[1] * len_m)
    y2 = (ox + ey[0] * len_m, oy + ey[1] * len_m)
    p0, px, py = fr.p(ox, oy), fr.p(*x2), fr.p(*y2)
    lx_pos = fr.p(ox + ex[0] * len_m * 1.12, oy + ex[1] * len_m * 1.12)
    ly_pos = fr.p(ox + ey[0] * len_m * 1.12, oy + ey[1] * len_m * 1.12)
    return [
        line(*p0, *px, c_x, 2.2),
        line(*p0, *py, c_y, 2.2),
        circle(*p0, 3.2, c_x, INK, 0.8),
        text(lx_pos[0], lx_pos[1] + 4, lx, size=size, fill=c_x, anchor="middle"),
        text(ly_pos[0], ly_pos[1] + 4, ly, size=size, fill=c_y, anchor="middle"),
    ]


def car_corners(psi, length=4.5, width=1.8):
    hl, hw = length / 2, width / 2
    body = [(hl, hw), (hl, -hw), (-hl, -hw), (-hl, hw)]
    return [rot(psi, x, y) for x, y in body]


def draw_car(fr: Frame, cg, psi, fill=FILL):
    X, Y = cg
    pts = []
    for x, y in car_corners(psi):
        pts.append(fr.p(X + x, Y + y))
    fx, fy = rot(psi, 1.2, 0)
    rx, ry = rot(psi, -1.6, 0)
    nose = rot(psi, 2.55, 0)
    return [
        poly(pts, fill, STROKE, 1.8),
        # tiny nose tick so heading is obvious
        line(*fr.p(X + fx * 0.85, Y + fy * 0.85), *fr.p(X + nose[0], Y + nose[1]), STROKE, 1.6, marker=False),
        circle(*fr.p(X, Y), 4.5, ORANGE, INK, 1.0),
        circle(*fr.p(X + fx, Y + fy), 3.4, "#fca5a5", RED, 1.0),
        circle(*fr.p(X + rx, Y + ry), 3.4, "#93c5fd", BLUE, 1.0),
    ]


def caption_bar(w, y, title: str) -> list[str]:
    return [
        f'<rect x="0" y="{y}" width="{w}" height="36" fill="{PANEL}"/>',
        text(20, y + 24, title, size=15, fill=INK, weight="600"),
    ]


def fig01_three_frames() -> str:
    w, h = 860, 540
    out = header(w, h, "arr-fig01")
    out += caption_bar(w, 0, "图 1-1　三个坐标系（俯视，z 向上、逆时针为正）")
    fr = Frame(70, 470, 58)
    # light inertial grid
    for i in range(0, 13):
        x0, y0 = fr.p(i, 0)
        x1, y1 = fr.p(i, 6.6)
        out.append(line(x0, y0, x1, y1, "#eef2f7", 1, marker=False))
    for j in range(0, 7):
        x0, y0 = fr.p(0, j)
        x1, y1 = fr.p(12.2, j)
        out.append(line(x0, y0, x1, y1, "#eef2f7", 1, marker=False))

    # inertial axes at origin
    out += axis_pair(fr, (0, 0), (1, 0), (0, 1), 2.6, BLUE, BLUE, "X", "Y")
    out.append(text(*fr.p(-0.15, -0.45), "{I} 惯性系（钉在地面）", size=13, fill=BLUE))

    cg = (6.4, 3.15)
    psi = math.radians(32)
    delta = math.radians(18)
    out += draw_car(fr, cg, psi)
    out.append(text(fr.p(*cg)[0] - 18, fr.p(*cg)[1] + 18, "质心", size=12, fill=ORANGE))

    # body axes
    ex, ey = rot(psi, 1, 0), rot(psi, 0, 1)
    out += axis_pair(fr, cg, ex, ey, 2.35, ORANGE, ORANGE, "x", "y")
    bx, by = fr.p(cg[0] - ex[0] * 2.4 - ey[0] * 0.15, cg[1] - ex[1] * 2.4 - ey[1] * 0.15)
    out.append(text(bx, by + 6, "{B} 车体系（钉在质心）", size=13, fill=ORANGE))

    # yaw arc from inertial X-parallel at CG
    arc_r = 1.15
    n = 18
    pts = []
    for k in range(n + 1):
        a = psi * k / n
        pts.append(fr.xy(cg[0] + math.cos(a) * arc_r, cg[1] + math.sin(a) * arc_r))
    out.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="{MUTED}" stroke-width="1.4" marker-end="url(#{CURRENT_MARKER})"/>'
    )
    mid = rot(psi / 2, arc_r * 1.25, 0)
    out.append(text(*fr.p(cg[0] + mid[0], cg[1] + mid[1] + 0.05), "ψ", size=16, fill=MUTED, anchor="middle"))

    # front tire frame at front axle
    fax, fay = rot(psi, 1.2, 0)
    tw = (cg[0] + fax, cg[1] + fay)
    tex, tey = rot(psi + delta, 1, 0), rot(psi + delta, 0, 1)
    out += axis_pair(fr, tw, tex, tey, 1.55, GREEN, GREEN, "x_w", "y_w", size=12)
    out.append(text(fr.p(tw[0] + 0.2, tw[1] + 1.85)[0], fr.p(tw[0] + 0.2, tw[1] + 1.85)[1], "{W} 前轮坐标系", size=13, fill=GREEN))
    # small wheel rectangle
    wl, ww = 0.55, 0.18
    wpts = []
    for x, y in [(wl, ww), (wl, -ww), (-wl, -ww), (-wl, ww)]:
        rx, ry = rot(psi + delta, x, y)
        wpts.append(fr.p(tw[0] + rx, tw[1] + ry))
    out.append(poly(wpts, "#dcfce7", GREEN, 1.4))

    # lf / lr
    fpt = (cg[0] + fax, cg[1] + fay)
    rax, ray = rot(psi, -1.6, 0)
    rpt = (cg[0] + rax, cg[1] + ray)
    out.append(line(*fr.p(*cg), *fr.p(*fpt), MUTED, 1.1, marker=False))
    out.append(line(*fr.p(*cg), *fr.p(*rpt), MUTED, 1.1, marker=False))
    mid_f = fr.p((cg[0] + fpt[0]) / 2 + 0.25, (cg[1] + fpt[1]) / 2 - 0.28)
    mid_r = fr.p((cg[0] + rpt[0]) / 2 - 0.15, (cg[1] + rpt[1]) / 2 - 0.32)
    out.append(text(mid_f[0], mid_f[1], "l_f", size=12, fill=MUTED, anchor="middle"))
    out.append(text(mid_r[0], mid_r[1], "l_r", size=12, fill=MUTED, anchor="middle"))

    # legend
    out.append(text(70, 518, "约定：x 向前、y 向左、z 向上。定位给 (X,Y,ψ)；动力学写在 {B}；轮胎力写在 {W}。", size=13, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig02_rotation() -> str:
    w, h = 860, 500
    out = header(w, h, "arr-fig02")
    out += caption_bar(w, 0, "图 1-2　二维旋转：同一点 P，先在 {B} 里写 (x,y)，再乘 R(ψ) 变到地面")
    fr = Frame(90, 430, 70)
    psi = math.radians(40)
    cg = (4.6, 2.4)
    # inertial axes
    out += axis_pair(fr, (0, 0), (1, 0), (0, 1), 1.9, BLUE, BLUE, "X", "Y")
    out.append(text(*fr.p(0.15, -0.38), "{I}", size=13, fill=BLUE))

    out += draw_car(fr, cg, psi, "#f3f4f6")
    ex, ey = rot(psi, 1, 0), rot(psi, 0, 1)
    out += axis_pair(fr, cg, ex, ey, 1.9, ORANGE, ORANGE, "x", "y")

    # point P: front-left corner in body
    pb = (2.25, 0.9)
    px, py = rot(psi, *pb)
    P = (cg[0] + px, cg[1] + py)
    # dashed body components
    along_x = (cg[0] + rot(psi, pb[0], 0)[0], cg[1] + rot(psi, pb[0], 0)[1])
    out.append(line(*fr.p(*cg), *fr.p(*along_x), ORANGE, 1.3, "4 3", marker=False))
    out.append(line(*fr.p(*along_x), *fr.p(*P), ORANGE, 1.3, "4 3", marker=False))
    out.append(circle(*fr.p(*P), 5.5, RED, INK, 1.1))
    out.append(text(fr.p(*P)[0] + 10, fr.p(*P)[1] - 8, "P", size=16, fill=RED, weight="700"))

    # inertial components dashed
    out.append(line(*fr.p(P[0], 0), *fr.p(*P), BLUE, 1.1, "3 3", marker=False))
    out.append(line(*fr.p(0, P[1]), *fr.p(*P), BLUE, 1.1, "3 3", marker=False))
    out.append(text(fr.p(P[0], -0.28)[0], fr.p(P[0], -0.28)[1], "X_P", size=13, fill=BLUE, anchor="middle"))
    out.append(text(fr.p(-0.45, P[1])[0], fr.p(-0.45, P[1])[1], "Y_P", size=13, fill=BLUE, anchor="end"))

    # labels x,y on dashed
    mx = fr.p((cg[0] + along_x[0]) / 2 + 0.12, (cg[1] + along_x[1]) / 2 - 0.22)
    my = fr.p((along_x[0] + P[0]) / 2 + 0.22, (along_x[1] + P[1]) / 2)
    out.append(text(mx[0], mx[1], "x", size=13, fill=ORANGE))
    out.append(text(my[0], my[1], "y", size=13, fill=ORANGE))

    # formula panel
    out.append(f'<rect x="560" y="70" width="280" height="360" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(580, 100, "变换公式", size=15, fill=INK, weight="700"))
    lines = [
        ("p_I = origin + R(ψ) p_B", INK),
        ("R 的第 1 列 = 车体 x 轴", ORANGE),
        ("R 的第 2 列 = 车体 y 轴", ORANGE),
        ("R⁻¹ = Rᵀ  （正交矩阵）", MUTED),
    ]
    y = 132
    for s, c in lines:
        out.append(text(580, y, s, size=13, fill=c))
        y += 28
    out.append(text(580, 250, "R(ψ) =", size=14, fill=INK))
    out.append(text(580, 286, "[  cosψ    −sinψ ]", size=15, fill=BLUE, weight="600"))
    out.append(text(580, 312, "[  sinψ     cosψ ]", size=15, fill=BLUE, weight="600"))
    out.append(text(580, 350, "本课程坑：不要写成", size=13, fill=RED))
    out.append(text(580, 374, "[ cos  sin ; −sin  cos ]", size=13, fill=RED))
    out.append(text(580, 398, "那是顺时针为正或 y 向右。", size=12, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig03_velocity() -> str:
    w, h = 860, 540
    out = header(w, h, "arr-fig03")
    out += caption_bar(w, 0, "图 1-3　同一根速度矢量，在 {B} 里是 (v_x, v_y)，在地面是 (Ẋ, Ẏ)")
    # left panel general, right panel vy=0
    for i, (ox, title, vy_on) in enumerate([(0, "一般情况：有侧偏 v_y ≠ 0", True), (430, "运动学常用：v_y = 0", False)]):
        out.append(f'<rect x="{ox + 16}" y="48" width="414" height="450" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
        out.append(text(ox + 32, 74, title, size=14, fill=INK, weight="700"))
        note = "第 05 章动力学保留 v_y" if vy_on else "第 02 章自行车模型从这里开始"
        out.append(text(ox + 32, 96, note, size=12, fill=MUTED))
        fr = Frame(ox + 78, 390, 46)
        psi = math.radians(38)
        cg = (3.15, 2.45)
        out += axis_pair(fr, (0, 0), (1, 0), (0, 1), 1.55, BLUE, BLUE, "X", "Y", size=12)
        out += draw_car(fr, cg, psi)
        ex, ey = rot(psi, 1, 0), rot(psi, 0, 1)
        out += axis_pair(fr, cg, ex, ey, 1.45, ORANGE, ORANGE, "x", "y", size=12)

        vx, vy = 2.15, (0.95 if vy_on else 0.0)
        # body components
        tip_x = (cg[0] + ex[0] * vx, cg[1] + ex[1] * vx)
        tip = (cg[0] + ex[0] * vx + ey[0] * vy, cg[1] + ex[1] * vx + ey[1] * vy)
        out.append(line(*fr.p(*cg), *fr.p(*tip_x), ORANGE, 1.6, marker=False))
        if vy_on:
            out.append(line(*fr.p(*tip_x), *fr.p(*tip), ORANGE, 1.6, marker=False))
            out.append(text(fr.p(*tip_x)[0] + 6, fr.p(*tip_x)[1] + 16, "v_x", size=13, fill=ORANGE))
            mid_vy = fr.p((tip_x[0] + tip[0]) / 2, (tip_x[1] + tip[1]) / 2)
            out.append(text(mid_vy[0] - 18, mid_vy[1] - 8, "v_y", size=13, fill=ORANGE))
        else:
            out.append(text(fr.p(*tip_x)[0] + 8, fr.p(*tip_x)[1] + 4, "v_x = v", size=13, fill=ORANGE))
        out.append(line(*fr.p(*cg), *fr.p(*tip), RED, 2.4))
        out.append(text(fr.p(*tip)[0] + 8, fr.p(*tip)[1] - 6, "v", size=15, fill=RED, weight="700"))

        # inertial components of the same v
        out.append(line(*fr.p(*cg), *fr.p(cg[0] + (tip[0] - cg[0]), cg[1]), BLUE, 1.3, "4 3", marker=False))
        out.append(line(*fr.p(cg[0] + (tip[0] - cg[0]), cg[1]), *fr.p(*tip), BLUE, 1.3, "4 3", marker=False))
        out.append(text(fr.p(cg[0] + (tip[0] - cg[0]) / 2, cg[1] - 0.28)[0],
                        fr.p(cg[0] + (tip[0] - cg[0]) / 2, cg[1] - 0.28)[1],
                        "Ẋ", size=14, fill=BLUE, anchor="middle"))
        if abs(tip[1] - cg[1]) > 0.05:
            out.append(text(fr.p(tip[0] + 0.22, (cg[1] + tip[1]) / 2)[0],
                            fr.p(tip[0] + 0.22, (cg[1] + tip[1]) / 2)[1],
                            "Ẏ", size=14, fill=BLUE))

        formula = "Ẋ = v_x cosψ − v_y sinψ" if vy_on else "Ẋ = v cosψ"
        formula2 = "Ẏ = v_x sinψ + v_y cosψ" if vy_on else "Ẏ = v sinψ"
        out.append(text(ox + 32, 430, formula, size=13, fill=INK))
        out.append(text(ox + 32, 454, formula2, size=13, fill=INK))
        out.append(text(ox + 32, 474, "同一根红箭头，只是换了一组基。", size=12, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig04_dof() -> str:
    w, h = 860, 480
    out = header(w, h, "arr-fig04")
    out += caption_bar(w, 0, "图 1-4　刚体自由度：路面先压掉 3 个，轮胎再限制速度（不直接减少位形维数）")

    # column 1: 6 DOF
    out.append(f'<rect x="20" y="52" width="260" height="400" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(150, 80, "三维刚体 6 自由度", size=14, fill=INK, weight="700", anchor="middle"))
    # isometric box
    def iso(x, y, z):
        # simple cabinet: X right, Y up-left, Z up
        sx = 150 + 38 * x - 22 * y
        sy = 250 - 18 * y - 32 * z
        return sx, sy
    faces = [(0, 0, 0), (1.6, 0, 0), (1.6, 0.9, 0), (0, 0.9, 0)]
    top = [(0, 0, 0.7), (1.6, 0, 0.7), (1.6, 0.9, 0.7), (0, 0.9, 0.7)]
    out.append(poly([iso(*p) for p in faces], "#d1d5db", STROKE, 1.4))
    out.append(poly([iso(*p) for p in top], "#e5e7eb", STROKE, 1.4))
    out.append(poly([iso(1.6, 0, 0), iso(1.6, 0.9, 0), iso(1.6, 0.9, 0.7), iso(1.6, 0, 0.7)], "#c4c9d1", STROKE, 1.4))
    o = iso(0.3, 0.2, 0.15)
    out.append(line(*o, o[0] + 50, o[1], BLUE, 2))
    out.append(line(*o, o[0] - 28, o[1] - 18, MUTED, 1.6))
    out.append(line(*o, o[0], o[1] - 48, MUTED, 1.6, dash="4 3"))
    out.append(text(o[0] + 54, o[1] + 4, "X", size=12, fill=BLUE))
    out.append(text(o[0] - 48, o[1] - 18, "Y", size=12, fill=MUTED))
    out.append(text(o[0] + 6, o[1] - 52, "Z 被路面约束", size=12, fill=MUTED))
    out.append(text(150, 340, "平移 X Y Z", size=13, fill=INK, anchor="middle"))
    out.append(text(150, 364, "转动 φ θ ψ", size=13, fill=INK, anchor="middle"))
    out.append(text(150, 396, "侧倾 φ、俯仰 θ、高度 Z", size=12, fill=MUTED, anchor="middle"))
    out.append(text(150, 418, "水平路上看成被约束住", size=12, fill=MUTED, anchor="middle"))

    # column 2: planar 3
    out.append(f'<rect x="300" y="52" width="260" height="400" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(430, 80, "平面课剩下 3 个", size=14, fill=INK, weight="700", anchor="middle"))
    fr = Frame(330, 300, 36)
    psi = math.radians(28)
    cg = (3.0, 2.0)
    out += draw_car(fr, cg, psi)
    out += axis_pair(fr, (0.2, 0.2), (1, 0), (0, 1), 1.4, BLUE, BLUE, "X", "Y", size=12)
    ex, ey = rot(psi, 1, 0), rot(psi, 0, 1)
    out += axis_pair(fr, cg, ex, ey, 1.3, ORANGE, ORANGE, "x", "y", size=12)
    out.append(text(430, 360, "位形：(X, Y, ψ)", size=14, fill=BLUE, anchor="middle", weight="600"))
    out.append(text(430, 390, "纸板在桌上：两移 + 一转", size=13, fill=MUTED, anchor="middle"))
    out.append(text(430, 416, "这就是平面刚体的全部", size=13, fill=MUTED, anchor="middle"))

    # column 3: nonholonomic
    out.append(f'<rect x="580" y="52" width="260" height="400" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(710, 80, "轮胎：非完整约束", size=14, fill=INK, weight="700", anchor="middle"))
    fr2 = Frame(620, 270, 32)
    psi2 = math.radians(18)
    cg2 = (2.15, 1.85)
    out += draw_car(fr2, cg2, psi2)
    ex2 = rot(psi2, 1, 0)
    ey2 = rot(psi2, 0, 1)
    # allowed vx
    tip_ok = (cg2[0] + ex2[0] * 1.7, cg2[1] + ex2[1] * 1.7)
    out.append(line(*fr2.p(*cg2), *fr2.p(*tip_ok), GREEN, 2.4))
    out.append(text(fr2.p(*tip_ok)[0] + 6, fr2.p(*tip_ok)[1] + 4, "可滚", size=12, fill=GREEN))
    # forbidden vy
    tip_no = (cg2[0] + ey2[0] * 1.5, cg2[1] + ey2[1] * 1.5)
    out.append(line(*fr2.p(*cg2), *fr2.p(*tip_no), RED, 2.2))
    pno = fr2.p(*tip_no)
    out.append(line(pno[0] - 8, pno[1] - 8, pno[0] + 8, pno[1] + 8, RED, 2.4, marker=False))
    out.append(line(pno[0] - 8, pno[1] + 8, pno[0] + 8, pno[1] - 8, RED, 2.4, marker=False))
    out.append(text(pno[0] + 12, pno[1] - 6, "不能侧滑", size=12, fill=RED))
    out.append(text(710, 330, "限制的是速度，不是位形", size=13, fill=INK, anchor="middle"))
    out.append(text(710, 356, "所以不能横着滑进车位", size=13, fill=MUTED, anchor="middle"))
    out.append(text(710, 380, "但沿可行轨迹仍能到达", size=13, fill=MUTED, anchor="middle"))
    out.append(text(710, 404, "大多数 (X,Y,ψ)（平行泊车）", size=13, fill=MUTED, anchor="middle"))
    out.append("</svg>")
    return "\n".join(out)


def fig05_actuators() -> str:
    w, h = 860, 460
    out = header(w, h, "arr-fig05")
    out += caption_bar(w, 0, "图 1-5　硬件在控制模型里被压成两个符号：δ 与 F_x")

    def box(x, y, ww, hh, label, color):
        r = [
            f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="7" fill="{WHITE}" stroke="{color}" stroke-width="1.8"/>',
            text(x + ww / 2, y + hh / 2 + 5, label, size=13, fill=color, anchor="middle", weight="600"),
        ]
        return r

    # steering row
    out.append(text(30, 78, "转向", size=14, fill=ORANGE, weight="700"))
    items = [(30, "方向盘"), (175, "管柱 / 齿条"), (340, "左右横拉杆"), (505, "δ_L , δ_R")]
    for i, (x, lab) in enumerate(items):
        out += box(x, 96, 130, 48, lab, ORANGE)
        if i < len(items) - 1:
            out.append(line(x + 130, 120, items[i + 1][0], 120, MUTED, 1.5))
    out += box(660, 88, 170, 64, "自行车模型：一个 δ", GREEN)
    out.append(line(635, 120, 660, 120, MUTED, 1.5))
    out.append(text(30, 168, "Ackermann：内侧轮转角更大，轴线交于后轴延长线。车道保持转角很小，左右合并即可。", size=12, fill=MUTED))

    # drive row
    out.append(text(30, 210, "驱动 / 制动", size=14, fill=BLUE, weight="700"))
    items2 = [(30, "油门 / 电机"), (175, "变速 / 减速"), (340, "差速器 / 半轴"), (505, "车轮纵向力")]
    for i, (x, lab) in enumerate(items2):
        out += box(x, 228, 130, 48, lab, BLUE)
        if i < len(items2) - 1:
            out.append(line(x + 130, 252, items2[i + 1][0], 252, MUTED, 1.5))
    out += box(660, 220, 170, 64, "模型里：一个 F_x", GREEN)
    out.append(line(635, 252, 660, 252, MUTED, 1.5))
    out.append(text(30, 300, "刹车是负的 F_x（带饱和）。更粗的模型甚至直接命令加速度 a_x。ABS / 侧倾入门时先忽略。", size=12, fill=MUTED))

    # mapping table visual
    out.append(f'<rect x="30" y="324" width="800" height="112" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(50, 356, "你在车上做的事", size=13, fill=MUTED, weight="600"))
    out.append(text(330, 356, "模型输入", size=13, fill=MUTED, weight="600"))
    out.append(text(560, 356, "后面哪一章用", size=13, fill=MUTED, weight="600"))
    out.append(text(50, 386, "拧方向盘", size=15, fill=INK))
    out.append(text(330, 386, "前轮转角 δ", size=15, fill=ORANGE, weight="700"))
    out.append(text(560, 386, "第 02、08、10 章", size=14, fill=MUTED))
    out.append(text(50, 416, "踩电门 / 刹车", size=15, fill=INK))
    out.append(text(330, 416, "纵向力 F_x（或 a_x）", size=15, fill=BLUE, weight="700"))
    out.append(text(560, 416, "第 04、07 章", size=14, fill=MUTED))
    out.append("</svg>")
    return "\n".join(out)


def fig06_bicycle() -> str:
    w, h = 860, 430
    out = header(w, h, "arr-fig06")
    out += caption_bar(w, 0, "图 1-6　四轮 → 自行车模型：左右收到中轴，只用一个 δ")
    # left 4 wheels
    out.append(f'<rect x="20" y="52" width="400" height="350" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(220, 80, "四轮 + Ackermann 几何", size=14, fill=INK, weight="700", anchor="middle"))
    fr = Frame(70, 360, 48)
    psi = 0.0
    cg = (3.4, 2.55)
    out += draw_car(fr, cg, psi, "#f9fafb")
    # four wheels
    lf, lr, tf = 1.2, 1.6, 0.75
    delta_in, delta_out = math.radians(28), math.radians(20)
    wheels = [
        ((lf, tf), delta_in, True),
        ((lf, -tf), delta_out, True),
        ((-lr, tf), 0.0, False),
        ((-lr, -tf), 0.0, False),
    ]
    for (bx, by), d, _ in wheels:
        wx, wy = cg[0] + bx, cg[1] + by
        wl, ww = 0.42, 0.16
        pts = []
        for x, y in [(wl, ww), (wl, -ww), (-wl, -ww), (-wl, ww)]:
            rx, ry = rot(d, x, y)
            pts.append(fr.p(wx + rx, wy + ry))
        out.append(poly(pts, "#bbf7d0", GREEN, 1.3))
    # ICR to the left (positive y)
    icr = (cg[0] - lr, cg[1] + 4.2)
    # rear axle line toward ICR
    icr_draw = (cg[0] - lr, min(icr[1], 5.05))
    out.append(line(*fr.p(cg[0] - lr, cg[1] + tf), *fr.p(*icr_draw), MUTED, 1.2, "4 3", marker=False))
    out.append(circle(*fr.p(*icr_draw), 4.5, WHITE, RED, 1.4))
    out.append(text(fr.p(icr_draw[0] - 0.2, icr_draw[1] + 0.35)[0], fr.p(icr_draw[0] - 0.2, icr_draw[1] + 0.35)[1], "ICR", size=12, fill=RED, anchor="end", weight="700"))
    out.append(text(220, 380, "内侧 δ 更大，轴线交于一点才纯滚动", size=12, fill=MUTED, anchor="middle"))

    # right bicycle
    out.append(f'<rect x="440" y="52" width="400" height="350" rx="8" fill="{PANEL}" stroke="#e5e7eb"/>')
    out.append(text(640, 80, "自行车模型（中轴两轮）", size=14, fill=INK, weight="700", anchor="middle"))
    fr2 = Frame(500, 360, 48)
    cg2 = (3.2, 2.55)
    out += draw_car(fr2, cg2, 0.0, "#f9fafb")
    dlt = math.radians(24)
    for (bx, by), d in [((1.2, 0.0), dlt), ((-1.6, 0.0), 0.0)]:
        wx, wy = cg2[0] + bx, cg2[1] + by
        pts = []
        for x, y in [(0.5, 0.18), (0.5, -0.18), (-0.5, -0.18), (-0.5, 0.18)]:
            rx, ry = rot(d, x, y)
            pts.append(fr2.p(wx + rx, wy + ry))
        out.append(poly(pts, "#bbf7d0", GREEN, 1.5))
    # single delta
    f = (cg2[0] + 1.2, cg2[1])
    out += axis_pair(fr2, f, rot(dlt, 1, 0), rot(dlt, 0, 1), 1.35, GREEN, GREEN, "前轮 x", "", size=12)
    out.append(text(fr2.p(f[0] + 0.9, f[1] + 1.35)[0], fr2.p(f[0] + 0.9, f[1] + 1.35)[1], "δ", size=16, fill=GREEN, weight="700"))
    # yaw arc at front
    out.append(text(640, 360, "对车道保持（小转角）足够", size=13, fill=INK, anchor="middle"))
    out.append(text(640, 384, "第 02 章会画出瞬时转动中心", size=12, fill=MUTED, anchor="middle"))
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    figs = {
        "fig01-three-frames.svg": fig01_three_frames(),
        "fig02-rotation.svg": fig02_rotation(),
        "fig03-velocity.svg": fig03_velocity(),
        "fig04-dof.svg": fig04_dof(),
        "fig05-actuators.svg": fig05_actuators(),
        "fig06-bicycle.svg": fig06_bicycle(),
    }
    for name, svg in figs.items():
        path = OUT / name
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
