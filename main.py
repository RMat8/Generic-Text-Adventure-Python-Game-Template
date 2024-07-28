from enum import Enum

"""
Generic Text-Adventure Python Game Template

This is my best shot at a text-adventure game template.
Some parts of the code are just the result of me goofing around.
"""

class CountingUnits(Enum): #this was created just for fun, it's ridiculous, there might even be a simpler way to do it, but my caveman brain couldn't fathom it
    UNIT = "unit"
    HUNDRED = "hundred"
    THOUSAND = "thousand"
    MILLION = "million"
    BILLION = "billion"
    TRILLION = "trillion"
    QUADRILLION = "quadrillion"
    QUINTILLION = "quintillion"
    SEXTILLION = "sextillion"
    SEPTILLION = "septillion"
    OCTILLION = "octillion"
    NONILLION = "nonillion"
    DECILLION = "decillion"

class HostilityLevel(Enum):
    EASY = "Easy"
    NORMAL = "Normal"
    HARD = "Hard"
    EXTREME = "Extreme"
    NIGHTMARE1 = "Nightmare"
    #secret difficulty levels below
    NIGHTMARE2 = "Nightmare+"
    NIGHTMARE3 = "Nightmare++"
    NIGHTMARE4 = "Nightmare+++"

class Command(Enum):
    HELP = "help"
    WALK = "walk"
    PICK = "pick"
    CHECK = "check"
    EXIT = "exit"

class World:
    worlds = []
    def __init__(self, name, index=len(worlds)+1, size=(-50, -50, 50, 50)):
        self.name = name
        self.index = index
        self.domain = { 
            "West":size[0],
            "South":size[1],
            "East":size[2],
            "North":size[3]
        }
        self.hostility = HostilityLevel.NORMAL
        World.worlds.append(self)
    
    def boundary(self, inp=(0, 0)):
        equator = (inp[0] > self.domain.values("West") and inp[0] < self.domain.values("East"))
        meridian = (inp[1] > self.domain.values("South") and inp[1] < self.domain.values("North"))

        if equator and meridian:
            return True
        else:
            return False


class Entity:
    def __init__(self, name, age=0, species=None, position=[0, 0]):
        self.position = position
        self.name = name
        self.age = age
        self.species = species
        self.level = [1, CountingUnits.UNIT]#<----
        #yes, I created an enumerator just for this, don't judge...         I just realized after I was finished with this, that I could use this to avoid integer limit

        self.stats = {
            "strength": 1,
            "speed": 1,
            "stamina": 1,
            "mana": 1,
            "health": 1,
            "regeneration": 1
        }

        ti = 0
        for _, i in self.stats.items():
            ti += i
        
        self.power_level = ["power", int(ti/len(self.stats))]

        self.abilities = {}

        self.inventory = {
            "Contents":{},
            "max_slots":30,
            "max_weight":(10+(self.stats.get("strength")))
        }

class Player(Entity):
    def __init__(self, name, age = 18, species="Human"):
        super().__init__(name, age, species)

        scrollGuidance = Item("Scroll of Guidance")
        self.inventory["Contents"].update({"Scroll of Guidance": scrollGuidance})

        self.quests = {}

    def display_help(self):
        print("----Help-----")
        print(f"You are a {self.species.lower()}.\nYou are {self.age} years old.\nYour name is {self.name}.")
        print("----Stats----")

        for a, b in self.stats.items():
            print(f"Your {str(a).capitalize()} level is {b}")
        
        print("--Inventory--")
        inv = self.inventory["Contents"]
        if len(inv) > 0:
            for i in inv:
                print(i)
        else:
            print("Your inventory is empty.")


        if len(self.abilities) == 0:
            print("---Skills----")
            print("None")
        else:
            print("---Skills----")
            for a, b in self.abilities.items():
                print(f"Your {a} level is {b}.")   
                     
        print("---Options---")
        print("You can type WALK <direction: north, south, west, east> to move arount.")
        print("-------------")

    def walk(self, ttyp) -> None:
        typs = ["west", "south", "east", "north"]
        direction_change = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        def execute(a):
            self.position[0] += direction_change[typs.index(a)][0]
            self.position[1] += direction_change[typs.index(a)][1]
            print(self.position)

        for i in ttyp.split():
            if i in typs:
                execute(i)
            else:
                print(f"{i} - Invalid Direction")
    
    def check(self, target="inventory"):
        def check_inventory() -> None:
            self.itemNumber = len(self.inventory.get("Contents").items())
            mw = "max_weight"
            ms = "max_slots"
            for i in self.inventory.get("Contents"):
                print(f"Item: {i}")
            print(f"The number of items you have is {self.itemNumber}")
            print(f"You can carry {self.inventory.get(mw)} weight units with {self.inventory.get(mw) - self.itemNumber} units left")
            print(f"You have {self.inventory.get(ms) - self.itemNumber} units of storage volume left")

        match target:
            case "inventory":
                check_inventory()
            case "surroundings":
                pass
            case "container":
                pass
            case "writing":
                pass
            #unfinished code
        
    def pick(self, arg="up", item=None):
        if arg == "up":
            if item == None:
                print("There is nothing to pick up")
        else:
            print(f"Invalid Argument: '{arg}'")

    def update(self):
        ti = 0
        for _, i in self.stats.items():
            ti += i
        
        ti -= self.power_level[1]
        self.power_level[1] = int(ti/(len(self.stats.items()) - 1))

        self.itemNumber = len(self.inventory.get("Contents").items())

class Item:
    def __init__(self, name, type="Consumable"):
        self.name = name
        self.type = type
        self.weight = 1

    def __str__(self) -> str:
        return f"{self.name} - ({self.type})"

def game_init():
    name = input("What is your name? ")
    overworld = World("Overworld")
    creature = Entity("Creature", 3, "Gnome")
    player = Player(name)

    #commands
    commands = {
        Command.HELP: (player.display_help, ()),
        Command.WALK: (player.walk, ("arg",)),
        Command.PICK: (player.pick, ("arg",)),
        Command.CHECK: (player.check, ("arg",)),
        Command.EXIT: (exit, ())
    }

    #game starts
    print("-------------")
    print("Welcome to the untitled text-adventure game!")
    print("Type HELP to see all details about you.")

    return player, commands

def handle_input(player, commands, pinp):
    func_request = pinp.lower().split()[0]
    args = ' '.join(pinp.lower().split()[1:])
    for command in Command:
        if func_request == "exit":
            exit()
        elif func_request == command.value:
            func, requires_args = commands[command]
            #print(f"Calling function: {func.__name__} with args: {args}")
            if requires_args:
                if hasattr(player, func.__name__):  # Check if player has the method
                    getattr(player, func.__name__)(args)  # Call the method on player
                else:
                    func(args)  # Call the function with args
            else:
                if hasattr(player, func.__name__):  # Check if player has the method
                    getattr(player, func.__name__)()  # Call the method on player
                else:
                    func()  # Call the function without args
            return
    print("Invalid command")

def game_loop(player, commands):
    running = True
    while running:
        player.update()
        try:
            pinp = input("What do you want to do? ")
            handle_input(player, commands, pinp)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    #initialization - this is where the code starts
    player, commands = game_init()

    game_loop(player, commands)
