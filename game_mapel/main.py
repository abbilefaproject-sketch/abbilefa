import pygame
import random
import sys
import math
import asyncio  # Diperlukan untuk Pygbag agar bisa jalan di web

# Inisialisasi Pygame
pygame.init()
pygame.font.init()

# Ukuran Layar Tetap (Sesuai Versi HTML)
W, H = 480, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mapel Dodge — by Abbilefa")
clock = pygame.time.Clock()

# WARNA (HEX konversi ke RGB Tuple)
C = {
    'BG':         (8, 14, 30),
    'BG2':        (12, 22, 50),
    'PANEL':      (15, 28, 65),
    'BORDER':     (30, 80, 180),
    'ACCENT':     (60, 140, 255),
    'ACCENT2':    (100, 200, 255),
    'WHITE':      (220, 235, 255),
    'DIM':        (80, 110, 160),
    'GOOD':       (50, 220, 130),
    'GOOD_DIM':   (20, 80, 50),
    'DANGER':     (255, 70, 80),
    'DANGER_DIM': (80, 16, 25),
    'GOLD':       (255, 200, 50),
    'HEART':      (255, 80, 100),
}

MAPEL_LIST = [
    ["MATEMATIKA",  (60, 130, 255)],
    ["FISIKA",      (100, 180, 255)],
    ["BIOLOGI",     (50, 220, 130)],
    ["KIMIA",       (180, 100, 255)],
    ["GEOGRAFI",    (255, 170, 60)],
    ["SOSIOLOGI",   (255, 220, 60)],
    ["EKONOMI",     (60, 210, 180)],
    ["SEJARAH",     (255, 130, 60)],
    ["PKN",         (255, 80, 100)],
    ["SENI RUPA",   (255, 120, 200)],
    ["PEND. AGAMA", (255, 200, 80)],
    ["INFORMATIKA", (80, 220, 255)],
    ["OLAHRAGA",    (130, 255, 130)],
]

# FONTS
font_sm = pygame.font.SysFont('Consolas', 13, bold=True)
font_md = pygame.font.SysFont('Consolas', 16, bold=True)
font_lg = pygame.font.SysFont('Consolas', 22, bold=True)
font_xl = pygame.font.SysFont('Consolas', 28, bold=True)
font_title = pygame.font.SysFont('Impact', 54)

# STARS MANAGEMENT
stars = [{'x': random.random()*W, 'y': random.random()*H, 'size': 0.3 + random.random()*1.2, 'phase': random.random()*math.pi*2} for _ in range(90)]

# PARTICLES MANAGEMENT
particles = []
def spawn_particles(x, y, color):
    for _ in range(12):
        angle = random.random() * math.pi * 2
        speed = 2 + random.random() * 4
        particles.append({
            'x': x, 'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'life': 1.0, 'color': color,
            'size': 3 + random.random() * 4
        })

# FLOAT TEXTS MANAGEMENT
float_texts = []
def spawn_float_text(x, y, text, color):
    float_texts.append({'x': x, 'y': y, 'text': text, 'color': color, 'life': 1.0, 'vy': -2.5})

# LERP COLOR HELPERS
def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

# DRAW GRID BACKGROUND
def draw_grid():
    for i in range(0, W, 40):
        pygame.draw.line(screen, (12, 20, 48), (i, 0), (i, H))
    for j in range(0, H, 40):
        pygame.draw.line(screen, (12, 20, 48), (0, j), (W, j))

# CLASSES GAME
class Block:
    def __init__(self, speed, is_target, mapel_idx):
        self.w, self.h = 90, 46
        self.x = 20 + random.random() * (W - 40 - self.w)
        self.y = -self.h - random.random() * 80
        self.speed = speed
        self.is_target = is_target
        self.mapel_name = MAPEL_LIST[mapel_idx][0]
        self.base_color = MAPEL_LIST[mapel_idx][1]
        self.alive = True
        self.wobble = random.random() * math.pi * 2

    def update(self):
        self.wobble += 0.05
        self.x += math.sin(self.wobble) * 0.4
        self.y += self.speed
        if self.y > H + self.h:
            self.alive = False

    def draw(self, tick):
        rx, ry = int(self.x), int(self.y)
        rect_obj = pygame.Rect(rx, ry, self.w, self.h)
        
        if self.is_target:
            pulse = 0.5 + 0.5 * math.sin(tick * 0.1)
            glow = lerp_color(C['GOOD_DIM'], C['GOOD'], pulse)
            pygame.draw.rect(screen, glow, (rx-3, ry-3, self.w+6, self.h+6), border_radius=12)
            pygame.draw.rect(screen, (15, 50, 32), rect_obj, border_radius=9)
            pygame.draw.rect(screen, C['GOOD'], rect_obj, width=2, border_radius=9)
        else:
            pygame.draw.rect(screen, (0, 0, 0, 150), (rx+3, ry+4, self.w, self.h), border_radius=9)
            bg = lerp_color(C['PANEL'], self.base_color, 0.18)
            pygame.draw.rect(screen, bg, rect_obj, border_radius=9)
            pygame.draw.rect(screen, self.base_color, rect_obj, width=2, border_radius=9)

        # Draw Text Mapel
        label_color = C['GOOD'] if self.is_target else self.base_color
        lines = self.mapel_name.split(' ')
        if len(lines) == 1:
            txt = font_sm.render(lines[0], True, label_color)
            screen.blit(txt, txt.get_rect(center=(rx + self.w/2, ry + self.h/2)))
        else:
            txt1 = font_sm.render(lines[0], True, label_color)
            txt2 = font_sm.render(lines[1], True, label_color)
            screen.blit(txt1, txt1.get_rect(center=(rx + self.w/2, ry + self.h/2 - 8)))
            screen.blit(txt2, txt2.get_rect(center=(rx + self.w/2, ry + self.h/2 + 8)))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Player:
    def __init__(self):
        self.w, self.h = 52, 52
        self.x = W/2 - self.w/2
        self.y = H - 110
        self.speed = 6
        self.invincible = 0
        self.trail = []

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        
        self.x = max(8, min(W - self.w - 8, self.x))
        if self.invincible > 0:
            self.invincible -= 1
            
        cx, cy = self.x + self.w/2, self.y + self.h/2
        self.trail.append((cx, cy))
        if len(self.trail) > 12:
            self.trail.pop(0)

    def draw(self, tick):
        for i, pos in enumerate(self.trail):
            alpha_ratio = i / len(self.trail)
            sz = max(2, int(8 * alpha_ratio))
            pygame.draw.circle(screen, (24, 60, 120), (int(pos[0]), int(pos[1])), sz)

        if self.invincible > 0 and (self.invincible // 4) % 2 == 0:
            return

        cx, cy = int(self.x + self.w/2), int(self.y + self.h/2)
        rx, ry = int(self.x), int(self.y)

        pulse = 0.4 + 0.3 * math.sin(tick * 0.12)
        glow_r = int(30 + 10 * pulse)
        pygame.draw.circle(screen, (20, 45, 90), (cx, cy), glow_r)

        pygame.draw.rect(screen, C['PANEL'], (rx+8, ry+16, 36, 32), border_radius=7)
        pygame.draw.rect(screen, C['ACCENT'], (rx+8, ry+16, 36, 32), width=2, border_radius=7)
        pygame.draw.circle(screen, C['ACCENT2'], (cx, ry+13), 13)
        pygame.draw.circle(screen, C['BORDER'], (cx, ry+13), 13, width=2)
        
        for ex in [cx-4, cx+4]:
            pygame.draw.circle(screen, C['BG'], (ex, ry+11), 3)
            pygame.draw.circle(screen, C['WHITE'], (ex, ry+11), 1)

        pygame.draw.line(screen, C['ACCENT'], (rx+16, ry+20), (rx+16, ry+44), width=3)
        pygame.draw.line(screen, C['ACCENT'], (rx+36, ry+20), (rx+36, ry+44), width=3)

    def get_rect(self):
        return pygame.Rect(self.x + 10, self.y + 14, 32, 36)

# Inisialisasi awal variabel game global
state = 'title'
score, highscore, lives, level, tick = 0, 0, 3, 1, 0
paused = False
player = Player()
blocks = []
target_idx = random.randint(0, len(MAPEL_LIST)-1)
spawn_timer = 0
BASE_SPEED = 2.8
block_speed = BASE_SPEED
spawn_interval = 90
blocks_per_spawn = 1

def reset_game():
    global score, lives, level, blocks, particles, float_texts, target_idx, block_speed, spawn_interval, blocks_per_spawn, spawn_timer
    score, lives, level = 0, 3, 1
    blocks, particles, float_texts = [], [], []
    target_idx = random.randint(0, len(MAPEL_LIST)-1)
    block_speed = BASE_SPEED
    spawn_interval = 90
    blocks_per_spawn = 1
    spawn_timer = 0
    player.x = W/2 - player.w/2
    player.invincible = 0
    player.trail = []

# GAME LOOP UTAMA (Diubah jadi async agar mendukung Pygbag di web browser)
async def main():
    global state, score, highscore, lives, level, tick, paused, blocks, spawn_timer, block_speed, spawn_interval, blocks_per_spawn, target_idx

    running = True
    while running:
        tick += 1
        screen.fill(C['BG'])
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == 'title' and event.key == pygame.K_RETURN:
                    reset_game()
                    state = 'game'
                elif state == 'game' and event.key == pygame.K_SPACE:
                    paused = not paused
                elif state == 'game' and event.key == pygame.K_RETURN and paused:
                    paused = False
                elif state == 'gameover' and event.key == pygame.K_RETURN:
                    reset_game()
                    state = 'game'

        # SISTEM BINTANG
        for s in stars:
            alpha = 0.5 + 0.5 * math.sin(tick * 0.02 + s['phase'])
            brightness = int(60 + 120 * alpha)
            color = (int(brightness/3), int(brightness/2), brightness)
            pygame.draw.circle(screen, color, (int(s['x']), int(s['y'])), max(1, int(s['size'])))

        draw_grid()

        # MENU UTAMA (TITLE)
        if state == 'title':
            lbl_title1 = font_title.render('MAPEL', True, C['ACCENT2'])
            lbl_title2 = font_title.render('DODGE', True, C['ACCENT'])
            screen.blit(lbl_title1, lbl_title1.get_rect(center=(W/2, 160)))
            screen.blit(lbl_title2, lbl_title2.get_rect(center=(W/2, 220)))

            pygame.draw.line(screen, C['BORDER'], (80, 255), (W-80, 255), width=2)
            
            sub1 = font_md.render('Hindari mapel yang salah!', True, C['DIM'])
            sub2 = font_md.render('Tangkap mapel yang ditunjuk!', True, C['WHITE'])
            screen.blit(sub1, sub1.get_rect(center=(W/2, 275)))
            screen.blit(sub2, sub2.get_rect(center=(W/2, 295)))

            pygame.draw.rect(screen, C['PANEL'], (60, 320, W-120, 168), border_radius=14)
            pygame.draw.rect(screen, C['BORDER'], (60, 320, W-120, 168), width=2, border_radius=14)
            
            lbl_ctrl = font_md.render('KONTROL', True, C['ACCENT'])
            screen.blit(lbl_ctrl, lbl_ctrl.get_rect(center=(W/2, 345)))

            controls_text = [
                ('<- / A', 'Gerak Kiri'),
                ('-> / D', 'Gerak Kanan'),
                ('SPACE', 'Pause / Lanjut'),
                ('ENTER', 'Mulai / Restart')
            ]
            for idx, (btn, act) in enumerate(controls_text):
                y_pos = 370 + idx * 26
                t_btn = font_sm.render(btn, True, C['GOLD'])
                t_sep = font_sm.render('—', True, C['DIM'])
                t_act = font_sm.render(act, True, C['WHITE'])
                screen.blit(t_btn, (84, y_pos))
                screen.blit(t_sep, (178, y_pos))
                screen.blit(t_act, (198, y_pos))

            if (tick // 30) % 2 == 0:
                lbl_start = font_md.render('[ ENTER untuk Mulai ]', True, C['ACCENT'])
                screen.blit(lbl_start, lbl_start.get_rect(center=(W/2, 518)))

            lbl_by = font_sm.render('by Abbilefa', True, C['DIM'])
            screen.blit(lbl_by, lbl_by.get_rect(center=(W/2, 548)))

        # PERMAINAN (GAMEPLAY)
        elif state == 'game':
            if not paused:
                player.update(keys)

                spawn_timer += 1
                if spawn_timer >= spawn_interval:
                    spawn_timer = 0
                    used_x = []
                    for _ in range(blocks_per_spawn):
                        is_target = random.random() < 0.35
                        midx = random.randint(0, len(MAPEL_LIST)-1)
                        if is_target:
                            midx = target_idx
                        else:
                            while midx == target_idx:
                                midx = random.randint(0, len(MAPEL_LIST)-1)
                        
                        b = Block(block_speed, is_target, midx)
                        attempts = 0
                        while any(abs(b.x - ux) < b.w + 10 for ux in used_x) and attempts < 10:
                            b.x = 20 + random.random() * (W - 40 - b.w)
                            attempts += 1
                        
                        used_x.append(b.x)
                        blocks.append(b)

                p_rect = player.get_rect()
                for b in blocks[:]:
                    b.update()
                    if not b.alive:
                        blocks.remove(b)
                        continue
                    
                    if b.get_rect().colliderect(p_rect):
                        cx, cy = b.x + b.w/2, b.y + b.h/2
                        if b.is_target:
                            score += 10
                            spawn_particles(cx, cy, C['GOOD'])
                            spawn_float_text(cx, cy-20, '+10', C['GOOD'])
                            old_t = target_idx
                            while target_idx == old_t:
                                target_idx = random.randint(0, len(MAPEL_LIST)-1)
                            blocks.remove(b)
                        elif player.invincible == 0:
                            lives -= 1
                            player.invincible = 90
                            spawn_particles(cx, cy, C['DANGER'])
                            spawn_float_text(cx, cy-20, '-NYAWA', C['DANGER'])
                            blocks.remove(b)
                            if lives <= 0:
                                highscore = max(highscore, score)
                                state = 'gameover'

                new_level = 1 + score // 50
                if new_level != level:
                    level = new_level
                    block_speed = BASE_SPEED + (level - 1) * 0.4
                    spawn_interval = max(35, 90 - (level - 1) * 8)
                    blocks_per_spawn = min(4, 1 + (level - 1) // 2)

            for b in blocks:
                b.draw(tick)
                
            player.draw(tick)

            for p in particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.15
                p['life'] -= 0.04
                if p['life'] <= 0:
                    particles.remove(p)
                else:
                    pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), max(1, int(p['size'] * p['life'])))

            for ft in float_texts[:]:
                ft['y'] += ft['vy']
                ft['life'] -= 0.025
                if ft['life'] <= 0:
                    float_texts.remove(ft)
                else:
                    txt_img = font_lg.render(ft['text'], True, ft['color'])
                    screen.blit(txt_img, txt_img.get_rect(center=(ft['x'], ft['y'])))

            # DRAW HUD
            pygame.draw.rect(screen, C['PANEL'], (0, 0, W, 58))
            pygame.draw.line(screen, C['BORDER'], (0, 58), (W, 58), width=2)
            
            screen.blit(font_sm.render('SKOR', True, C['DIM']), (14, 8))
            screen.blit(font_xl.render(str(score), True, C['GOLD']), (14, 22))
            screen.blit(font_sm.render('LV', True, C['DIM']), (200, 8))
            screen.blit(font_xl.render(str(level), True, C['ACCENT2']), (200, 22))

            for i in range(3):
                hx = W - 30 - i * 36
                h_color = C['HEART'] if i < lives else C['DIM']
                screen.blit(font_lg.render('♥', True, h_color), (hx-10, 20))

            t_name, t_color = MAPEL_LIST[target_idx]
            bx, by = W/2 - 130, H - 74
            pulse = 0.6 + 0.4 * math.sin(tick * 0.08)
            bg_banner = lerp_color(C['GOOD_DIM'], (20, 70, 40), pulse)
            pygame.draw.rect(screen, bg_banner, (bx, by, 260, 42), border_radius=10)
            pygame.draw.rect(screen, C['GOOD'], (bx, by, 260, 42), width=2, border_radius=10)
            
            lbl_tg = font_sm.render('▶ TANGKAP ◀', True, C['DIM'])
            screen.blit(lbl_tg, lbl_tg.get_rect(center=(W/2, by + 12)))
            lbl_name = font_md.render(t_name, True, C['GOOD'])
            screen.blit(lbl_name, lbl_name.get_rect(center=(W/2, by + 28)))

            pygame.draw.line(screen, C['BORDER'], (0, H-80), (W, H-80), width=1)
            screen.blit(font_sm.render('by Abbilefa', True, C['DIM']), (W - 100, H - 24))

            if paused:
                pygame.draw.rect(screen, C['PANEL'], (100, 240, W-200, 180), border_radius=14)
                pygame.draw.rect(screen, C['ACCENT'], (100, 240, W-200, 180), width=2, border_radius=14)
                p_head = font_xl.render('|| PAUSE', True, C['ACCENT2'])
                p_sub = font_sm.render('Tekan SPACE untuk Lanjut', True, C['DIM'])
                screen.blit(p_head, p_head.get_rect(center=(W/2, 300)))
                screen.blit(p_sub, p_sub.get_rect(center=(W/2, 360)))

        # KALAH (GAME OVER)
        elif state == 'gameover':
            pygame.draw.rect(screen, C['PANEL'], (60, 160, W-120, 340), border_radius=18)
            pygame.draw.rect(screen, C['DANGER'], (60, 160, W-120, 340), width=3, border_radius=18)
            
            go_lbl = font_title.render('GAME OVER', True, C['DANGER'])
            screen.blit(go_lbl, go_lbl.get_rect(center=(W/2, 220)))
            pygame.draw.line(screen, C['DANGER'], (100, 260), (W-100, 260), width=2)

            sc_lbl1 = font_sm.render('SKOR KAMU', True, C['DIM'])
            sc_lbl2 = font_title.render(str(score), True, C['GOLD'])
            screen.blit(sc_lbl1, sc_lbl1.get_rect(center=(W/2, 285)))
            screen.blit(sc_lbl2, sc_lbl2.get_rect(center=(W/2, 335)))

            hs_lbl = font_md.render(f'REKOR TERTINGGI : {highscore}', True, C['ACCENT'])
            screen.blit(hs_lbl, hs_lbl.get_rect(center=(W/2, 385)))

            if score >= highscore and score > 0:
                pulse = 0.5 + 0.5 * math.sin(tick * 0.15)
                flash_c = lerp_color(C['GOLD'], C['WHITE'], pulse)
                nb_lbl = font_md.render('★ REKOR BARU! ★', True, flash_c)
                screen.blit(nb_lbl, nb_lbl.get_rect(center=(W/2, 415)))

            if (tick // 30) % 2 == 0:
                ag_lbl = font_sm.render('[ ENTER untuk Main Lagi ]', True, C['ACCENT'])
                screen.blit(ag_lbl, ag_lbl.get_rect(center=(W/2, 455)))

        pygame.display.flip()
        clock.tick(60)
        
        # BARIS WAJIB PYGBAG: Biar web browser tidak hang/membeku
        await asyncio.sleep(0)

# Menjalankan fungsi utama menggunakan loop asyncio
asyncio.run(main())