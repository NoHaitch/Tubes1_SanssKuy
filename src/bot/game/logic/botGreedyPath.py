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

class BotGreedyPath(BaseLogic):
    def __init__(self):
        self.step_variation : bool = False
        self.step_ignore_portal : int = 0
        self.step_chase_enemy : int = 0
        self.current_distance_to_base : int = 0
        self.current_inventory_space : int = None

        # self.self.sorted_portals[0] is the portal closest to player, while [1] is further
        self.sorted_portals : list[GameObject] = []
        # self.self.distance_self_to_portals[0] is the distant to the portal closest to player, while [1] is further
        self.distance_self_to_portals : list[int] = []
        self.base : GameObject = None

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
    
    def getPortals(self, board: Board) -> list[GameObject]: return [portal for portal in board.game_objects if portal.type=="TeleportGameObject"]
    def getSortedPortals(self, this_bot: GameObject, board: Board) -> list[GameObject]: 
        # Sort portals based on distance to bot
        portals = self.getPortals(board)
        if portals:
            if self.distanceWithoutPortal(this_bot, portals[0]) < self.distanceWithoutPortal(this_bot, portals[1]):
                return portals[0], portals[1]
            else:
                return portals[1], portals[0]
        return None
    def getSortedPortalsDistance(self, this_bot: GameObject, board: Board) -> list[int]:
        if self.sorted_portals:
            return (self.distance(this_bot, self.sorted_portals[0], board), self.distance(this_bot, self.sorted_portals[1], board))
        else:
            return (-1, -1)

    def getDiamondButton(self, board: Board) -> GameObject: return [button for button in board.game_objects if button.type=="DiamondButtonGameObject"][0]

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

    def getUsedInventorySpace(self, this_bot:GameObject) -> int: return this_bot.properties.diamonds
    def getEmptyInventorySpace(self, this_bot:GameObject) -> int: return this_bot.properties.inventory_size - this_bot.properties.diamonds
    
    def getTimeRemaining(self, this_bot:GameObject) -> int: return this_bot.properties.milliseconds_left 

    # ==================== Checks ==================== #
    def isInventoryFull(self) -> bool: return self.current_inventory_space == 0
    def isInventoryEmpty(self, this_bot: GameObject) -> bool: return self.current_inventory_space == this_bot.properties.inventory_size

    # ==================== Distance ===================== #
    def distance(self, objectFrom: GameObject, objectTo: GameObject, board: Board) -> int: 
        if objectTo.type =="TeleportGameObject": return self.distanceWithoutPortal(objectFrom, objectTo)
        return min(self.distanceWithoutPortal(objectFrom, objectTo), self.distanceUsingPortal(objectFrom, objectTo, board))
    def distanceWithoutPortal(self, objectFrom: GameObject, objectTo: GameObject) -> int: return abs(objectFrom.position.y - objectTo.position.y) + abs(objectFrom.position.x - objectTo.position.x)
    def distanceUsingPortal(self, objectFrom: GameObject, objectTo: GameObject, board: Board) -> int:
        return self.distanceWithoutPortal(objectFrom, self.sorted_portals[0]) + self.distanceWithoutPortal(self.sorted_portals[1], objectTo)
    def getClosestEnemyDistance(self, this_bot: GameObject, board: Board) -> int: 
        enemy = self.getClosestEnemy(this_bot, board)
        if not enemy:
            return -1
        return self.distance(this_bot, self.getClosestEnemy(this_bot, board), board)
    def getBaseDistance(self, this_bot: GameObject, board: Board) -> int: return self.distance(this_bot, self.base, board)

    # ==================== Movement ==================== #
    def moveRight(self): return (1,0)
    def moveLeft(self): return (-1,0)
    def moveUp(self): return (0,1)
    def moveDown(self): return (0,-1)

    def moveToObjective(self, this_bot: GameObject, objective: GameObject, board: Board):
        x_diff:int = this_bot.position.x - objective.position.x
        y_diff:int = this_bot.position.y - objective.position.y

        # After Teleport
        if objective.type=="TeleportGameObject" and self.distance(this_bot, self.base, board) == 0:
            temp:int = randint(1,4)
            if temp == 1:
                return self.moveUp(this_bot, board)
            elif temp == 2:
                return self.moveDown(this_bot, board)
            elif temp == 3:
                return self.moveLeft(this_bot, board)
            else:
                return self.moveRight(this_bot, board)

        # Go To Portal if faster
        if objective.type!="TeleportGameObject" and self.distance(this_bot, self.base, board) > self.distanceUsingPortal(this_bot, self.base, board):
            print("PORTAL is closer!")
            return self.moveToObjective(this_bot, self.sorted_portals[0], board)

        if objective.type!="TeleportGameObject":
            # self.distance_self_to_portals[0] is the distance to the nearest portal
            if self.distance_self_to_portals[0] == 1:
                print("TRYING TO IGNORE PORTAL")
                x_portal_diff:int  = this_bot.position.x - self.sorted_portals[0].position.x
                y_portal_diff:int  = this_bot.position.y - self.sorted_portals[0].position.y

                # because portal is near make sure to avoid it
                if x_diff < 0 and x_portal_diff == -1 : 
                    self.step_ignore_portal = 1
                    if y_diff < 0 : return self.moveUp()
                    else : return self.moveDown()
                    
                elif x_diff > 0 and x_portal_diff == 1 : 
                    self.step_ignore_portal = 2
                    if y_diff < 0 : return self.moveUp()
                    else : return self.moveDown()
                    
                elif y_diff < 0 and y_portal_diff == -1 : 
                    self.step_ignore_portal = 3
                    if x_diff < 0 : return self.moveRight()
                    else : return self.moveLeft()

                elif y_diff > 0 and y_portal_diff == 1 : 
                    self.step_ignore_portal = 4
                    if x_diff < 0 : return self.moveRight()
                    else : return self.moveLeft()

        if self.step_ignore_portal == 1: self.step_ignore_portal = 0; print("IGNORE PORTAL Follow up"); return self.moveRight()
        elif self.step_ignore_portal == 2: self.step_ignore_portal = 0; print("IGNORE PORTAL Follow up"); return self.moveLeft()
        elif self.step_ignore_portal == 3: self.step_ignore_portal = 0; print("IGNORE PORTAL Follow up"); return self.moveUp()
        elif self.step_ignore_portal == 4: self.step_ignore_portal = 0; print("IGNORE PORTAL Follow up"); return self.moveDown()

        # Move directly toward objective
        if self.step_variation :
            self.step_variation = False
            if x_diff < 0 : return self.moveRight()
            elif x_diff > 0 : return self.moveLeft()
            elif y_diff < 0 : return self.moveUp()
            elif y_diff > 0 : return self.moveDown()
        else:
            self.step_variation = True
            if y_diff < 0 : return self.moveUp()
            elif y_diff > 0 : return self.moveDown()
            elif x_diff < 0 : return self.moveRight()
            elif x_diff > 0 : return self.moveLeft()

        return None
    def moveToBase(self, this_bot: GameObject, board: Board):
        if self.distanceWithoutPortal(this_bot, self.base) > self.distanceUsingPortal(this_bot, self.base, board):
            return self.moveToObjective(this_bot, self.sorted_portals[0], board)
        return self.moveToObjective(this_bot, self.base, board)
    def movetoClosestEnemy(self, this_bot: GameObject, board: Board): return self.moveToObjective(this_bot, self.getClosestEnemy(this_bot, board), board)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # ==================== MAIN FUNCTION ==================== 
    # CURRENT ALGORITHM :
    #   1 If timeleft is less than the distance to home, then go home
    #   2 Check for near Enemy        (incase of attacking)
    #   3 Check inventory full        (if full then go home)
    #   4 If inventory is half full but the base is near, deposit the points
    #   5 Go to the diamond that is within 2 moves and have sufficient inventory
    #   6 Go to nearest diamond if inventory space is more than equal 2 
    #   7 Go to blue diamond if sufficient inventory and distance is within 2 moves
    #   8 If no diamonds found, and inventory is not empty, go to base
    #   9 If no diamonds found, with empty inventory, go to diamond button
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def next_move(self, this_bot: GameObject, board: Board):
    # BOT FUNCTION CALL BY ENGINE
        # Static var
        if not self.base:
            self.base = self.getHomeBaseObject(this_bot, board)

        # Dynamic Var
        self.sorted_portals = self.getSortedPortals(this_bot, board)
        self.distance_self_to_portals = self.getSortedPortalsDistance(this_bot, board)
        self.current_distance_to_base = self.getBaseDistance(this_bot, board)
        self.current_inventory_space = self.getEmptyInventorySpace(this_bot)

    # 1 If timeleft is less than the distance to home, then go home
        if not self.isInventoryEmpty(this_bot) and (self.getTimeRemaining(this_bot) // 1000) - 2 <= self.current_distance_to_base:
            # print("LOW TIME - GOING HOME")
            return self.moveToBase(this_bot, board)

    # 2 Check for near Enemy 
        if self.getClosestEnemyDistance(this_bot, board) == 1 and self.step_chase_enemy <= 2:
            # print("Attack Close Enemy.")
            self.step_chase_enemy += 1
            return self.movetoClosestEnemy(this_bot, board) 
        elif self.step_chase_enemy == 4:
            self.step_chase_enemy = 0
        elif self.step_chase_enemy < 2:
            self.step_chase_enemy += 1

    # 3 Check inventory full    
        if self.isInventoryFull():  
            # print("Inventory Full.")
            return self.moveToBase(this_bot, board)

    # 4 If inventory is half full but the base is near, deposit the points
        if self.current_distance_to_base <= 2 and self.current_inventory_space < 3:
            return self.moveToBase(this_bot, board)

    # 5 Go to the diamond that is within 2 moves and have sufficient inventory
        closest_diamond:GameObject = self.getClosestDiamond(this_bot, board)
        if closest_diamond:
            diamond_distance = self.distance(this_bot, closest_diamond, board)
            if diamond_distance and diamond_distance > (self.distance(this_bot, self.getDiamondButton(board), board) + 3):
                # print("Going to Diamond Button.")
                return self.moveToObjective(this_bot, self.getDiamondButton(board), board)
        
    # 6 Go to nearest diamond if inventory space is more than equal 2   
        if closest_diamond and self.current_inventory_space >= 2:
            # print(f"Going to Diamond. Location : {closest_diamond.position}")
            return self.moveToObjective(this_bot, closest_diamond, board) 
            
    # 7 Go to blue diamond if sufficient inventory and distance is within 2 moves
        closest_diamond = self.getClosestBlueDiamond(this_bot, board)
        if closest_diamond and self.current_inventory_space == 1 and closest_diamond.properties.points == 1 and diamond_distance <= 2:
            # print(f"Going to Diamond. Location : {closest_diamond.position}")
            return self.moveToObjective(this_bot, closest_diamond, board) 

    # 8 If no diamonds found, and inventory is not empty, go to base
        if(not self.isInventoryEmpty(this_bot)):
            # print("Emptying Inventory.")
            return self.moveToBase(this_bot, board)
        
    # 9 If no diamonds, with empty inventory, go to diamond button
        # print("Going to Diamond Button.")
        return self.moveToObjective(this_bot, self.getDiamondButton(board), board)

        

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
            
        