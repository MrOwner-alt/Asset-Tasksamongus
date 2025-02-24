import pygame
import random
import time
import math
import os
import subprocess
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PLAYER_SPEED = 5
TASK_RADIUS = 30

# Task Completion Variables
TASKS_COMPLETED = 0
TASKS_TOTAL = 3
TASK_DURATION = 3  # seconds
task_in_progress = False
task_start_time = None

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tasks Among Us")

# Generate stars for the background
STARS = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(200)]

# Function to search for a file across all drives and directories
def find_file_quickly(filename):
    search_paths = [os.getcwd()] + [f"{chr(d)}:/" for d in range(65, 91) if os.path.exists(f"{chr(d)}:/")]
    for path in search_paths:
        for root, _, files in os.walk(path):
            if filename in files:
                return os.path.join(root, filename)
    return None

# Function to launch a file
def launch_file(filename):
    file_path = find_file_quickly(filename)
    if file_path:
        print(f"Launching: {file_path}")
        subprocess.run([file_path], shell=True)
    else:
        print(f"File {filename} not found in any directory!")

# Load and play the sound only once
sound_file_path = find_file_quickly("Voicy_Among Us defeat (imposter win).mp3")

if sound_file_path:
    try:
        print(f"Sound file found: {sound_file_path}")  # Debug: Print file path
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load(sound_file_path)
        pygame.mixer.music.play(loops=-1, start=0.0)  # Loop indefinitely in the menu
    except pygame.error as e:
        print(f"Error loading or playing the sound: {e}")
else:
    print("Sound file not found!")

# Button class
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, is_hovered):
        pygame.draw.rect(screen, WHITE, self.rect, 3)  # Original button design
        if is_hovered:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 3)  # Yellow edge for hover
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(
            text_surface,
            (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2),
        )

    def is_pressed(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

# Draw rotating 3D cube
def draw_rotating_cube(angle_x, angle_y):
    cube_size = 100
    cube_color = GREEN

    # Draw the text "Tasks Among Us" at the top of the screen
    font = pygame.font.SysFont("Arial", 40)
    text_surface = font.render("Tasks Among Us", True, WHITE)
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 20))

    vertices = [
        (-cube_size, -cube_size, -cube_size),
        (cube_size, -cube_size, -cube_size),
        (cube_size, cube_size, -cube_size),
        (-cube_size, cube_size, -cube_size),
        (-cube_size, -cube_size, cube_size),
        (cube_size, -cube_size, cube_size),
        (cube_size, cube_size, cube_size),
        (-cube_size, cube_size, cube_size),
    ]

    # Rotate the cube around x-axis and y-axis
    rotated_vertices = []
    for x, y, z in vertices:
        # Rotation around X-axis
        y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
        # Rotation around Y-axis
        x, z = x * math.cos(angle_y) + z * math.sin(angle_y), -x * math.sin(angle_y) + z * math.cos(angle_y)
        rotated_vertices.append((x, y, z))

    # Project the 3D vertices to 2D
    screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    scale = 300
    projected_points = []
    for x, y, z in rotated_vertices:
        factor = scale / (z + 400)
        x_proj = screen_center[0] + int(x * factor)
        y_proj = screen_center[1] + int(y * factor)
        projected_points.append((x_proj, y_proj))

    # Define the cube edges
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    # Draw edges
    for edge in edges:
        pygame.draw.line(screen, cube_color, projected_points[edge[0]], projected_points[edge[1]], 2)

# Main menu
def main_menu():
    angle_x, angle_y = 0, 0
    menu_running = True

    # Centering buttons directly in the middle of the screen
    button_width = 300
    button_height = 50
    button_y_offset = 60  # Vertical space between buttons

    # Create buttons with centered positions
    single_player_button = Button("Single Player", (SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2 - 1.5 * button_y_offset, button_width, button_height)
    multi_player_button = Button("Multiplayer", (SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2 - 0.5 * button_y_offset, button_width, button_height)
    addons_button = Button("Add-ons", (SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2 + 0.5 * button_y_offset, button_width, button_height)
    credits_button = Button("Credits", (SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2 + 1.5 * button_y_offset, button_width, button_height)

    while menu_running:
        screen.fill(BLACK)

        # Draw stars
        for star in STARS:
            pygame.draw.circle(screen, WHITE, star, random.randint(1, 3))

        # Draw rotating cube
        draw_rotating_cube(angle_x, angle_y)
        angle_x += 0.01
        angle_y += 0.01

        # Check if buttons are hovered and draw them
        single_player_hovered = single_player_button.is_hovered()
        multi_player_hovered = multi_player_button.is_hovered()
        addons_hovered = addons_button.is_hovered()
        credits_hovered = credits_button.is_hovered()

        single_player_button.draw(single_player_hovered)
        multi_player_button.draw(multi_player_hovered)
        addons_button.draw(addons_hovered)
        credits_button.draw(credits_hovered)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if single_player_button.is_pressed(event):
                return "single_player"
            if multi_player_button.is_pressed(event):
                return "multiplayer"
            if addons_button.is_pressed(event):
                open_addons_page()
            if credits_button.is_pressed(event):
                start_credits()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Function to open the Add-ons HTML file
def open_addons_page():
    addons_file = find_file_quickly("addones.html")
    if addons_file:
        subprocess.run(["start", addons_file], shell=True)
    else:
        print("Add-ons page not found!")

# Start the Credits Script
def start_credits():
    launch_file("credits.py")

# Main loop
def game_loop():
    # Your game loop for single player
    print("Single Player Mode")
    launch_file("single_player.py")

def start_multiplayer():
    # Your game loop for multiplayer
    print("Multiplayer Mode")
    launch_file("Tasks among us 1.1.3 multiplayer.py")

while True:
    selected_mode = main_menu()
    if selected_mode == "single_player":
        game_loop()
    elif selected_mode == "multiplayer":
        start_multiplayer()
