import pygame
import random

# 게임 화면 크기
WIDTH = 800
HEIGHT = 600

# 색깔 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 적 비행기 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # 작은 원을 위한 Surface 생성
        self.image.fill(WHITE)  # 흰색으로 채움
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.rect.y = random.randrange(-100, -10)
            self.rect.x = random.randrange(0, WIDTH)
            global score
            score += 1

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # 작은 원을 위한 Surface 생성
        self.image.fill(WHITE)  # 흰색으로 채움
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("스페이스 인베이더 게임")

# 폰트 설정
font = pygame.font.Font(None, 36)

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()

# 적 비행기 그룹 생성
enemy_sprites = pygame.sprite.Group()

# 플레이어 생성
player = Player()
all_sprites.add(player)

# 적 비행기 생성
ENEMY_FREQ = 30  # 적 비행기 생성 주기 설정

enemy_spawn_counter = 0  # 적 비행기 생성 주기를 세는 카운터 변수
enemy_spawn_rate = 60  # 적 비행기 생성 주기 초기값



# 게임 상태 변수
global score 
score = 0
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    enemy_spawn_counter += 1
    if enemy_spawn_counter >= enemy_spawn_rate:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        enemy_spawn_counter = 0

    # 게임 로직 업데이트
    all_sprites.update()

    # 충돌 체크
    hits = pygame.sprite.spritecollide(player, enemy_sprites, False)
    if hits:
        running = False

    # 화면 업데이트
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 점수 표시
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # 초당 프레임 수 설정 
    clock.tick(60)

# 게임 종료
pygame.quit()
