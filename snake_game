#Snake game
import pygame
import random
import sys
import keyboard

# 초기화하는것
pygame.init()

# 색상 정한 것
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
SKY_BLUE = (135, 206, 235)
LIGHT_YELLOW = (255, 255, 102)
DARK_YELLOW = (204, 204, 0)

# 게임 설정하는 것
WINDOW_WIDTH = 960  
WINDOW_HEIGHT = 720 
BLOCK_SIZE = 20
GAME_SPEED = 11  
SPEED_INCREMENT = 1  # 사과를 먹을 때마다 증가할 속도
TIME_LIMIT = 120  # 제한 시간 (초)

# 화면 설정하는 것
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.direction = "RIGHT"
        self.length = 1

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == "RIGHT":
            x += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE

        new_head = (x, y)

        # 벽과 충돌 확인하는거임
        if (x < 0 or x >= WINDOW_WIDTH or 
            y < 0 or y >= WINDOW_HEIGHT or 
            new_head in self.positions[:-1]):
            return False, "WALL"  # 벽에 부딪힌 경우

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True, ""

    def draw(self, surface):
        for i, position in enumerate(self.positions):
            color = DARK_YELLOW if i == 0 else LIGHT_YELLOW
            pygame.draw.rect(surface, color, 
                             pygame.Rect(position[0], position[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
            pygame.draw.circle(surface, WHITE, (position[0] + BLOCK_SIZE // 2, position[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 4)

class Apple:
    def __init__(self, bomb_positions):  # 폭탄 위치를 인자로 받음
        self.position = self.randomize_position(bomb_positions)

    def randomize_position(self, bomb_positions):  
        while True:
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_position = (x, y)
            if new_position not in bomb_positions:  # 폭탄과 위치가 다르면
                return new_position

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.position[0] + BLOCK_SIZE // 2, self.position[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        pygame.draw.circle(surface, WHITE, (self.position[0] + BLOCK_SIZE // 3, self.position[1] + BLOCK_SIZE // 3), BLOCK_SIZE // 5)

class Bomb:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):  
        x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y) 
    
    def draw(self, surface):
        pygame.draw.circle(surface, GRAY, (self.position[0] + BLOCK_SIZE // 2, self.position[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        pygame.draw.circle(surface, WHITE, (self.position[0] + BLOCK_SIZE // 3, self.position[1] + BLOCK_SIZE // 3), BLOCK_SIZE // 5)

def main():
    snake = Snake()
    bombs = []  # 폭탄 리스트 초기화
    apple = Apple(bombs)  # 초기 폭탄 리스트를 인자로 전달
    running = True
    victory = False
    game_over_reason = ""
    global GAME_SPEED  # 게임 속도를 전역 변수로 설정

    # 게임 시작 시간 기록
    start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        # 뱀 이동하는 함수
        alive, reason = snake.move()
        if not alive:
            running = False
            game_over_reason = reason
            continue

        # 사과를 먹었는지 확인하는 것
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position([bomb.position for bomb in bombs])  # 폭탄 위치를 인자로 전달
            # 폭탄 위치를 랜덤으로 변경
            for bomb in bombs:
                bomb.position = bomb.randomize_position()

            # 새로운 폭탄 추가
            new_bomb = Bomb()
            bombs.append(new_bomb)  # 새로운 폭탄을 리스트에 추가

            # 게임 속도 증가
            GAME_SPEED += SPEED_INCREMENT

        # 승리 조건: 사과 10개 이상 먹었을 때
        if snake.length > 10:
            victory = True
            running = False
        
        # 패배 조건: 폭탄을 먹었을 때
        for bomb in bombs:
            if snake.get_head_position() == bomb.position:
                running = False  # 게임 종료
                game_over_reason = "BOMB"
                break

        # 제한 시간 체크
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 초 단위로 변환
        if elapsed_time >= TIME_LIMIT:
            running = False  # 게임 종료

        # 화면 그리기
        screen.fill(SKY_BLUE)
        snake.draw(screen)
        apple.draw(screen)
        for bomb in bombs:
            bomb.draw(screen)  # 모든 폭탄 그리기

        # 점수 및 남은 시간 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {snake.length - 1}', True, WHITE)
        time_text = font.render(f'Time Left: {max(0, TIME_LIMIT - int(elapsed_time))}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))

        pygame.display.update()
        clock.tick(GAME_SPEED)

    # 게임 종료 또는 승리 화면
    font = pygame.font.Font(None, 50)
    if victory:
        end_text = font.render('You Win!', True, WHITE)
    elif game_over_reason == "WALL":
        end_text = font.render('GAME OVER!', True, WHITE)
    elif game_over_reason == "BOMB":
        end_text = font.render('BOOM!', True, WHITE)
    elif elapsed_time >= TIME_LIMIT:
        end_text = font.render('TIME UP!', True, WHITE)

    screen.blit(end_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 30))
    pygame.display.update()
    
    # 3초 대기 후 종료
    keyboard.wait(hotkey='Enter')
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
