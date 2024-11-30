from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# 각각의 게임을 실행하는 함수
def run_snake_game():
    # Snake 게임 코드 또는 실행 명령
    print("Snake game started")
    # 실제로 게임을 실행할 코드를 여기에 추가

def run_tictactoe_game():
    # Tic-Tac-Toe 게임 코드 또는 실행 명령
    print("Tic-Tac-Toe game started")
    # 실제로 게임을 실행할 코드를 여기에 추가

def run_brick_game():
    # Brick 게임 실행 함수
    import pygame

    # Pygame 초기화
    pygame.init()
    screen_width = 960
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Brick Game")
    running = True
    clock = pygame.time.Clock()

    # 게임 루프
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Flask 엔드포인트에서 게임 실행
@app.route('/start-game', methods=['POST'])
def start_game():
    game = request.json.get('game')  # 클라이언트에서 요청한 게임 이름
    if not game:
        return jsonify({"error": "Game not specified"}), 400

    # 게임 실행 스레드 생성
    game_thread = None
    if game == "snake":
        game_thread = threading.Thread(target=run_snake_game)
    elif game == "tictactoe":
        game_thread = threading.Thread(target=run_tictactoe_game)
    elif game == "brick":
        game_thread = threading.Thread(target=run_brick_game)
    else:
        return jsonify({"error": "Unknown game"}), 400

    # 게임 실행
    game_thread.start()
    return jsonify({"status": f"{game.capitalize()} game started!"})

if __name__ == '__main__':
    app.run(debug=True)
