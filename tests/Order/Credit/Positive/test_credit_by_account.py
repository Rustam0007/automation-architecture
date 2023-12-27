import time
import allure
import json
from allure import attach, attachment_type, step
from data.client_data import SERVICE_NAME, OURACCOUNT
from lib.allure_step_text import *
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREDIT_URL
from statuses import statusCode, currency, orderType, transactionStatus
from random import randint
from statuses.operationText import *


@allure.label('owner', 'Rustam Saidov')
class TestCreditByAccount(BaseCase):
    @allure.feature(f'{positive_cases} Credit By Account')
    def test_credit_by_account(self, select_value):
        with allure.step(f'{data_create} для Credit By Account'):
            data_credit = self.creditByAccount(externalRef=None, account=OURACCOUNT, amount=randint(101, 300),
                                           currency=currency.TJS, hasFee='0')
        with allure.step(send_request):
            credit_response = MyRequests.post(url=CREDIT_URL, data=data_credit)
            allure.attach(json.dumps(data_credit), name='Request:', attachment_type=attachment_type.JSON)
            allure.attach(json.dumps(credit_response.json()), name='Response:', attachment_type=attachment_type.JSON)

        with allure.step(response_code):
            Assertions.assert_code_status(credit_response, statusCode.APPROVED)

        with allure.step('Сохранение id для валидации'):
            credit_id = credit_response.json()['payload']['id']
        with allure.step('Сохранение externalRef для валидации'):
            externalRef = credit_response.json()['payload']['externalRef']
        with allure.step('Сохранение amount для валидации'):
            amount = credit_response.json()['payload']['amount']

        with allure.step("БД: берём из бд значение колонки: status, amount, code, type, description для валидации"):
            db_info = select_value('status, amount, code, type, description', 'transaction', 'id', credit_id)
        db_info_dict = {
            "status": db_info[0],
            "amount": db_info[1],
            "code": db_info[2],
            "type": db_info[3],
            "description": db_info[4]
        }

        with allure.step("Проверка: status в БД равен 1 (approved)"):
            assert db_info_dict["status"] == transactionStatus.APPROVED, \
                f"UnExpected: status. Expected: {transactionStatus.APPROVED}. Actually: {db_info_dict['status']}"

        with allure.step("Проверка: amount в БД равен amount который отправляем в запросе"):
            assert db_info_dict["amount"] == amount, f"UnExpected: amount. Expected: {amount}. Actually: {db_info_dict['amount']}"

        with allure.step("Проверка: code в БД равен 1000 (approved)"):
            assert db_info_dict["code"] == statusCode.APPROVED, \
                f"UnExpected: code. Expected: {statusCode.APPROVED}. Actually: {db_info_dict['code']}"

        with allure.step("Проверка: type в БД равен 12 (Credit)"):
            assert db_info_dict["type"] == orderType.CREDIT, \
                f"UnExpected: type. Expected: {orderType.CREDIT}. Actually: {db_info_dict['type']}"

        with allure.step("Проверка: description в БД совпадет с шаблоном: decription, название сервиса: SERVICE_NAME, ИД сервиса: externalRef"):
            assert db_info_dict["description"] == f"{CREDITBYACCOUNT}, название сервиса: {SERVICE_NAME}, ИД сервиса: {externalRef}", \
                f"UnExpected: description. " \
                f"Expected: {CREDITBYACCOUNT}, название сервиса: {SERVICE_NAME}, ИД сервиса: {externalRef}. " \
                f"Actually: {db_info_dict['description']}"
