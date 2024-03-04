#GUI CONFIG
from config import COLORS
from config import SIM_CONFIG

DO_RENDER = SIM_CONFIG.DO_RENDER
SIM_TITLE = "<SIM TITLE>"

######################################################
#                                                    #
#                Renderer Settings                   #
#                                                    #
######################################################

# Screen Sizing
PLOT_SIZE = 900

LARGE_SCREEN_SIZING = WIDTH, HEIGHT = 1500, 1000
SMALL_SCREEN_SIZING = WIDTH, HEIGHT = 1200, 700
WINDOW_SIZE = WIDTH, HEIGHT = SMALL_SCREEN_SIZING
GAME_BOARD_ORIGIN = (10,10)
GAME_BOARD_SIZE = WINDOW_SIZE[1] - 40

# Grid Setting
GRID_DIMENSION = SIM_CONFIG.MAP_DIMENSION
GRID_LINE_WIDTH = 1
MAIN_SURFACE_BASE_COLOR = COLORS.LIGHT_GREY
GRID_LINE_COLOR = COLORS.GREY
OUTER_BORDER_COLOR = COLORS.BLACK
GAME_BASE_COLOR = COLORS.YELLOW1

OVERLAY_TYPES = ["<OVERLAY1>", "<OVERLAY2>", "..."]

######################################################
#                                                    #
#                Table Settings                      #
#                                                    #
######################################################

DO_DRAW_TABLE = True

TABLE = (   ["Heading 1"],
            ["E1", 0],
            ["E2", 0],
            ["E3", 0],
            ["E4", 0],      
            [" "],
            ["Heading 2"],
            ["E1", 0, 0],
            ["E3", 0, 0],
            ["E4", 0, 0],
            [" "],
            ["Heading 3"],
            ["TITLE", "TITLE", "TITLE", "TITLE", "TITLE"],
            ["[SITE NAME]","[ABS_CAP]","[OP_CAP]", "[OCC]", "[%]"],
            ["[SITE NAME]","[ABS_CAP]","[OP_CAP]", "[OCC]", "[%]"],
            ["[SITE NAME]","[ABS_CAP]","[OP_CAP]", "[OCC]", "[%]"],
            ["[SITE NAME]","[ABS_CAP]","[OP_CAP]", "[OCC]", "[%]"],
            ["[SITE NAME]","[ABS_CAP]","[OP_CAP]", "[OCC]", "[%]"],
            ["[SITE NAME]","[ABS_CAP]","[OP_CAP]", "[OCC]", "[%]"]
        )

ROW_HEIGHT = 20
TABLE_SITE_INDEX = 13

TABLE_BASE_COLOR = COLORS.LIGHT_GREY
TABLE_ORIGIN = WIDTH, HEIGHT = (GAME_BOARD_SIZE + 50, GAME_BOARD_ORIGIN[1])
TABLE_SIZE = WIDTH, HEIGHT = (WINDOW_SIZE[0]/3, GAME_BOARD_SIZE)

PAUSE_BUTTON_LOC = WIDTH, HEIGHT = TABLE_SIZE[0] - TABLE_SIZE[0] + 25, TABLE_SIZE[1] - 50
PAUSE_BUTTON_SIZE = WIDTH, HEIGHT = 75, 25