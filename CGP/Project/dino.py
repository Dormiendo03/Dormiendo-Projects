# ═══════════════════════════════════════════════════════════════════════════
#  DINO MARIO RUNNER
#  A Chrome Dinosaur Game with Super Mushroom Powerup
#
#  Final Project · Computer Graphics Programming · Option 2: Dinosaur Jump
#  Developer  : [Your Name Here]
#  Platform   : Python 3 + Pygame
#
#  HOW TO RUN:
#    pip install pygame
#    python dino_mario_runner.py
# ═══════════════════════════════════════════════════════════════════════════

import pygame
import random
import sys
import math

# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 1  —  INITIALISATION
# ═══════════════════════════════════════════════════════════════════════════
pygame.init()

SCREEN_W, SCREEN_H = 900, 450
FPS      = 60
GROUND_Y = 360          # y-coordinate of the ground surface

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Dino Mario Runner")
clock  = pygame.time.Clock()

# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 2  —  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════
GRAVITY           = 0.85
JUMP_VELOCITY     = -17.0
SPEED_INITIAL     = 7.0
SPEED_MAX         = 16.0
SPEED_INTERVAL    = 300      # score points between speed increases
POWERUP_DURATION  = 6000     # milliseconds the Super Mushroom lasts
SCORE_PER_FRAME   = 0.12     # score added every frame

# ── Colour Palette ──────────────────────────────────────────────────────────
P = {
    "sky_day"   : (247, 247, 247),
    "sky_night" : ( 12,  14,  40),
    "ground"    : ( 83,  83,  83),
    "dino"      : ( 83,  83,  83),
    "dino_eye_w": (255, 255, 255),
    "dino_eye_b": ( 15,  15,  15),
    "cactus"    : ( 35, 120,  35),
    "bird"      : (100, 100, 100),
    "bird_wing" : ( 55,  55,  55),
    "beak_nrm"  : (170,  90,  30),
    "beak_gld"  : (200, 140,  40),
    "gold"      : (255, 215,   0),
    "gold_light": (255, 240, 130),
    "gold_dark" : (180, 150,   0),
    "mush_red"  : (220,  50,  47),
    "mush_wht"  : (255, 255, 255),
    "white"     : (255, 255, 255),
    "black"     : (  0,   0,   0),
    "text"      : ( 83,  83,  83),
    "cloud_day" : (220, 220, 220),
    "cloud_ngt" : ( 55,  60, 100),
    "bar_bg"    : (210, 210, 210),
    "bar_fg"    : (255, 200,  50),
    "orange"    : (255, 140,  30),
    "red_txt"   : (200,  40,  40),
}

# ── Fonts ────────────────────────────────────────────────────────────────────
F_BIG  = pygame.font.SysFont("Courier New", 46, bold=True)
F_MED  = pygame.font.SysFont("Courier New", 26, bold=True)
F_SML  = pygame.font.SysFont("Courier New", 17)
F_TINY = pygame.font.SysFont("Courier New", 13)

# ── Hi-score file I/O ──────────────────────────────────────────────────────
def _load_hi():
    try:
        with open("hi_score.dat") as f:
            return int(f.read().strip())
    except Exception:
        return 0

def _save_hi(n):
    try:
        with open("hi_score.dat", "w") as f:
            f.write(str(int(n)))
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 3  —  DRAWING PRIMITIVES
#  All graphics are drawn programmatically using pygame shapes.
#  No external image files are required.
# ═══════════════════════════════════════════════════════════════════════════

def draw_dino(surf, x, bottom, frame, powered, ducking):
    """
    Render the player dinosaur using pygame shapes.
      x       — left edge pixel position
      bottom  — y-coordinate of feet (ground contact point)
      frame   — 0 or 1 for leg-cycle animation
      powered — True when Super Mushroom is active (larger + golden)
      ducking — True when player holds DOWN
    """
    sc  = (lambda v: int(v * 1.40)) if powered else (lambda v: int(v))
    dc  = P["gold"] if powered else P["dino"]
    ew  = P["dino_eye_w"]
    eb  = P["dino_eye_b"]

    # Head rect — set in both branches, used by eye/powerup blocks below
    hx = hy = hw = hh = 0

    # ── DUCKING STATE ────────────────────────────────────────────────────
    if ducking:
        bw, bh = sc(56), sc(26)
        bx = x
        by = bottom - bh - sc(4)

        # Tail
        pygame.draw.polygon(surf, dc, [
            (bx - sc(10), by + sc(8)),
            (bx + sc(4),  by + sc(2)),
            (bx + sc(4),  by + sc(18)),
        ])
        # Body
        pygame.draw.rect(surf, dc, (bx, by, bw, bh), border_radius=sc(5))

        # Head (stretches forward)
        hw, hh = sc(28), sc(22)
        hx = bx + bw - sc(2)
        hy = by - sc(4)
        pygame.draw.rect(surf, dc, (hx, hy, hw, hh), border_radius=sc(4))

        # Short legs
        pygame.draw.rect(surf, dc, (bx + sc(8),  bottom - sc(10), sc(10), sc(10)))
        pygame.draw.rect(surf, dc, (bx + sc(26), bottom - sc(10), sc(10), sc(10)))

    # ── STANDING / RUNNING STATE ─────────────────────────────────────────
    else:
        bw, bh = sc(38), sc(28)
        bx = x
        by = bottom - sc(20) - bh

        # Tail
        ty = by + sc(18)
        pygame.draw.polygon(surf, dc, [
            (bx - sc(12), ty + sc(6)),
            (bx + sc(4),  ty),
            (bx + sc(4),  ty + sc(14)),
        ])
        # Body
        pygame.draw.rect(surf, dc, (bx, by, bw, bh), border_radius=sc(5))

        # Neck
        nw, nh = sc(14), sc(18)
        nx = bx + bw - sc(18)
        ny = by - nh + sc(6)
        pygame.draw.rect(surf, dc, (nx, ny, nw, nh))

        # Head
        hw, hh = sc(26), sc(22)
        hx = nx + nw - sc(8)
        hy = ny - sc(12)
        pygame.draw.rect(surf, dc, (hx, hy, hw, hh), border_radius=sc(4))

        # Animated legs
        lw, lh = sc(10), sc(20)
        ly = bottom - lh
        if frame == 0:
            pygame.draw.rect(surf, dc, (bx + sc(6),  ly,          lw, lh))
            pygame.draw.rect(surf, dc, (bx + sc(22), ly - sc(8),  lw, lh - sc(6)))
        else:
            pygame.draw.rect(surf, dc, (bx + sc(6),  ly - sc(8),  lw, lh - sc(6)))
            pygame.draw.rect(surf, dc, (bx + sc(22), ly,          lw, lh))

    # ── Eye & Nostril (both states share this) ───────────────────────────
    ex = hx + hw - sc(8)
    ey = hy + sc(7)
    pygame.draw.circle(surf, ew, (ex, ey), sc(5))
    pygame.draw.circle(surf, eb, (ex + sc(1), ey), sc(2))
    pygame.draw.rect(surf, eb,
                     (hx + hw - sc(4), hy + hh - sc(5), sc(4), sc(2)))

    # ── Powered-up visual effects ────────────────────────────────────────
    if powered:
        # Golden glow behind dino
        gx = x - sc(10)
        gy = hy - sc(8)
        gw = sc(80)
        gh = max(4, (bottom - gy) + sc(4))
        gs = pygame.Surface((gw, gh), pygame.SRCALPHA)
        pygame.draw.rect(gs, (255, 200, 50, 40), (0, 0, gw, gh),
                         border_radius=sc(10))
        surf.blit(gs, (gx, gy))

        # Mushroom cap worn on head (like Mario)
        mx = hx + hw // 2
        my = hy - sc(16)
        # Stalk
        pygame.draw.rect(surf, P["mush_wht"],
                         (mx - sc(6), my + sc(8), sc(12), sc(10)))
        # Cap
        pygame.draw.ellipse(surf, P["mush_red"],
                            (mx - sc(14), my, sc(28), sc(16)))
        # White spots on cap
        pygame.draw.circle(surf, P["mush_wht"], (mx - sc(5), my + sc(4)), sc(3))
        pygame.draw.circle(surf, P["mush_wht"], (mx + sc(5), my + sc(4)), sc(3))


# ── Cactus ────────────────────────────────────────────────────────────────
def draw_cactus(surf, x, gy, variant):
    """
    Render a cactus obstacle. gy = ground y-coordinate.
    4 variants: small single, tall single, double, triple cluster.
    """
    c = P["cactus"]

    def trunk(cx, base, tw, th):
        """Draw a cactus trunk pillar with rounded top."""
        pygame.draw.rect(surf, c, (cx - tw // 2, base - th, tw, th))
        pygame.draw.ellipse(surf, c, (cx - tw // 2, base - th - 5, tw, 10))

    def side_arm(cx, base, tw, arm_ht, arm_len, side):
        """Draw a horizontal arm extending left (-1) or right (+1)."""
        aw, ah = 7, 16
        ay = base - arm_ht
        if side < 0:
            pygame.draw.rect(surf, c,
                             (cx - tw // 2 - arm_len, ay - aw, arm_len, aw))
            trunk(cx - tw // 2 - arm_len + aw // 2, ay, aw, ah)
        else:
            pygame.draw.rect(surf, c,
                             (cx + tw // 2, ay - aw, arm_len, aw))
            trunk(cx + tw // 2 + arm_len - aw // 2, ay, aw, ah)

    def full_cactus(cx, base, tw, th, arm_ht, arm_len):
        trunk(cx, base, tw, th)
        side_arm(cx, base, tw, arm_ht, arm_len, -1)
        side_arm(cx, base, tw, arm_ht, arm_len,  1)

    if   variant == 0: full_cactus(x + 18, gy, 14, 44, 18, 12)          # small
    elif variant == 1: full_cactus(x + 18, gy, 16, 62, 26, 16)          # tall
    elif variant == 2:                                                    # double
        full_cactus(x + 14, gy, 12, 40, 16, 10)
        full_cactus(x + 36, gy, 14, 54, 22, 12)
    else:                                                                 # triple
        full_cactus(x + 12, gy, 10, 36, 12,  8)
        full_cactus(x + 30, gy, 14, 56, 22, 14)
        full_cactus(x + 52, gy, 10, 38, 14,  8)


# ── Bird ──────────────────────────────────────────────────────────────────
def draw_bird(surf, x, y, frame, golden):
    """
    Render a flying bird.
    golden=True → golden colour + sparkles + "?" hint = powerup source.
    """
    bc  = P["gold"]      if golden else P["bird"]
    wc  = P["gold_dark"] if golden else P["bird_wing"]
    bkc = P["beak_gld"]  if golden else P["beak_nrm"]

    # Body ellipse
    pygame.draw.ellipse(surf, bc, (x, y - 8, 36, 18))
    # Beak
    pygame.draw.polygon(surf, bkc,
                        [(x + 36, y), (x + 47, y + 4), (x + 36, y + 8)])
    # Eye
    pygame.draw.circle(surf, P["white"], (x + 28, y - 1), 4)
    pygame.draw.circle(surf, P["black"], (x + 29, y - 1), 2)

    # Animated wing (frame 0 = up, frame 1 = down)
    if frame == 0:
        wp = [(x + 8, y - 8), (x + 22, y - 20), (x + 30, y - 8)]
    else:
        wp = [(x + 8, y + 8), (x + 22, y + 18), (x + 30, y + 8)]
    pygame.draw.polygon(surf, wc, wp)

    # Golden bird extras: sparkle animation + "?" powerup hint
    if golden:
        t = pygame.time.get_ticks()
        sparks = [(-10, -14), (38, -14), (20, -24), (44, 0), (0, 4)]
        for i, (ox, oy) in enumerate(sparks):
            if (t // 160 + i) % 3 == 0:
                pygame.draw.circle(surf, P["gold_light"],
                                   (x + ox, y + oy), 2 + i % 2)
        hint = F_TINY.render("?", True, P["white"])
        surf.blit(hint, (x + 12, y - 7))


# ── Mushroom icon (HUD & start screen) ───────────────────────────────────
def draw_mushroom_icon(surf, cx, cy, s=1.0):
    """Draw a Mario-style Super Mushroom centred at (cx, cy)."""
    def sc(v): return int(v * s)
    # Stalk
    pygame.draw.rect(surf, P["mush_wht"],
                     (cx - sc(7), cy + sc(2), sc(14), sc(12)))
    # Cap
    pygame.draw.ellipse(surf, P["mush_red"],
                        (cx - sc(18), cy - sc(10), sc(36), sc(20)))
    # White spots
    for dx, dy in [(-8, -4), (7, -4), (0, -9)]:
        pygame.draw.circle(surf, P["mush_wht"],
                           (cx + sc(dx), cy + sc(dy)), sc(4))
    # Face
    pygame.draw.circle(surf, P["black"], (cx - sc(4), cy + sc(4)), sc(2))
    pygame.draw.circle(surf, P["black"], (cx + sc(4), cy + sc(4)), sc(2))
    pygame.draw.arc(surf, P["black"],
                    (cx - sc(5), cy + sc(4), sc(10), sc(6)),
                    math.pi, 2 * math.pi, 2)


# ── Cloud ─────────────────────────────────────────────────────────────────
def draw_cloud(surf, x, y, night):
    c = P["cloud_ngt"] if night else P["cloud_day"]
    pygame.draw.ellipse(surf, c, (x,      y,      58, 22))
    pygame.draw.ellipse(surf, c, (x + 10, y - 12, 36, 26))
    pygame.draw.ellipse(surf, c, (x + 30, y -  5, 32, 20))


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 4  —  GAME OBJECTS
# ═══════════════════════════════════════════════════════════════════════════

class Dino:
    """
    The player-controlled dinosaur.
    States: running, jumping, ducking, powered (Super Mushroom active).
    """
    BASE_W, BASE_H, DUCK_H = 52, 60, 32

    def __init__(self):
        self.reset()

    def reset(self):
        self.x         = 80
        self.y         = float(GROUND_Y)   # y of feet (bottom of dino)
        self.vy        = 0.0
        self.on_ground = True
        self.ducking   = False
        self.frame     = 0
        self.ftick     = 0
        self.powered   = False
        self.power_ms  = 0.0              # remaining powerup milliseconds

    @property
    def rect(self):
        """Collision rectangle — slightly inset for fair gameplay."""
        scale = 1.40 if self.powered else 1.0
        w = int(self.BASE_W * scale)
        h = int((self.DUCK_H if self.ducking else self.BASE_H) * scale)
        m = 8   # inset margin
        return pygame.Rect(
            int(self.x) + m,
            int(self.y) - h + m,
            w - m * 2,
            h - m
        )

    def jump(self):
        """Trigger a jump if on the ground and not ducking."""
        if self.on_ground and not self.ducking:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def set_duck(self, v: bool):
        """Start or stop ducking (only while on the ground)."""
        if self.on_ground:
            self.ducking = v

    def activate_powerup(self):
        """Activate the Super Mushroom powerup."""
        self.powered  = True
        self.power_ms = float(POWERUP_DURATION)

    def update(self, dt_ms: float):
        # Apply gravity and move
        self.vy += GRAVITY
        self.y  += self.vy

        # Land check
        if self.y >= GROUND_Y:
            self.y = float(GROUND_Y)
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        # Powerup countdown
        if self.powered:
            self.power_ms -= dt_ms
            if self.power_ms <= 0:
                self.powered  = False
                self.power_ms = 0.0

        # Leg animation cycle
        self.ftick += 1
        if self.ftick >= 7:
            self.ftick = 0
            self.frame = 1 - self.frame

    def draw(self, surf):
        draw_dino(surf, self.x, int(self.y),
                  self.frame, self.powered, self.ducking)


# ── Cactus hitbox sizes per variant ───────────────────────────────────────
_CW = [40, 44, 66, 82]   # width  (variants 0-3)
_CH = [54, 72, 64, 66]   # height (variants 0-3)

class Cactus:
    """A ground-based cactus obstacle (4 size variants)."""

    def __init__(self, x: float, speed: float):
        self.variant = random.randint(0, 3)
        self.x       = x
        self.speed   = speed
        self.w       = _CW[self.variant]
        self.h       = _CH[self.variant]

    @property
    def rect(self):
        m = 6
        return pygame.Rect(int(self.x) + m,
                           GROUND_Y - self.h + m,
                           self.w - m * 2,
                           self.h - m)

    def update(self): self.x -= self.speed
    def draw(self, s): draw_cactus(s, int(self.x), GROUND_Y, self.variant)
    def gone(self):  return self.x + self.w < 0


# ── Bird flight heights ────────────────────────────────────────────────────
# Low  (305) → dino must duck or jump to avoid
# Mid  (265) → flies just over dino's head; risky to jump near
# High (205) → free pass; dino easily runs beneath
_BIRD_HEIGHTS = [GROUND_Y - 55, GROUND_Y - 95, GROUND_Y - 155]

class Bird:
    """
    A flying bird obstacle.
    golden=True → this is the special powerup source bird.
    """
    W, H = 50, 32

    def __init__(self, x: float, speed: float, golden: bool = False):
        self.x      = x
        self.speed  = speed
        self.golden = golden
        self.y      = random.choice(_BIRD_HEIGHTS)
        self.frame  = 0
        self.ftick  = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x) + 4, self.y - 6,
                           self.W - 8, self.H - 8)

    def update(self):
        self.x    -= self.speed
        self.ftick += 1
        if self.ftick >= 10:
            self.ftick = 0
            self.frame = 1 - self.frame

    def draw(self, s): draw_bird(s, int(self.x), self.y, self.frame, self.golden)
    def gone(self):   return self.x + self.W < 0


class Cloud:
    """Decorative background cloud."""

    def __init__(self, x):
        self.x = float(x)
        self.y = random.randint(50, 180)

    def update(self, speed): self.x -= speed * 0.28
    def draw(self, s, night): draw_cloud(s, int(self.x), self.y, night)
    def gone(self): return self.x + 90 < 0


class Particle:
    """
    A single coloured particle for smash/collect explosion effects.
    Spawned in bursts when the dino smashes obstacles or collects a powerup.
    """

    def __init__(self, x, y, col=None):
        self.x  = float(x)
        self.y  = float(y)
        self.vx = random.uniform(-4.0, 4.0)
        self.vy = random.uniform(-6.0, -1.0)
        self.life = self.max_life = random.randint(22, 44)
        self.col  = col or random.choice([
            P["gold"], P["gold_light"], P["mush_red"], P["white"], P["orange"]
        ])
        self.r = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25        # gravity on particles
        self.life -= 1

    def draw(self, surf):
        if self.life <= 0:
            return
        alpha = max(0, int(255 * self.life / self.max_life))
        s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.col, alpha), (self.r, self.r), self.r)
        surf.blit(s, (int(self.x) - self.r, int(self.y) - self.r))


class ScorePopup:
    """Floating score text (+50, +30, SUPER!) that rises and fades out."""

    def __init__(self, x, y, text, colour=None):
        self.x    = float(x)
        self.y    = float(y)
        self.text = text
        self.col  = colour or P["gold"]
        self.life = 55

    def update(self):
        self.y    -= 0.9
        self.life -= 1

    def draw(self, surf):
        if self.life <= 0:
            return
        alpha = max(0, int(255 * self.life / 55))
        s = F_SML.render(self.text, True, self.col)
        s.set_alpha(alpha)
        surf.blit(s, (int(self.x), int(self.y)))


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 5  —  GAME MANAGER
# ═══════════════════════════════════════════════════════════════════════════

class Game:
    """
    Central game manager.
    Handles state machine (menu → instructions → playing → gameover),
    all game-object updates, collision detection, and rendering.
    """
    MENU         = "menu"
    INSTRUCTIONS = "instructions"
    PLAYING      = "playing"
    GAMEOVER     = "gameover"

    def __init__(self):
        self.hi_score = _load_hi()
        self.state    = self.MENU
        # Menu selection (0=Start, 1=Instructions, 2=Exit)
        self.menu_selected = 0
        # Gameover menu selection (0=Retry, 1=Main Menu)
        self.gameover_selected = 0
        # Star positions (fixed per session, shown during night mode)
        self.stars = [(random.randint(0, SCREEN_W),
                       random.randint(20, GROUND_Y - 60))
                      for _ in range(80)]
        self._reset()

    # ── Reset all game state for a new run ─────────────────────────────
    def _reset(self):
        self.dino       = Dino()
        self.cacti      = []
        self.birds      = []
        self.clouds     = [Cloud(random.randint(0, SCREEN_W)) for _ in range(5)]
        self.particles  = []
        self.popups     = []
        self.score      = 0.0
        self.speed      = SPEED_INITIAL
        self.spawn_timer   = 0
        self.spawn_gap     = 90      # frames between obstacle spawns
        self.night         = False
        self.night_next    = 700.0   # score threshold for next day/night toggle
        self.gnd_offset    = 0.0     # ground texture scroll offset
        self.flash_timer   = 0       # frames remaining for white speed-up flash
        self.milestones    = set()   # speed milestones already applied
        self.gameover_selected = 0   # reset menu selection

    # ── Input / Event Handling ─────────────────────────────────────────
    def handle_event(self, ev):
        # Handle key-up (duck release) for any non-KEYDOWN event
        if ev.type != pygame.KEYDOWN:
            if (ev.type == pygame.KEYUP and ev.key == pygame.K_DOWN
                    and self.state == self.PLAYING):
                self.dino.set_duck(False)
            return

        k = ev.key

        if self.state == self.MENU:
            if k == pygame.K_UP:
                self.menu_selected = (self.menu_selected - 1) % 3
            elif k == pygame.K_DOWN:
                self.menu_selected = (self.menu_selected + 1) % 3
            elif k in (pygame.K_SPACE, pygame.K_RETURN):
                if self.menu_selected == 0:      # Start Game
                    self.state = self.PLAYING
                    self._reset()
                elif self.menu_selected == 1:    # Instructions
                    self.state = self.INSTRUCTIONS
                elif self.menu_selected == 2:    # Exit
                    pygame.quit()
                    sys.exit()

        elif self.state == self.INSTRUCTIONS:
            if k in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                self.state = self.MENU

        elif self.state == self.PLAYING:
            if   k in (pygame.K_SPACE, pygame.K_UP): self.dino.jump()
            elif k == pygame.K_DOWN:                  self.dino.set_duck(True)

        elif self.state == self.GAMEOVER:
            if k == pygame.K_UP:
                self.gameover_selected = (self.gameover_selected - 1) % 2
            elif k == pygame.K_DOWN:
                self.gameover_selected = (self.gameover_selected + 1) % 2
            elif k in (pygame.K_SPACE, pygame.K_r, pygame.K_RETURN):
                if self.gameover_selected == 0:  # Retry
                    self.state = self.PLAYING
                    self._reset()
                elif self.gameover_selected == 1:  # Main Menu
                    self.state = self.MENU
                    self.menu_selected = 0

    # ── Obstacle Spawning ──────────────────────────────────────────────
    def _try_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer < self.spawn_gap:
            return
        self.spawn_timer = 0

        # Gradually shrink the gap as score increases (harder game)
        min_gap = max(28, 75  - int(self.score // 120))
        max_gap = max(55, 110 - int(self.score // 90))
        self.spawn_gap = random.randint(min_gap, max_gap)

        roll = random.random()
        x    = float(SCREEN_W + 20)

        if   roll < 0.06:  self.birds.append(Bird(x, self.speed, golden=True))
        elif roll < 0.25:  self.birds.append(Bird(x, self.speed))
        else:              self.cacti.append(Cactus(x, self.speed))

    # ── Particle Burst Helper ──────────────────────────────────────────
    def _burst(self, cx, cy, n=20):
        for _ in range(n):
            self.particles.append(Particle(cx, cy))

    # ── Main Update (called every frame during PLAYING) ────────────────
    def update(self):
        if self.state != self.PLAYING:
            return

        dt = float(clock.get_time())   # ms elapsed since last frame

        # ── Score ──────────────────────────────────────────────────────
        self.score += SCORE_PER_FRAME
        iscore = int(self.score)

        # ── Speed milestone check ──────────────────────────────────────
        ms_key = (iscore // SPEED_INTERVAL) * SPEED_INTERVAL
        if ms_key > 0 and ms_key not in self.milestones:
            self.milestones.add(ms_key)
            self.speed = min(self.speed + 1.0, SPEED_MAX)
            self.flash_timer = 28     # brief white flash to signal speed-up

        # ── Night / day toggle every 700 points ───────────────────────
        if self.score >= self.night_next:
            self.night      = not self.night
            self.night_next += 700.0

        # ── Ground scroll offset ───────────────────────────────────────
        self.gnd_offset = (self.gnd_offset + self.speed) % SCREEN_W

        # ── Update all objects ─────────────────────────────────────────
        self.dino.update(dt)

        for o in self.cacti[:]:
            o.update()
            if o.gone(): self.cacti.remove(o)

        for o in self.birds[:]:
            o.update()
            if o.gone(): self.birds.remove(o)

        for o in self.clouds[:]:
            o.update(self.speed)
            if o.gone():
                self.clouds.remove(o)
                self.clouds.append(Cloud(SCREEN_W + 40))

        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)

        for p in self.popups[:]:
            p.update()
            if p.life <= 0: self.popups.remove(p)

        self._try_spawn()

        # ── Collision Detection ────────────────────────────────────────
        self._check_collisions()

        if self.flash_timer > 0:
            self.flash_timer -= 1

    def _check_collisions(self):
        dr = self.dino.rect

        # ── Dino vs Cactus ─────────────────────────────────────────────
        for obs in self.cacti[:]:
            if dr.colliderect(obs.rect):
                if self.dino.powered:
                    # Super Mushroom active → SMASH through the cactus!
                    cx, cy = obs.rect.centerx, obs.rect.centery
                    self._burst(cx, cy, 24)
                    self.popups.append(ScorePopup(cx - 12, cy - 24, "+50"))
                    self.score += 50
                    self.cacti.remove(obs)
                else:
                    self._game_over()
                    return

        # ── Dino vs Bird ───────────────────────────────────────────────
        for bird in self.birds[:]:
            if dr.colliderect(bird.rect):
                if bird.golden:
                    # ★ COLLECT the Super Mushroom powerup! ★
                    self._burst(bird.rect.centerx, bird.rect.centery, 38)
                    self.popups.append(
                        ScorePopup(bird.rect.x - 10, bird.rect.y - 26,
                                   "SUPER!", colour=P["gold"]))
                    self.dino.activate_powerup()
                    self.birds.remove(bird)

                elif self.dino.powered:
                    # Powered → smash the regular bird too
                    cx, cy = bird.rect.centerx, bird.rect.centery
                    self._burst(cx, cy, 16)
                    self.popups.append(ScorePopup(cx - 12, cy - 24, "+30"))
                    self.score += 30
                    self.birds.remove(bird)

                else:
                    self._game_over()
                    return

    def _game_over(self):
        self.state = self.GAMEOVER
        if self.score > self.hi_score:
            self.hi_score = self.score
            _save_hi(self.hi_score)

    # ═══════════════════════════════════════════════════════════════════
    #  RENDERING
    # ═══════════════════════════════════════════════════════════════════

    def draw(self):
        # ── Sky ────────────────────────────────────────────────────────
        screen.fill(P["sky_night"] if self.night else P["sky_day"])

        # ── Stars (night only) ─────────────────────────────────────────
        if self.night:
            for sx, sy in self.stars:
                pygame.draw.circle(screen, P["white"], (sx, sy), 1)

        # ── Clouds ─────────────────────────────────────────────────────
        for c in self.clouds:
            c.draw(screen, self.night)

        # ── Ground line + scrolling pebble texture ─────────────────────
        gc   = P["ground"]
        goff = int(self.gnd_offset)
        pygame.draw.line(screen, gc, (0, GROUND_Y), (SCREEN_W, GROUND_Y), 2)
        for i in range(0, SCREEN_W + 80, 80):
            bx = (i - goff) % SCREEN_W
            pygame.draw.rect(screen, gc, (bx,      GROUND_Y + 4, 4,  2))
            pygame.draw.rect(screen, gc, (bx + 24, GROUND_Y + 8, 8,  2))
            pygame.draw.rect(screen, gc, (bx + 50, GROUND_Y + 4, 5,  2))
            pygame.draw.rect(screen, gc, (bx + 65, GROUND_Y + 7, 4,  2))

        # ── Game objects ───────────────────────────────────────────────
        for o in self.cacti:  o.draw(screen)
        for o in self.birds:  o.draw(screen)

        # Particles (drawn behind the dino so they feel like an explosion)
        for p in self.particles: p.draw(screen)

        self.dino.draw(screen)

        # Score popups float above smashed obstacles
        for p in self.popups: p.draw(screen)

        # ── HUD ────────────────────────────────────────────────────────
        self._draw_hud()

        # ── Speed-up white flash ───────────────────────────────────────
        if self.flash_timer > 0:
            alpha = int(110 * self.flash_timer / 28)
            fs = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            fs.fill((255, 255, 255, alpha))
            screen.blit(fs, (0, 0))

        # ── State overlays ─────────────────────────────────────────────
        if   self.state == self.MENU:         self._draw_menu()
        elif self.state == self.INSTRUCTIONS: self._draw_instructions()
        elif self.state == self.GAMEOVER:     self._draw_gameover()

    # ── HUD (scores + powerup bar) ─────────────────────────────────────
    def _draw_hud(self):
        # Scores — top right, Chrome-dino style "HI XXXXX  XXXXX"
        stxt = F_SML.render(
            f"HI {int(self.hi_score):05d}   {int(self.score):05d}",
            True, P["text"])
        screen.blit(stxt, (SCREEN_W - stxt.get_width() - 18, 14))

        # Powerup bar — top left, only visible when powered
        if self.dino.powered:
            ratio = max(0.0, self.dino.power_ms / POWERUP_DURATION)
            bx, by, bw, bh = 30, 18, 170, 20
            low = ratio < 0.25

            # Flicker bar when nearly expired (< 25%)
            if not low or (pygame.time.get_ticks() // 200) % 2 == 0:
                pygame.draw.rect(screen, P["bar_bg"],
                                 (bx, by, bw, bh), border_radius=5)
                bar_col = P["orange"] if low else P["bar_fg"]
                pygame.draw.rect(screen, bar_col,
                                 (bx, by, int(bw * ratio), bh),
                                 border_radius=5)
                pygame.draw.rect(screen, P["gold"],
                                 (bx, by, bw, bh), 2, border_radius=5)
                lbl = F_SML.render("SUPER!", True, P["black"])
                screen.blit(lbl, (bx + 10, by + 2))

            # Mushroom icon to the left of the bar
            draw_mushroom_icon(screen, bx - 22, by + 10, s=0.95)

    # ── Main Menu Screen ───────────────────────────────────────────────
    def _draw_menu(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((245, 245, 245, 220))
        screen.blit(ov, (0, 0))

        title = F_BIG.render("DINO  MARIO  RUNNER", True, P["dino"])
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))

        # Big mushroom icon
        draw_mushroom_icon(screen, SCREEN_W // 2, 130, s=2.2)

        # Menu options
        menu_options = [
            ("START  GAME", 0),
            ("HOW  TO  PLAY", 1),
            ("EXIT", 2),
        ]

        my = 210
        for text, idx in menu_options:
            is_selected = (idx == self.menu_selected)
            col = P["gold"] if is_selected else P["text"]
            prefix = "▶  " if is_selected else "   "
            opt = F_MED.render(prefix + text, True, col)
            screen.blit(opt, (SCREEN_W // 2 - opt.get_width() // 2, my))
            my += 50

        # Navigation hint
        hint = F_SML.render("↑ ↓  SELECT   SPACE/ENTER  CONFIRM", True, P["text"])
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 400))

    # ── Instructions Screen ────────────────────────────────────────────
    def _draw_instructions(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((245, 245, 245, 220))
        screen.blit(ov, (0, 0))

        title = F_BIG.render("HOW  TO  PLAY", True, P["dino"])
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))

        lines = [
            ("─── OBJECTIVE ────────────────────────", P["text"]),
            ("Run as far as you can! Avoid obstacles", P["text"]),
            ("and collect the golden bird powerup.  ", P["text"]),
            ("",                                       P["text"]),
            ("─── CONTROLS ────────────────────────", P["text"]),
            ("SPACE / ↑     Jump over obstacles",    P["text"]),
            ("↓ (hold)      Duck under flying birds", P["text"]),
            ("",                                       P["text"]),
            ("─── GOLDEN BIRD POWERUP ─────────────", P["red_txt"]),
            ("Collide with the GOLDEN BIRD (⭐)",     P["text"]),
            ("to get the SUPER MUSHROOM!",            P["text"]),
            ("While powered: smash ALL obstacles",    P["text"]),
            ("+50 per cactus   +30 per bird",         P["text"]),
            ("",                                       P["text"]),
            ("─────────────────────────────────────", P["text"]),
            ("SPACE/ENTER  Back to Menu",              P["dino"]),
        ]

        sy = 70
        for text, col in lines:
            if text:
                s = F_SML.render(text, True, col)
                screen.blit(s, (SCREEN_W // 2 - s.get_width() // 2, sy))
            sy += 20

    # ── Start Screen ───────────────────────────────────────────────────
    def _draw_start(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((245, 245, 245, 200))
        screen.blit(ov, (0, 0))

        title = F_BIG.render("DINO  MARIO  RUNNER", True, P["dino"])
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 68))

        # Big mushroom icon
        draw_mushroom_icon(screen, SCREEN_W // 2, 155, s=2.5)

        prompt = F_MED.render("PRESS  SPACE / \u2191  TO  START", True, P["dino"])
        screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, 200))

        lines = [
            ("─── CONTROLS ────────────────────", P["text"]),
            ("SPACE / \u2191  \u2192  Jump",       P["text"]),
            ("\u2193 (hold)  \u2192  Duck",         P["text"]),
            ("",                                    P["text"]),
            ("─── GOLDEN BIRD POWERUP ─────────", P["red_txt"]),
            ("Collide with the  GOLDEN BIRD (\u2605)", P["text"]),
            ("to collect the  SUPER MUSHROOM!", P["text"]),
            ("Powered up: smash ALL obstacles!", P["text"]),
            ("+50 per cactus   +30 per bird",   P["text"]),
        ]
        sy = 248
        for text, col in lines:
            if text:
                s = F_SML.render(text, True, col)
                screen.blit(s, (SCREEN_W // 2 - s.get_width() // 2, sy))
            sy += 22

    # ── Game Over Screen ───────────────────────────────────────────────
    def _draw_gameover(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((245, 245, 245, 200))
        screen.blit(ov, (0, 0))

        go = F_BIG.render("GAME  OVER", True, P["dino"])
        screen.blit(go, (SCREEN_W // 2 - go.get_width() // 2, 100))

        sc = F_MED.render(f"SCORE :  {int(self.score):05d}", True, P["dino"])
        screen.blit(sc, (SCREEN_W // 2 - sc.get_width() // 2, 160))

        if self.score > 0 and int(self.score) >= int(self.hi_score):
            nh = F_SML.render("\u2605  NEW  HIGH  SCORE  \u2605", True, P["gold"])
            screen.blit(nh, (SCREEN_W // 2 - nh.get_width() // 2, 210))

        # Game Over menu options
        menu_options = [
            ("RETRY", 0),
            ("MAIN  MENU", 1),
        ]

        my = 260
        for text, idx in menu_options:
            is_selected = (idx == self.gameover_selected)
            col = P["gold"] if is_selected else P["text"]
            prefix = "▶  " if is_selected else "   "
            opt = F_MED.render(prefix + text, True, col)
            screen.blit(opt, (SCREEN_W // 2 - opt.get_width() // 2, my))
            my += 50

        # Navigation hint
        hint = F_SML.render("↑ ↓  SELECT   SPACE/R/ENTER  CONFIRM", True, P["text"])
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 400))


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 6  —  MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Entry point: initialises the Game and runs the main loop."""
    game = Game()

    while True:
        # ── Process all queued events ───────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(ev)

        # ── Update game state ───────────────────────────────────────────
        game.update()

        # ── Render everything ───────────────────────────────────────────
        game.draw()

        # ── Push frame to display ───────────────────────────────────────
        pygame.display.flip()

        # ── Maintain 60 FPS ────────────────────────────────────────────
        clock.tick(FPS)


if __name__ == "__main__":
    main()