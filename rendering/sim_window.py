import pygame
from config import GUI_CONFIG
from config import COLORS
from rendering import sim_table

class Sim_Window():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GUI_CONFIG.SIM_TITLE)
        self.mainSurface = pygame.display.set_mode(GUI_CONFIG.WINDOW_SIZE)
        self.mainSurface.fill(GUI_CONFIG.MAIN_SURFACE_BASE_COLOR)
        self.gameSurface = pygame.Surface((GUI_CONFIG.GAME_BOARD_SIZE, GUI_CONFIG.GAME_BOARD_SIZE))

        if(GUI_CONFIG.DO_DRAW_TABLE):
            self.table = sim_table.Sim_Table()
            self.mainSurface.blit(self.table.tableSurface, (GUI_CONFIG.TABLE_ORIGIN[0], GUI_CONFIG.TABLE_ORIGIN[1]))
            self.mainSurface.blit(self.gameSurface, (GUI_CONFIG.GAME_BOARD_ORIGIN[0], GUI_CONFIG.GAME_BOARD_ORIGIN[1]))

    def drawGameBoard(self):
        self.gameSurface.fill(GUI_CONFIG.GAME_BASE_COLOR)
        # DRAW Grid Border:
        # TOP lEFT TO RIGHT
        pygame.draw.line(
        self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
        (0, 0),
        (GUI_CONFIG.GAME_BOARD_SIZE, 0), GUI_CONFIG.GRID_LINE_WIDTH)
        # # BOTTOM lEFT TO RIGHT
        pygame.draw.line(
        self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
        (0, GUI_CONFIG.GAME_BOARD_SIZE),
        (GUI_CONFIG.GAME_BOARD_SIZE,
            GUI_CONFIG.GAME_BOARD_SIZE), GUI_CONFIG.GRID_LINE_WIDTH)
        # # LEFT TOP TO BOTTOM
        pygame.draw.line(
        self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
        (0, 0),
        (0, GUI_CONFIG.GAME_BOARD_SIZE), GUI_CONFIG.GRID_LINE_WIDTH)
        # # RIGHT TOP TO BOTTOM
        pygame.draw.line(
        self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
        (GUI_CONFIG.GAME_BOARD_SIZE, 0),
        (GUI_CONFIG.GAME_BOARD_SIZE,
            GUI_CONFIG.GAME_BOARD_SIZE), GUI_CONFIG.GRID_LINE_WIDTH)

        # Get cell size, just one since its a square grid.
        cellSize = GUI_CONFIG.GAME_BOARD_SIZE/GUI_CONFIG.GRID_DIMENSION

        # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
        for x in range(GUI_CONFIG.GRID_DIMENSION):
            pygame.draw.line(
                self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
                ((cellSize * x), 0),
                ((cellSize * x), GUI_CONFIG.GAME_BOARD_SIZE), 2)
        # # HORIZONTAl DIVISIONS
            pygame.draw.line(
            self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
            (0, (cellSize*x)),
            (GUI_CONFIG.GAME_BOARD_SIZE, (cellSize*x)), 2)
  
    def redraw(self):
        self.mainSurface.blit(self.gameSurface, (GUI_CONFIG.GAME_BOARD_ORIGIN[0], GUI_CONFIG.GAME_BOARD_ORIGIN[1]))
        if(GUI_CONFIG.DO_DRAW_TABLE):
            self.table.update_table()
            self.mainSurface.blit(self.table.tableSurface, (GUI_CONFIG.TABLE_ORIGIN[0], GUI_CONFIG.TABLE_ORIGIN[1]))
        pygame.display.update()

    # Parameters: An overlay, a 2d map of variables
    def drawOverlay(self, overlay):
        #gridCells = cellMAP.shape[0]
        dimension = len(overlay)
        cellBorderPadding = 1
        celldimX = celldimY = (GUI_CONFIG.GAME_BOARD_SIZE/dimension) - (cellBorderPadding*2)
        # DOUBLE LOOP
        for row in range(0, dimension):
            for column in range(0, dimension):
                if(overlay[row][column][0] == "SQUARE"):
                    x = (celldimX*row) + cellBorderPadding + (2*row*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2
                    y = (celldimY*column) + cellBorderPadding + (2*column*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2
                    self.drawSquareCell(x, y, celldimX, celldimY, overlay[row][column][1])

                elif(overlay[row][column][0] == "CIRCLE"):
                    x = (celldimX*row) + cellBorderPadding + (2*row*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2 + (1/2 * celldimX)
                    y = (celldimY*column) + cellBorderPadding + (2*column*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2 + (1/2 * celldimY)
                    self.drawCircleCell(x, y, overlay[row][column][2], overlay[row][column][1])

    # Draw filled rectangle at coordinates
    def drawSquareCell(self, x, y, dimX, dimY, COLOR):
        pygame.draw.rect(
            self.gameSurface, COLOR,
            (x, y, dimX, dimY)
        )

    def drawCircleCell(self, x, y, value, COLOR):
        radius = value
        pygame.draw.circle(self.gameSurface, COLOR, (x,y), radius)

    def drawSquareGrid(self, origin, gridWH, cells):
        CONTAINER_WIDTH_HEIGHT = gridWH
        cont_x, cont_y = origin

        # DRAW Grid Border:
        # TOP lEFT TO RIGHT
        pygame.draw.line(
            self.gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
            (cont_x, cont_y),
            (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), GUI_CONFIG.GRID_LINE_WIDTH)
        # # BOTTOM lEFT TO RIGHT
        pygame.draw.line(
            self.gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
            (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
            (CONTAINER_WIDTH_HEIGHT + cont_x,
            CONTAINER_WIDTH_HEIGHT + cont_y), GUI_CONFIG.GRID_LINE_WIDTH)
        # # LEFT TOP TO BOTTOM
        pygame.draw.line(
            self.gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
            (cont_x, cont_y),
            (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), GUI_CONFIG.GRID_LINE_WIDTH)
        # # RIGHT TOP TO BOTTOM
        pygame.draw.line(
            self.gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
            (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
            (CONTAINER_WIDTH_HEIGHT + cont_x,
            CONTAINER_WIDTH_HEIGHT + cont_y), GUI_CONFIG.GRID_LINE_WIDTH)

        # Get cell size, just one since its a square grid.
        cellSize = CONTAINER_WIDTH_HEIGHT/cells

        # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
        for x in range(cells):
            pygame.draw.line(
                self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
                (cont_x + (cellSize * x), cont_y),
                (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
        # # HORIZONTAl DIVISIONS
            pygame.draw.line(
                self.gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
                (cont_x, cont_y + (cellSize*x)),
                (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)

    def get_heat_color(value):
        green = 255 - (value/5)
        if(green < 0):
            blue = 1 - green
            green = 0
            return (0, green, 0)