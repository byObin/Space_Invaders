import pygame
import random

# 게임 화면 크기
WIDTH = 800
HEIGHT = 600

# 색깔 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255,153,153)
BLUE = (0,51,255)



# 적 비행기 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # 작은 원을 위한 Surface 생성
        self.image.fill(PINK)  # 흰색으로 채움
        self.rect = self.image.get_rect()

        self.shoot_timer = random.randint(2000, 4000)  # 총알 발사 타이머
        self.last_shoot_time = pygame.time.get_ticks()  # 마지막 총알 발사 시간


    def update(self):
        self.rect.y += 5  # 비행기의 속도를 5로 증가
        if self.rect.y > HEIGHT:
            self.reset()

        # 랜덤한 시간 간격으로 총알 발사
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time >= self.shoot_timer:
            self.shoot_bullet()
            self.last_shoot_time = now
            self.shoot_timer = random.randint(2000, 4000)  # 다음 총알 발사 타이머 설정


    def reset(self):
        self.rect.y = random.randrange(-100, -10)
        self.rect.x = random.randrange(0, WIDTH)

    def shoot_bullet(self):
        bullet = BulletFromEnemy(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullet_from_enemy_sprites.add(bullet)

# 적 비행기에서 발사되는 총알 클래스
class BulletFromEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # 작은 직사각형을 위한 Surface 생성
        self.image.fill(RED)  # 흰색으로 채움
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 10  # 총알의 속도를 5로 감소
        if self.rect.y < 0:
            self.kill()

# 플레이어가 발사하는 총알 클래스
class BulletFromPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # 작은 직사각형을 위한 Surface 생성
        self.image.fill(BLUE)  # 흰색으로 채움
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5  # 총알의 속도를 5로 감소
        if self.rect.y < 0:
            self.kill()
        
        # 적과의 충돌 체크
        hits = pygame.sprite.spritecollide(self, enemy_sprites, True)
        if hits:
            # 충돌한 적 비행기 삭제
            self.kill()
            # 점수 증가 등 추가 작업 수행
            global score 
            score += 1        

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # 작은 원을 위한 Surface 생성
        self.image.fill(WHITE)  # 흰색으로 채움
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

    def shoot(self):
        bullet = BulletFromPlayer(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullet_from_player_sprites.add(bullet)

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

# 적이 발사하는 총알 그룹 생성
bullet_from_enemy_sprites = pygame.sprite.Group()

# 플레이어가 발사하는 총알 그룹 생성
bullet_from_player_sprites = pygame.sprite.Group()

# 플레이어 생성
player = Player()
all_sprites.add(player)

# 적 비행기 생성
for i in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

# 게임 상태 변수
global score 
score = 0
global running 
running = True
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()  # 스페이스 바를 누르면 플레이어가 총알을 발사

    # 게임 로직 업데이트
    all_sprites.update()

    # 충돌 체크
    hits = pygame.sprite.spritecollide(player, bullet_from_enemy_sprites, False)
    hits_with_enemy = pygame.sprite.spritecollide(player, enemy_sprites, False)

    if hits or hits_with_enemy :
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
#pygame.quit()