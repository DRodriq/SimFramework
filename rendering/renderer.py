import sys
import pygame
from pygame import USEREVENT
from pygame.locals import *
import time
import os
from config import GUI_CONFIG
from config import SIM_CONFIG
from config import COLORS
from rendering import sim_window
from utils import logging

# Events
for i in range(len(GUI_CONFIG.OVERLAY_TYPES)):
  GUI_CONFIG.OVERLAY_TYPES[i] = USEREVENT + (i+1)

STOP_RENDERING = USEREVENT + 10
MOUSE_CLICK = USEREVENT + 11

def start_rendering():
  sim = sim_window.Sim_Window()
  sim.drawGameBoard()

  while True:
    checkEvents(sim)
    sim.redraw()
    time.sleep(SIM_CONFIG.SIM_SPEED)


def checkEvents(sim_window):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == KEYDOWN and event.key == K_q:
      pygame.quit()
      sys.exit()
    elif event.type == GUI_CONFIG.OVERLAY_TYPES[0]:
      overlay_transform = [list(map(overlay_1_map, x)) for x in event.message]
      sim_window.drawOverlay(overlay_transform)
    elif event.type == GUI_CONFIG.OVERLAY_TYPES[1]:
      overlay_transform = [list(map(overlay_2_map, x)) for x in event.message]
      sim_window.drawOverlay(overlay_transform)
    elif event.type == STOP_RENDERING:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      #  CONFIG.PAUSE = 1 if CONFIG.PAUSE == 0 else 0
      click_loc = pygame.mouse.get_pos()
      register_button_click(click_loc)


# Transform overlay values into something the draw overlay function can understand
def overlay_1_map(value):
  if(value == 0):
    color = COLORS.WHITE
  if(value == 1):
    color = COLORS.BLACK
  shape = "SQUARE"
  size = 1
  return(shape, color, size)

def overlay_2_map(value):
  color = COLORS.TRUE_RED
  shape = "CIRCLE"
  size = value/5
  return(shape, color, size)


def register_button_click(click):
  pause_button_loc = [GUI_CONFIG.TABLE_ORIGIN[0] + GUI_CONFIG.PAUSE_BUTTON_LOC[0], GUI_CONFIG.TABLE_ORIGIN[1] +GUI_CONFIG.PAUSE_BUTTON_LOC[1]]
  pause_button_size = [GUI_CONFIG.PAUSE_BUTTON_SIZE[0], GUI_CONFIG.PAUSE_BUTTON_SIZE[1]]
  if(click[0] >= pause_button_loc[0] and click[0] <= pause_button_loc[0] + pause_button_size[0]
         and click[1] >= pause_button_loc[1] and click[1] <= pause_button_loc[1] + pause_button_size[1]):
    SIM_CONFIG.PAUSE_SIMULATION = 1 if SIM_CONFIG.PAUSE_SIMULATION == 0 else 0
