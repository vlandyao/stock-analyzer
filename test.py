import pygame
import random
import sys
import time

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")
pygame.mouse.set_visible(False)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

    def check_collision(self):
        head_x, head_y = self.body[0]
        
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        
        if (head_x, head_y) in self.body[1:]:
            return True
        
        return False

    def draw(self):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)

    def draw(self):
        x, y = self.position
        pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.default_move_interval = 0.5
        self.move_interval = 0.5
        self.last_move_time = time.time()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.snake.direction == (0, -1):
                        self.move_interval = self.default_move_interval / 2
                    elif self.snake.direction != (0, 1):
                        self.snake.next_direction = (0, -1)
                        self.move_interval = self.default_move_interval
                elif event.key == pygame.K_DOWN:
                    if self.snake.direction == (0, 1):
                        self.move_interval = self.default_move_interval / 2
                    elif self.snake.direction != (0, -1):
                        self.snake.next_direction = (0, 1)
                        self.move_interval = self.default_move_interval
                elif event.key == pygame.K_LEFT:
                    if self.snake.direction == (-1, 0):
                        self.move_interval = self.default_move_interval / 2
                    elif self.snake.direction != (1, 0):
                        self.snake.next_direction = (-1, 0)
                        self.move_interval = self.default_move_interval
                elif event.key == pygame.K_RIGHT:
                    if self.snake.direction == (1, 0):
                        self.move_interval = self.default_move_interval / 2
                    elif self.snake.direction != (-1, 0):
                        self.snake.next_direction = (1, 0)
                        self.move_interval = self.default_move_interval
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()

    def update(self):
        if not self.game_over:
            current_time = time.time()
            if current_time - self.last_move_time >= self.move_interval:
                self.snake.move()
                self.last_move_time = current_time
                
                if self.snake.check_collision():
                    self.game_over = True
                
                if self.snake.body[0] == self.food.position:
                    self.snake.grow()
                    self.score += 10
                    self.food.position = self.food.generate_position()

    def draw(self):
        screen.fill(BLACK)
        
        self.snake.draw()
        self.food.draw()
        
        font_path = "C:/Windows/Fonts/msyh.ttc"
        try:
            font = pygame.font.Font(font_path, 36)
        except:
            font = pygame.font.SysFont("microsoftyahei", 36)
        
        score_text = font.render(f"得分: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = font.render("游戏结束! 按R键重新开始", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.time.wait(10)

if __name__ == "__main__":
    game = Game()
    game.run()
