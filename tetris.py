import pygame
import random
import copy

# 게임 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE // 2
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# 색깔 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
COLORS = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 0, 255),  
    (0, 255, 255)   
]

# 모양 설정
SHAPES = [
    [[1, 1, 1, 1]],  # I 블록
    [[1, 1], [1, 1]],  # 사각형 블록
    [[1, 1, 1], [0, 1, 0]],  # T 블록
    [[1, 1, 1], [1, 0, 0]],  # L 블록
    [[1, 1, 1], [0, 0, 1]]   # 역 L 블록
]

class TetrisGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.lines_cleared = 0
        self.fall_counter = 0
        self.fall_threshold = 30
        self.score = 0

    def get_new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return shape, color

    def is_valid_move(self, piece, x, y):
        shape, _ = piece
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = x + col_idx
                    grid_y = y + row_idx
                    if (grid_x < 0 or grid_x >= GRID_WIDTH or 
                        grid_y >= GRID_HEIGHT or 
                        (grid_y >= 0 and self.grid[grid_y][grid_x])):
                        return False
        return True

    def lock_piece(self):
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_x + x
                    grid_y = self.piece_y + y
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = color

        # 완성된 라인 제거
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                self.lines_cleared += 1
                self.score += 100
            else:
                y -= 1

    def rotate_piece(self):
        shape, color = self.current_piece
        rotated_shape = list(zip(*shape[::-1]))
        
        if self.is_valid_move((rotated_shape, color), self.piece_x, self.piece_y):
            self.current_piece = (rotated_shape, color)

    def fall_piece(self):
        self.fall_counter += 1
        if self.fall_counter >= self.fall_threshold:
            if self.is_valid_move(self.current_piece, self.piece_x, self.piece_y + 1):
                self.piece_y += 1
            else:
                self.lock_piece()
                self.current_piece = self.get_new_piece()
                self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
                self.piece_y = 0
            self.fall_counter = 0

class MultiplayerTetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('2P 테트리스')
        self.clock = pygame.time.Clock()
        
        self.player1 = TetrisGame()
        self.player2 = TetrisGame()
        
        self.game_over = False

    def draw_grid(self, player_grid, x_offset):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x_offset + x*BLOCK_SIZE, y*BLOCK_SIZE, 
                                   BLOCK_SIZE-1, BLOCK_SIZE-1)
                if player_grid.grid[y][x]:
                    pygame.draw.rect(self.screen, player_grid.grid[y][x], rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_current_piece(self, player_grid, x_offset):
        shape, color = player_grid.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(x_offset + (player_grid.piece_x + x) * BLOCK_SIZE, 
                                       (player_grid.piece_y + y) * BLOCK_SIZE, 
                                       BLOCK_SIZE-1, BLOCK_SIZE-1)
                    pygame.draw.rect(self.screen, color, rect)

    def draw_separator(self):
        pygame.draw.line(self.screen, DARK_GRAY, 
                         (SCREEN_WIDTH // 2, 0), 
                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    # 플레이어 1 컨트롤 (WASD)
                    if event.key == pygame.K_a:
                        if self.player1.is_valid_move(self.player1.current_piece, 
                                                      self.player1.piece_x - 1, 
                                                      self.player1.piece_y):
                            self.player1.piece_x -= 1
                    elif event.key == pygame.K_d:
                        if self.player1.is_valid_move(self.player1.current_piece, 
                                                      self.player1.piece_x + 1, 
                                                      self.player1.piece_y):
                            self.player1.piece_x += 1
                    elif event.key == pygame.K_s:
                        if self.player1.is_valid_move(self.player1.current_piece, 
                                                      self.player1.piece_x, 
                                                      self.player1.piece_y + 1):
                            self.player1.piece_y += 1
                    elif event.key == pygame.K_w:
                        self.player1.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while self.player1.is_valid_move(self.player1.current_piece, 
                                                         self.player1.piece_x, 
                                                         self.player1.piece_y + 1):
                            self.player1.piece_y += 1
                        self.player1.lock_piece()
                        self.player1.current_piece = self.player1.get_new_piece()
                        self.player1.piece_x = GRID_WIDTH // 2 - len(self.player1.current_piece[0]) // 2
                        self.player1.piece_y = 0

                    # 플레이어 2 컨트롤 (방향키)
                    elif event.key == pygame.K_LEFT:
                        if self.player2.is_valid_move(self.player2.current_piece, 
                                                      self.player2.piece_x - 1, 
                                                      self.player2.piece_y):
                            self.player2.piece_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.player2.is_valid_move(self.player2.current_piece, 
                                                      self.player2.piece_x + 1, 
                                                      self.player2.piece_y):
                            self.player2.piece_x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.player2.is_valid_move(self.player2.current_piece, 
                                                      self.player2.piece_x, 
                                                      self.player2.piece_y + 1):
                            self.player2.piece_y += 1
                    elif event.key == pygame.K_UP:
                        self.player2.rotate_piece()
                    elif event.key == pygame.K_KP0:  # 숫자패드 0
                        while self.player2.is_valid_move(self.player2.current_piece, 
                                                         self.player2.piece_x, 
                                                         self.player2.piece_y + 1):
                            self.player2.piece_y += 1
                        self.player2.lock_piece()
                        self.player2.current_piece = self.player2.get_new_piece()
                        self.player2.piece_x = GRID_WIDTH // 2 - len(self.player2.current_piece[0]) // 2
                        self.player2.piece_y = 0

            # 블록 자동 하강
            self.player1.fall_piece()
            self.player2.fall_piece()

            # 승리 조건 확인
            if self.player1.lines_cleared >= 30:
                self.game_over = True
                winner = "플레이어 1"
            elif self.player2.lines_cleared >= 30:
                self.game_over = True
                winner = "플레이어 2"

            # 화면 그리기
            self.screen.fill(BLACK)
            
            self.draw_separator()
            
            self.draw_grid(self.player1, 0)
            self.draw_current_piece(self.player1, 0)
            
            self.draw_grid(self.player2, SCREEN_WIDTH // 2)
            self.draw_current_piece(self.player2, SCREEN_WIDTH // 2)
            
            # 점수 및 라인 표시
            font = pygame.font.Font(None, 36)
            p1_lines = font.render(f'P1 Lines: {self.player1.lines_cleared}', True, WHITE)
            p2_lines = font.render(f'P2 Lines: {self.player2.lines_cleared}', True, WHITE)
            
            self.screen.blit(p1_lines, (10, 10))
            self.screen.blit(p2_lines, (SCREEN_WIDTH // 2 + 10, 10))

            pygame.display.flip()
            self.clock.tick(60)

            # 게임 오버 처리
            if self.game_over:
                font = pygame.font.Font(None, 74)
                text = font.render(f'{winner} 승리!', True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  
                return

def main():
    game = MultiplayerTetris()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()