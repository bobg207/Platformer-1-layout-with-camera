import pygame
from settings import *

pygame.init()


class Block(pygame.sprite.Sprite):
    """class to create a block object for walls and platforms
    x_loc, y_loc: the position of the block in the LAYOUT
    tile_size: the size of the block from settings TILE_SIZE
    """

    def __init__(self, x_loc, y_loc, tile_size):
        super().__init__()
        # the Surface class can be replaced with a specific image
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x_loc
        self.rect.y = y_loc

    def update(self, x_shift, y_shift):
        """method for shifting the blocks by x_shift creating a horizontal 'camera' effect"""

        self.rect.x += x_shift
        self.rect.y += y_shift


class Layout:
    """class to handle creating the level and interaction between objects in the level
    layout_map: the list containing the layout for a level
    display: the surface that the layout is being drawn to
    """

    def __init__(self, layout_map, display):
        self.display = display
        self.blocks = None
        self.players = None
        self.bg_img = None
        self.bg_rect = None
        self.create_layout(layout_map)  # call method, pass in the map param

        self.camera_shift_x = 0  # updated based on player movement
        self.camera_shift_y = 0

    def create_layout(self, layout_map):
        """method to create layout
            map: the layout_map passed into the __init__
            """
        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.GroupSingle()
        self.bg_img = pygame.Surface((LAYOUT_WIDTH, DISPLAY_HEIGHT))
        self.bg_img.fill(WHITE)
        # bg = pygame.image.load('bg_img.jpeg')
        # self.bg_img = pygame.transform.scale(bg, (LAYOUT_WIDTH, DISPLAY_HEIGHT))
        self.bg_rect = self.bg_img.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        for i, row in enumerate(layout_map):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * TILE_SIZE

                if col == '1':
                    block = Block(x_val, y_val, TILE_SIZE)
                    self.blocks.add(block)
                if col == 'P':
                    player = Player(x_val, y_val, TILE_SIZE)
                    self.players.add(player)

    def move_camera(self):

        left_edge = DISPLAY_WIDTH // 4
        right_edge = DISPLAY_WIDTH - left_edge
        top_edge = DISPLAY_HEIGHT // 4
        bottom_edge = DISPLAY_HEIGHT - top_edge

        # get the sprite that is in the Group, only needed to shorten amount of typing throughout this method
        player = self.players.sprite
        player_dir_x = player.dir_x
        player_dir_y = player.dir_y

        if player.rect.left <= left_edge and player_dir_x == -1:  # close to left and moving left
            self.camera_shift_x = 5
            player.rect.left = left_edge
            player.speed = 0
        elif player.rect.right >= right_edge and player_dir_x == 1:  # close to right and moving right
            self.camera_shift_x = -5
            player.rect.right = right_edge
            player.speed = 0
        else:
            self.camera_shift_x = 0
            player.speed = 5

        # close to top and moving up
        if player.rect.top <= top_edge and player_dir_y == -1:
            self.camera_shift_y = 5
            player.rect.top = top_edge
            player.speed = 0
        # close to bottom and moving down
        elif player.rect.bottom >= bottom_edge and player_dir_y == 1:
            self.camera_shift_y = -5
            player.rect.right = bottom_edge
            player.speed = 0
        else:
            self.camera_shift_y = 0
            player.speed = 5

        # if self.bg_rect.right <= DISPLAY_WIDTH - 2 * TILE_SIZE and dir_x == 1:
        #     self.camera_shift = 0
        # elif self.bg_rect.left >= 0 and dir_x == -1:
        #     self.camera_shift = 0

    def update(self):
        """method to update all objects on the map
                called in the game loop"""

        # level walls and platforms
        self.bg_rect.x += self.camera_shift_x
        self.bg_rect.y += self.camera_shift_y
        self.display.blit(self.bg_img, (self.bg_rect.x, self.bg_rect.y))
        self.blocks.update(self.camera_shift_x, self.camera_shift_y)
        self.blocks.draw(self.display)

        # level player
        self.move_camera()
        self.players.update()
        self.players.draw(self.display)


class Player(pygame.sprite.Sprite):
    """class to create a player object
    x, y: the location of the player in the layout
    """

    def __init__(self, x_loc, y_loc, tile_size):
        super().__init__()
        self.tile_size = tile_size
        # change the image to actual image
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x_loc
        self.rect.y = y_loc

        self.dir_y = 0  # up=1, down=-1
        self.dir_x = 0  # rt=1, lft=-1

        self.speed = 5

    def update(self):
        self.get_keys()
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

    def get_keys(self):
        """method to handle keyboard presses"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.dir_x = 1
        elif keys[pygame.K_LEFT]:
            self.dir_x = -1
        else:
            self.dir_x = 0

        if keys[pygame.K_UP]:
            self.dir_y = -1
        elif keys[pygame.K_DOWN]:
            self.dir_y = 1
        else:
            self.dir_y = 0
