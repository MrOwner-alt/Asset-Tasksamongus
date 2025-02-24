import pygame
import random
import time
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLOOD_COLOR = (150, 0, 0)
PLAYER_SPEED = 5
TASK_RADIUS = 30
KILL_RADIUS = 50
TASK_DURATION = 3  # Seconds to complete a task

# Player class
class Player:
    def __init__(self, color, x, y, controls):
        self.color = color
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.controls = controls

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        if keys[self.controls["up"]]:
            self.y -= PLAYER_SPEED
        if keys[self.controls["down"]]:
            self.y += PLAYER_SPEED
        if keys[self.controls["left"]]:
            self.x -= PLAYER_SPEED
        if keys[self.controls["right"]]:
            self.x += PLAYER_SPEED
        # Prevent going out of bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

# Generate tasks
def generate_tasks(n):
    return [(random.randint(TASK_RADIUS, SCREEN_WIDTH - TASK_RADIUS), random.randint(TASK_RADIUS, SCREEN_HEIGHT - TASK_RADIUS)) for _ in range(n)]

# Show popup
def show_popup(screen, message, duration=2):
    start_time = time.time()
    font = pygame.font.SysFont("Arial", 30)

    while time.time() - start_time < duration:
        screen.fill(BLACK)
        text_surface = font.render(message, True, WHITE)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Draw blood effect
def draw_blood(screen, x, y):
    blood_radius = 10
    pygame.draw.circle(screen, BLOOD_COLOR, (x, y), blood_radius)

# Draw confetti effect
def draw_confetti(screen):
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.rect(screen, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (x, y, 5, 5))

# Main game loop
def game_loop():
    pygame.display.set_caption("Crewmate vs Impostor")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create players
    crewmate = Player(BLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, {"up": K_w, "down": K_s, "left": K_a, "right": K_d})
    impostor = Player(RED, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, {"up": K_UP, "down": K_DOWN, "left": K_LEFT, "right": K_RIGHT})

    # Generate tasks
    tasks = generate_tasks(3)
    tasks_completed = 0
    task_in_progress = False
    task_start_time = None

    clock = pygame.time.Clock()
    running = True
    game_over = False
    game_won = False

    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw tasks
        for task in tasks:
            pygame.draw.circle(screen, GREEN, task, TASK_RADIUS)

        # Move and draw players
        crewmate.move(keys)
        impostor.move(keys)
        crewmate.draw(screen)
        impostor.draw(screen)

        # Crewmate task interaction
        if not task_in_progress:
            for task in tasks:
                distance = math.hypot(crewmate.x + crewmate.width // 2 - task[0], crewmate.y + crewmate.height // 2 - task[1])
                if distance <= TASK_RADIUS:
                    font = pygame.font.SysFont("Arial", 20)
                    task_prompt = font.render("Press E to do the task", True, WHITE)
                    screen.blit(task_prompt, (task[0] - task_prompt.get_width() // 2, task[1] - TASK_RADIUS - 20))
                    if keys[K_e]:
                        task_in_progress = True
                        task_start_time = time.time()
                        tasks.remove(task)  # Remove task from the list
                        break

        # Task completion logic
        if task_in_progress:
            elapsed = time.time() - task_start_time
            if elapsed >= TASK_DURATION:
                tasks_completed += 1
                task_in_progress = False

        # Check if all tasks are completed
        if tasks_completed == 3:
            game_won = True
            running = False

        # Impostor kill logic
        distance_to_crewmate = math.hypot(impostor.x + impostor.width // 2 - crewmate.x - crewmate.width // 2,
                                          impostor.y + impostor.height // 2 - crewmate.y - crewmate.height // 2)
        if distance_to_crewmate <= KILL_RADIUS:
            game_over = True
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Game Over / Win Screen
    if game_over:
        for _ in range(50):  # Draw blood effect
            draw_blood(screen, crewmate.x + crewmate.width // 2, crewmate.y + crewmate.height // 2)
        pygame.display.flip()
        show_popup(screen, "Impostor Wins!")

    if game_won:
        draw_confetti(screen)  # Draw confetti effect
        pygame.display.flip()
        show_popup(screen, "Crewmate Wins!")

# Main function
def main():
    game_loop()

if __name__ == "__main__":
    main()
