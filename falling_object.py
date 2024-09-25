import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Falling Object with Adjustable Speed")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load your image (make sure the image file exists in the same directory or provide the full path)
object_image = pygame.image.load('jumpling.png')  # Replace with your image filename
object_image = pygame.transform.scale(object_image, (150, 150))  # Scale the image to fit nicely

# Get the width and height of the object image
object_width = object_image.get_width()
object_height = object_image.get_height()

# Load the background image (replace with your background image)
background_image = pygame.image.load('cliffs.jpeg')
background_image = pygame.transform.scale(background_image, (width, height))  # Scale to fit the full screen


# Object properties
object_x = width // 2 - object_width // 2  # Center the object horizontally
object_y = 0  # Start from the top

# Initial velocity
velocity = 5
user_input = ""  # Store the user's input for velocity

# Font for text input
font = pygame.font.SysFont(None, 48)
# Font for the label
label_font = pygame.font.SysFont(None, 36)

# Create an input box class
class InputBox:
    def __init__(self, x, y, w, h, label='Velocity:', text='5'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.label = label
        self.label_surface = label_font.render(label, True, self.color)  # Label color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = RED if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        # Draw the label text above the input box
        screen.blit(self.label_surface, (self.rect.x, self.rect.y - 40))
        # Fill the input box with white color
        pygame.draw.rect(screen, WHITE, self.rect)
        # Draw the text on top of the white fill
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the outline of the input box
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create an input box instance and move it to the right side of the screen
input_box_width = 140  # Input box width
input_box_x = width - input_box_width - 50  # Adjusting to place it on the right side with some padding
input_box = InputBox(input_box_x, 50, input_box_width, 48)  # Positioned on the right side

# Main game loop
running = True
while running:
    # Draw the full background image
    screen.blit(background_image, (0, 0))
    
# Draw the falling object (image)
    screen.blit(object_image, (object_x, object_y))

    # Update object position based on velocity
    object_y += velocity  
    
    # Reset object to the top when it reaches the bottom of the screen
    if object_y > height:
        object_y = 0 - object_height  # Reset the object to just above the top of the screen

    # Draw and handle input box
    input_box.draw(screen)
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle input box events
        result = input_box.handle_event(event)
        if result:
            try:
                # Try to set the velocity based on user input
                velocity = int(result)
                user_input = ""  # Reset the input text
            except ValueError:
                velocity = 5  # Default to 5 if input is invalid

    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
