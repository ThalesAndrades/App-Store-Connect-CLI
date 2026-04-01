#!/usr/bin/env python3
"""
Klabin SM - App Store Screenshots Generator
iPhone 6.7" format: 1290x2796 (APP_IPHONE_67)
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT_DIR = "/tmp/klabin_screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1290, 2796

# Brand colors
GREEN_DARK  = (27,  77,  46)
GREEN_MID   = (45, 122,  79)
GREEN_LIGHT = (76, 175,  80)
GREEN_PALE  = (165,214,167)
WHITE       = (255,255,255)
GRAY_LIGHT  = (245,245,245)
GRAY        = (158,158,158)
DARK        = ( 26, 26, 26)
TEAL        = (  0,137,123)
RED         = (229, 57, 53)
CARD_SHADOW = (200,200,200)

def font(size, bold=False):
    """Load a system font, fall back gracefully."""
    paths_bold = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    ]
    paths_reg = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ]
    for p in (paths_bold if bold else paths_reg):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient_bg(colors, size=(W,H)):
    """Vertical gradient between multiple colors."""
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    n = len(colors) - 1
    seg_h = size[1] // n
    for i in range(n):
        c1, c2 = colors[i], colors[i+1]
        for y in range(seg_h):
            t = y / seg_h
            r = int(c1[0]+(c2[0]-c1[0])*t)
            g = int(c1[1]+(c2[1]-c1[1])*t)
            b = int(c1[2]+(c2[2]-c1[2])*t)
            ys = i*seg_h + y
            draw.line([(0,ys),(size[0],ys)], fill=(r,g,b))
    return img, draw

def rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    x0,y0,x1,y1 = xy
    draw.rounded_rectangle([x0,y0,x1,y1], radius=radius, fill=fill, outline=outline, width=width)

def centered_text(draw, text, y, fnt, color):
    bb = draw.textbbox((0,0), text, font=fnt)
    tw = bb[2]-bb[0]
    draw.text(((W-tw)//2, y), text, font=fnt, fill=color)

def status_bar(draw):
    draw.text((80, 55), "9:41", font=font(42, bold=True), fill=WHITE)
    # Battery
    bx, by = 1150, 55
    draw.rounded_rectangle([bx,by,bx+80,by+36], radius=6, outline=WHITE, width=3)
    draw.rounded_rectangle([bx+4,by+4,bx+60,by+32], radius=4, fill=WHITE)
    draw.rounded_rectangle([bx+82,by+10,bx+90,by+26], radius=3, fill=WHITE)

# ─────────────────────────────────────────────
# SCREEN 1 — Login
# ─────────────────────────────────────────────
def screen_login():
    img, draw = gradient_bg([GREEN_DARK, GREEN_MID, (30,90,55)])
    status_bar(draw)

    # Logo circle
    cx, cy, r = W//2, 560, 130
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=GREEN_LIGHT)
    draw.ellipse([cx-r+12, cy-r+12, cx+r-12, cy+r-12], fill=GREEN_DARK)
    centered_text(draw, "KSM", cy-42, font(80, bold=True), WHITE)

    centered_text(draw, "Klabin SM", 740, font(90, bold=True), WHITE)
    centered_text(draw, "Saúde Mental para Motoristas", 860, font(46), GREEN_PALE)

    # Input CPF
    rounded_rect(draw, [120, 1020, W-120, 1170], 28, WHITE)
    draw.text((170, 1060), "CPF", font=font(38), fill=GRAY)
    draw.line([(170, 1135), (W-170, 1135)], fill=(220,220,220), width=2)

    # Input data
    rounded_rect(draw, [120, 1210, W-120, 1360], 28, WHITE)
    draw.text((170, 1250), "Data de Nascimento", font=font(38), fill=GRAY)
    draw.line([(170, 1325), (W-170, 1325)], fill=(220,220,220), width=2)

    # Button
    rounded_rect(draw, [120, 1430, W-120, 1600], 36, GREEN_LIGHT)
    centered_text(draw, "ENTRAR", 1482, font(60, bold=True), WHITE)

    # Demo mode
    centered_text(draw, "Modo Demonstração", 1670, font(42), GREEN_PALE)
    draw.line([(W//2-200, 1720), (W//2+200, 1720)], fill=GREEN_PALE, width=2)

    centered_text(draw, "© 2026 Klabin S.A.  •  LGPD Compliant", 1780, font(32), (120,180,130))
    img.save(f"{OUT_DIR}/01_login.png")
    print("✓ screen1 login")

# ─────────────────────────────────────────────
# SCREEN 2 — Home
# ─────────────────────────────────────────────
def screen_home():
    img = Image.new("RGB", (W,H), GRAY_LIGHT)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0,0,W,220], fill=GREEN_DARK)
    status_bar(draw)
    draw.text((80, 115), "Olá, João!", font=font(62, bold=True), fill=WHITE)
    draw.text((80, 180), "Seu benefício Klabin está ativo", font=font(38), fill=GREEN_PALE)

    # Next session card
    rounded_rect(draw, [40, 260, W-40, 560], 30, WHITE)
    draw.text((90, 300), "Próxima Sessão", font=font(38), fill=GRAY)
    draw.text((90, 360), "Dr. Carlos Mendes", font=font(56, bold=True), fill=DARK)
    draw.text((90, 440), "📅  Terça, 15 Abr  •  14:00", font=font(42), fill=GREEN_MID)
    rounded_rect(draw, [W-280, 480, W-80, 550], 20, GREEN_LIGHT)
    draw.text((W-260, 492), "Entrar", font=font(40, bold=True), fill=WHITE)

    # Quick action buttons
    rounded_rect(draw, [40, 600, 615, 820], 28, GREEN_MID)
    centered_text(draw, "📅", 620, font(70), WHITE)
    centered_text(draw, "Agendar", 720, font(48, bold=True), WHITE)

    rounded_rect(draw, [675, 600, W-40, 820], 28, TEAL)
    centered_text(draw, "📋", 620, font(70), WHITE)
    centered_text(draw, "Histórico", 720, font(48, bold=True), WHITE)

    # Sessions badge
    rounded_rect(draw, [40, 870, W-40, 1060], 30, GREEN_DARK)
    draw.text((90, 900), "Sessões disponíveis este mês", font=font(42), fill=GREEN_PALE)
    draw.text((90, 965), "2 de 2", font=font(76, bold=True), fill=WHITE)
    # Progress bar
    draw.rounded_rectangle([90, 1045, W-90, 1065], radius=10, fill=(60,120,70))
    draw.rounded_rectangle([90, 1045, W//2+200, 1065], radius=10, fill=GREEN_LIGHT)

    # Recent list
    draw.text((80, 1110), "Últimas Sessões", font=font(52, bold=True), fill=DARK)
    for i, (name, date, state, color) in enumerate([
        ("Dr. Carlos Mendes",  "08 Abr 2026", "Realizada",  GREEN_LIGHT),
        ("Dra. Ana Souza",     "22 Mar 2026", "Realizada",  GREEN_LIGHT),
        ("Dr. Carlos Mendes",  "08 Mar 2026", "Cancelada",  RED),
    ]):
        y0 = 1190 + i*180
        rounded_rect(draw, [40, y0, W-40, y0+160], 24, WHITE)
        draw.text((90, y0+28), name, font=font(46, bold=True), fill=DARK)
        draw.text((90, y0+94), date, font=font(38), fill=GRAY)
        rounded_rect(draw, [W-240, y0+50, W-60, y0+110], 16, color)
        draw.text((W-222, y0+58), state, font=font(32, bold=True), fill=WHITE)

    # Bottom nav
    draw.rectangle([0, H-160, W, H], fill=WHITE)
    draw.line([(0, H-160), (W, H-160)], fill=(220,220,220), width=2)
    for i, (lbl, active) in enumerate([("Início","1"),("Agendar","0"),("Carteirinha","0"),("Perfil","0")]):
        nx = 80 + i*(W-160)//3
        c = GREEN_DARK if active=="1" else GRAY
        draw.text((nx, H-130), lbl, font=font(36, bold=active=="1"), fill=c)

    img.save(f"{OUT_DIR}/02_home.png")
    print("✓ screen2 home")

# ─────────────────────────────────────────────
# SCREEN 3 — Booking
# ─────────────────────────────────────────────
def screen_booking():
    img = Image.new("RGB", (W,H), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0,0,W,200], fill=GREEN_DARK)
    status_bar(draw)
    draw.text((80, 115), "← Agendar Sessão", font=font(56, bold=True), fill=WHITE)

    draw.text((80, 250), "Escolha o Psicólogo", font=font(52, bold=True), fill=DARK)

    for i, (name, crp, avail) in enumerate([
        ("Dr. Carlos Mendes",  "CRP 08/12345", "Disponível hoje"),
        ("Dra. Ana Souza",     "CRP 08/67890", "Disponível amanhã"),
        ("Dr. Pedro Lima",     "CRP 08/11111", "Disponível em 2 dias"),
    ]):
        y0 = 340 + i*220
        selected = i==0
        rounded_rect(draw, [40, y0, W-40, y0+200],
                     28, GREEN_DARK if selected else WHITE,
                     outline=GREEN_MID if selected else (220,220,220), width=2)
        fc = WHITE if selected else DARK
        gc = GREEN_PALE if selected else GREEN_MID
        # avatar circle
        draw.ellipse([70, y0+30, 170, y0+170], fill=GREEN_MID if selected else GRAY_LIGHT)
        draw.text((100, y0+70), name[3], font=font(60, bold=True), fill=WHITE)
        draw.text((200, y0+40), name, font=font(46, bold=True), fill=fc)
        draw.text((200, y0+105), crp, font=font(36), fill=gc)
        draw.text((200, y0+155), avail, font=font(36), fill=gc)

    # Calendar
    draw.text((80, 1030), "Selecione a Data", font=font(52, bold=True), fill=DARK)
    draw.text((80, 1110), "◀  Abril 2026  ▶", font=font(46, bold=True), fill=GREEN_DARK)

    days = ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"]
    for j, d in enumerate(days):
        draw.text((90 + j*170, 1200), d, font=font(34), fill=GRAY)
    for row in range(5):
        for col in range(7):
            day = row*7+col+1
            if 1 <= day <= 30:
                cx = 90 + col*170 + 60
                cy = 1320 + row*140
                if day == 15:
                    draw.ellipse([cx-50,cy-50,cx+50,cy+50], fill=GREEN_DARK)
                    draw.text((cx-22, cy-32), str(day), font=font(46, bold=True), fill=WHITE)
                elif day in [8,22,29]:
                    draw.ellipse([cx-50,cy-50,cx+50,cy+50], fill=GREEN_PALE)
                    draw.text((cx-22, cy-32), str(day), font=font(46), fill=GREEN_DARK)
                else:
                    draw.text((cx-22 if day>9 else cx-14, cy-32), str(day), font=font(46), fill=DARK)

    # Confirm button
    rounded_rect(draw, [80, 2580, W-80, 2740], 40, GREEN_DARK)
    centered_text(draw, "CONFIRMAR AGENDAMENTO", 2630, font(52, bold=True), WHITE)

    img.save(f"{OUT_DIR}/03_booking.png")
    print("✓ screen3 booking")

# ─────────────────────────────────────────────
# SCREEN 4 — Carteirinha
# ─────────────────────────────────────────────
def screen_card():
    img = Image.new("RGB", (W,H), GRAY_LIGHT)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0,0,W,200], fill=GREEN_DARK)
    status_bar(draw)
    draw.text((80, 115), "Carteirinha Digital", font=font(58, bold=True), fill=WHITE)

    # Card
    rounded_rect(draw, [40, 240, W-40, 980], 40, WHITE)
    rounded_rect(draw, [40, 240, W-40, 540], 40, GREEN_DARK)
    draw.rectangle([40, 440, W-40, 540], fill=GREEN_DARK)
    draw.text((110, 280), "KLABIN  SM", font=font(76, bold=True), fill=WHITE)
    draw.text((110, 375), "Benefício Saúde Mental", font=font(42), fill=GREEN_PALE)
    # Watermark circles
    for r2, a in [(220,40),(280,25),(340,15)]:
        draw.ellipse([W-r2-80, 240-r2//2, W-80+r2, 540+r2//2],
                     outline=(255,255,255,a), width=3)

    draw.text((110, 580), "João da Silva", font=font(62, bold=True), fill=DARK)
    draw.text((110, 660), "Motorista Profissional  •  Filial Paraná", font=font(38), fill=GRAY)
    draw.text((110, 740), "CPF: 123.456.789-00", font=font(46), fill=DARK)
    draw.text((110, 810), "Matrícula: KLB-2024-00789", font=font(46), fill=DARK)

    rounded_rect(draw, [110, 880, 370, 960], 18, GREEN_LIGHT)
    draw.text((145, 898), "● ATIVO", font=font(40, bold=True), fill=WHITE)
    draw.text((500, 898), "Válido até: 31/12/2026", font=font(38), fill=GRAY)

    # Sessions info
    draw.text((80, 1030), "Sessões do Mês", font=font(54, bold=True), fill=DARK)

    for i, (n, label, c) in enumerate([(2,"Disponíveis",GREEN_DARK),(2,"Utilizadas",GREEN_MID),(0,"Agendadas",TEAL)]):
        x0 = 40 + i*410
        rounded_rect(draw, [x0, 1110, x0+380, 1340], 24, WHITE)
        centered_text_in = lambda txt, y, f, col: \
            draw.text(((x0+x0+380)//2 - draw.textbbox((0,0),txt,font=f)[2]//2, y), txt, font=f, fill=col)
        draw.text((x0+130, 1140), str(n), font=font(96, bold=True), fill=c)
        draw.text((x0+20, 1265), label, font=font(38), fill=GRAY)

    # QR code placeholder
    rounded_rect(draw, [40, 1390, W-40, 1880], 30, WHITE)
    draw.text((80, 1430), "QR Code de Verificação", font=font(48, bold=True), fill=DARK)
    qx, qy = W//2-200, 1530
    draw.rectangle([qx, qy, qx+400, qy+280], outline=DARK, width=4)
    for step in range(0, 400, 40):
        draw.line([(qx+step, qy), (qx+step, qy+280)], fill=(220,220,220), width=1)
        draw.line([(qx, qy+step*280//400), (qx+400, qy+step*280//400)], fill=(220,220,220), width=1)
    for rx, ry, rs in [(qx+20,qy+20,80),(qx+300,qy+20,80),(qx+20,qy+180,80)]:
        draw.rectangle([rx,ry,rx+rs,ry+rs], outline=DARK, width=6)
        draw.rectangle([rx+14,ry+14,rx+rs-14,ry+rs-14], fill=DARK)
    draw.text((W//2-260, 1830), "Apresente na portaria Klabin", font=font(36), fill=GRAY)

    img.save(f"{OUT_DIR}/04_carteirinha.png")
    print("✓ screen4 carteirinha")

# ─────────────────────────────────────────────
# SCREEN 5 — Histórico
# ─────────────────────────────────────────────
def screen_history():
    img = Image.new("RGB", (W,H), GRAY_LIGHT)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0,0,W,200], fill=GREEN_DARK)
    status_bar(draw)
    draw.text((80, 115), "Histórico de Sessões", font=font(56, bold=True), fill=WHITE)

    # Summary strip
    rounded_rect(draw, [40,230,W-40,420], 28, WHITE)
    draw.text((90, 255), "Total de Sessões", font=font(38), fill=GRAY)
    draw.text((90, 308), "8 sessões realizadas", font=font(56, bold=True), fill=DARK)
    rounded_rect(draw, [W-320, 260, W-60, 395], 18, GREEN_PALE)
    draw.text((W-305, 275), "Bem-estar +", font=font(36, bold=True), fill=GREEN_DARK)
    draw.text((W-305, 328), "  92%", font=font(46, bold=True), fill=GREEN_DARK)

    sessions = [
        ("Dr. Carlos Mendes",  "08 Abr 2026", "14:00 – 15:00", "Realizada",  GREEN_LIGHT, "★★★★★"),
        ("Dra. Ana Souza",     "22 Mar 2026", "10:00 – 11:00", "Realizada",  GREEN_LIGHT, "★★★★☆"),
        ("Dr. Carlos Mendes",  "08 Mar 2026", "14:00 – 15:00", "Cancelada",  RED,         "—"),
        ("Dra. Ana Souza",     "22 Fev 2026", "09:00 – 10:00", "Realizada",  GREEN_LIGHT, "★★★★★"),
        ("Dr. Pedro Lima",     "08 Fev 2026", "15:00 – 16:00", "Realizada",  GREEN_LIGHT, "★★★★☆"),
    ]

    for i, (name, date, time_r, state, sc, stars) in enumerate(sessions):
        y0 = 460 + i*220
        rounded_rect(draw, [40, y0, W-40, y0+200], 28, WHITE)
        draw.ellipse([70, y0+30, 190, y0+170], fill=GREEN_MID if state=="Realizada" else (220,220,220))
        draw.text((108, y0+70), name[3], font=font(68, bold=True), fill=WHITE if state=="Realizada" else GRAY)
        draw.text((220, y0+30), name, font=font(46, bold=True), fill=DARK)
        draw.text((220, y0+92), date + "  •  " + time_r, font=font(36), fill=GRAY)
        draw.text((220, y0+148), stars, font=font(36), fill=(255,180,0) if state=="Realizada" else GRAY)
        rounded_rect(draw, [W-250, y0+65, W-60, y0+130], 16, sc)
        draw.text((W-235, y0+73), state, font=font(32, bold=True), fill=WHITE)

    # Bottom nav
    draw.rectangle([0, H-160, W, H], fill=WHITE)
    draw.line([(0, H-160), (W, H-160)], fill=(220,220,220), width=2)
    for i, (lbl, active) in enumerate([("Início","0"),("Agendar","0"),("Carteirinha","0"),("Perfil","0")]):
        nx = 80 + i*(W-160)//3
        c = GREEN_DARK if active=="1" else GRAY
        draw.text((nx, H-130), lbl, font=font(36, bold=active=="1"), fill=c)

    img.save(f"{OUT_DIR}/05_historico.png")
    print("✓ screen5 historico")

# Run all
screen_login()
screen_home()
screen_booking()
screen_card()
screen_history()

print("\n=== All screenshots generated ===")
import subprocess
result = subprocess.run(["ls","-lh",OUT_DIR], capture_output=True, text=True)
print(result.stdout)
