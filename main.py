# importanto pygame e mixer
from pydoc import cli
from tkinter import EventType
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
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

# criando a tela e definindo a legenda
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Electronic Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)

# taxa de quadros
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
# lista de beats
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True

def draw_grid(clicks, beat):
  # rect(display, cor, [posição e altura], espessura da borda, arredondamento do canto)
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
  for i in range(instruments):
    # line(tela, cor, inicia da linha, fim da linha, espessora da linha)
    pygame.draw.line(screen, gray, (0, (i * 100) +100), (200, (i * 100) + 100), 5)

  # criando retangulos para as batidas
  for i in range(beats):
    for j in range(instruments):
      if clicks[j][i] == -1:
        color = gray
      else:
        color = green

      rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5,
        ((WIDTH - 200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)

      pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
        ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 5, 5)

      pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
        ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 2, 5)

      # armazenando os rectangulos, nos boxes, com posição de linha (i) e coluna (j)
      boxes.append((rect, (i, j)))

    # linha para saber a batida que esta tocando
    active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0,
      ((WIDTH - 200) // beats), instruments * 100], 5, 3)
  return boxes



# variavel de execução
run = True
while run:
  timer.tick(fps)
  screen.fill(black)

  # grade de desenho
  boxes = draw_grid(clicked, active_beat)

  # verificar click nas boxes


  # manipulação de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      for i in range(len(boxes)):
        # pegando as coordenadas do mouse usando função collidepoint()
        if boxes[i][0].collidepoint(event.pos):
          coords = boxes[i][1]
          # lista de beats clicked
          clicked[coords[1]][coords[0]] *= -1

  # controle de duração de batida
  beat_length = 3600 // bpm

  # if estiver jogando então
  if playing:
    if active_length < beat_length:
      active_length += 1
    else:
      active_length = 0
      if active_beat < beats - 1:
        active_beat += 1
        beat_changed = True
      else:
        active_beat = 0
        beat_changed = True

  
  pygame.display.flip()
pygame.quit()

