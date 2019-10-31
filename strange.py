import board
import neopixel
import random
import time
import MySQLdb as mariadb
import math
from itertools import chain

PIXEL_PIN	= board.D18
LED_COUNT	= 100
ORDER		= neopixel.RGB
BRIGHTNESS	= 0.5

#Alphabet
ALPHABET = '***********************z**y*x***w**v*u*t*s*r*****ij*k*l*m**n*o*p***q**********h**g*f**e***dc**b*a***'

#Predefined Colors and Masks
OFF	= (0,0,0)
WHITE	= (255,255,255)
RED 	= (255,0,0)
GREEN	= (0,255,0)
BLUE	= (0,0,255)
PURPLE	= (128,0,128)
YELLOW	= (255,255,0)
ORANGE	= (255,50,0)
TURQUOISE = (64,224,208)

#list of colors, tried to match the show as close as possible
COLORS = (YELLOW, BLUE, PURPLE, RED, ORANGE, TURQUOISE, GREEN, YELLOW, BLUE, PURPLE, RED, ORANGE, TURQUOISE, GREEN,
  YELLOW, BLUE, PURPLE, RED, ORANGE, TURQUOISE, GREEN, YELLOW, BLUE, PURPLE, RED, ORANGE)


def main():
  initialize()
  routineTurnAllOnThenOff()
  while True:
    doNextThing()
    pauseBetweenPhrases()

def doNextThing():
  latestFromDb = getLatestFromDb()
  if (latestFromDb is not None):
    if (latestFromDb == 'run'):
      dbCursor = db.cursor()
      dbCursor.execute('DELETE FROM phrases WHERE phrase="run" ')   # clear it out
      db.commit()
      dbCursor.close()
      return routineRun()

    for i in range(1):
      routineShowWord(latestFromDb)
      pauseBetweenPhrases()
    routineShowWord(latestFromDb)
    return

  # no new SQL. Business as usual
  randomPercent = random.randint(1, 100)

  if (randomPercent < 75):
    return routineShowWord(getRandomGenerated())
  elif (randomPercent < 85):
    randomWord = getRandomFromDb()
    if (randomWord is not None):
      return routineShowWord(randomWord)
    else:
      return routineShowWord(getRandomPredefined())
  elif (randomPercent < 90):
    return routineTurnAllOnThenOff()
  elif (randomPercent < 92):
    return routineRun()
  else:
    return routineShowWord(getRandomPredefined())

def initialize():
  global leds
  leds = neopixel.NeoPixel(PIXEL_PIN, LED_COUNT, brightness=BRIGHTNESS,auto_write=False, pixel_order=ORDER)
  random.seed()

  global db;
  db = mariadb.connect(database="stranger", user="stranger", passwd="danger")

  global lastSqlid
  dbCursor = db.cursor()
  dbCursor.execute('SELECT id FROM phrases WHERE 1 ORDER BY id DESC LIMIT 1')
  lastRow = dbCursor.fetchone()
  dbCursor.close()
  if (lastRow is None):
    lastSqlid = 0
  else:
    lastSqlid = lastRow[0]
  

def routineShowWord(word):
  print(word)
  for letter in word:
    if letter in ALPHABET:
      subroutineLightUpLetter(letter)
    else:
      pauseBetweenWords()

def routineRun():
  word = 'run'
  routineShowWord(word)

  for loop in range(20):  # blink all 3 lights frantically
    for letter in word:
      if letter in ALPHABET:
        leds[getPosOfLetter(letter)] = getColorOfLetter(letter)
    leds.show()
    time.sleep(random.uniform(0.05, 0.2))
    for letter in word:
      if letter in ALPHABET:
        leds[getPosOfLetter(letter)] = OFF
    leds.show()
    time.sleep(random.uniform(0.05, 0.2))

  subroutinePulsateAllLights()
  clearAll()

def routineTurnAllOnThenOff():
  subroutineTurnAllOn()
  time.sleep(5)
  subroutineTurnAllOffRandomly()
  time.sleep(20)

def subroutineLightUpLetter(letter):
  if (random.randint(1, 15) == 1):
    return effectPulsateLetter(letter)
  if (random.randint(1, 20) == 1):
    return effectHardFlickerLetter(letter)
  if (random.randint(1, 20) == 1):
    return effectSoftFlickerLetter(letter)
  return effectBlinkLetter(letter)

def subroutineTurnAllOn():
  for letter in ALPHABET:
    pos = getPosOfLetter(letter)
    if (pos < 1):
      continue;
    leds[pos] = getColorOfLetter(letter)
  leds.show()

def subroutineTurnAllOffRandomly():
  randomOrder = list(ALPHABET)
  random.shuffle(randomOrder)
  for letter in randomOrder:
    pos = getPosOfLetter(letter)
    if (pos < 1):
      continue;
    leds[pos] = OFF
    leds.show()
    time.sleep(random.uniform(0, 0.3))

def subroutinePulsateAllLights():
  for cycles in range(random.randint(10, 17)):
    for i in range(2,178):
      modifier = abs(math.sin(math.radians(i)))
      for letter in ALPHABET:
        pos = getPosOfLetter(letter)
        if (pos < 1):
          continue;
        newColor = list()
        for normalColor in getColorOfLetter(letter):
          newColor.append(round(normalColor * modifier))
        leds[pos] = newColor

      leds.show()
      time.sleep(0.001)
      leds.fill(OFF)

def getPosOfLetter(letter):
  letter = letter.lower()
  return ALPHABET.find(letter)

def getColorOfLetter(letter):
  letter = letter.lower()
  pos = ALPHABET.replace('*', '').find(letter)
  if pos < 0:
    return OFF
  return COLORS[pos]

def turnOn(letter):
  leds[getPosOfLetter(letter)] = getColorOfLetter(letter)
  leds.show()

def turnOff(letter):
  leds[getPosOfLetter(letter)] = OFF
  leds.show()

def clearAll():
  leds.fill(OFF)
  leds.show()

def effectBlinkLetter(letter):
  turnOn(letter)
  pauseBeforeLightOff()
  turnOff(letter)
  pauseBetweenLetters()

def effectHardFlickerLetter(letter):
  for i in range(random.randint(7, 15)):
    if (i % 2 == 1):
      turnOn(letter)
      time.sleep(random.uniform(0.1, 0.4))
    else:
      turnOff(letter)
      time.sleep(random.uniform(0.05, 0.2))

  turnOff(letter)
  pauseBetweenLetters()

def effectSoftFlickerLetter(letter):
  for i in range(random.randint(10, 20)):
    modifier = random.uniform(0.1, 1)
    newColor = list()
    for normalColor in getColorOfLetter(letter):
      newColor.append(round(normalColor * modifier))
    leds[getPosOfLetter(letter)] = newColor
    leds.show()
    time.sleep(random.uniform(0.05, 0.2))

  turnOff(letter)
  pauseBetweenLetters()

def effectPulsateLetter(letter):
  for cycles in range(random.randint(2, 6)):
    for i in chain(range(15,90), range(91,165)):
      modifier = abs(math.sin(math.radians(i)))
      newColor = list()
      for normalColor in getColorOfLetter(letter):
        newColor.append(round(normalColor * modifier))
      leds[getPosOfLetter(letter)] = newColor
      leds.show()
      time.sleep(0.002)

  turnOff(letter)
  pauseBetweenLetters()

def pauseBeforeLightOff():
  time.sleep(random.uniform(1, 2.5))

def pauseBetweenLetters():
  time.sleep(random.uniform(0.5, 1.25))

def pauseBetweenWords():
  time.sleep(random.uniform(1, 2.75))

def pauseBetweenPhrases():
  time.sleep(random.uniform(5, 10))

def getRandomPredefined():
  return random.choice((
    'elevens eggos',
    'joyce byers',
    'the upside down',
    'happy halloween',
    'michael myers',
    'friday the thirteenth',
    'a nightmare on edwards st',
    'wutang forever',
    'trevor belmont',
    'castlevania',
    'welcome to heck',
    'texas chainsaw massacre',
    'nancy wheeler',
    'abandon hope',
    'theyre here',
    'i see dead people',
    'fava beans and a nice chianti',
    'its alive',
    'were gonna get you'
  ))

def getRandomGenerated():
  verbs = (
    'beware the',
    'watch out for the',
    'stab the',
    'avoid the',
    'run from the',
    'bury the',
    'night of the',
    'return of the',
    'curse of the',
    'you must kill the',
    'godzilla vs',
    'invasion of the',
    'revenge of the',
    'follow the',
    'the secret of the',
    'dont trust the',
    'half man half',
    'abbott and costello meet the',
    'cult of the',
    'fear the',
    'lair of the',
    'tomb of the',
    'crypt of the',
    'mansion of the',
    'orgy of the',
    'house of the',
    'unfreeze the',
    'dont wake the',
    'see the',
    'witness the',
    'awaken the',
    'you awoke the',
    'release the',
    'web of the',
    'plague of the',
    'obey the',
    'message from the',
    'heart of the',
    'draculas pet',
    'legend of the',
    'fangs of the',
    'party with the',
    'vault of the',
    'arise'
  )
  adjectives = (
    'haunted',
    'scary',
    'terrifying',
    'sinister',
    'terrible',
    'eerie',
    'ghoulish',
    'nasty',
    'bloody',
    'spooky',
    'electric',
    'undead',
    'radioactive',
    'creepy',
    'evil',
    'gruesome',
    'hideous',
    'flying',
    'mecha',
    'robot',
    'decapitated',
    'demonic',
    'crazy',
    'insane',
    'rabid',
    'retarded',
    'deadly',
    'toxic',
    'horrible',
    'dreadful',
    'ghastly',
    'grim',
    'heinous',
    'horrid',
    'shocking',
    'obnoxious',
    'repulsive',
    'revolting',
    'unholy',
    'horrifying',
    'fearsome',
    'vile',
    'gothic',
    'satanic',
    'sadistic',
    'gigantic',
    'annoying',
    'slimey',
    'violent',
    'malevolent',
    'samurai',
    'headless',
    'invisible',
    'metallic',
    'demented',
    'baby',
    'floating',
    'man eating',
    'cryptic',
    'ancient',
    'insane clown',
    'rattling',
    'tormented',
    'possessed',
    'putrid',
    'funky',
    'mad',
    'voodoo',
    'decaying',
    'rotting',
    'plagued',
    'maggot infested',
    'infested',
    'repugnant',
    'cackling',
    'bizzaro',
    'insane clown',
    'cloaked',
    'paranormal'
  )
  nouns = (
    'werewolf',
    'vampire',
    'republicans',
    'living dead',
    'ghosts',
    'goblins',
    'ghoul',
    'mummy',
    'monster',
    'psychopath',
    'spider',
    'snakes',
    'boogeyman',
    'zombies',
    'bats',
    'skeletons',
    'witch coven',
    'witch',
    'dracula',
    'slenderman',
    'clowns',
    'demon',
    'corpse',
    'cannibals',
    'maniacs',
    'fishman',
    'gerbils',
    'gremlins',
    'jerkwads',
    'spirit',
    'phantom',
    'witch doctor',
    'puppet master',
    'specter',
    'vulture',
    'scarecrow',
    'bigfoot',
    'mannequin',
    'troll',
    'horseman',
    'mermaid',
    'chupacabra',
    'banshee',
    'poltergeist',
    'sheet ghost',
    'alligator',
    'gorilla',
    'octopus',
    'devil',
    'creature',
    'pirate',
    'gargoyle',
    'slime',
    'cyclops',
    'skull',
    'madman',
    'reaper',
    'gatekeeper',
    'mutant',
    'wizard',
    'magician',
    'freaks',
    'graveyard',
    'sorcerer',
    'crypt',
    'sea monster',
    'gingerdead man',
    'shapeshifter',
    'tarantula', 
    'rattlesnake',
    'bees',
    'tentacles',
    'chainsaw hand',
    'mystery',
    'tomb',
    'serpent',
    'mole people',
    'claw',
    'castle',
    'monster manor',
    'cave',
    'virus',
    'hellhound',
    'orcs',
    'elves',
    'trolls',
    'hobgoblins',
    'sharknado',
    'lobsterman',
    'spooktacular',
    'exorcist',
    'chainsaw hookers',
    'boys and ghouls',
    'sea creature',
    'alchemist',
    'ventriloquist',
    'slugs',
    'mind taker',
    'mind flayer',
    'cenobites',
    'necrophiliac',
    'old gypsy lady',
    'skeletor',
    'skeleton army',
    'footclan ninjas',
    'cacodemon',
    'black cat',
    'space pirates'
  )
  if (random.randint(1,7) == 1):
    if (random.randint(1,75) <= 75):
      return random.choice(verbs) + ' ' + random.choice(adjectives) + ' ' + random.choice(nouns)
    else:
      return random.choice(verbs) + ' ' + random.choice(nouns)

  if (random.randint(1,25) == 1):
    return random.choice(nouns) + ' vs ' + random.choice(nouns)

  return random.choice(adjectives) + ' ' + random.choice(nouns)

def getLatestFromDb():
  global lastSqlid

  dbCursor = db.cursor()
  dbCursor.execute('SELECT * FROM phrases WHERE id > %s ORDER BY id ASC LIMIT 1', (lastSqlid,))
  latestRow = dbCursor.fetchone()
  dbCursor.close()

  if (latestRow is None):
    return latestRow

  if (latestRow[0] > lastSqlid): # should always be
    lastSqlid = latestRow[0]

  return latestRow[1]
  


def getRandomFromDb():
  dbCursor = db.cursor()
  dbCursor.execute('SELECT phrase FROM phrases WHERE 1 ORDER BY RAND() LIMIT 1')
  randomRow = dbCursor.fetchone()
  dbCursor.close()

  if (randomRow is None):
    return randomRow

  return randomRow[0]

## main
if __name__ == '__main__':
  main()
