import pygame
import random

# 게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("벽돌 게임")

# 색상 정의
BLACK = "#000000"
PINK = "#ff8ea0"
RED = "#ff0000"
BLUE = "#3c00ff"

# 패들 설정
paddle_width = 100
paddle_height = 10
paddle_speed = 6
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 40, paddle_width, paddle_height)

# 공 설정
ball_radius = 10
ball_speed_x = 6
ball_speed_y = -6
ball = pygame.Rect(screen_width // 2 - ball_radius, screen_height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# 벽돌 설정
brick_width = 60
brick_height = 20
bricks = []

for row in range(5):
    for col in range(12):
        brick = pygame.Rect(col * (brick_width + 5) + 35, row * (brick_height + 5) + 50, brick_width, brick_height)
        bricks.append(brick)

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.x += paddle_speed

    # 공 이동
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 공이 벽에 부딪힐 때 반사
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    # 공이 패들과 부딪히는지 확인
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y

    # 공이 벽돌에 부딪히는지 확인
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y

    # 공이 바닥에 떨어졌을 때
    if ball.bottom >= screen_height:
        running = False
        print("게임 오버!")

    # 화면 그리기
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, PINK, ball)

    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    pygame.display.flip()

    # 게임 속도 설정
    clock.tick(60)

pygame.quit()
