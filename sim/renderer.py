import sys
import pygame
from pygame import USEREVENT
from pygame.locals import *
import time
from config import COLORS
from config import GUI_CONFIG
from config import SIM_CONFIG

# Events
for i in range(len(GUI_CONFIG.OVERLAY_TYPES)):
  GUI_CONFIG.OVERLAY_TYPES[i] = USEREVENT + (i+1)

STOP_RENDERING = USEREVENT + 10
MOUSE_CLICK = USEREVENT + 11

def start_rendering():
  pygame.init()
  pygame.display.set_caption(GUI_CONFIG.SIM_TITLE)

  # Initialize Surfaces
  global mainSurface
  mainSurface = pygame.display.set_mode(GUI_CONFIG.WINDOW_SIZE)
  mainSurface.fill(GUI_CONFIG.MAIN_SURFACE_BASE_COLOR)

  global gameSurface 
  gameSurface = pygame.Surface((GUI_CONFIG.GAME_BOARD_SIZE, GUI_CONFIG.GAME_BOARD_SIZE))
  drawGameBoard()

  if(GUI_CONFIG.DO_DRAW_TABLE):
    global tableSurface 
    tableFont = pygame.font.SysFont('arial.ttf', 18)
    buttonFont = pygame.font.SysFont('arial.ttf', 22, bold = pygame.font.Font.bold)
    tableSurface = pygame.Surface((GUI_CONFIG.TABLE_SIZE[0], GUI_CONFIG.TABLE_SIZE[1]))
    pygame.draw.rect(tableSurface, COLORS.BLACK, (GUI_CONFIG.TABLE_ORIGIN[0], GUI_CONFIG.TABLE_ORIGIN[1], 100, 100))

  if(GUI_CONFIG.DO_DRAW_TABLE):
    mainSurface.blit(tableSurface, (GUI_CONFIG.TABLE_ORIGIN[0], GUI_CONFIG.TABLE_ORIGIN[1]))
    mainSurface.blit(gameSurface, (GUI_CONFIG.GAME_BOARD_ORIGIN[0], GUI_CONFIG.GAME_BOARD_ORIGIN[1]))

  while True:
    checkEvents()
    mainSurface.blit(gameSurface, (GUI_CONFIG.GAME_BOARD_ORIGIN[0], GUI_CONFIG.GAME_BOARD_ORIGIN[1]))
    if(GUI_CONFIG.DO_DRAW_TABLE):
      drawTable(tableFont)
      drawButtons(buttonFont)
      mainSurface.blit(tableSurface, (GUI_CONFIG.TABLE_ORIGIN[0], GUI_CONFIG.TABLE_ORIGIN[1]))
    pygame.display.update()
    time.sleep(SIM_CONFIG.SIM_SPEED)

def drawGameBoard():
  gameSurface.fill(GUI_CONFIG.GAME_BASE_COLOR)
  # DRAW Grid Border:
  # TOP lEFT TO RIGHT
  pygame.draw.line(
    gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
    (0, 0),
    (GUI_CONFIG.GAME_BOARD_SIZE, 0), GUI_CONFIG.GRID_LINE_WIDTH)
  # # BOTTOM lEFT TO RIGHT
  pygame.draw.line(
    gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
    (0, GUI_CONFIG.GAME_BOARD_SIZE),
    (GUI_CONFIG.GAME_BOARD_SIZE,
      GUI_CONFIG.GAME_BOARD_SIZE), GUI_CONFIG.GRID_LINE_WIDTH)
  # # LEFT TOP TO BOTTOM
  pygame.draw.line(
    gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
    (0, 0),
    (0, GUI_CONFIG.GAME_BOARD_SIZE), GUI_CONFIG.GRID_LINE_WIDTH)
  # # RIGHT TOP TO BOTTOM
  pygame.draw.line(
    gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
    (GUI_CONFIG.GAME_BOARD_SIZE, 0),
    (GUI_CONFIG.GAME_BOARD_SIZE,
      GUI_CONFIG.GAME_BOARD_SIZE), GUI_CONFIG.GRID_LINE_WIDTH)

  # Get cell size, just one since its a square grid.
  cellSize = GUI_CONFIG.GAME_BOARD_SIZE/GUI_CONFIG.GRID_DIMENSION

  # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
  for x in range(GUI_CONFIG.GRID_DIMENSION):
      pygame.draw.line(
          gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
          ((cellSize * x), 0),
          ((cellSize * x), GUI_CONFIG.GAME_BOARD_SIZE), 2)
  # # HORIZONTAl DIVISIONS
      pygame.draw.line(
        gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
        (0, (cellSize*x)),
        (GUI_CONFIG.GAME_BOARD_SIZE, (cellSize*x)), 2)

# Parameters: An overlay, a 2d map of variables
def drawOverlay(overlay, overlayType):
  #gridCells = cellMAP.shape[0]
  dimension = len(overlay)
  cellBorderPadding = 1
  celldimX = celldimY = (GUI_CONFIG.GAME_BOARD_SIZE/dimension) - (cellBorderPadding*2)
  # DOUBLE LOOP
  for row in range(0, dimension):
    for column in range(0, dimension):
      if(overlayType == GUI_CONFIG.OVERLAY_TYPES[0]): # Define how this overlay is treated
        x = (celldimY*row) + cellBorderPadding + (2*row*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2
        y = (celldimX*column) + cellBorderPadding + (2*column*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2
        if(overlay[row][column] == 0):
          drawSquareCell(x, y, celldimX, celldimY, COLORS.WHITE)
        else:
          drawSquareCell(x, y, celldimX, celldimY, COLORS.BLACK)
      elif(overlayType == GUI_CONFIG.OVERLAY_TYPES[1]): # Define how this overlay is treated
        x = GUI_CONFIG.GAME_BOARD_ORIGIN[0] + (celldimY*row) + cellBorderPadding + (2*row*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2
        y = GUI_CONFIG.GAME_BOARD_ORIGIN[1] + (celldimX*column) + cellBorderPadding + (2*column*cellBorderPadding) + GUI_CONFIG.GRID_LINE_WIDTH/2
        #x = CONFIG.GAME_BOARD_ORIGIN[0] + ( (celldimY*row + celldimY*(row+1))/2) + cellBorderPadding + (2*row*cellBorderPadding) + CONFIG.GRID_LINE_WIDTH/2
        #y = CONFIG.GAME_BOARD_ORIGIN[1] + ( (celldimX*column + celldimX*(column+1))/2) + cellBorderPadding + (2*column*cellBorderPadding) + CONFIG.GRID_LINE_WIDTH/2
        drawSquareCell(x, y, celldimX, celldimY, COLORS.TRUE_RED)

# Draw filled rectangle at coordinates
def drawSquareCell(x, y, dimX, dimY, COLOR):
  pygame.draw.rect(
    gameSurface, COLOR,
    (x, y, dimX, dimY)
  )

def drawCircleCell(x, y, value, COLOR):
  radius = (value) * (value/100 + 1)
  if(radius > 4):
    radius = 4
  pygame.draw.circle(gameSurface, COLOR, (x,y), radius)

def drawSquareGrid(origin, gridWH, cells):
  CONTAINER_WIDTH_HEIGHT = gridWH
  cont_x, cont_y = origin

  # DRAW Grid Border:
  # TOP lEFT TO RIGHT
  pygame.draw.line(
    gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
    (cont_x, cont_y),
    (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), GUI_CONFIG.GRID_LINE_WIDTH)
  # # BOTTOM lEFT TO RIGHT
  pygame.draw.line(
    gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
    (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
    (CONTAINER_WIDTH_HEIGHT + cont_x,
      CONTAINER_WIDTH_HEIGHT + cont_y), GUI_CONFIG.GRID_LINE_WIDTH)
  # # LEFT TOP TO BOTTOM
  pygame.draw.line(
    gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
    (cont_x, cont_y),
    (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), GUI_CONFIG.GRID_LINE_WIDTH)
  # # RIGHT TOP TO BOTTOM
  pygame.draw.line(
    gameSurface, GUI_CONFIG.OUTER_BORDER_COLOR,
    (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
    (CONTAINER_WIDTH_HEIGHT + cont_x,
      CONTAINER_WIDTH_HEIGHT + cont_y), GUI_CONFIG.GRID_LINE_WIDTH)

  # Get cell size, just one since its a square grid.
  cellSize = CONTAINER_WIDTH_HEIGHT/cells

  # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
  for x in range(cells):
      pygame.draw.line(
          gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
          (cont_x + (cellSize * x), cont_y),
          (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
  # # HORIZONTAl DIVISIONS
      pygame.draw.line(
        gameSurface, GUI_CONFIG.GRID_LINE_COLOR,
        (cont_x, cont_y + (cellSize*x)),
        (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)

def drawTable(font):
  tableSurface.fill(GUI_CONFIG.TABLE_BASE_COLOR)
  for i in range(len(GUI_CONFIG.TABLE)):
    num_entries = len(GUI_CONFIG.TABLE[i])
    col_width = GUI_CONFIG.TABLE_SIZE[0] / num_entries
    for j in range(num_entries):
      pygame.draw.rect(tableSurface, COLORS.BLACK, ((j*col_width), (i*GUI_CONFIG.ROW_HEIGHT), col_width, GUI_CONFIG.ROW_HEIGHT), width = 1)
      img = font.render(str(GUI_CONFIG.TABLE[i][j]), True, COLORS.BLACK)
      tableSurface.blit(img, ((j*col_width) + 5, (i*GUI_CONFIG.ROW_HEIGHT) + 5))

def drawButtons(font):
  if(SIM_CONFIG.PAUSE_SIMULATION == 0):
    color = COLORS.TRUE_RED
    text = "PAUSE"
  else:
    color = COLORS.GREEN_2
    text = "PLAY"
  pygame.draw.rect(tableSurface, color, (GUI_CONFIG.PAUSE_BUTTON_LOC[0] , GUI_CONFIG.PAUSE_BUTTON_LOC[1], GUI_CONFIG.PAUSE_BUTTON_SIZE[0], GUI_CONFIG.PAUSE_BUTTON_SIZE[1]))
  img = font.render(text, True, COLORS.BLACK)
  tableSurface.blit(img, (GUI_CONFIG.PAUSE_BUTTON_LOC[0] + 10, GUI_CONFIG.PAUSE_BUTTON_LOC[1] + 5)) 

def get_heat_color(value):
    green = 255 - (value/5)
    if(green < 0):
      blue = 1 - green
      green = 0
    return (0, green, 0)
    
def checkEvents():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == KEYDOWN and event.key == K_q:
      pygame.quit()
      sys.exit()
    elif event.type == GUI_CONFIG.OVERLAY_TYPES[0]:
      drawOverlay(event.message, GUI_CONFIG.OVERLAY_TYPES[0])
    elif event.type == GUI_CONFIG.OVERLAY_TYPES[1]:
      drawOverlay(event.message, GUI_CONFIG.OVERLAY_TYPES[1])
    elif event.type == STOP_RENDERING:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
 #     CONFIG.PAUSE = 1 if CONFIG.PAUSE == 0 else 0
      click_loc = pygame.mouse.get_pos()
      register_button_click(click_loc)

def register_button_click(click):
  pause_button_loc = [GUI_CONFIG.TABLE_ORIGIN[0] + GUI_CONFIG.PAUSE_BUTTON_LOC[0], GUI_CONFIG.TABLE_ORIGIN[1] +GUI_CONFIG.PAUSE_BUTTON_LOC[1]]
  pause_button_size = [GUI_CONFIG.PAUSE_BUTTON_SIZE[0], GUI_CONFIG.PAUSE_BUTTON_SIZE[1]]
  if(click[0] >= pause_button_loc[0] and click[0] <= pause_button_loc[0] + pause_button_size[0]
         and click[1] >= pause_button_loc[1] and click[1] <= pause_button_loc[1] + pause_button_size[1]):
    SIM_CONFIG.PAUSE_SIMULATION = 1 if SIM_CONFIG.PAUSE_SIMULATION == 0 else 0