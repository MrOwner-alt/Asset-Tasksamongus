import pygame

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Credits")

# Function to display credits
def show_credits():
    running = True
    font = pygame.font.SysFont("Arial", 30)
    credit_lines = [
        "Version 1.0.3",
        "Patch Notes:",
        "- File search improved for better efficiency.",
        "- Added randomized file selection when duplicates are found.",
        "- Improved error handling and user feedback.",
        "- Streamlined the credits display process.",
        "- Added blood effect when killed.",
        "- Added confetti effect for wins.",
        "- Added task interaction prompts.",
        "- Improved task completion logic.",
        "InnovaDev Community Discord",
        "Thanks for playing Tasks Among Us!",
    ]

    # Prepare the credit surface
    credit_surface = []
    for line in credit_lines:
        text_surface = font.render(line, True, WHITE)
        credit_surface.append(text_surface)

    scroll_speed = 1  # Speed of scrolling
    scroll_offset = SCREEN_HEIGHT  # Start scrolling from the bottom

    while running:
        screen.fill(BLACK)

        # Display credits with scrolling effect
        for i, text_surface in enumerate(credit_surface):
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, scroll_offset + i * 40))

        scroll_offset -= scroll_speed  # Move up the credits

        # Reset scroll offset when all credits have scrolled out of view
        if scroll_offset + len(credit_surface) * 40 < 0:
            scroll_offset = SCREEN_HEIGHT

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

# Run the credits screen
show_credits()
