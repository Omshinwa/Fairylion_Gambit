# idk if i should, the only advantage is knowing the can_drive
class Simple_Pilot():
    def __init__(self, pilot=None, id=None, can_drive=None):
        if pilot:
            self.id = pilot.id
            self.can_drive = pilot.can_drive
        else:
            self.id = id
            self.can_drive = can_drive or {}