import configparser

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, send, emit

from listener import Listener

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyforsocket'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./front_dist/dashboard/', path)

@app.route('/')
def root():
  return send_from_directory('./front_dist/dashboard/', 'index.html')

@socketio.on('give_status')
def send_status():
    """
    Emit a json with an array having a json with each pilot information (sorted in position).
    If the race is not started, emit an empty array.

    Exemple for one pilot:
    {
        "name" : "Max Verstappen",
        "position" : 1,
        "tyre" : "soft",
        "team" : "Red Bull Racing",
        "lap" : 3,
        "total_lap" : 10,
        "fastest_lap" : 84.248,
        "status" : 2,
        "is_fastest" : true,
        "is_bot" : true,
        "wear" : 3.25
    }
    """
    if udp_listener.status is None:
        emit('status', [])
    else:
        sorted_pilot = sorted(udp_listener.status, key=lambda x:x.position)
        data = [pilot.to_json() for pilot in sorted_pilot if pilot.position > 0]  # filter 21 and 22st pilot out of myTeam
        emit('status', data)

@socketio.on('give_track')
def send_track():
    """
    emit a json with the race information.

    Exemple:
    {
        "track" : "Sakhir (Bahrain)",
        "weather" : "wi-day-sunny",
        "trackTemperature" : "29",
        "airTemperature" : "21",
        "sessionDuration" : 127
    }
    """
    emit('track', udp_listener.race_info)

if __name__ == '__main__':
    """
    Run the Listener to parse UDP in a Thread
    Run the Flask website using socketio in a separated Thread
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('config.ini')

    udp_listener = Listener(
        host=config["UDP"]["host"], 
        port=int(config["UDP"]["port"]), 
        my_name=config["UDP"]["my_name"]
    )
    udp_listener.start()

    socketio.run(app, 
        debug=bool(int(config["server"]["debug"])), 
        use_reloader=bool(int(config["server"]["use_reloader"])), 
        host=config["server"]["host"], 
        port=int(config["server"]["port"])
    )

