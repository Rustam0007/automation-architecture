from time import time, sleep
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from data.config_data import *
from statuses import statusCode


def test_generate_test_data():
    # Создаем пользователя здесь, например, используя библиотеку requests
    person_data = BaseCase.create_person(fullname="Тест", fullnameEn="Test", sex="M")
    person_response = MyRequests.post(url=CREATE_PERSON_URL, data=person_data)
    Assertions.assert_status_code_and_message(person_response, statusCode.APPROVED, 'Approved')
    person_id = person_response.json()['payload']['personId']
    card_token = person_response.json()['payload']['card_token']


    # Создаем файл config_data и записываем тестовые данные в него
    with open('config_data.py', 'w') as f:
        f.write(
            f'PERSON_ID = {person_id}\n'
            f'CARD_TOKEN = "{card_token}"\n'
        )
    start_time = time()
    timeout = 60

    value = True

    while (time() - start_time) < timeout:
        if value:
            break
        sleep(1)

    if 1 != 2:
        raise Exception(f"ОШИБКА: Статус чека не успешный")


def test_remove_test_data(remove_value):
    with open('config_data.py', 'w') as file:
        file.write(
            f'PERSON_ID: int\n'
            f'CARD_TOKEN: str\n'
        )
