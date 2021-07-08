
# Utilizador administrador
base de dados nome:
    - leonardo
coleção: 
    - users

Username: leo2
Password: leo2

{"_id":"leo2","nome":"Leonardo","email":"leo@leo.pt","password":"pbkdf2:sha256:150000$5XMSWg5I$c678dd226f21777e757600e9b068a83ee5b422ab0f2ce1964ad284e7be270728","tipo":"Admin","universidade":"UM","departamento":"di","data":"2021-05-14 16:35","obs":""}

# How to run
Tendo a base de dado povoada é preciso por o backend a correr

## Backend
$ cd backend

Caso seja a 1ª vez
    $ pip3 install -r requirements.txt
    
Depois de ter os pacotes instalados
$ FLASK_APP=leonardo.py nohup flask run --host=0.0.0.0 &

## Frontend Leonardo
Tendo o backend a correr
$ cd leonardo2

Caso seja a 1ª vez
    $ npm i

Depois de ter os pacotes instalados
$ npm run serve &
