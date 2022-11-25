import pygame

pygame.init()

class PSS:
  def __new__(cls):
    if not hasattr(cls, 'instance'):
        cls.instance = super(PSS, cls).__new__(cls)
    return cls.instance
  def __init__(self, pygame_instance):
    self.pygame = pygame_instance
    self.surface = surface
    self.components = []

  def addComponent(self, component):
    self.components.append(component)

  def sendEvent(self, e):
    for component in self.components:
      component.sendEvent(e)

class Component:
  def __init__(self, surface, pygame_instance, left=0, top=0, width=0, height=0):
    self.pygame_instance = pygame_instance
    self.surface = surface
    self.rect = pygame_instance.Rect(left, top, width, height)
    self.clicked = None

  def sendEvent(self, e):
    if e.type == self.pygame_instance.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(e.pos):
        if self.clicked is not None:
          self.clicked()
    if e.type == self.pygame_instance.MOUSEMOTION:
      if self.rect.collidepoint(e.pos):
        self.pygame_instance.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

  def onclick(self, callback):
    self.clicked = callback

class Button(Component):
  def __init__(self, surface, pygame_instance, left=0, top=0, width=0, height=0):
    super().__init__(surface, pygame_instance, left, top, width, height)
  
  def draw(self):
    self.pygame_instance.draw.rect(self.surface, [100, 100, 100], self.rect)





def main():
  screen = pygame.display.set_mode([500, 500])
  b = Button(screen, pygame, 100, 100, 100, 20)

  app_run = True
  while app_run:
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        app_run = False
      b.sendEvent(e)

    screen.fill([0,0,0])
    pygame.draw.circle(screen, (0, 0, 255), (100, 100), 50)
    
    b.draw()
    b.onclick(quit_game)

    pygame.display.flip()
    pygame.time.delay(100)

  pygame.quit()

def quit_game():
  pygame.quit()

if __name__ == "__main__":
  main()