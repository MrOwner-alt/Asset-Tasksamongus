import pygame
import random
import time
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PLAYER_SPEED = 5
TASK_RADIUS = 30
TASKS_TOTAL = 3
TASK_DURATION = 3  # seconds

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Single Player Mode")

# Player class
class Player:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.y += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.x += PLAYER_SPEED
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

# Generate tasks
def generate_tasks(n):
    return [(random.randint(TASK_RADIUS, SCREEN_WIDTH - TASK_RADIUS), random.randint(TASK_RADIUS, SCREEN_HEIGHT - TASK_RADIUS)) for _ in range(n)]

# Show popup
def show_popup(message, duration=3):
    start_time = time.time()
    font = pygame.font.SysFont("Arial", 30)
    while time.time() - start_time < duration:
        screen.fill(BLACK)
        popup_text = font.render(message, True, WHITE)
        screen.blit(popup_text, (SCREEN_WIDTH // 2 - popup_text.get_width() // 2, SCREEN_HEIGHT // 2 - popup_text.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.time.Clock().tick(60)

# Main game loop
def game_loop():
    global TASKS_COMPLETED, task_in_progress, task_start_time
    TASKS_COMPLETED = 0
    task_in_progress = False
    task_start_time = None
    clock = pygame.time.Clock()
    player = Player(BLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    tasks = generate_tasks(TASKS_TOTAL)
    running = True

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for task in tasks:
            pygame.draw.circle(screen, GREEN, task, TASK_RADIUS)

        player.move()
        player.draw()

        for task in tasks:
            distance = ((player.x + player.width // 2 - task[0]) ** 2 + (player.y + player.height // 2 - task[1]) ** 2) ** 0.5
            if distance <= TASK_RADIUS:
                font = pygame.font.SysFont("Arial", 20)
                text_surface = font.render("Press E to do the task", True, WHITE)
                screen.blit(text_surface, (task[0] - text_surface.get_width() // 2, task[1] - TASK_RADIUS - 20))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e] and not task_in_progress:
                    task_in_progress = True
                    task_start_time = time.time()

        if task_in_progress:
            elapsed = time.time() - task_start_time
            if elapsed >= TASK_DURATION:
                TASKS_COMPLETED += 1
                task_in_progress = False
                if tasks:
                    tasks.pop(0)

        if TASKS_COMPLETED == TASKS_TOTAL:
            show_popup("All tasks completed!")
            running = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
