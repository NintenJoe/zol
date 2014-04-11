##  @file
#   Module file for the "Animation" type, which represents game animations.
#       @authors Joseph Ciurej / Edwin Chan
#       TODO: Fix everything in this file (duct tape with frame delta instead of game time).

# Pygame Imports #
import pygame as PG
from pygame.locals import *

# Game Library Imports #
from Globals import load_image
from Globals import clamp

##  Blueprint class for standard game animations.  Specialized derivatives of 
#   the "Sprite" class may contain several different animation instances and 
#   cycle between them based on state.
class Animation(object):
    # Constructors #

    ##  Constructs an animation from a sprite sheet file given the amount of time 
    #   per frame and the width of each frame in the sprite sheet.
    #   
    #   @param filename A string that points to the file in the "assets/graphics/" 
    #       file folder that conatins the sprite sheet for the given animation.
    #   @param frame_count The total number of frames contained within the 
    #       animation depicted by the given sprite sheet (default value 1).
    #   @param frame_time The amount of time that each frame will play before 
    #       the next frame is shown (in milliseconds) (default value 33 milliseconds).
    #   @param is_looping A boolean value that indicates whether or not the animation
    #       represented should loop or not (default value false).
    def __init__(self, filename, frame_time=33, is_looping=False):

                self.sprite_sheet = load_image(filename, PG.Color(255, 0, 255))     
                sheet_rect = self.sprite_sheet.get_rect()

                self.sheet_path = filename
                self.frame_width = self._get_frame_width()
                self.frame_count = int(sheet_rect.width / self.frame_width)
                self.frame_height = sheet_rect.height
                self.frame_time = frame_time
                self.is_looping = is_looping

                # Initializes the starting time for the animation to a negative value to 
                # track bugs related to animations that are polled for frames but that
                # haven't been queued to start.
                self.start_time = -1


    # Methods #

    ##      Returns the uploaded image
    #
    
    def get_full_image(self):
        return self.sprite_sheet

    ##      Loads a specific sprite from the spritesheet
    #
    #       @param rectangle The coordinates of the 4 corners of the sprite rectangle in
    #       the sprite sheet. i.e. (X, Y, width, height)
    #

    def get_image_at(self, rectangle):
        rect = PG.Rect(rectangle)
        img = PG.Surface(rect.size).convert()
        img.blit(self.sprite_sheet, (0,0), rect)
        return img

    ##      Loads several specific sprite from the spritesheet and puts them into a list
    #
    #       @param rectangles The coordinates of the 4 corners of the sprite rectangle in
    #       the sprite sheet. i.e. (X, Y, width, height)
    #

    def get_images_at(self, rectangles):
        imgs = []
        for rect in rectangles:
                imgs.append(self.get_image_at(rect))
        return imgs

    ##      Stores all the file names for all images associated
    #       with a given entity into a list
    #
    #       @return List of image names for a given entity
    #

    def load_entities(self):
        image_names = []
        entities_foldername = os.path.join('assets', 'graphics', 'entities', self)

        for filename in entities_foldername:
                image_names.append(filename)
                
        return image_names
        
    ##  Starts the animation at the given time (which should be measured in 
    #   milliseconds since the game started up).
    #
    #   @param game_time The time relative to the start of the game at which the
    #       the animation is queued to start.
    def start(self, game_time):
        self.start_time = game_time

    ##  Retrieves the frame for the given update period based on the given time 
    #   (which should be given in terms of milliseconds since the game started up).
    #   
    #   @param game_time The time at which the frame is being retrieved (in terms
    #       of milliseconds since the game started).
    #   @return A reference to the image that represents the current frame for 
    #       the animation.
    def get_frame(self, time_delta):
        frame_num = self._get_frame_number(time_delta)
        frame_rect = PG.Rect(frame_num * self.frame_width, 0, self.frame_width, self.frame_height)

        return self.sprite_sheet.subsurface(frame_rect)

    ##  A courtesy function that resets the timer for an animation instance.  
    #   This function should be called whenever an animation should stop playing.
    def end(self):
        self.start_time = -1

    # Helper Functions #

    ##  Returns the number for the current frame given the current game time,
    #   which can be used to position the subsurface for the current frame.
    #   
    #   @param game_time The time at which the frame is being retrieved (in terms
    #       of milliseconds since the game started).
    #   @return A number that uniquely identifies the current frame that will be
    #       displayed in the animation.
    def _get_frame_number(self, time_delta):
        frame_num = int(time_delta / self.frame_time)

        if self.is_looping:
            frame_num = frame_num % self.frame_count
        else:
            frame_num = clamp(frame_num, 0, self.frame_count - 1)

        return frame_num

    ## Detects the frame width by looking for the pixel with alpha=0
    #  which indicates the beginning of the second frame.
    #
    #   @return The width of each frame in the sprite sheet
    def _get_frame_width(self):
        sprite_sheet = load_image(self.sheet_path, PG.Color(0,0,0,0))
        for x in range(0,sprite_sheet.get_width()):
            color = sprite_sheet.get_at((x,0))
            if (color.a == 0):
                return x
            elif (color.r == 255 and color.g == 255 and color.b == 255):
                return x

        return sprite_sheet.get_width()