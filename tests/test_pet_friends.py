import os.path

from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_add_new_pet_with_valid_data(name = 'Граф', animal_type = 'Корсак', age = '2', pet_photo = 'images/images.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_inf_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_post_add_new_pet_without_photo_with_valid_data(name='Морф', animal_type='Морф', age='2', pet_photo=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet_with_valid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.post_add_inf_about_new_pet(auth_key, 'Граф', 'Кане-корсо', '2', 'images/images.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Лорд', animal_type='Кане-корсо', age='3'):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   if len(my_pets['pets']) > 0:
       status, result = pf.successful_update_self_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

       assert status == 200
       assert result['name'] == name
   else:
       raise Exception("There is no my pets")


def test_add_new_pet_photo_info(pet_photo='images\images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200

    else:
        raise Exception("There is no my pets")