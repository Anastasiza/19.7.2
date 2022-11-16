import requests

headers = {
            'email': 'a.solovyeva@urent.city',
            'password': 'OpirOp86',
        }
api_key = requests.get("https://petfriends.skillfactory.ru/"+'api/key', headers=headers)
print(api_key.json())

api_key_headers = {'auth_key': api_key.json()['key']}

filter_param = {'filter': "my_pets"}

my_pets = requests.get("https://petfriends.skillfactory.ru/" + 'api/pets', headers=api_key_headers, params=filter_param)
print(my_pets.json())