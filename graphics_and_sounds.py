from pygame import image, mixer
mixer.init()

# grafika
icon = image.load("simba.ico")
cursor_1 = image.load("sprites/cursor_1.png")
cursor_2 = image.load("sprites/cursor_2.png")
start_background = image.load("backgrounds/start.png")
tutorial_background = image.load("backgrounds/how_to_play.png")
pridelands = image.load("backgrounds/1-1.png")
simba_lives = image.load("sprites/simba/lives.png")
ryan_lives = image.load("sprites/ryan/lives.png")
heart = image.load("sprites/heart.png")
simba_victory = image.load("backgrounds/game_completed.png")
simba_cry = image.load("backgrounds/game_over.png")

# sprite'y
tile1 = image.load("sprites/tiles/1.png")
tile2 = image.load("sprites/tiles/2.png")
tile3 = image.load("sprites/tiles/3.png")
tile4 = image.load("sprites/tiles/4.png")
tile5 = image.load("sprites/tiles/5.png")
tile6_1 = image.load("sprites/tiles/6_1.png")
tile6_2 = image.load("sprites/tiles/6_2.png")
tile9 = image.load("sprites/tiles/9.png")
tileA = image.load("sprites/tiles/A.png")
tileB1 = image.load("sprites/tiles/B1.png")
tileB2 = image.load("sprites/tiles/B2.png")
tileB3 = image.load("sprites/tiles/B3.png")
tileB4 = image.load("sprites/tiles/B4.png")
tileC = image.load("sprites/tiles/C.png")
tileD = image.load("sprites/tiles/D.png")
tileE = image.load("sprites/tiles/E.png")
tileF = image.load("sprites/tiles/F.png")
tileG = image.load("sprites/tiles/G.png")
tileH = image.load("sprites/tiles/H.png")
tileI1 = image.load("sprites/tiles/I1.png")
tileI2 = image.load("sprites/tiles/I2.png")
tileI3 = image.load("sprites/tiles/I3.png")
tileI4 = image.load("sprites/tiles/I4.png")
tileJ = image.load("sprites/tiles/J.png")
tileK = image.load("sprites/tiles/K.png")
tileL = image.load("sprites/tiles/L.png")
tileM = image.load("sprites/tiles/M.png")
tileN = image.load("sprites/tiles/N.png")
tileP = image.load("sprites/tiles/P.png")
tileS1 = image.load("sprites/tiles/S1.png")
tileS2 = image.load("sprites/tiles/S2.png")
tileW = image.load("sprites/tiles/W.png")

# efekty dźwiękowe
sel_sound = mixer.Sound("sfx/select.mp3")
my_sound = mixer.Sound("sfx/950_1024.mp3")
jump = mixer.Sound("sfx/jump.mp3")
roar = mixer.Sound("sfx/roar.mp3")
spin = mixer.Sound("sfx/spin.mp3")
ring = mixer.Sound("sfx/ring.mp3")
power_up = mixer.Sound("sfx/power_up.mp3")
one_up = mixer.Sound("sfx/1up.mp3")
defeat = mixer.Sound("sfx/defeat.mp3")
hurt = mixer.Sound("sfx/hurt.mp3")
death = mixer.Sound("sfx/die.mp3")
game_over = mixer.Sound("sfx/game_over.mp3")
lvl_complete = mixer.Sound("sfx/level_completed.mp3")
game_complete = mixer.Sound("sfx/game_completed.mp3")

# speed values
PLAYER_SPEED = 2
PLAYER_UNDERWATER_SPEED = 1
PLATFORM_SPEED = 0.1
ENEMY_SPEED = 0.05

intro_text = '''THIS IS AN ALTERNATE SIMBA\'S STORY.
ONE DAY SIMBA AND NALA WERE PLAYING HIDE AND SEEK.
SUDDENLY, THEY BOTH HEARD A LOUD CRY. THEY LOOKED
AROUND AND FOUND TWO HYENA CUBS TANGLED IN THORNS.
THE YOUNG LIONS KNEW HYENAS ARE LIONS\' ENEMIES,
HOWEVER THEY JUST COULDN\'T LOOK AT TWO SUFFERING
INNOCENT BEINGS. THEY HELPED HYENA CUBS TO GET
OUT OF THE THORNS. THE YOUNG HYENAS THANKED SIMBA
AND NALA AND SUGGESTED TO PLAY TOGETHER.

PRESS ENTER TO BEGIN THE ADVENTURE.
'''
