class Pilot():
    def __init__(self, totalLap):
        self.name = ""
        self.team = ""
        self.tyre = ""
        self.position = 0
        self.fastest_lap = 0
        self.lap = 0
        self.total_lap = totalLap
        self.status = 2  # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = disqualified, 5 = not classified, 6 = retired
        self.is_fastest = False
        self.is_bot = True
        self.wear = 0

    def to_json(self):
        return {
            "name" : self.name,
            "position" : self.position,
            "tyre" : self.tyre,
            "team" : self.team,
            "lap" : self.lap,
            "total_lap" : self.total_lap,
            "fastest_lap" : self.fastest_lap,
            "status" : self.status,
            "is_fastest" : self.is_fastest,
            "is_bot" : self.is_bot,
            "wear" : self.wear
        }