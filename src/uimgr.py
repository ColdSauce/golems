import pygame

class Singleton(object):
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls, *args, **kwargs)
        return cls._instances[cls]

# Any class can use this by importing uimgr and getting an instance of the manager.
# I know the singleton stuff is weird, but just call uimgr.UIManager() to get this instance
class UIManager(Singleton):
    
    # Warning:
    # do not put children of container objects in here, or they will be rendered twice.
    parentUI = {}
        
    def clear(self):
        self.parentUI = {}

    def addElement(self, ele, ID):
        ele.ID = ID
        self.parentUI[ID] = ele
    
    def render(self, surface):
        for key in self.parentUI.keys():
            self.parentUI[key].render(surface)
        
    # has a position, size, background, border, on/off switch for rendering
    class UIElement(object):
        def __init__(self, rect, bgColor = None, borderColor = None, borderSize = 5):
            self.rect = rect
            self.bgColor = bgColor
            self.borderColor = borderColor
            self.parent = None # changes when placed in a container
            self.fullLoc = None # updated when parent exists
            self.enabled = True
            self.bSize = borderSize 

        def setEnabled(self, state):
            self.enabled = state

        def getFullLocation(self):
            if self.parent is None:
                return self.rect
            else:
                pRect = self.parent.getFullLocation()
                pX = pRect[0]
                pY = pRect[1]

                sX = self.rect[0]
                sY = self.rect[1]
                sW = self.rect[2]
                sH = self.rect[3]
                
                newX = pX + sX
                newY = pY + sY
                return (newX,newY,sW,sH)
    
        def render(self, surface):
            if self.bgColor is not None:
                pygame.draw.rect(surface, self.bgColor, self.rect)

            if self.borderColor is not None:
                pygame.draw.rect(surface, self.borderColor, self.rect, self.bSize)
            

    class ImageElement(UIElement):
        def __init__(self, position, spriteSrc, sizeMod = None):
            self.image = pygame.image.load(spriteSrc).convert()
            self.position = position
    
            if sizeMod is None: 
                self.scaledImg = self.image
            else:
                self.setMod(sizeMod)
                self.scaledImg = self.scaleImage(sizeMod)
                     
            self.setRect()
            super(type(self),self).__init__(self.rect)
        
        def setMod(self, mod):
            self.mod = mod
            self.scaleImage()
            self.setRect()

        def setRect(self):
            x = position[0]
            y = position[1]
            size = self.scaledImg.get_size()
            self.rect = (x,y,size[0],size[1])

        def scaleImage(self):
            size = self.image.get_size() 
            self.scaledImg = pygame.transform.scale(self.image,(int(size[0]*self.mod),int(size[1]*self.mod)))
    
        def render(self, surface):
            super(type(self),self).render(surface)
            surface.blit(self.scaledImg, self.rect)

    # Text element
    class TextElement(UIElement):
        def __init__(self, position, text, color, size):       
            self.font = pygame.font.SysFont("comicsansms", size)
            self.text = text
            self.fontSize = size
            self.color = color
            self.position = position
            
            self.rText = self.preRender() # sets the self.rect attr
            
            super(type(self),self).__init__(self.rect)
        
        def preRender(self):
            self.width, self.height = self.font.size(self.text)
            self.rect = (self.position[0],self.position[1],self.width,self.height)        
            renderedText = self.font.render(self.text, 0, self.color)
            return renderedText

        def setText(self, text):
            self.text = text
            self.rText = self.preRender()

        def render(self, surface):
            super(type(self),self).render(surface)
            surface.blit(self.rText, self.rect)
    
     

    # Used for grouping things
    class Container(UIElement):
        def __init__(self, rect, bgColor = None, borderColor = None):
            super(type(self),self).__init__(rect,bgColor,borderColor)
            self.children = []

        def addUIElement(self, ele):
            self.children.append(ele)
            ele.parent = self

        def render(self,surface):
            super(type(self),self).render(surface)            
            for i in range(0,self.children):
                self.children[i].render(surface)

    
#End UIManager
