import pygame
pygame.init()

# Define Colors
LIGHT_BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
DARK_BLUE = (20, 52, 100)
BLUE = (42, 121, 254)
AQUA = (0, 236, 240)

window = pygame.display.set_mode((600, 500))
win_width, win_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Sudoku")
window.fill(WHITE)
background = pygame.Surface(window.get_size())


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (int(self.x + (self.width / 2 - text.get_width() / 2)), int(self.y + (self.height / 2 - text.get_height() / 2))))

    def is_over(self, position):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False


def draw_title(title, size, color):
    title_font = pygame.font.SysFont("Courier", size, bold=True)
    text_title, text_rect = text_object(title_font, title, color)
    return text_title, text_rect


def text_object(font, text, color):
    text_surface = font.render(text, 1, color)
    return text_surface, text_surface.get_rect()


def redraw_start_window():
    """ Draws main starting menu window """
    # Create title text
    text_title, text_rect = draw_title("Sudoku", 60, LIGHT_BLUE)

    # Center title rectangle and add to center of display
    text_rect.center = (win_width // 2, win_height // 5)
    window.blit(text_title, text_rect)

    # Draw start menu buttons
    play.draw(window)
    difficulty.draw(window)
    quitter.draw(window)

    pygame.display.update()


def redraw_difficulty_window():
    """ Draws difficulty selector window """
    # Create title text
    text_title, text_rect = draw_title("Select Difficulty", 50, LIGHT_BLUE)

    # Center title rectangle and add to center of display
    text_rect.center = (win_width // 2, win_height // 5)
    window.blit(text_title, text_rect)

    easy.draw(window)
    medium.draw(window)
    hard.draw(window)


def clear_window():
    """ Clear screen"""
    # Get background surface
    background.convert()

    # Make background empty
    background.fill(WHITE)

    # Blit background to window
    window.blit(background, (0, 0))
    pygame.display.update()


# Start menu buttons
play = Button(BLUE, (win_width // 3) - 25, (win_height // 4) + 50, 250, 60, 'Play')
difficulty = Button(AQUA, win_width // 3, (win_height // 4) + 150, 200, 50, "Difficulty")
quitter = Button(AQUA, (win_width // 3), (win_height // 4) + 240, 200, 50, "Quit")

# Difficulty select buttons
easy = Button(BLUE, (win_width // 3), (win_height // 4) + 50, 200, 50, 'Easy')
medium = Button(BLUE, win_width // 3, (win_height // 4) + 150, 200, 50, "Medium")
hard = Button(BLUE, (win_width // 3), (win_height // 4) + 240, 200, 50, "Hard")


def main():
    run = True
    on_start_window = True
    on_difficulty_window = False
    redraw_start_window()

    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEMOTION:
                if on_start_window:
                    if play.is_over(pos):
                        play.color = DARK_BLUE
                    else:
                        play.color = BLUE
                    if difficulty.is_over(pos):
                        difficulty.color = DARK_BLUE
                    else:
                        difficulty.color = AQUA
                    if quitter.is_over(pos):
                        quitter.color = DARK_BLUE
                    else:
                        quitter.color = AQUA
                if on_difficulty_window:
                    if easy.is_over(pos):
                        easy.color = DARK_BLUE
                    else:
                        easy.color = BLUE
                    if medium.is_over(pos):
                        medium.color = DARK_BLUE
                    else:
                        medium.color = BLUE
                    if hard.is_over(pos):
                        hard.color = DARK_BLUE
                    else:
                        hard.color = BLUE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if on_start_window:
                    if play.is_over(pos):
                        print('Starting game')
                    if difficulty.is_over(pos):
                        print('Select difficulty')

                        # Clear window
                        clear_window()

                        on_start_window = False
                        on_difficulty_window = True

                        # Draw new screen (difficulty selector menu)
                        redraw_difficulty_window()
                        continue
                    if quitter.is_over(pos):
                        print('Quitting game')
                        run = False
                if on_difficulty_window:
                    if easy.is_over(pos):
                        print('Easy difficulty')

                    if medium.is_over(pos):
                        print('Medium difficulty')

                    if hard.is_over(pos):
                        print('Hard difficulty')

                    # Change window flags to go back to start menu
                    on_start_window = True
                    on_difficulty_window = False

                    # Clear window
                    clear_window()

        if on_start_window:
            redraw_start_window()
        if on_difficulty_window:
            redraw_difficulty_window()
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()