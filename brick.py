import pygame

# 게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 960
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("벽돌 게임")

# 색상 정의
BLACK = "#000000"
BRONZE = "#CD7F32"
RED = "#B22222"
BLUE = "#556B2F"
SKY_BLUE = "#FFFFF0"

# 패들 설정
paddle_width = 120
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
brick_gap = 5  # 벽돌 사이의 간격
bricks_per_row = screen_width // (brick_width + brick_gap)  # 벽돌이 화면 가로를 꽉 채우도록 계산

# 전체 벽돌 너비 계산 (벽돌 수 x 각 벽돌의 너비 + 간격)
total_bricks_width = bricks_per_row * (brick_width + brick_gap) - brick_gap  # 마지막 벽돌의 간격 제외
center_offset_x = (screen_width - total_bricks_width) // 2  # 화면 가로의 중앙에 맞추는 오프셋

# 벽돌의 Y 좌표 (상단에 배치)
start_y = 50
bricks = []

# 벽돌들의 배치
for row in range(5):  # 총 5행
    for col in range(bricks_per_row):  # 각 행에 맞게 벽돌 배치
        brick_x = center_offset_x + col * (brick_width + brick_gap)  # X 좌표에 중앙 정렬 오프셋 추가
        brick_y = start_y + row * (brick_height + brick_gap)
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
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
        print("Game over!")

    # 화면 그리기
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, BRONZE, ball)

    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    pygame.display.flip()

    # 게임 속도 설정
    clock.tick(60)

pygame.quit()
