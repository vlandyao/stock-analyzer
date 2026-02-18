import pygame
import random
import math
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
BIRD_SIZE = 40
PIPE_WIDTH = 80
PIPE_GAP = 180
PIPE_SPEED = 3
SPAWN_PIPE_INTERVAL = 1500

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("小鸟拍打翅膀 - 躲避障碍物")

# 时钟
clock = pygame.time.Clock()

# 字体
try:
    # 尝试使用微软雅黑
    font_large = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 72)
    font_medium = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
    font_small = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
except:
    try:
        # 尝试使用宋体
        font_large = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 72)
        font_medium = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 48)
        font_small = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 36)
    except:
        # 如果都找不到，使用默认字体
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)

class Bird:
    """小鸟类"""
    
    def __init__(self):
        self.x = 150
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.wing_angle = 0
        self.wing_direction = 1
        self.alive = True
        self.score = 0
    
    def update(self, mouse_pos):
        """更新小鸟位置和翅膀动画"""
        if not self.alive:
            return
        
        if mouse_pos:
            mouse_y = mouse_pos[1]
            if mouse_y < self.y - 20:
                self.velocity = -6
            elif mouse_y > self.y + 20:
                self.velocity = 4
            else:
                self.velocity *= 0.9
        
        self.velocity += GRAVITY
        self.y += self.velocity
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > SCREEN_HEIGHT - BIRD_SIZE:
            self.y = SCREEN_HEIGHT - BIRD_SIZE
            self.velocity = 0
            self.alive = False
        
        self.wing_angle += self.wing_direction * 0.2
        if self.wing_angle > 0.5 or self.wing_angle < -0.5:
            self.wing_direction *= -1
    
    def draw(self):
        """绘制小鸟"""
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), BIRD_SIZE // 2)
        
        eye_x = self.x + 10
        eye_y = self.y - 5
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 8)
        pygame.draw.circle(screen, BLACK, (eye_x + 2, eye_y), 4)
        
        beak_x = self.x + BIRD_SIZE // 2
        beak_y = self.y
        pygame.draw.polygon(screen, ORANGE, [
            (beak_x, beak_y),
            (beak_x + 20, beak_y - 5),
            (beak_x + 20, beak_y + 5)
        ])
        
        wing_offset_y = int(math.sin(self.wing_angle) * 10)
        wing_x = self.x - 15
        wing_y = self.y + wing_offset_y
        
        pygame.draw.ellipse(screen, ORANGE, (wing_x - 15, wing_y - 8, 25, 16))
        
        tail_x = self.x - BIRD_SIZE // 2
        tail_y = self.y
        pygame.draw.polygon(screen, BROWN, [
            (tail_x, tail_y - 5),
            (tail_x - 15, tail_y - 10),
            (tail_x - 15, tail_y + 10),
            (tail_x, tail_y + 5)
        ])
    
    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x - BIRD_SIZE // 2, self.y - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)

class Pipe:
    """障碍物管道类"""
    
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
        self.passed = False
    
    def update(self):
        """更新管道位置"""
        self.x -= PIPE_SPEED
    
    def draw(self):
        """绘制管道"""
        top_pipe_height = self.gap_y
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, top_pipe_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, top_pipe_height - 30, PIPE_WIDTH + 10, 30))
        
        bottom_pipe_y = self.gap_y + PIPE_GAP
        bottom_pipe_height = SCREEN_HEIGHT - bottom_pipe_y
        pygame.draw.rect(screen, GREEN, (self.x, bottom_pipe_y, PIPE_WIDTH, bottom_pipe_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, bottom_pipe_y, PIPE_WIDTH + 10, 30))
    
    def get_top_rect(self):
        """获取上管道碰撞矩形"""
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
    
    def get_bottom_rect(self):
        """获取下管道碰撞矩形"""
        return pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.gap_y - PIPE_GAP)
    
    def is_off_screen(self):
        """判断管道是否超出屏幕"""
        return self.x + PIPE_WIDTH < 0

class Game:
    """游戏主类"""
    
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.last_pipe_spawn = 0
        self.game_state = "menu"
        self.high_score = self.load_high_score()
    
    def load_high_score(self):
        """加载最高分"""
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        """保存最高分"""
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))
    
    def reset(self):
        """重置游戏"""
        self.bird = Bird()
        self.pipes = []
        self.last_pipe_spawn = 0
        self.game_state = "playing"
    
    def spawn_pipe(self):
        """生成新管道"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_spawn > SPAWN_PIPE_INTERVAL:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.last_pipe_spawn = current_time
    
    def check_collisions(self):
        """检测碰撞"""
        bird_rect = self.bird.get_rect()
        
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                self.bird.alive = False
                return True
        
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.bird.score += 1
        
        return False
    
    def update(self, mouse_pos):
        """更新游戏状态"""
        if self.game_state == "playing":
            self.bird.update(mouse_pos)
            self.spawn_pipe()
            
            for pipe in self.pipes:
                pipe.update()
            
            self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
            
            if self.check_collisions() or not self.bird.alive:
                self.game_state = "gameover"
                if self.bird.score > self.high_score:
                    self.high_score = self.bird.score
                    self.save_high_score()
    
    def draw_background(self):
        """绘制背景"""
        for y in range(SCREEN_HEIGHT):
            color = (135, 206 - y // 4, 235 - y // 6)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
        
        ground_height = 50
        pygame.draw.rect(screen, (34, 139, 34), (0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height))
        
        for x in range(0, SCREEN_WIDTH, 10):
            grass_height = random.randint(5, 15)
            pygame.draw.rect(screen, (50, 205, 50), (x, SCREEN_HEIGHT - ground_height - grass_height, 3, grass_height))
    
    def draw(self):
        """绘制游戏"""
        self.draw_background()
        
        for pipe in self.pipes:
            pipe.draw()
        
        self.bird.draw()
        
        if self.game_state == "playing":
            score_text = font_large.render(str(self.bird.score), True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(score_text, score_rect)
        
        if self.game_state == "menu":
            self.draw_menu()
        
        if self.game_state == "gameover":
            self.draw_gameover()
    
    def draw_menu(self):
        """绘制菜单界面"""
        title_text = font_large.render("小鸟拍打翅膀", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        instruction_text1 = font_medium.render("鼠标上下移动控制小鸟", True, WHITE)
        instruction_rect1 = instruction_text1.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(instruction_text1, instruction_rect1)
        
        instruction_text2 = font_medium.render("躲避障碍物！", True, WHITE)
        instruction_rect2 = instruction_text2.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(instruction_text2, instruction_rect2)
        
        if self.high_score > 0:
            high_score_text = font_small.render(f"最高分: {self.high_score}", True, ORANGE)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
            screen.blit(high_score_text, high_score_rect)
        
        start_text = font_medium.render("点击任意位置开始游戏", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(start_text, start_rect)
    
    def draw_gameover(self):
        """绘制游戏结束界面"""
        gameover_text = font_large.render("游戏结束!", True, RED)
        gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(gameover_text, gameover_rect)
        
        score_text = font_medium.render(f"得分: {self.bird.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(score_text, score_rect)
        
        high_score_text = font_medium.render(f"最高分: {self.high_score}", True, ORANGE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(high_score_text, high_score_rect)
        
        restart_text = font_medium.render("点击任意位置重新开始", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        screen.blit(restart_text, restart_rect)
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "menu" or self.game_state == "gameover":
                    self.reset()
        
        return True

def main():
    """主游戏函数"""
    game = Game()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        running = game.handle_events()
        game.update(mouse_pos)
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
