from game.logic.base import BaseLogic
from game.models import Board, GameObject
from random import randint
import time

# GAME OBJECT TYPE:
# - Bot : BotGameObject 
# - Base : BaseGameObject 
# - Diamond : DiamondGameObject
# - Portal : TeleportGameObject
# - Diamond Button : DiamondButtonGameObject 

class BotChase(BaseLogic):
    def __init__(self):
        self.stepVariation = 0
        self.stepChaseEnemy = 0
        self.diamonds = []


    # ==================== GETTER ==================== #
    def getBots(self, board: Board) -> list[GameObject]: return board.bots
    def getEnemyBots(self, this_bot: GameObject, board: Board) -> list[GameObject]: return [enemy for enemy in board.bots if enemy != this_bot]
    def getBases(self, board: Board) -> list[GameObject]: return [base for base in board.game_objects if base.type=="BaseGameObject"]
    def getHomeBaseObject(self, this_bot: GameObject, board: Board) -> GameObject: 
        for base in self.getBases(board):
            if base.properties.name == this_bot.properties.name:
                return base
        return None
    
    def getDiamonds(self, board: Board) -> list[GameObject]: return board.diamonds
    def getRedDiamonds(self, board: Board) -> list[GameObject]: return [diamond for diamond in board.diamonds if diamond.properties.points == 2]
    def getBlueDiamonds(self, board: Board) -> list[GameObject]: return [diamond for diamond in board.diamonds if diamond.properties.points == 1]
    
    def getPortals(self, board: Board) -> list[GameObject]: return [home for home in board.game_objects if home.type=="TeleportGameObject"]
    def getDiamondButton(self, board: Board) -> GameObject: return [home for home in board.game_objects if home.type=="DiamondButtonGameObject"][0]

    def getClosestRedDiamond(self, this_bot: GameObject, board: Board) -> GameObject:
        red_diamonds = self.getRedDiamonds(board)
        if not red_diamonds:
            return None
        return min(red_diamonds, key=lambda diamond: self.distance(this_bot, diamond, board))
    def getClosestBlueDiamond(self, this_bot: GameObject, board: Board) -> GameObject:
        blue_diamonds = self.getBlueDiamonds(board)
        if not blue_diamonds:
            return None
        return min(blue_diamonds, key=lambda diamond: self.distance(this_bot, diamond, board))
    def getClosestDiamond(self, this_bot: GameObject, board: Board) -> GameObject:
        diamonds = self.getDiamonds(board)
        if not diamonds:
            return None
        return min(diamonds, key=lambda diamond: self.distance(this_bot, diamond, board))
    def getClosestEnemy(self, this_bot: GameObject, board: Board) -> GameObject:
        enemies = self.getEnemyBots(this_bot, board)
        if not enemies:
            return None
        return min(enemies, key=lambda enemies: self.distance(this_bot, enemies, board))

    def getSortedPortals(self, board_bot: GameObject, board: Board) -> list[GameObject]: 
        # Sort portals based on distance to bot
        portals = self.getPortals(board)
        if(self.distanceWithoutPortal(board_bot, portals[0]) < self.distanceWithoutPortal(board_bot, portals[1])):
            return portals[0], portals[1]
        else:
            return portals[1], portals[0]

    def getUsedInventorySpace(self, board_bot:GameObject) -> int: return board_bot.properties.diamonds
    def getEmptyInventorySpace(self, board_bot:GameObject) -> int: return board_bot.properties.inventory_size - board_bot.properties.diamonds
    
    # ==================== Checks ==================== #
    def isInventoryFull(self, this_bot: GameObject) -> bool: return this_bot.properties.diamonds == this_bot.properties.inventory_size
    def isInventoryEmpty(self, this_bot: GameObject) -> bool: return this_bot.properties.diamonds == 0

    # ===== Distance ====== #
    def distance(self, objectFrom: GameObject, objectTo: GameObject, board: Board) -> int: return min(self.distanceWithoutPortal(objectFrom, objectTo), self.distanceUsingPortal(objectFrom, objectTo, board))
    def distanceWithoutPortal(self, objectFrom: GameObject, objectTo: GameObject) -> int: return abs(objectFrom.position.y - objectTo.position.y) + abs(objectFrom.position.x - objectTo.position.x)
    def distanceUsingPortal(self, objectFrom: GameObject, objectTo: GameObject, board: Board) -> int:
        portals = self.getSortedPortals(objectFrom, board)
        return self.distanceWithoutPortal(objectFrom, portals[0]) + self.distanceWithoutPortal(portals[1], objectTo)
    def getClosestEnemyDistance(self, this_bot: GameObject, board: Board) -> int: 
        enemy = self.getClosestEnemy(this_bot, board)
        if not enemy:
            return -1
        return self.distance(this_bot, self.getClosestEnemy(this_bot, board), board)
    def getBaseDistance(self, this_bot: GameObject, board: Board) -> int: return self.distance(this_bot, self.getHomeBaseObject(this_bot, board), board)

    # ===== Movement ===== #
    def moveRight(self): return (1,0)
    def moveLeft(self): return (-1,0)
    def moveUp(self): return (0,1)
    def moveDown(self): return (0,-1)
    def moveToObjective(self, board_bot: GameObject, objective: GameObject, board: Board):
        x_diff:int = board_bot.position.x - objective.position.x
        y_diff:int = board_bot.position.y - objective.position.y

        if objective.type=="TeleportGameObject" and self.distance(board_bot, self.getHomeBaseObject(board_bot, board), board) == 0:
            temp = randint(1,4)
            if temp == 1:
                return self.moveUp(board_bot, board)
            elif temp == 2:
                return self.moveDown(board_bot, board)
            elif temp == 3:
                return self.moveLeft(board_bot, board)
            else:
                return self.moveRight(board_bot, board)

        if objective.type!="TeleportGameObject" and self.distance(board_bot, self.getHomeBaseObject(board_bot, board), board) > self.distanceUsingPortal(board_bot, self.getHomeBaseObject(board_bot, board), board):
            return self.moveToObjective(board_bot, self.getSortedPortals(board_bot, board)[0], board)

        if(self.stepVariation % 2 == 0):
            self.stepVariation += 1
            if x_diff < 0: return self.moveRight()
            elif x_diff > 0: return self.moveLeft()
            elif y_diff > 0: return self.moveDown()
            elif y_diff < 0: return self.moveUp()
        else:
            self.stepVariation -= 1
            if y_diff > 0: return self.moveDown()
            elif y_diff < 0: return self.moveUp()
            elif x_diff < 0: return self.moveRight()
            elif x_diff > 0: return self.moveLeft()
                
        return None
    
    def moveToBase(self, board_bot: GameObject, board: Board):
        if self.distanceWithoutPortal(board_bot, self.getHomeBaseObject(board_bot, board)) > self.distanceUsingPortal(board_bot, self.getHomeBaseObject(board_bot, board), board):
            return self.moveToObjective(board_bot, self.getSortedPortals(board_bot, board)[0], board)
        return self.moveToObjective(board_bot, self.getHomeBaseObject(board_bot, board), board)
    def movetoClosestEnemy(self, board_bot: GameObject, board: Board): return self.moveToObjective(board_bot, self.getClosestEnemy(board_bot, board), board)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # ==================== MAIN FUNCTION ==================== 
    # CURRENT ALGORITHM :
    #   1 Check for near Enemy        (incase of attacking)
    #   2 Check inventory full        (if full then go home)
    #   3 If inventory is half full but the base is near, deposit the points
    #   4 Go to the diamond that is within 2 moves and have sufficient inventory
    #   5 Go to nearest diamond if inventory space is more than equal 2 
    #   6 Go to blue diamond if sufficient inventory and distance is within 2 moves
    #   7 If no diamonds found, and inventory is not empty, go to base
    #   8 If no diamonds found, with empty inventory, go to diamond button
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def next_move(self, this_bot: GameObject, board: Board):
    # BOT FUNCTION CALL BY ENGINE

        closest_enemy = self.getClosestEnemy(this_bot, board)
        if closest_enemy:
            return self.movetoClosestEnemy(this_bot, board)

    # TEMP
        temp = randint(1,4)
        if temp == 1:
            return self.moveUp(this_bot, board)
        elif temp == 2:
            return self.moveDown(this_bot, board)
        elif temp == 3:
            return self.moveLeft(this_bot, board)
        else:
            return self.moveRight(this_bot, board)
        