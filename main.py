import requests

resp = requests.get('https://mario-s-car-default-rtdb.firebaseio.com/osMardiesel.json').json()

ids_os = [i for i in resp]

listaDeOs = []
for id_os in ids_os:
    objetoRaw = resp.get(id_os)

    documento = objetoRaw.get('usuarioModel').get('documento')

    if documento == "03804225225":
        print(objetoRaw)


