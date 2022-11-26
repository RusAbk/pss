import pygame
pygame.init()




class PSS:
  def __new__(cls, surface, pygame_instance):
    if not hasattr(cls, 'instance'):
        cls.instance = super(PSS, cls).__new__(cls)
    return cls.instance
  def __init__(self, surface, pygame_instance):
    """
      Constructor for PSS instance

      Parameters
      ---
      surface
        Surface to draw components
      pygame_instance
        PyGame instance to operate with it
    """
    self.pygame_instance = pygame_instance
    self.components = []
    self.surface = surface
    self.default_cursor = pygame.SYSTEM_CURSOR_ARROW

  def addComponent(self, clsName, style = {}):
    """
      Creates new component of clsName type

      Parameters
      ---
      clsName
        Classname of component to create
      props
        Style properties

      Returns
      ---
      object
        Created component
    """
    if isinstance(style, Style):
      component = clsName(surface=self.surface, pygame_instance=self.pygame_instance, style=style)
    else:
      component = clsName(surface=self.surface, pygame_instance=self.pygame_instance, style=Style(style))
    self.components.append(component)
    return component

  def sendEvent(self, e):
    hover_component = None
    mouse_moved = False
    if e.type == self.pygame_instance.MOUSEMOTION:
      mouse_moved = True

    for component in self.components:
      component.sendEvent(e)
      if mouse_moved and component.rect.collidepoint(e.pos):
        hover_component = component
        component.hover()
      else: 
        component.unhover()

    if hover_component is None:
      self.pygame_instance.mouse.set_cursor(self.default_cursor)


  def tick(self):
    for component in self.components:
      component.tick()

  def draw(self):
    for component in self.components:
      component.draw()

  def update(self):
    self.tick()
    self.draw()




class Style:
  def __init__(self, props = {}):
    self.props = props
    

class Component:
  def __init__(self, surface, pygame_instance, left=0, top=0, width=0, height=0, style = Style()):
    self.pygame_instance = pygame_instance
    self.surface = surface
    self.rect = pygame_instance.Rect(left, top, width, height)
    self.clicked = None
    self.style = style
    self.cursor = pygame.SYSTEM_CURSOR_ARROW

  def sendEvent(self, e):
    if e.type == self.pygame_instance.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(e.pos):
        if self.clicked is not None:
          self.clicked()

  def onclick(self, callback):
    self.clicked = callback

  def setStyle(self, style):
    self.style = dict(style)

  def draw(self):
    pass
  def tick(self):
    pass
  def hover(self):
    self.pygame_instance.mouse.set_cursor(self.cursor)
  def unhover(self):
    pass




class Button(Component):
  def __init__(self, surface, pygame_instance, left=0, top=0, width=100, height=40, style = Style()):
    super().__init__(surface, pygame_instance, left, top, width, height, style)
    self.cursor = pygame.SYSTEM_CURSOR_HAND 
  
  def draw(self):
    super().draw()
    self.pygame_instance.draw.rect(self.surface, [100, 100, 100], self.rect)





def main():
  screen = pygame.display.set_mode([500, 500])
  pss = PSS(screen, pygame)
  b = pss.addComponent(Button)
  b.onclick(quit_game)

  app_run = True
  while app_run:
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        app_run = False
      pss.sendEvent(e)

    screen.fill([0,0,0])
    pygame.draw.circle(screen, (0, 0, 255), (100, 100), 50)
    
    pss.update()

    pygame.display.flip()
    pygame.time.delay(30)

  pygame.quit()

def quit_game():
  pygame.quit()

if __name__ == "__main__":
  main()