import time
from blessed import Terminal
from playsound import playsound
import random
from pygame import mixer
from pygame import time as pygtime
from inputimeout import inputimeout, TimeoutOccurred
import math
import sys

terminal = Terminal()  # Emulator for the terminal to make it compatible with animations played
global chapter  # Keeps track of what chapter the player is on
global has_key  # Keeps track of if the user has treasure key or not
global volume  # Sets music volume
global four_digit_code  # Four-digit code for Room 2
global has_weapon  # Keeps track of if the user has a weapon or not
global has_code  # Keeps track of it the user has the 4-digit code or not
global player_weapon  # Stores what weapon the player gets

mixer.init()  # Initializes the music player


# Typewriting Animation
def typewrite(msg, delay=0.05):
    with terminal.cbreak():
        for char in msg:
            print(char, end='', flush=True)
            time.sleep(delay)
        print('')


# Makes sure input is an integer
def read_int(var):
    try:
        var = int(var)
        return True
    except ValueError:
        return False


# Game over scene
def game_over():
    print(''' @@@@@                                        @@@@@
@@@@@@@                                      @@@@@@@
@@@@@@@           @@@@@@@@@@@@@@@            @@@@@@@
 @@@@@@@@       @@@@@@@@@@@@@@@@@@@        @@@@@@@@
     @@@@@     @@@@@@@@@@@@@@@@@@@@@     @@@@@
       @@@@@  @@@@@@@@@@@@@@@@@@@@@@@  @@@@@
         @@  @@@@@@@@@@@@@@@@@@@@@@@@@  @@
            @@@@@@@    @@@@@@    @@@@@@
            @@@@@@      @@@@      @@@@@
            @@@@@@      @@@@      @@@@@
             @@@@@@    @@@@@@    @@@@@
              @@@@@@@@@@@  @@@@@@@@@@
               @@@@@@@@@@  @@@@@@@@@
           @@   @@@@@@@@@@@@@@@@@   @@
           @@@@  @@@@ @ @ @ @ @@@@  @@@@
          @@@@@   @@@ @ @ @ @ @@@   @@@@@
        @@@@@      @@@@@@@@@@@@@      @@@@@
      @@@@          @@@@@@@@@@@          @@@@
   @@@@@              @@@@@@@              @@@@@
  @@@@@@@                                 @@@@@@@
   @@@@@                                   @@@@@''')
    print()
    playsound('audio/dead.wav')
    typewrite('GAME OVER.', 0.2)
    sys.exit()


# Pauses music with a fade effect
def pause_fade_music(sec):
    global volume
    volume = 1.0
    num_times = sec * 100
    volume_reduction_per_ms = volume / num_times
    for i in range(int(num_times)):
        volume -= volume_reduction_per_ms
        mixer.music.set_volume(volume)
        pygtime.wait(10)

    mixer.music.pause()


# Resumes music with a fade effect
def unpause_fade_music(sec):
    global volume
    volume = 0.0
    num_times = sec * 100
    volume_increase_per_ms = 1.0 / num_times
    mixer.music.unpause()
    for i in range(int(num_times)):
        volume += volume_increase_per_ms
        mixer.music.set_volume(volume)
        pygtime.wait(10)

    volume = 1.0
    mixer.music.set_volume(volume)


# Stops music with a fade effect
def stop_fade_music(sec):
    global volume
    volume = 1.0
    num_times = sec * 100
    volume_reduction_per_ms = volume / num_times
    for i in range(int(num_times)):
        volume -= volume_reduction_per_ms
        mixer.music.set_volume(volume)
        pygtime.wait(10)

    mixer.music.stop()


# Smoothly changes the volume of the music
def change_fade_volume(target_volume, sec):
    current_volume = mixer.music.get_volume()
    num_times = sec * 100
    volume_change_per_ms = (target_volume - current_volume) / num_times
    for i in range(num_times):
        current_volume += volume_change_per_ms
        mixer.music.set_volume(current_volume)
        pygtime.wait(10)


# Treasure key scene for whenever user finds the treasure key
def key_scene():
    typewrite('It is a small key, but it has grand design.')
    typewrite("The handle is shaped like a dragon head's, with ruby eyes and silver scales.")
    typewrite('The teeth are extremely ornate, forming a complex pattern that matches a lock of a vault.')
    typewrite('The key is made of gold, but it has signs of age.')
    typewrite('It feels heavy and cold in your hand, as if it holds great power.')
    time.sleep(2)
    typewrite('After a few seconds of touching the key, you feel a jolt of electricity run through your '
              'body.')
    typewrite('The world around you is blurring and fading, being replaced by a swirling vortex of '
              'colours and sounds.')
    typewrite('You lose your sense of direction and time, employing only a sense of being pulled by an '
              'invisible force.')
    time.sleep(2)
    typewrite('Then suddenly, the vortex stops, and you find yourself at a different place.')


# Class for the whole game!
class Game:
    # Class for room choice stage containing the function that initiates the stage
    class ChoiceStage:
        # The choice stage
        @staticmethod
        def room_choice_scene():
            global chapter

            unpause_fade_music(2.5)

            print(''' __________
|  __  __  |
| |  ||  | |
| |  ||  | |
| |__||__| |
|  __  __()|
| |  ||  | |
| |  ||  | |
| |  ||  | |
| |  ||  | |
| |__||__| |
|__________|''')
            typewrite(f'Chapter {chapter}: Six Rooms, One Choice')
            time.sleep(2)
            typewrite('After taking several long breaths, you finally gather enough courage to push open the old, '
                      'rusty metal door and step into the entrance.')
            typewrite('Apart from the unusual scent of oak filling the building, the first thing you notice is a path '
                      'leading to six different rooms.')
            typewrite("Since it's dark, you cannot see what is inside the room from a distance.")
            typewrite('You must decide what room to enter first.')
            typewrite('Enter a number between 1-6 to decide what room to enter:')
            chosen_room = 0
            rooms = [1, 2, 3, 4, 5, 6]
            while chosen_room not in rooms:
                chosen_room = input('> ')
                if read_int(chosen_room):
                    chosen_room = int(chosen_room)
                if chosen_room == 1:
                    print()
                    stop_fade_music(2.5)
                    room_1 = game.Room1()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_1.lantern_scene()
                elif chosen_room == 2:
                    print()
                    stop_fade_music(2.5)
                    room_2 = game.Room2()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_2.north_or_south_scene()
                elif chosen_room == 3:
                    print()
                    stop_fade_music(2.5)
                    room_3 = game.Room3()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_3.ask_for_code_scene()
                elif chosen_room == 4:
                    print()
                    stop_fade_music(2.5)
                    room_4 = game.Room4()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_4.check_weapon_scene()
                elif chosen_room == 5:
                    print()
                    stop_fade_music(2.5)
                    room_5 = game.Room5()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_5.weapon_roll_scene()
                elif chosen_room == 6:
                    print()
                    stop_fade_music(2.5)
                    room_6 = game.Room6()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_6.ask_for_key_scene()
                else:
                    typewrite('Please enter a valid option.', 0.01)

    # Class for all the scenes for Room 1
    class Room1:
        # Lantern scene
        def lantern_scene(self):

            mixer.music.load('audio/music/library.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            print('''    _______
   /      /,
  /      //
 /______//
(______(/''')
            global chapter
            typewrite(f'Chapter {chapter}: The Library')
            time.sleep(2)
            typewrite('A void of nothingness surrounds you, or that is what you feel like.')
            typewrite('It is pitch black.')
            typewrite('You decide to take a walk around and find a light switch to get rid of this abyssal darkness.')
            typewrite('After a few minutes of walking here and there, a luminous object grabs your attention.')
            typewrite('You decide to draw closer to the object.')
            typewrite('Just being a few metres away, you can see a glowing lantern sitting on a desk.')
            typewrite('This may be useful for navigating your way.')
            typewrite('Do you want to pick up the lantern? [yes/no]')
            pick_lantern = ''
            options = ['yes', 'no', 'y', 'n']
            while pick_lantern not in options:
                pick_lantern = input('> ').lower()
                if pick_lantern == 'yes' or pick_lantern == 'y':
                    print()
                    time.sleep(1)
                    self.book_scene()
                elif pick_lantern == 'no' or pick_lantern == 'n':
                    print()
                    time.sleep(1)
                    self.skeleton_scene()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Book scene if user chooses to pick up lantern
        def book_scene(self):
            typewrite('You choose to pick up the lantern.')
            typewrite('You can now see your surroundings as far as the lantern shines.')
            typewrite('Exploring around with the lantern, you now see another luminous object.')
            typewrite('The light is purple and is coming from one of the books in the endless shelves of the library.')
            typewrite('The book stands out from the others, and it looks eerie. ')
            time.sleep(1)
            typewrite('You decide to go closer.')
            time.sleep(1)
            typewrite('The book does look beautiful, but you feel like it radiates a sinister aura that is chilling '
                      'the air.')
            typewrite('Do you want to pick up the book and see what is inside? [yes/no]')
            pick_book = ''
            options = ['yes', 'no', 'y', 'n']
            while pick_book not in options:
                pick_book = input('> ').lower()
                if pick_book == 'yes' or pick_book == 'y':
                    print()
                    time.sleep(1)
                    self.map_scene()
                elif pick_book == 'no' or pick_book == 'n':
                    print()
                    time.sleep(1)
                    self.monster_scene()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Map scene if user chooses to pick up book
        @staticmethod
        def map_scene():
            global chapter
            typewrite('As soon as you touch the book, it sends a chill down your spine.')
            typewrite('You open the book.')
            change_fade_volume(0.5, 1)
            playsound('audio/turn.wav')
            change_fade_volume(1.0, 1)
            time.sleep(1)
            typewrite('You see a strange illustration on the dusty, nice-smelling front page.')
            typewrite('It takes a second for your brain to register that it is a map outlining the way for Room 2.')
            typewrite("Doesn't this make the job easier?")
            print()
            stop_fade_music(2.5)
            room_2 = game.Room2()
            chapter += 1
            playsound('audio/tran.wav')
            time.sleep(1)
            room_2.north_or_south_scene()

        # Monster scene if the user does not pick up book
        @staticmethod
        def monster_scene():
            global chapter
            typewrite('You back off from the shelf holding the book.')
            typewrite('You decide to explore for a little bit more.')
            typewrite('Just as you are decide to move out from the library, you hear footsteps coming from enormous '
                      'feet.')
            change_fade_volume(0.5, 1)
            playsound('audio/mfo1.wav')
            typewrite('THUMP!', 0.1)
            time.sleep(1)
            playsound('audio/mfo2.wav')
            typewrite('THUMP!', 0.2)
            time.sleep(1)
            playsound('audio/mfo1.wav')
            typewrite('THUMP!', 0.3)
            time.sleep(1)
            playsound('audio/mfo2.wav')
            playsound('audio/mvo1.wav')
            typewrite('Your brain tells you to flee from the room and just as you are thinking to do so, a grotesque '
                      'monster towers over your head.')
            playsound('audio/mvo2.wav')
            typewrite('Just as you are about to bolt to the exit, the monster tightly grasps your hand.')
            playsound('audio/mvo3.wav')
            typewrite('It gazes at your soul, and you feel like it is the end.')
            change_fade_volume(1.0, 2)
            typewrite('Guess a number between 1-2 to decide your fate, only one of them would be able to save you.')
            safe_num = random.randint(1, 2)
            player_num = 0
            options = [1, 2]
            while player_num not in options:
                player_num = input('> ')
                if read_int(player_num):
                    player_num = int(player_num)
                if player_num == safe_num:
                    time.sleep(1)
                    typewrite("You use all your strength to fight for your life and you finally manage to break free "
                              "from the monster's grip.")
                    typewrite('You bolt towards the exit and the monster tries to chase you.')
                    typewrite("You quickly push open the door and slam it on the monster's face.")
                    typewrite('You decide to find your way to Room 5.')
                    print()
                    stop_fade_music(2.5)
                    room_5 = game.Room5()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_5.weapon_roll_scene()
                elif player_num != safe_num and player_num in options:
                    time.sleep(1)
                    typewrite('Trying to do everything you can, the monster grasps your wrist harder and harder.')
                    typewrite('It finally opens its jaw, and you can see the gaping hole of misaligned teeth.')
                    time.sleep(1)
                    typewrite('It lowers its mouth towards your head.')
                    change_fade_volume(0.5, 2)
                    typewrite("Consequently, it snaps its mouth shut.", 0.1)
                    playsound('audio/mro1.wav')
                    stop_fade_music(1)
                    game_over()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Skeleton scene if the user does not pick up lantern
        def skeleton_scene(self):
            global has_key
            global chapter
            typewrite('Even though you decide to not pick up the lantern, you still explore around for some time.')
            time.sleep(1)
            typewrite('You start to regret your decision of not picking up the lantern as it is getting hard to '
                      'navigate around.')
            time.sleep(0.5)
            typewrite('But then your brain tells you that the lantern might have exposed your location to some '
                      'monsters.')
            time.sleep(1)
            typewrite('So... are you safe?', 0.2)
            time.sleep(1)
            typewrite('Just as you start to ponder about your safety, you bump into a hard object.')
            typewrite("It hurts quite a lot, but you don't really care about pain right now.")
            typewrite('All you care about right now is what you bumped into.')
            time.sleep(1)
            typewrite('It is very hard to see what the object is, so you try to see if rubbing your eyes will work.')
            typewrite('Then you start to make out the object as a creepy skeleton, sitting beside many others.')
            typewrite('You think to yourself, are these the skeletons of people who failed or refused to abandon this '
                      'clock tower and later got slaughtered by horrifying creatures?')
            time.sleep(2)
            typewrite('Will you join the skeletons...?', 0.2)
            time.sleep(3)
            typewrite('Suddenly, you feel one of the skeletons moving.')
            typewrite('At first, you think you are hallucinating, but then you change your mind.')
            time.sleep(1)
            typewrite('You step back and witness the skeleton standing up, ready to attack you.')
            time.sleep(0.5)
            typewrite('You have two choices: either to run or fight the skeleton.')
            typewrite('What do you want to do?')
            fight_or_run = ''
            options = ['fight', 'run', 'f', 'r']
            while fight_or_run not in options:
                fight_or_run = input('> ').lower()
                if fight_or_run == 'fight' or fight_or_run == 'f':
                    print()
                    time.sleep(1)
                    self.skeleton_fight_scene()
                elif fight_or_run == 'run' or fight_or_run == 'r':
                    print()
                    time.sleep(1)
                    typewrite('Your legs start shaking rapidly, and you choose to run.')
                    typewrite('When you are wandering outside the library, you see the entrance for Room 5.')
                    time.sleep(0.5)
                    typewrite('You choose to enter it.')
                    print()
                    stop_fade_music(2.5)
                    room_3 = game.Room3()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_3.ask_for_code_scene()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Skeleton fight scene if the user chooses to fight with the skeleton
        @staticmethod
        def skeleton_fight_scene():
            global chapter
            global has_key
            typewrite('You tell yourself you are not afraid of anything, and this skeleton is no big deal for you.')
            typewrite('You get into your attack position, ready to charge.')
            time.sleep(1)
            typewrite('The skeleton dashes towards you.')
            win_num = random.randint(1, 100)
            if win_num > 90:
                typewrite('Just like you thought, you easily beat the skeleton up.')
                time.sleep(1)
                typewrite('It looks like the skeleton is crying, even though there are no tears coming out.')
                time.sleep(0.5)
                typewrite("You hit your last blow, knocking the skeleton's skull.")
                typewrite('The skeleton falls over, and drops a key.')
                time.sleep(2)
                key_scene()
                print()
                stop_fade_music(2.5)
                room_6 = game.Room6()
                chapter += 1
                has_key = True
                playsound('audio/tran.wav')
                time.sleep(1)
                room_6.ask_for_key_scene()
            else:
                typewrite('You and the skeleton get into an endless fight.')
                time.sleep(0.5)
                typewrite('You wish you had brought some handy weapons to fight these stupid monsters.')
                typewrite('It seems like the skeleton is winning so far, since you have started to get exhausted.')
                typewrite('Suddenly, the skeleton grabs your neck, attempting to CHOKE you.')
                time.sleep(1)
                typewrite('You struggle to break free, and you are suffocating.')
                time.sleep(2)
                typewrite('You feel like it is the end, and regret even being in the clock tower.')
                time.sleep(2)
                typewrite('You start feeling dizzy, and you are on the verge of dying.', 0.1)
                stop_fade_music(2.5)
                time.sleep(2)
                game_over()

    # Class for all the scenes for Room 2
    class Room2:
        # Explore north part or south part scene
        def north_or_south_scene(self):

            mixer.music.load('audio/music/storeroom.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            print('''            ________
        _jgN########Ngg_
      _N##N@@""  ""9NN##Np_
     d###P            N####p
     "^^"              T####
                       d###P
                    _g###@F
                 _gN##@P
               gN###F"
              d###F
             0###F
             0###F
             0###F
             "NN@'

              ___
             q###r
              ""''')
            global chapter
            typewrite(f'Chapter {chapter}: The Storeroom')
            time.sleep(2)
            typewrite('The room feels a little empty, before you see a sign.')
            time.sleep(1)
            typewrite('It reads, "North or South?".')
            typewrite('There are also arrows pointing to each part of the room.')
            time.sleep(1)
            typewrite('It is unusual how you cannot check what is in each part before actually stepping in that part.')
            time.sleep(0.5)
            typewrite('Once you step in, there is no turning back.')
            time.sleep(1)
            typewrite('So, which part do you want to explore? [north/south]')
            north_or_south = ''
            options = ['north', 'n', 'south', 's']
            while north_or_south not in options:
                north_or_south = input('> ').lower()
                if north_or_south == 'north' or north_or_south == 'n':
                    print()
                    time.sleep(1)
                    self.code_scene()
                elif north_or_south == 'south' or north_or_south == 's':
                    print()
                    time.sleep(1)
                    self.weapon_scene()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Code scene if user wants to explore north part
        @staticmethod
        def code_scene():
            global four_digit_code
            global chapter
            global has_code
            typewrite('You step into the north part.')
            time.sleep(1)
            typewrite('Suddenly, a translucent wall forms behind you.')
            time.sleep(0.5)
            typewrite('You now cannot turn back.')
            time.sleep(0.5)
            typewrite('You see a piece of paper in front of you.')
            typewrite('You decide to go up to it and see what is written on it.')
            typewrite('It seems like it is some kind of 4-digit code.')
            time.sleep(1)
            typewrite('It is probably a good idea to remember it.')
            time.sleep(1)
            typewrite('Your 4-digit code is:')
            four_digit_code = str(random.randint(1000, 9999))
            typewrite(four_digit_code, 0.5)
            has_code = True
            time.sleep(2)
            typewrite('You are now able to step out of the room, ready to go to a new room where the code can be '
                      'utilised.')
            time.sleep(2)
            typewrite("You see a room labelled 'Puzzle Room'.")
            print()
            stop_fade_music(2.5)
            room_3 = game.Room3()
            chapter += 1
            playsound('audio/tran.wav')
            time.sleep(1)
            room_3.ask_for_code_scene()

        # Weapon scene if user wants to explore south part
        @staticmethod
        def weapon_scene():
            global has_weapon
            global chapter
            global player_weapon
            typewrite('You step into the south part.')
            time.sleep(1)
            typewrite('Suddenly, a translucent wall forms behind you.')
            time.sleep(0.5)
            typewrite('You now cannot turn back.')
            time.sleep(0.5)
            typewrite('You see a fascinating and powerful weapon in front of you.')
            time.sleep(1)
            typewrite('Suddenly, you feel much better about fighting any possible monsters.')
            time.sleep(0.5)
            typewrite('You decide to go up to it and pick the weapon up.')
            time.sleep(1)
            typewrite("The weapon is labelled 'Dragonfire Sword'.")
            has_weapon = True
            player_weapon = 'Dragonfire Sword'
            typewrite('You feel like you now hold great power, ready to fight anything that attempts to interrupt '
                      'your journey.')
            time.sleep(2)
            typewrite('You are now able to step out of the room, ready to go to a new room where the weapon can be '
                      'utilised to find the treasure.')
            time.sleep(2)
            typewrite("You see a room labelled 'Creature Room'.")
            print()
            stop_fade_music(2.5)
            room_4 = game.Room4()
            chapter += 1
            playsound('audio/tran.wav')
            time.sleep(1)
            room_4.check_weapon_scene()

    # Class for all the scenes for Room 3
    class Room3:
        # Scene where if user has code question is asked
        def ask_for_code_scene(self):
            mixer.music.load('audio/music/storeroom.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            print('''_________
|       (_
|        _)
|  _   _(
|_| |_|
|_| |_|''')
            global chapter
            global has_code
            typewrite(f'Chapter {chapter}: The Puzzle Room')
            time.sleep(2)
            typewrite('You have entered the puzzle room where your 4-digit code can be utilised.')
            time.sleep(2)
            typewrite('So... do you have the code? [yes/no]')
            user_has_code = ''
            options = ['yes', 'y', 'no', 'n']
            while user_has_code not in options:
                user_has_code = input('> ').lower()
                if (user_has_code == 'yes' and has_code) or (user_has_code == 'y' and has_code):
                    print()
                    time.sleep(1)
                    self.enter_code_scene()
                elif (user_has_code == 'no' and not has_code) or (user_has_code == 'n' and not has_code):
                    print()
                    time.sleep(1)
                    typewrite('Well... then you should not be here.')
                    typewrite('You are lucky that you are being let go without any consequences.')
                    time.sleep(2)
                    typewrite('You step out of the room.')
                    typewrite("You spot a room labelled 'Storeroom'.")
                    print()
                    stop_fade_music(2.5)
                    room_2 = game.Room2()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_2.north_or_south_scene()
                elif (user_has_code == 'yes' and not has_code) or (user_has_code == 'y' and not has_code):
                    print()
                    time.sleep(1)
                    typewrite('Haha... nice joke.')
                    time.sleep(1)
                    typewrite("I know you don't.", 0.1)
                    time.sleep(2)
                    typewrite('You are lucky that you are being let go without any consequences.')
                    time.sleep(2)
                    typewrite('You step out of the room.')
                    typewrite("You spot a room labelled 'Storeroom'.")
                    print()
                    stop_fade_music(2.5)
                    room_2 = game.Room2()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_2.north_or_south_scene()
                elif (user_has_code == 'no' and has_code) or (user_has_code == 'n' and has_code):
                    print()
                    time.sleep(1)
                    typewrite('Haha... nice joke.')
                    time.sleep(1)
                    typewrite('I know you do.', 0.1)
                    print()
                    time.sleep(1)
                    self.enter_code_scene()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Scene where code is entered
        @staticmethod
        def enter_code_scene():
            global four_digit_code
            global chapter
            global has_key
            typewrite('Great! So you have the code!')
            typewrite('It is time to enter it.')
            typewrite('Enter your code:')
            user_code = input('> ')
            if user_code == four_digit_code:
                print()
                time.sleep(1)
                typewrite('The code you entered is... correct!')
                time.sleep(1)
                typewrite('After a few seconds, a key drops in front of you.')
                time.sleep(2)
                key_scene()
                print()
                stop_fade_music(2.5)
                room_6 = game.Room6()
                chapter += 1
                has_key = True
                playsound('audio/tran.wav')
                time.sleep(1)
                room_6.ask_for_key_scene()
            else:
                print()
                time.sleep(1)
                typewrite('The code you entered is... INCORRECT!')
                time.sleep(2)
                typewrite('Suddenly, your heart starts beating rapidly.')
                typewrite('A horrifying monster teleports right in front of you.')
                time.sleep(1)
                typewrite('It is ready to give you the consequence of not entering the correct code.', 0.1)
                stop_fade_music(2.5)
                time.sleep(2)
                game_over()

    # Class for all the scenes in Room 4
    class Room4:
        # Scene where it is checked that the player actually has a weapon or not
        def check_weapon_scene(self):
            mixer.music.load('audio/music/creature1.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            print("""
 //`-||-'\\ 
(| -=||=- |)
 \\,-||-.// 
  `  ||  '  
     ||     
     ||     
     ||     
     ||     
     ||     
     ()""")

            global chapter
            global has_weapon
            typewrite(f'Chapter {chapter}: The Creature Room')
            time.sleep(2)
            typewrite('You enter the creature room, your legs shaking and your heart palpitating.')
            time.sleep(1)
            typewrite('You hear an unusual sound of thunderstorms.')
            typewrite('The environment is gloomy, and you feel like you are in peril.')
            time.sleep(1)
            typewrite('Suddenly, an enormous silhouette appears in the large middle part of the room. It is a '
                      'monster!!!')
            time.sleep(2)
            typewrite('It is huge and bigger than other monsters dwelling in this tower.')
            time.sleep(1)
            typewrite('You should keep your weapon ready with you, the monster may show you the path to treasure if '
                      'you defeat it.')
            time.sleep(2)
            if has_weapon:
                print()
                self.minigame_scene()
            else:
                print()
                self.no_weapon_scene()

        # Scene if player employs no weapon
        @staticmethod
        def no_weapon_scene():
            global chapter
            typewrite('Wait a minute... you do not have a weapon...')
            time.sleep(2)
            typewrite('Well... this is not going to be a great time for you.')
            time.sleep(1)
            typewrite("Don't worry, there is still some chance for you to survive.")
            time.sleep(0.5)
            typewrite('Guess a number between 1-6 to survive, only one of them will be able to save you.')
            safe_num = random.randint(1, 6)
            player_num = 0
            options = [1, 2, 3, 4, 5, 6]
            while player_num not in options:
                player_num = input('> ')
                if read_int(player_num):
                    player_num = int(player_num)
                if player_num == safe_num:
                    time.sleep(1)
                    typewrite('The number you guessed is... CORRECT!')
                    time.sleep(1)
                    typewrite('You bolt out of this room to search for a weapon.')
                    time.sleep(1)
                    typewrite('You see the weapon room.')
                    print()
                    stop_fade_music(2.5)
                    room_5 = game.Room5()
                    chapter += 1
                    playsound('audio/tran.wav')
                    time.sleep(1)
                    room_5.weapon_roll_scene()
                elif player_num != safe_num:
                    time.sleep(1)
                    typewrite('The number you guessed is... INCORRECT!')
                    time.sleep(1)
                    typewrite('The monster runs in front of you, and lifts its feet to crush you.')
                    time.sleep(1)
                    stop_fade_music(1)
                    game_over()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        # Scene if player employs a weapon
        @staticmethod
        def minigame_scene():
            global player_weapon
            global chapter
            global has_key
            typewrite('Great! You have your weapon in your hand, ready to attack the huge monster.')
            time.sleep(0.5)
            typewrite('You will play a minigame, you will only defeat the monster if you win.')

            typewrite('In the minigame, you will be asked to type words as quickly as you can since there will be a '
                      'timer.')
            time.sleep(0.5)
            typewrite('If you type the word correctly, the monster will be pushed away from you. The better weapon '
                      'you have, the farther you will be able to push the monster.')
            time.sleep(0.5)
            typewrite('If you type the word incorrectly or fail to type it on time, the monster will move closer to '
                      'you.')
            time.sleep(0.5)
            typewrite('If the monster gets too close, game over...')
            time.sleep(0.5)
            typewrite('However, you will defeat the monster if it is very far away.')

            words = ['attack', 'defend', 'dodge', 'block', 'charge', 'juke', 'counter', 'retreat', 'sweep', 'knock']
            time_2_type = 5.0
            monster_pos = 10
            push_vel = 0
            if player_weapon == 'Rusty Dagger':
                push_vel = 1
            elif player_weapon == 'Blunt Mace':
                push_vel = 2
            elif player_weapon == 'Poisoned Arrows':
                push_vel = 3
            elif player_weapon == 'Thunderbolt Spear':
                push_vel = 4
            elif player_weapon == 'Dragonfire Sword':
                push_vel = 5
            elif player_weapon == 'Celestial Hammer':
                push_vel = 6

            stop_fade_music(1)

            mixer.music.load('audio/music/creature2.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            typewrite('Get ready!', 0.01)
            time.sleep(1)
            typewrite('3!', 0.01)
            time.sleep(1)
            typewrite('2!', 0.01)
            time.sleep(1)
            typewrite('1!', 0.01)
            time.sleep(1)
            typewrite('GO!', 0.01)

            print(f'Monster distance from you: {monster_pos}')

            while monster_pos < 100:
                if monster_pos > 0 and time_2_type > 0:
                    print(f'You have {math.ceil(time_2_type)} seconds to type the word.')
                    word_2_type = random.choice(words)
                    print(f'\nType {word_2_type}:')
                    try:
                        user_input = inputimeout(prompt='> ', timeout=math.ceil(time_2_type))
                        if user_input == word_2_type:
                            print('\nYou typed the word correctly!')
                            monster_pos += push_vel
                        else:
                            print('\nYou typed the word incorrectly!')
                            monster_pos -= push_vel + 1
                    except TimeoutOccurred:
                        print('\nYou ran out of time!')
                        monster_pos -= push_vel + 1
                    print(f'\nMonster distance from you: {monster_pos}')
                    time_2_type -= 0.025
                elif monster_pos <= 0:
                    stop_fade_music(2)
                    typewrite('The monster is too close to you!!!')
                    time.sleep(2)
                    game_over()
                    break
                else:
                    stop_fade_music(2)
                    typewrite("You don't have any time to type the words!")
                    time.sleep(2)
                    game_over()
                    break

            time.sleep(2)
            typewrite("You have successfully defeated the enormous monster!!!")
            time.sleep(1)
            typewrite('The monster drops a key.', 0.1)
            time.sleep(2)
            key_scene()
            print()
            stop_fade_music(2.5)
            room_6 = game.Room6()
            chapter += 1
            has_key = True
            playsound('audio/tran.wav')
            time.sleep(1)
            room_6.ask_for_key_scene()

    # Class for all the scenes in Room 5
    class Room5:
        # Scene where user rolls dice to get a weapon
        @staticmethod
        def weapon_roll_scene():
            mixer.music.load('audio/music/creature1.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            print(r"""   _______
  /\ o o o\
 /o \ o o o\_______
<    >------>   o /|
 \ o/  o   /_____/o|
  \/______/     |oo|
        |   o   |o/
        |_______|/""")

            global chapter
            global has_weapon
            global player_weapon
            typewrite(f'Chapter {chapter}: The Weapon Room')
            time.sleep(2)
            typewrite('You have entered the weapon room.')
            time.sleep(1)
            typewrite('The room is almost empty, except the dice that is randomly on the floor.')
            typewrite('You will roll a dice and get a weapon based on what number you get.')
            time.sleep(0.5)
            typewrite('Each weapon does different damage.')
            time.sleep(1)
            typewrite('So... are you ready to roll the dice?')
            typewrite('Press enter to roll the dice.')
            input()
            typewrite('Rolling...')
            time.sleep(2)
            weapon_num = random.randint(1, 6)
            has_weapon = True
            if weapon_num == 1:
                player_weapon = 'Rusty Dagger'
                typewrite(f'You rolled a 1. So you get a {player_weapon}.')
                time.sleep(1)
                typewrite('This is not the best weapon to fight a possible monster...')
                time.sleep(0.5)
                typewrite('But at least you have a weapon now.')
            elif weapon_num == 2:
                player_weapon = 'Blunt Mace'
                typewrite(f'You rolled a 2. So you get a {player_weapon}.')
                time.sleep(1)
                typewrite('This may be able to fight any possible monsters... but it is blunt.')
                time.sleep(0.5)
                typewrite('But at least you have a weapon now.')
            elif weapon_num == 3:
                player_weapon = 'Poisoned Arrows'
                typewrite(f'You rolled a 3. So you get a {player_weapon}.')
                time.sleep(1)
                typewrite('This is pretty good for fighting monsters... but it does not have long range.')
                time.sleep(0.5)
                typewrite('You will need to get close to a monster to effective fight.')
            elif weapon_num == 4:
                player_weapon = 'Thunderbolt Spear'
                typewrite(f'You rolled a 4! So you get a {player_weapon}!')
                time.sleep(1)
                typewrite('This is a lightning charged spear that will deliver electric shocks to the monster.')
            elif weapon_num == 5:
                player_weapon = 'Dragonfire Sword'
                typewrite(f'You rolled a 5!! So you get a {player_weapon}!!')
                time.sleep(1)
                typewrite(
                    "This is a flaming sword infused with dragon's breath capable of burning anything it touches.")
            elif weapon_num == 6:
                player_weapon = 'Celestial Hammer'
                typewrite(f'You rolled a 6!!! So you get a {player_weapon}!!!')
                time.sleep(1)
                typewrite('This is a mystical, deadly, and godly weapon capable of obliterating any small monsters '
                          'with a single strike!')

            print()
            time.sleep(1)
            typewrite(f'It is now time to utilise your {player_weapon} and fight monsters that may drop rewards.')
            time.sleep(2)
            typewrite('You step out of the room, and see the Creature Room.')
            print()
            stop_fade_music(2.5)
            room_4 = game.Room4()
            chapter += 1
            playsound('audio/tran.wav')
            time.sleep(1)
            room_4.check_weapon_scene()

    # Class for all the scenes in Room 6
    class Room6:
        # Scene where player will be asked if they have the treasure key
        def ask_for_key_scene(self):
            mixer.music.load('audio/music/living.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(-1, fade_ms=2500)

            print(r""" ⢠⡄⢠⣤⣤⠀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⠀⣤⣤⡄⢠⡄⠀⠀⠀
⠀⢸⡇⢸⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⡇⢸⡇⠀⠀⠀
⠀⣿⡇⢸⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⡇⢸⣿⠀⠀⠀
⢀⣿⡇⢸⣿⣿⠀⣿⣿⣿⠟⠛⠛⠛⠛⠻⣿⣿⣿⠀⣿⣿⡇⢸⣿⡀⠀⠀
⢈⡉⢁⣀⣉⣉⣀⣉⣉⣉⠀⣴⠖⠲⣦⠀⣉⣉⣉⣀⣉⣉⣀⡈⢉⡁⠀⠀
⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⠀⣿⡄⢠⣿⠀⣿⣿⣿⣿⣿⣿⣿⡇⢸⡇⠀⠀
⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⠀⣿⣧⣼⣿⠀⣿⣿⣿⣿⣿⣿⣿⡇⢸⡇⠀⠀
⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣀⣉⣉⣉⣉⣀⣿⣿⣿⣿⣿⣿⣿⡇⢸⡇⠀⠀
⠘⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⠃⠀⠀
⢰⣄⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⣠⡆⠀⠀
⠘⠛⠃⠈⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠁⠘⠛⠃""")

            global chapter
            global has_key
            typewrite(f'Chapter {chapter}: The Living Room')
            time.sleep(2)
            typewrite('You have entered the Living Room.')
            time.sleep(1)
            typewrite('It is exactly like a living room, there is a couch, TV, coffee table.')
            typewrite('However, something is weird about this, it is modern... unlike the rest of the clock tower.')
            time.sleep(1)
            typewrite('Also, this room feels like it is very... special?')
            time.sleep(2)
            typewrite('Oh! I see.', 0.1)
            time.sleep(1)
            typewrite('This may look like a normal living room, but this room may contain treasure.')
            time.sleep(1)
            typewrite('Suddenly, a vault grabs your attention.')
            typewrite('It needs a key to be opened.')
            time.sleep(1)
            typewrite('Does it contain the treasure you have been looking for all this time?')
            typewrite('Well, to find out... you need the treasure key.')
            typewrite('Do you have the treasure key? [yes/no]')
            user_has_key = ''
            options = ['yes', 'y', 'no', 'n']
            while user_has_key not in options:
                user_has_key = input('> ').lower()
                if (user_has_key == 'yes' and has_key) or (user_has_key == 'y' and has_key):
                    print()
                    time.sleep(1)
                    self.open_vault_scene()
                elif (user_has_key == 'no' and not has_key) or (user_has_key == 'n' and not has_key):
                    print()
                    time.sleep(1)
                    typewrite('Well... people without the treasure key are strictly prohibited here...')
                    time.sleep(1)
                    typewrite('And the consequences are extremely harsh... a bit too harsh.')
                    print()
                    time.sleep(1)
                    stop_fade_music(1.5)
                    game_over()
                elif (user_has_key == 'yes' and not has_key) or (user_has_key == 'y' and not has_key):
                    print()
                    time.sleep(1)
                    typewrite('Hooray! It is time to open the vault!')
                    time.sleep(2)
                    typewrite('Wait a minute... the Monster Clock Intelligence Agency have found out you do not have '
                              'a key.')
                    time.sleep(2)
                    typewrite('Nothing ends well when that Intelligence Agency is involved...')
                    time.sleep(1)
                    stop_fade_music(1.5)
                    game_over()
                elif (user_has_key == 'no' and has_key) or (user_has_key == 'n' and has_key):
                    print()
                    time.sleep(1)
                    typewrite('What... why would you do that?')
                    time.sleep(1)
                    typewrite('You DID have the key!')
                    time.sleep(1)
                    typewrite('Uh oh... now they think that you actually do not have the key...')
                    time.sleep(1)
                    typewrite("And they will give you the harsh consequences of 'not' having the key...")
                    time.sleep(1)
                    typewrite('Probably a good idea not to joke around next time.')
                    time.sleep(1)
                    stop_fade_music(1.5)
                    game_over()
                else:
                    typewrite('Please enter a valid option.', 0.01)

        @staticmethod
        def open_vault_scene():
            typewrite('Great, you have the treasure key to open the vault!')
            time.sleep(1)
            typewrite('You tip-toe to the vault, making sure no one is watching you...')
            typewrite('The vault is extremely shiny and treasure is definitely in there.')
            time.sleep(1)
            typewrite('You bring out the key, ready to unlock the vault and claim the treasure.')
            time.sleep(1)
            typewrite('Press enter to unlock the vault.')
            input()
            typewrite('The vault slowly opens by itself, making an eerie sound.')
            typewrite('You can partly see what is inside.')
            time.sleep(1)
            typewrite("You don't know what it is, but it's not the treasure you were expecting.")
            time.sleep(1)
            typewrite('The vault fully opens, it is storing a special card.')
            time.sleep(1)
            typewrite('You take the card in your hand.')
            time.sleep(1)
            typewrite('Maybe THIS is the key to treasure.')
            time.sleep(1)
            typewrite('You look around the living room, looking for clues.')
            time.sleep(1)
            typewrite('You spot a wall contrasting from the neighbouring walls.')
            typewrite('You decide to check it out.')
            time.sleep(1)
            typewrite('You touch it, and discover that it can be moved. You decide to move it by pushing.')
            typewrite('Press enter to push the wall.')
            input()
            typewrite('You push the wall, and... see a chest!')
            time.sleep(1)
            typewrite('You feel overjoyed, after all of that your treasure is finally here.')
            time.sleep(1)
            typewrite('But... is it real?')
            time.sleep(1)
            typewrite('Think positive, try scanning the card on the scanner attached to the chest.')
            typewrite('Press enter to scan the card.')
            input()
            typewrite('You scan the card, and the chest opens.')
            time.sleep(1)
            typewrite('YES!', 0.2)
            stop_fade_music(1)
            mixer.music.load('audio/music/win.mp3')
            mixer.music.set_volume(1)
            mixer.music.play(1, fade_ms=1500)
            typewrite('It is exactly what you were longing for, THE TREASURE!')
            typewrite('The chest is filled with gold, diamonds, emeralds, and even some gems you cannot name.')
            time.sleep(1)
            typewrite('You grab the chest in your hand.')
            typewrite('The chest suddenly teleports you outside of the clock tower.')
            typewrite('Freedom.', 0.1)
            typewrite('You finally get to say goodbye to the clocktower, and the monsters dwelling there.')
            time.sleep(1)
            typewrite('Congrats!')
            time.sleep(1)
            print("""
██╗░░░██╗░█████╗░██╗░░░██╗        ░██╗░░░░░░░██╗██╗███╗░░██╗██╗
╚██╗░██╔╝██╔══██╗██║░░░██║        ░██║░░██╗░░██║██║████╗░██║██║
░╚████╔╝░██║░░██║██║░░░██║        ░╚██╗████╗██╔╝██║██╔██╗██║██║
░░╚██╔╝░░██║░░██║██║░░░██         ░░████╔═████║░██║██║╚████║╚═╝
░░░██║░░░╚█████╔╝╚██████╔╝        ░░╚██╔╝░╚██╔╝░██║██║░╚███║██╗
░░░╚═╝░░░░╚════╝░░╚═════╝░        ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝""")
            time.sleep(1)
            typewrite('Now enjoy this playful music!')
            typewrite('Press CTRL + C to exit.')
            try:
                while True:
                    if not mixer.music.get_busy():
                        break
                    pygtime.Clock().tick(10)
                sys.exit()
            except KeyboardInterrupt:
                sys.exit()


# Variable pointing to game class
game = Game()

if __name__ == '__main__':  # Makes sure script is executed when invoked directly

    # Plays music
    mixer.music.load('audio/music/intro.mp3')
    mixer.music.set_volume(1)
    mixer.music.play(-1, fade_ms=2500)

    chapter = 0
    has_key = False
    four_digit_code = ''
    has_weapon = False
    has_code = False
    player_weapon = ''
    # Game Introduction
    print(r'''  _______
 /  12   \
|    |    |
|9   |   3|
|     \   |
|         |
 \___6___/''')
    typewrite('Welcome to your adventure!')
    typewrite('As an avid explorer and traveller, you have decided to search for treasure in this spooky clock tower.')
    typewrite('However, legend has it that this clock tower was abandoned decades ago and deadly creatures currently '
              'dwell in this place.')
    typewrite('Hopefully you have enough determination and courage for this journey.')
    typewrite("You may call me the guiding light, and as the name suggests, I will be there to guide you.")
    typewrite("Let's start with your name: ")
    name = input('> ')
    typewrite(f'Good luck, {name}.')
    print()
    choice_stage = game.ChoiceStage()
    chapter += 1
    pause_fade_music(2.5)
    playsound('audio/tran.wav')  # Plays transition sound effect
    time.sleep(1)
    choice_stage.room_choice_scene()
