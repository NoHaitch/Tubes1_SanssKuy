from game.logic.base import BaseLogic
from game.models import Board, GameObject
from random import randint

class StayAtHome(BaseLogic):
    def next_move(self, this_bot: GameObject, board: Board):
        return None