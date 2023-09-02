from api import PetFriends
from settings import valid_email, valid_password
import os.path
from models import *


pf = PetFriends()


def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """Проверяем возможность получить API ключ при авторизации."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert Key(**result)
    pass

def test_get_all_pets_with_valid_key(filter = "my_pets"):
    """Проверяем что запрос всех питомцев возвращает не пустой список."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0
    assert PetsCollection(**result)

def test_add_new_pet_with_valid_data(name = "котяра", animal_type = "кот", age = 2, pet_photo = "images/test_cat.jpg"):
    """Проверяем возможность добавить нового питомца."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name
    assert Pet(**result)

def test_successful_update_self_pet_info(name="чумазый", animal_type="кошакер", age=5):
    """Проверяем возможность обновления информации о питомце."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result["name"] == name
        assert Pet(**result)
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца."""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "котяра", "кот", "2", "images/test_cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    assert PetsCollection(**my_pets)

def test_add_new_pet_without_photo_valid_data(name = "котяра", animal_type = "кот", age = 2):
    """Проверяем возможность добавить нового питомца без фото."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name
    assert Pet(**result)

def test_successful_update_pet_photo(pet_photo = "images/test_cat.jpg"):
    """Проверяем возможность добавить фото созданному питомцу."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets["pets"][0]["id"], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result["pet_photo"] != " "
        assert PetsCollection(**my_pets)
    else:
        raise Exception("There is no my pets")
