import pygame
pygame.init()
win= pygame.display.set_mode((600,500))
win.fill((200,200,200))
class button():
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
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

def redrawWindow():
    win.fill((200,200,200))
    easy.draw(win, (0,0,0))
    medium.draw(win,(0,0,0))
    hard.draw(win,(0,0,0))
    quitter.draw(win,(0,0,0))
    title.draw(win,(100,100,100))

run= True
easy= button((0,255,0),0,225,200,100,'Easy')
medium= button((255,162,0),200,225,200,100,'Medium')
hard= button((255,0,0),400,225,200,100,'Hard')
quitter= button((0,0,255),200,350,200,100,'Quit')
title=button((200,200,200),0,0,600,225,'Sudoku')

while run:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos=pygame.mouse.get_pos()

        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if easy.isOver(pos):
                print('Starting easy mode')
            if quitter.isOver(pos):
                run=False
                pygame.quit()
                quit()
            if medium.isOver(pos):
                print('Starting medium mode')
            if hard.isOver(pos):
                print('Starting hard mode')

        if event.type== pygame.MOUSEMOTION:
            if easy.isOver(pos):
                easy.color=(255,255,0)
            else:
                easy.color=(0,255,0)
            if medium.isOver(pos):
                medium.color = (255, 255, 0)
            else:
                medium.color = (255, 162, 0)
            if hard.isOver(pos):
                hard.color=(255,255,0)
            else:
                hard.color=(255,0,0)
            if quitter.isOver(pos):
                quitter.color=(255,255,0)
            else:
                quitter.color=(0,0,255)
