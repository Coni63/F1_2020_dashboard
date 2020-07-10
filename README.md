
# F1 2019 - Dashboard

This repository is offering a capability to see the current position of each pilot during a race with few additionnal informations. 

![preview](https://github.com/Coni63/F1_2020_dashboard/blob/master/preview.png)

## How to use

### Install Python 3.5+

If you don't have python installed, you should install it from [python.org](https://www.python.org/downloads/). 
Pay attention to add it to the path during the installation:

![installation](https://datatofish.com/wp-content/uploads/2018/10/0001_add_Python_to_Path.png)

### Setup the environment

First, create in the backend's folder a virtual environment called `venv` and install all libraries in `requirements.txt` with:

```
cd ./backend
python -m venv ./venv
activate ./venv
pip install -r requirements.txt
```

### Run the server

Everything is now set and you can run the server using:

```console
cd ./backend
activate ./venv
python server.py
```

### Access the UI

#### From the same computer as the one running the server
In this case, you can access it from *http://localhost:5000* or *http://127.0.0.1:5000*
#### From another device connected to the same network
In this other case, you can access it by entering the IP of the computer running the server such as *http://192.168.0.XX:5000/*

#### Shortcut

In the repository `start_server.bat` is a simple way to start it, just make a shortcut somewhere and execute it when you want to start playing. It will open a new tab with the page and run the server.

## Adjust parameters

You can adjust UDP and server parameters in `./backend/config.ini` This is adjusted to default parameters of F1 2019 but you can still update them. For developer, pay attention, if you change the port use for the backend to also adjust `./frontend/dashboard/src/environments/environment.ts`

There is also 2 parameters on the refresh rate in `./frontend/dashboard/src/environments/environment.ts` and `./frontend/dashboard/src/environments/environment.prod.ts` but they have to be adjusted only if you know how to build an angular project (see next part)

## Development

### Backend
Nothing specific has to be done if you develop a new feature on the backend side. There is no compilation stage. Just keep in mind to activate the virtual environment with and also to regenerate `requirements.txt` by running

```bash
cd ./backend
activate ./venv
pip freeze >requirements.txt
```
### Frontend

The frontend has been developped using Angular 8. This section will not be completely detailed as you should know a big part of it if you are willing to modify the project:).
First, you should download and install **Node 8.9+** and **NPM 5.5.1+**. Once they are installed you can install dependancies with :

```bash
cd ./frontend/dashboard
npm install
```

You can now run a development version by running:

```bash
cd ./frontend/dashboard
ng serve
```

The UI will be available at *http://localhost:4200*. You can now make your changes if the server is also running obviously. When everything is done, delete files in `./backend/front_dist/` (This is because when you will build the frontend, it's gonna be stored as static files to be served by the Flask server) and run the command:

```bash
cd ./frontend/dashboard
ng build --prod
```

### Record and play games for faster development

Instead of having a game running in background to develop the interface, the library **f1-2020-telemetry** offers a very nice feature to record the UDP stream, save it and make it available to be replayed using UDP. As a result, I strongly advice you to record 1 game of few laps and use it to test it. 

#### Record

To record, run the command:
```bash
cd ./backend
activate ./venv
f1-2020-telemetry-recorder
```
This will create a file like `F1_2019_d01261af93b140b9.sqlite3` in your backend folder. 
You can after replay it using the command:

 ```bash
cd ./backend
activate ./venv
f1-2020-telemetry-player F1_2019_d01261af93b140b9.sqlite3 -r 2
```

You can look at options in [the documentation](https://f1-2020-telemetry.readthedocs.io/en/latest/package-documentation.html#command-line-tools)

## Architecture

The objective of this library is to listen on 1 Thread the UDP packets from the game and parse them using the library (f1-2019-telemetry). In parallel a second Thread is running a Flaks server to serve the UI as static files and provide socket to update the UI on regular basis.

![architecture](https://github.com/Coni63/F1_2020_dashboard/blob/master/architecture.png)

## Acknowledgments

Thanks to the author of [f1-2019-telemetry's library](https://f1-2019-telemetry.readthedocs.io/en/latest/index.html)