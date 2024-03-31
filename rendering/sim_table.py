import pygame
from config import GUI_CONFIG
from config import SIM_CONFIG
from config import COLORS

class Sim_Table():
    def __init__(self):
        self.tableFont = pygame.font.SysFont('arial.ttf', 18)
        self.buttonFont = pygame.font.SysFont('arial.ttf', 22, bold = pygame.font.Font.bold)
        self.tableSurface  = pygame.Surface((GUI_CONFIG.TABLE_SIZE[0], GUI_CONFIG.TABLE_SIZE[1]))
        pygame.draw.rect(self.tableSurface, COLORS.BLACK, (GUI_CONFIG.TABLE_ORIGIN[0], GUI_CONFIG.TABLE_ORIGIN[1], 100, 100))

    def update_table(self):
        self.drawTable()
        self.drawButtons()

    def drawTable(self):
        self.tableSurface.fill(GUI_CONFIG.TABLE_BASE_COLOR)
        for i in range(len(GUI_CONFIG.TABLE)):
            num_entries = len(GUI_CONFIG.TABLE[i])
            col_width = GUI_CONFIG.TABLE_SIZE[0] / num_entries
            for j in range(num_entries):
                pygame.draw.rect(self.tableSurface, COLORS.BLACK, ((j*col_width), (i*GUI_CONFIG.ROW_HEIGHT), col_width, GUI_CONFIG.ROW_HEIGHT), width = 1)
                img = self.tableFont.render(str(GUI_CONFIG.TABLE[i][j]), True, COLORS.BLACK)
                self.tableSurface.blit(img, ((j*col_width) + 5, (i*GUI_CONFIG.ROW_HEIGHT) + 5))

    def drawButtons(self):
        if(SIM_CONFIG.PAUSE_SIMULATION == 0):
            color = COLORS.TRUE_RED
            text = "PAUSE"
        else:
            color = COLORS.GREEN_2
            text = "PLAY"
        pygame.draw.rect(self.tableSurface, color, (GUI_CONFIG.PAUSE_BUTTON_LOC[0] , GUI_CONFIG.PAUSE_BUTTON_LOC[1], GUI_CONFIG.PAUSE_BUTTON_SIZE[0], GUI_CONFIG.PAUSE_BUTTON_SIZE[1]))
        img = self.tableFont.render(text, True, COLORS.BLACK)
        self.tableSurface.blit(img, (GUI_CONFIG.PAUSE_BUTTON_LOC[0] + 10, GUI_CONFIG.PAUSE_BUTTON_LOC[1] + 5)) 