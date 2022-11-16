import get_id
from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/kot.png'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/kot.png")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test1_creat_pet_simpel(name='Пес', animal_type='доберман',
                                     age = 4):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status = pf.creat_pet_simpel(auth_key, name, animal_type, age)
    assert status == 200

def test2_add_photo(pet_photo = 'images/racoon1.jpeg'):
    pet_photo_full_path = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status = pf.add_photo(auth_key, pet_id, pet_photo)
    assert status == 200

def test3_get_key_invalid_user_email(email = invalid_email, password = valid_password):
    status,result = PetFriends().get_api_key(email,password)
    assert status != 200
    assert 'key' not in result

def test4_get_key_invalid_user_password(email = valid_email, password = invalid_password):
    status,result = PetFriends().get_api_key(email,password)
    assert status != 200
    assert 'key' not in result

def test5_get_key_invalid_user_email_password(email = invalid_email, password = invalid_password):
    status,result = PetFriends().get_api_key(email,password)
    assert status != 200
    assert 'key' not in result

def test6_add_new_pet_with_special_symbols_name(name = 'W#@%', animal_type = 'Sobaca', age = '3', pet_photo = 'images/racoon1.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['name'] != 'W#@%'

def test7_add_new_pet_with_empty_name(name = ' ', animal_type = 'dog', age = '3', pet_photo = 'images/racoon1.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email,valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo )
    assert  status != 200
    assert result['name'] != ''

def test8_add_new_pet_with_empty_animal_type(name = 'Sobaka', animal_type = '', age = '3', pet_photo = 'images/racoon1.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo )
    assert status != 200
    assert result['animal_type'] != ''

def test9_add_new_pet_with_special_animal_type(name = 'Sobaka', animal_type = 'W#@%', age = '3', pet_photo = 'images/racoon1.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo )
    assert status != 200
    assert result['animal_type'] != 'W#@%'

def test10_add_new_pet_negative_age(name = 'Sobaka', animal_type = 'dog', age = '-3', pet_photo = 'images/racoon1.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo )
    assert status != 200
    assert age not in result['age']
