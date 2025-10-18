import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Bouncing Circle")

    # Set up colors
    white = (255, 255, 255)
    blue = (0, 0, 255)
    black = (0, 0, 0)

    # Circle properties
    circle_x, circle_y = 200, 200  # Initial position
    circle_radius = 50
    circle_speed_x, circle_speed_y = 3, 3  # Speed in x and y directions

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update circle position
        circle_x += circle_speed_x
        circle_y += circle_speed_y

        # Bounce off the edges
        if circle_x - circle_radius <= 0 or circle_x + circle_radius >= 400:
            circle_speed_x = -circle_speed_x
        if circle_y - circle_radius <= 0 or circle_y + circle_radius >= 400:
            circle_speed_y = -circle_speed_y

        # Fill the screen with white
        screen.fill(white)

        # Draw the circle
        pygame.draw.circle(screen, blue, (circle_x, circle_y), circle_radius)
        pygame.draw.circle(screen, black, (circle_x, circle_y), circle_radius, 2)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()