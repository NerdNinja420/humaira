import pygame

# Initialize pygame
pygame.init()

# Window size
WIN_WIDTH, WIN_HEIGHT = 800, 600
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Create two surfaces with the same initial size
surface1 = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
surface2 = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Resize transformations
scaled_surface1 = pygame.transform.scale(surface1, (WIN_WIDTH // 2, WIN_HEIGHT // 2))
scaled_surface2 = pygame.transform.scale(surface2, (WIN_WIDTH, WIN_HEIGHT))

surface1.get_width()
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    # Fill the transformed surfaces with colors
    scaled_surface1.fill(RED)  # Top-left quarter
    scaled_surface2.fill(BLUE)  # Entire background

    # Draw some elements for visibility
    pygame.draw.circle(scaled_surface1, GREEN, (WIN_WIDTH // 4, WIN_HEIGHT // 4), 40)
    pygame.draw.rect(scaled_surface2, YELLOW, (100, 100, 200, 150))

    # Blit the transformed surfaces
    screen.blit(scaled_surface2, (0, 0))  # Background first
    screen.blit(scaled_surface1, (0, 0))  # Top-left corner

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
