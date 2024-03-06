from game.logic.base import BaseLogic
from game.models import Board, GameObject

class Stay(BaseLogic):
    def next_move(self, this_bot: GameObject, board: Board):
        return (0, 0)