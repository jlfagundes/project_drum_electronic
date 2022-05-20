# importanto pygame e mixer
from tkinter import W
import pygame
from pygame import mixer 

# inicializando o pygame
pygame.init()

# configurando a tela
WIDTH = 1400
HEIGHT = 800

# adicioando cores
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# criando a tela e definindo a legenda
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Electronic Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)

# taxa de quadros
fps = 60
timer = pygame.time.Clock()

def draw_grid():
  # rect(display, cor, [posição e altura], espessura da borda)
  lef_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
  bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
  boxes = []
  # biblioteca de cores
  colors = [gray, white, gray]

  # botão dos instrumentos
  hi_hat_text = label_font.render('Hi Hat', True, white)
  # blit(texto, posição) renderiza o texto na tela
  screen.blit(hi_hat_text, (30, 30))
  snare_text = label_font.render('Snare', True, white)
  screen.blit(snare_text, (30, 130))
  kick_text = label_font.render('Bass Drum', True, white)
  screen.blit(kick_text, (30, 230))
  crash_text = label_font.render('Crash', True, white)
  screen.blit(crash_text, (30, 330))
  clap_text = label_font.render('Clap', True, white)
  screen.blit(clap_text, (30, 430))
  floor_text = label_font.render('Floor Tom', True, white)
  screen.blit(floor_text, (30, 530))

  # craindo linhas
  for i in range(6):
    # line(tela, cor, inicia da linha, fim da linha, espessora da linha)
    pygame.draw.line(screen, gray, (0, (i * 100) +100), (200, (i * 100) + 100), 5)



# variavel de execução
run = True
while run:
  timer.tick(fps)
  screen.fill(black)

  # grade de desenho
  draw_grid()

  # manipulação de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  pygame.display.flip()
pygame.quit()

