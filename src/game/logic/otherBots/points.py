from game.logic.base import BaseLogic
from game.models import Board, GameObject
from random import randint

# GAME OBJECT TYPE:
# - Bot : BotGameObject 
# - Base : BaseGameObject 
# - Diamond : DiamondGameObject
# - Portal : TeleportGameObject
# - Diamond Button : DiamondButtonGameObject 

class Points(BaseLogic):
    def __init__(self):
        self.step = 0

    # ==================== GETTER ==================== #
    def getBots(self, board: Board) -> list[GameObject]: return board.bots
    def getEnemyBots(self, thisBot: GameObject, board: Board) -> list[GameObject]: return [enemy for enemy in board.bots if enemy != thisBot]
    def getBases(self, board: Board) -> list[GameObject]: return [base for base in board.game_objects if base.type=="BaseGameObject"]
    def getHomeBaseObject(self, thisBot: GameObject, board: Board) -> GameObject: 
        for base in self.getBases(board):
            if base.properties.name == thisBot.properties.name:
                return base
        return None
    
    def getDiamonds(self, board: Board) -> list[GameObject]: return board.diamonds
    def getRedDiamonds(self, board: Board) -> list[GameObject]: return [diamond for diamond in board.diamonds if diamond.properties.points == 2]
    def getBlueDiamonds(self, board: Board) -> list[GameObject]: return [diamond for diamond in board.diamonds if diamond.properties.points == 1]
    
    def getPortals(self, board: Board) -> list[GameObject]: return [home for home in board.game_objects if home.type=="TeleportGameObject"]
    def getSortedPortals(self, this_bot: GameObject, board: Board) -> list[GameObject]: 
        # Sort portals based on distance to bot
        portals = self.getPortals(board)
        if(self.distanceWithoutPortal(this_bot, portals[0]) < self.distanceWithoutPortal(this_bot, portals[1])):
            return portals[0], portals[1]
        else:
            return portals[1], portals[0]
    def getDiamondButton(self, board: Board) -> GameObject: return [home for home in board.game_objects if home.type=="DiamondButtonGameObject"][0]

    def getClosestRedDiamond(self, thisBot: GameObject, board: Board) -> GameObject:
        red_diamonds = self.getRedDiamonds(board)
        if not red_diamonds:
            return None
        return min(red_diamonds, key=lambda diamond: self.distance(thisBot, diamond, board))
    def getClosestBlueDiamond(self, thisBot: GameObject, board: Board) -> GameObject:
        blue_diamonds = self.getBlueDiamonds(board)
        if not blue_diamonds:
            return None
        return min(blue_diamonds, key=lambda diamond: self.distance(thisBot, diamond, board))
    def getClosestDiamond(self, thisBot: GameObject, board: Board) -> GameObject:
        diamonds = self.getDiamonds(board)
        if not diamonds:
            return None
        return min(diamonds, key=lambda diamond: self.distance(thisBot, diamond, board))
    def getClosestEnemy(self, thisBot: GameObject, board: Board) -> GameObject:
        enemies = self.getEnemyBots(thisBot, board)
        if not enemies:
            return None
        return min(enemies, key=lambda enemies: self.distance(thisBot, enemies, board))
    def getClosestEnemyDistance(self, thisBot: GameObject, board: Board) -> int: return self.distance(thisBot, self.getClosestEnemy(thisBot, board), board)

    def getEmptyInventorySpace(self, this_bot:GameObject) -> int: return this_bot.properties.inventory_size - this_bot.properties.diamonds

    # ==================== Checks ==================== #
    def isInventoryFull(self, this_bot: GameObject) -> bool: return this_bot.properties.diamonds == this_bot.properties.inventory_size

    # ===== Distance ====== #
    def distance(self, objectFrom: GameObject, objectTo: GameObject, board: Board) -> int: return min(self.distanceWithoutPortal(objectFrom, objectTo), self.distanceUsingPortal(objectFrom, objectTo, board))
    def distanceWithoutPortal(self, objectFrom: GameObject, objectTo: GameObject) -> int: return abs(objectFrom.position.y - objectTo.position.y) + abs(objectFrom.position.x - objectTo.position.x)
    def distanceUsingPortal(self, objectFrom: GameObject, objectTo: GameObject, board: Board) -> int:
        portals = self.getSortedPortals(objectFrom, board)
        return self.distanceWithoutPortal(objectFrom, portals[0]) + self.distanceWithoutPortal(portals[1], objectTo)

    # ===== Base Move ===== #
    def moveRight(self): return (1,0)
    def moveLeft(self): return (-1,0)
    def moveUp(self): return (0,1)
    def moveDown(self): return (0,-1)
    def moveToObjective(self, this_bot: GameObject, objective: GameObject, board: Board):
        x_diff:int = this_bot.position.x - objective.position.x
        y_diff:int = this_bot.position.y - objective.position.y

        if objective.type=="TeleportGameObject" and self.distance(this_bot, self.getHomeBaseObject(this_bot, board), board) == 0:
            temp = randint(1,4)
            if temp == 1:
                return self.moveUp(this_bot, board)
            elif temp == 2:
                return self.moveDown(this_bot, board)
            elif temp == 3:
                return self.moveLeft(this_bot, board)
            else:
                return self.moveRight(this_bot, board)

        if objective.type!="TeleportGameObject" and self.distance(this_bot, self.getHomeBaseObject(this_bot, board), board) > self.distanceUsingPortal(this_bot, self.getHomeBaseObject(this_bot, board), board):
            return self.moveToObjective(this_bot, self.getSortedPortals(this_bot, board)[0], board)

        board.features

        if(self.step % 2 == 0):
            self.step += 1
            if x_diff < 0: return self.moveRight()
            elif x_diff > 0: return self.moveLeft()
            elif y_diff > 0: return self.moveDown()
            elif y_diff < 0: return self.moveUp()
        else:
            self.step -= 1
            if y_diff > 0: return self.moveDown()
            elif y_diff < 0: return self.moveUp()
            elif x_diff < 0: return self.moveRight()
            elif x_diff > 0: return self.moveLeft()
                
        return None
    
    def moveToBase(self, this_bot: GameObject, board: Board):
        if self.distanceWithoutPortal(this_bot, self.getHomeBaseObject(this_bot, board)) > self.distanceUsingPortal(this_bot, self.getHomeBaseObject(this_bot, board), board):
            return self.moveToObjective(this_bot, self.getSortedPortals(this_bot, board)[0], board)
        return self.moveToObjective(this_bot, self.getHomeBaseObject(this_bot, board), board)
    

    # ===== MAIN FUNCTION ===== #
    def next_move(self, this_bot: GameObject, board: Board):
        if self.isInventoryFull(this_bot):
            print("Inventory Full.")
            return self.moveToBase(this_bot, board)
        
        if(self.getEmptyInventorySpace(this_bot) >= 2):
            temp:GameObject = self.getClosestRedDiamond(this_bot, board)
            if temp != None:
                print(f"Going to red Diamond. Location : {temp.position}")
                return self.moveToObjective(this_bot, temp, board) 
        
        temp:GameObject = self.getClosestBlueDiamond(this_bot, board)
        if temp != None:
            print(f"Going to Blue Diamond. Location : {temp.position}")
            return self.moveToObjective(this_bot, temp, board)

        if(self.getEmptyInventorySpace(this_bot) >= 1):
            print("Emptying Inventory.")
            return self.moveToBase(this_bot, board)
        
        print("Going to Diamond Button.")
        return self.moveToObjective(this_bot, self.getDiamondButton(board), board)


        temp = randint(1,4)
        if temp == 1:
            return self.moveUp(this_bot, board)
        elif temp == 2:
            return self.moveDown(this_bot, board)
        elif temp == 3:
            return self.moveLeft(this_bot, board)
        else:
            return self.moveRight(this_bot, board)
        
        