import socket

from threading import Thread

from f1_2020_telemetry.packets import *
from pilot import Pilot

class Listener(Thread):
    def __init__(self, host : str, port: int, my_name: str=""):
        super(Listener, self).__init__()

        # setup socket
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.bind((host, port))

        self.status = None                     # store the status of the car 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
        self.totalLaps = None                  # number of lap of the race
        self.race_info = {                     # info for the header of the page
            "track" : "",
            "weather" : "",
            "trackTemperature" : "",
            "airTemperature" : "",
            "sessionDuration" : 0
        }
        self.tyresID = {                       # mapping tyreID to image name
            0 : "",
            16 : "soft", 
            17 : "medium", 
            18 : "hard", 
            7 : "intermediate", 
            8 : "wet"
        }
        self.weatherID = [                     # mapping weather number to image name
            "wi-day-sunny", 
            "wi-day-cloudy", 
            "wi-cloud", 
            "wi-day-showers", 
            "wi-day-rain", 
            "wi-day-snow-thunderstorm"
        ]
        
        # update the dictionnary of <ID: name> to add missing ones
        self.DriverIDs = DriverIDs
        self.DriverIDs[100] = my_name
        self.DriverIDs[72] = "Devon Butler"
        self.DriverIDs[73] = "Lukas Weber"

    def run(self):
        print("Start Listening")
        while True:

            # set all pilots at the first "race" at the server starts
            if self.status is None and self.totalLaps is not None:
                self.status = [Pilot(self.totalLaps) for _ in range(22)]

            udp_packet = self.udp_socket.recv(2048)
            packet = unpack_udp_packet(udp_packet)

            if isinstance(packet, PacketEventData_V1):
                if packet.eventStringCode == b"SSTA":
                    # reset fastest player at start, else keep data from previoous race
                    self.update_fastest_pilot() 
                if packet.eventStringCode == b'FTLP':
                    self.update_fastest_pilot()
                if packet.eventStringCode == b"SEND":
                    pass # for now
            if isinstance(packet, PacketSessionData_V1):
                # print(packet.sessionDuration, packet.sessionTimeLeft)
                self.race_info["track"] = TrackIDs[packet.trackId]
                self.race_info["weather"] = self.weatherID[packet.weather]
                self.race_info["trackTemperature"] = packet.trackTemperature
                self.race_info["airTemperature"] = packet.airTemperature
                self.race_info["sessionDuration"] = packet.sessionDuration - packet.sessionTimeLeft
                if self.totalLaps != packet.totalLaps:
                    # reset pilots when the number of lap changes (usually due to map change)
                    self.totalLaps = packet.totalLaps
                    self.status = [Pilot(self.totalLaps) for _ in range(22)]
            if isinstance(packet, PacketLapData_V1):
                for i, lap in enumerate(packet.lapData):
                    self.status[i].lap = lap.currentLapNum
                    self.status[i].position = lap.carPosition
                    self.status[i].fastest_lap = lap.bestLapTime
                    self.status[i].status = lap.resultStatus
            if isinstance(packet, PacketParticipantsData_V1):
                for i, participant in enumerate(packet.participants):
                    self.status[i].name = self.DriverIDs[participant.driverId]
                    self.status[i].team = TeamIDs[participant.teamId]
                    self.status[i].is_bot = bool(participant.aiControlled)
            if isinstance(packet, PacketCarStatusData_V1):
                for i, car in enumerate(packet.carStatusData):
                    self.status[i].tyre = self.tyresID[car.visualTyreCompound]
                    self.status[i].wear = sum(car.tyresWear) / 4
        
    def update_fastest_pilot(self):
        """
        Reset all pilot to not be the fastest. If fastest time is above > 0, set to True the fastest pilot
        """
        if self.status is None:
            return

        fastest_pilot = None
        fastest_time = 1e8
        for idx, pilot in enumerate(self.status):
            if 0 < pilot.fastest_lap < fastest_time:
                fastest_pilot = pilot
                fastest_time = pilot.fastest_lap
            pilot.is_fastest = False  # set all to false

        if fastest_pilot is not None:
            fastest_pilot.is_fastest = True  # set only the fastest one to True