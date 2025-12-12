import pygame
pygame.init()

# ---------------------------
# WINDOW
# ---------------------------
win_width = 800
win_height = 600
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("PINGPONG GAME")

clock = pygame.time.Clock()
FPS = 60


# ---------------------------
# BACKGROUND
# ---------------------------
def draw_background():
    window.fill((30, 120, 50))
    pygame.draw.line(window, (255, 255, 255),
                     (win_width // 2, 0),
                     (win_width // 2, win_height), 5)
    pygame.draw.rect(window, (255, 255, 255),
                     (0, 0, win_width, win_height), 5)


# ---------------------------
# PLAYER CLASS
# ---------------------------
class Player:
    def __init__(self, x, y, w, h, speed, up_key, down_key):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key

    def show(self):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[self.up_key]:
            self.rect.y -= self.speed
        if keys[self.down_key]:
            self.rect.y += self.speed

        # Batas agar tidak keluar
        if self.rect.y < 10:
            self.rect.y = 10
        if self.rect.y > win_height - 110:
            self.rect.y = win_height - 110


# ---------------------------
# BALL CLASS
# ---------------------------
class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def show(self):
        pygame.draw.ellipse(window, (255, 255, 255), self.rect)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Mantul atas / bawah
        if self.rect.top <= 0 or self.rect.bottom >= win_height:
            self.speed_y *= -1

    def bounce(self, left, right):
        # Mantul raket kiri
        if self.rect.colliderect(left.rect):
            self.speed_x = abs(self.speed_x)

        # Mantul raket kanan
        if self.rect.colliderect(right.rect):
            self.speed_x = -abs(self.speed_x)

    def check_out(self):
        if self.rect.left <= 0:
            return "LEFT_LOSE"
        if self.rect.right >= win_width:
            return "RIGHT_LOSE"
        return None


# ---------------------------
# OBJECTS
# ---------------------------
racket_left = Player(30, 250, 20, 100, 7, pygame.K_w, pygame.K_s)
racket_right = Player(win_width - 50, 250, 20, 100, 7, pygame.K_UP, pygame.K_DOWN)

ball = Ball(win_width // 2, win_height // 2, 20, 6, 6)

# ---------------------------
# GAME VARIABLES
# ---------------------------
run = True
game_over = False
winner_text = ""
font = pygame.font.SysFont("Arial", 50)


# ---------------------------
# GAME LOOP
# ---------------------------
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    if not game_over:
        draw_background()

        # Gerak raket
        racket_left.move()
        racket_right.move()

        # Tampilkan raket
        racket_left.show()
        racket_right.show()

        # Bola bergerak & mantul
        ball.move()
        ball.bounce(racket_left, racket_right)
        ball.show()

        # Cek kalah
        result = ball.check_out()
        if result == "LEFT_LOSE":
            winner_text = "PLAYER LEFT KALAH!"
            game_over = True
        elif result == "RIGHT_LOSE":
            winner_text = "PLAYER RIGHT KALAH!"
            game_over = True

    else:
        # Tampilkan background dan hasil
        draw_background()
        text = font.render(winner_text, True, (255, 255, 255))
        window.blit(text, (win_width // 2 - text.get_width() // 2,
                           win_height // 2 - text.get_height() // 2))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
