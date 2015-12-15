import pygame

def isUpPressed(keys, vim = True):
    return keys != None and (keys[pygame.K_UP] or keys[pygame.K_KP8] or (vim and keys[pygame.K_k]))
def isDownPressed(keys, vim = True):
    return keys != None and (keys[pygame.K_DOWN] or keys[pygame.K_KP2] or (vim and keys[pygame.K_j]))
def isLeftPressed(keys, vim = True):
    return keys != None and (keys[pygame.K_LEFT] or keys[pygame.K_KP4] or (vim and keys[pygame.K_h]))
def isRightPressed(keys, vim = True):
    return keys != None and (keys[pygame.K_RIGHT] or keys[pygame.K_KP6] or (vim and keys[pygame.K_l]))
def isOkayPressed(keys): # Okay uses Check on Gamepad. 
    return keys != None and (keys[pygame.K_RETURN] or keys[pygame.K_KP1])
def isBackPressed(keys): # Back uses the X
    return keys != None and (keys[pygame.K_BACKSPACE] or keys[pygame.K_KP3])
def isMenuPressed(keys): # Menu uses the Square.
    return keys != None and (keys[pygame.K_TAB] or keys[pygame.K_KP7])

def kbTextInput(keys, pKeys, workingString, index):
    if(keys == None or pKeys == None):
        return (workingString, index)
    
    def released(keys, pKeys, key):
        return not keys[key] and pKeys[key]
        
    if(released(keys, pKeys, pygame.K_BACKSPACE)):
        return (workingString[:index - 1] + workingString[index:], index - 1)
    if(released(keys, pKeys, pygame.K_DELETE)):
        return (workingString[:index] + workingString[index + 1:], index)
        
    if(released(keys, pKeys, pygame.K_SPACE)): return (workingString[:index] + ' ' + workingString[index:], index + 1)
    
    if(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
        if(released(keys, pKeys, pygame.K_0)): return (workingString[:index] + ')' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_1)): return (workingString[:index] + '!' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_2)): return (workingString[:index] + '@' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_3)): return (workingString[:index] + '#' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_4)): return (workingString[:index] + '$' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_5)): return (workingString[:index] + '%' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_6)): return (workingString[:index] + '^' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_7)): return (workingString[:index] + '&' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_8)): return (workingString[:index] + '*' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_9)): return (workingString[:index] + '(' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_a)): return (workingString[:index] + 'A' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_b)): return (workingString[:index] + 'B' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_c)): return (workingString[:index] + 'C' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_d)): return (workingString[:index] + 'D' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_e)): return (workingString[:index] + 'E' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_f)): return (workingString[:index] + 'F' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_g)): return (workingString[:index] + 'G' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_h)): return (workingString[:index] + 'H' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_i)): return (workingString[:index] + 'I' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_j)): return (workingString[:index] + 'J' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_k)): return (workingString[:index] + 'K' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_l)): return (workingString[:index] + 'L' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_m)): return (workingString[:index] + 'M' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_n)): return (workingString[:index] + 'N' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_o)): return (workingString[:index] + 'O' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_p)): return (workingString[:index] + 'P' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_q)): return (workingString[:index] + 'Q' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_r)): return (workingString[:index] + 'R' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_s)): return (workingString[:index] + 'S' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_t)): return (workingString[:index] + 'T' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_u)): return (workingString[:index] + 'U' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_v)): return (workingString[:index] + 'V' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_w)): return (workingString[:index] + 'W' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_x)): return (workingString[:index] + 'X' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_y)): return (workingString[:index] + 'Y' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_z)): return (workingString[:index] + 'Z' + workingString[index:], index + 1)
    else:
        if(released(keys, pKeys, pygame.K_0)): return (workingString[:index] + '0' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_1)): return (workingString[:index] + '1' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_2)): return (workingString[:index] + '2' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_3)): return (workingString[:index] + '3' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_4)): return (workingString[:index] + '4' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_5)): return (workingString[:index] + '5' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_6)): return (workingString[:index] + '6' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_7)): return (workingString[:index] + '7' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_8)): return (workingString[:index] + '8' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_9)): return (workingString[:index] + '9' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_a)): return (workingString[:index] + 'a' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_b)): return (workingString[:index] + 'b' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_c)): return (workingString[:index] + 'c' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_d)): return (workingString[:index] + 'd' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_e)): return (workingString[:index] + 'e' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_f)): return (workingString[:index] + 'f' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_g)): return (workingString[:index] + 'g' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_h)): return (workingString[:index] + 'h' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_i)): return (workingString[:index] + 'i' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_j)): return (workingString[:index] + 'j' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_k)): return (workingString[:index] + 'k' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_l)): return (workingString[:index] + 'l' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_m)): return (workingString[:index] + 'm' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_n)): return (workingString[:index] + 'n' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_o)): return (workingString[:index] + 'o' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_p)): return (workingString[:index] + 'p' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_q)): return (workingString[:index] + 'q' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_r)): return (workingString[:index] + 'r' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_s)): return (workingString[:index] + 's' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_t)): return (workingString[:index] + 't' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_u)): return (workingString[:index] + 'u' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_v)): return (workingString[:index] + 'v' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_w)): return (workingString[:index] + 'w' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_x)): return (workingString[:index] + 'x' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_y)): return (workingString[:index] + 'y' + workingString[index:], index + 1)
        elif(released(keys, pKeys, pygame.K_z)): return (workingString[:index] + 'z' + workingString[index:], index + 1)
    
    return(workingString, index)

def kbNumInput(keys, pKeys, workingNum, index):
    if(keys == None or pKeys == None):
        return (workingNum, index)
    
    workingString = str(workingNum)
    
    def released(keys, pKeys, key):
        return not keys[key] and pKeys[key]
        
    if(released(keys, pKeys, pygame.K_BACKSPACE)):
        return (int('0' + workingString[:index - 1] + workingString[index:]), index - 1)
    if(released(keys, pKeys, pygame.K_DELETE)):
        return (int('0' + workingString[:index] + workingString[index + 1:]), index)
    
    if(released(keys, pKeys, pygame.K_0)): return (int(workingString[:index] + '0' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_1)): return (int(workingString[:index] + '1' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_2)): return (int(workingString[:index] + '2' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_3)): return (int(workingString[:index] + '3' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_4)): return (int(workingString[:index] + '4' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_5)): return (int(workingString[:index] + '5' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_6)): return (int(workingString[:index] + '6' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_7)): return (int(workingString[:index] + '7' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_8)): return (int(workingString[:index] + '8' + workingString[index:]), index + 1)
    elif(released(keys, pKeys, pygame.K_9)): return (int(workingString[:index] + '9' + workingString[index:]), index + 1)
    
    return (workingNum, index)