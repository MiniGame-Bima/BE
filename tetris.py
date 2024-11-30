import pygame
import random
import sys
import math

#폭탄같은거 날라와서 한번에 아웃되는 거 추가해보기




# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("장애물 피하기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.missiles = []
        self.missile_count = 5
        self.hits = 0
    
    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH // 2:  # 화면 중앙까지만 이동 가능
            self.x += self.speed
    
    def shoot(self):
        if self.missile_count > 0:
            self.missiles.append(Missile(self.x + self.width, self.y + self.height//2))
            self.missile_count -= 1
    
    def draw(self, screen):
        # 전투기 본체
        pygame.draw.polygon(screen, BLUE, [
            (self.x, self.y + self.height//2),  # 기수
            (self.x + self.width, self.y),      # 상단
            (self.x + self.width - 10, self.y + self.height//2),  # 후미
            (self.x + self.width, self.y + self.height)  # 하단
        ])
        
        # 날개
        pygame.draw.polygon(screen, GRAY, [
            (self.x + self.width//3, self.y + self.height//2),
            (self.x + self.width//2, self.y - 10),
            (self.x + self.width//1.5, self.y + self.height//2)
        ])
        pygame.draw.polygon(screen, GRAY, [
            (self.x + self.width//3, self.y + self.height//2),
            (self.x + self.width//2, self.y + self.height + 10),
            (self.x + self.width//1.5, self.y + self.height//2)
        ])
        
        # 조종석
        pygame.draw.ellipse(screen, YELLOW, 
                          (self.x + self.width//3, self.y + self.height//3,
                           self.width//4, self.height//3))

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.width = 15
        self.height = 4
    
    def move(self):
        self.x += self.speed
    
    def draw(self, screen):
        # 미사일 본체
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # 미사일 꼬리
        pygame.draw.polygon(screen, YELLOW, [
            (self.x, self.y),
            (self.x - 5, self.y + self.height//2),
            (self.x, self.y + self.height)
        ])

class Obstacle:
    def __init__(self, round_num):
        self.width = 40
        self.height = 40
        self.x = SCREEN_WIDTH
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.base_speed = 10  # 기본 속도를 10으로 증가
        self.speed = self.base_speed * (1 + round_num * 0.1)
        self.type = random.choice(['plane', 'bird', 'fighter'])
        self.angle = random.randint(-20, 20)
    
    def move(self):
        self.x -= self.speed
        self.y += math.sin(self.x / 30) * 2  # 사인파 움직임 추가
    
    def draw(self, screen):
        if self.type == 'plane':
            self.draw_enemy_plane(screen)
        elif self.type == 'bird':
            self.draw_bird(screen)
        else:
            self.draw_enemy_fighter(screen)
    
    def draw_enemy_plane(self, screen):
        # 비행기 본체
        pygame.draw.polygon(screen, RED, [
            (self.x + self.width, self.y + self.height//2),
            (self.x, self.y),
            (self.x, self.y + self.height)
        ])
        # 날개
        pygame.draw.polygon(screen, GRAY, [
            (self.x + self.width//2, self.y),
            (self.x + self.width//2, self.y - 15),
            (self.x + self.width//2 + 20, self.y)
        ])
    
    def draw_bird(self, screen):
        # 새의 몸체
        pygame.draw.ellipse(screen, RED, (self.x, self.y, self.width//2, self.height//2))
        # 날개
        pygame.draw.arc(screen, RED, (self.x - 10, self.y - 10, self.width, self.height//2), 0, math.pi, 2)
        pygame.draw.arc(screen, RED, (self.x - 10, self.y + 10, self.width, self.height//2), math.pi, 2*math.pi, 2)
    
    def draw_enemy_fighter(self, screen):
        # 전투기 본체
        pygame.draw.polygon(screen, RED, [
            (self.x, self.y + self.height//2),
            (self.x + self.width, self.y),
            (self.x + self.width - 10, self.y + self.height//2),
            (self.x + self.width, self.y + self.height)
        ])
        # 날개
        pygame.draw.polygon(screen, GRAY, [
            (self.x + 10, self.y + self.height//2),
            (self.x + 20, self.y - 10),
            (self.x + 30, self.y + self.height//2)
        ])

class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.round = 1
        self.max_round = 5
        self.obstacle_spawn_timer = 0
        self.game_over = False
        self.game_won = False
        self.font = pygame.font.Font(None, 36)
        self.background_stars = [(random.randint(0, SCREEN_WIDTH), 
                                random.randint(0, SCREEN_HEIGHT)) 
                               for _ in range(50)]
        self.obstacles_avoided = 0
    
    def spawn_obstacle(self):
        if self.obstacle_spawn_timer <= 0:
            self.obstacles.append(Obstacle(self.round))
            self.obstacle_spawn_timer = 60  # 약 1초
        self.obstacle_spawn_timer -= 1
    
    def draw_background(self, screen):
        # 우주 배경
        screen.fill(BLACK)
        for star in self.background_stars:
            pygame.draw.circle(screen, WHITE, star, 1)
        
        # 스크롤 효과
        self.background_stars = [(x-1 if x > 0 else SCREEN_WIDTH, y) 
                               for x, y in self.background_stars]
    
    def check_collisions(self):
        # 미사일과 장애물 충돌
        for missile in self.player.missiles[:]:
            for obstacle in self.obstacles[:]:
                if (missile.x < obstacle.x + obstacle.width and
                    missile.x + missile.width > obstacle.x and
                    missile.y < obstacle.y + obstacle.height and
                    missile.y + missile.height > obstacle.y):
                    if missile in self.player.missiles:
                        self.player.missiles.remove(missile)
                    if obstacle in self.obstacles:
                        self.obstacles.remove(obstacle)
        
        # 플레이어와 장애물 충돌
        for obstacle in self.obstacles[:]:
            if (self.player.x < obstacle.x + obstacle.width and
                self.player.x + self.player.width > obstacle.x and
                self.player.y < obstacle.y + obstacle.height and
                self.player.y + self.player.height > obstacle.y):
                if obstacle in self.obstacles:
                    self.obstacles.remove(obstacle)
                    self.player.hits += 1
                    if self.player.hits >= 3:
                        self.round_failed()
    
    def update(self):
        if not self.game_over and not self.game_won:
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            
            # 미사일 업데이트
            for missile in self.player.missiles[:]:
                missile.move()
                if missile.x > SCREEN_WIDTH:
                    self.player.missiles.remove(missile)
            
            # 장애물 업데이트
            self.spawn_obstacle()
            for obstacle in self.obstacles[:]:
                obstacle.move()
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)
                    self.obstacles_avoided += 1
                    
                    # 20개의 장애물을 피하면 라운드 클리어
                    if self.obstacles_avoided >= 20:
                        self.round_complete()
                        self.obstacles_avoided = 0  # 카운터 리셋
            
            self.check_collisions()

    def round_failed(self):
        if self.round > 1:
            self.round -= 1
        else:
            self.game_over = True  # 1라운드에서 실패하면 게임 오버
        self.reset_round()
    
    def round_complete(self):
        if self.round < self.max_round:
            self.round += 1
            self.reset_round()
        else:
            self.game_won = True  # 모든 라운드 클리어시 게임 승리
    
    def reset_round(self):
        self.player.hits = 0
        self.player.missile_count = 5
        self.obstacles.clear()
        self.player.missiles.clear()
        self.player.y = SCREEN_HEIGHT // 2
        self.player.x = 50
        self.obstacles_avoided = 0
    
    def draw(self, screen):
        self.draw_background(screen)
        
        # 게임 요소 그리기
        self.player.draw(screen)
        for missile in self.player.missiles:
            missile.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        # UI 정보 표시
        round_text = self.font.render(f'Round: {self.round}', True, WHITE)
        hits_text = self.font.render(f'Hits: {self.player.hits}/3', True, WHITE)
        missiles_text = self.font.render(f'Missiles: {self.player.missile_count}', True, WHITE)
        obstacles_text = self.font.render(f'Obstacles Avoided: {self.obstacles_avoided}/20', True, WHITE)
        
        screen.blit(round_text, (10, 10))
        screen.blit(hits_text, (10, 40))
        screen.blit(missiles_text, (10, 70))
        screen.blit(obstacles_text, (10, 100))
        
        # 게임 오버 또는 승리 메시지
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            # 검은색 반투명 배경
            s = pygame.Surface((300, 100))
            s.set_alpha(128)
            s.fill(BLACK)
            screen.blit(s, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
            
            screen.blit(game_over_text, game_over_rect)
            
            # 재시작 안내
            restart_text = self.font.render('Press R to Restart', True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            screen.blit(restart_text, restart_rect)
        
        elif self.game_won:
            victory_text = self.font.render('VICTORY!', True, YELLOW)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            # 검은색 반투명 배경
            s = pygame.Surface((300, 100))
            s.set_alpha(128)
            s.fill(BLACK)
            screen.blit(s, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
            
            screen.blit(victory_text, victory_rect)
            
            # 재시작 안내
            restart_text = self.font.render('Press R to Restart', True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.player.shoot()
                elif event.key == pygame.K_r and (game.game_over or game.game_won):
                    # R키를 눌러 게임 재시작
                    game = Game()
        
        game.update()
        game.draw(screen)
        clock.tick(60)

if __name__ == '__main__':
    main()



# 설치파일로 만들기는 pyinstaller snake_games2.py  cmd창 안들어갈려면 pyinstaller --noconsole snake_games2.py