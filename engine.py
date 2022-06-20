"""
Logical Game
"""

class Game:
    def __init__(self):
        self._init_entities()

    def _init_entities(self):
        self.solids = {}
        self.movables = []
        raise NotImplementedError('Entities have to be initialized.')
    
    def update(self):
        raise NotImplementedError('logical update has to be implemented.')

    def handle_command(self,command):
        raise NotImplementedError('handle_command has to be implemented.')
