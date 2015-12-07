import pygame

def isUpPressed(keys):
    return keys != None and (keys[pygame.K_UP] or keys[pygame.K_KP8] or keys[pygame.K_k])
def isDownPressed(keys):
    return keys != None and (keys[pygame.K_DOWN] or keys[pygame.K_KP2] or keys[pygame.K_j])
def isLeftPressed(keys):
    return keys != None and (keys[pygame.K_LEFT] or keys[pygame.K_KP4] or keys[pygame.K_h])
def isRightPressed(keys):
    return keys != None and (keys[pygame.K_RIGHT] or keys[pygame.K_KP6] or keys[pygame.K_l])
def isOkayPressed(keys): # Okay uses Check on Gamepad. 
    return keys != None and (keys[pygame.K_RETURN] or keys[pygame.K_KP1])
def isBackPressed(keys): # Back uses the X
    return keys != None and (keys[pygame.K_BACKSPACE] or keys[pygame.K_KP3])
def isMenuPressed(keys): # Menu uses the Square.
    return keys != None and (keys[pygame.K_TAB] or keys[pygame.K_KP7])
