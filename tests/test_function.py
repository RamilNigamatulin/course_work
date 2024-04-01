import json
from project.function import load_transactions, execute_transaction, replace_in_date, hide_sensitive_info, program_launch
from unittest.mock import mock_open, patch

def test_load_transactions(monkeypatch):
    test_data = [
        {'id': 1, 'date': '2022-01-01T00:00:00'},
        {'id': 2, 'date': '2022-01-02T00:00:00'},
        {'id': 3, 'date': '2022-01-03T00:00:00'},
    ]
    mocked_file = mock_open(read_data=json.dumps(test_data))
    with patch('builtins.open', mocked_file):
        result = load_transactions()
    assert result == test_data
    assert result is not None

def test_execute_transaction():
    base = [
        {'id': 1, 'state': 'EXECUTED'},
        {'id': 2, 'state': 'CANCELED'},
        {'id': 3, 'state': 'EXECUTED'}
    ]
    final_result = [
        {'id': 1, 'state': 'EXECUTED'},
        {'id': 3, 'state': 'EXECUTED'}
    ]

    actual_result = execute_transaction(base)
    assert actual_result == final_result
    assert final_result is not None

def test_replace_in_date():
    base = [
        {'id': 1, 'date': '2019-12-15T10:10:10'},
        {'id': 2, 'date': '2019-12-07T10:10:10'},
        {'id': 3, 'date': '2019-12-10T10:10:10'}
    ]
    final_result = [
        {'id': 1, 'date': '15.12.2019 10:10:10'},
        {'id': 3, 'date': '10.12.2019 10:10:10'},
        {'id': 2, 'date': '07.12.2019 10:10:10'}
    ]
    assert replace_in_date(base) == final_result
    assert final_result is not None

def test_hide_sensitive_info():
    test_file = [
        {'id': 1, 'state': 'EXECUTED', 'from': 'Счет 12345678901234567890', 'to': 'Visa 1234567890123456'},
        {'id': 2, 'state': 'CANCELED', 'from': 'Visa 1234567890123456', 'to': 'Счет 12345678901234567890'},
    ]
    final_result = [
        {'id': 1, 'state': 'EXECUTED', 'from': 'Счет 1234 45** **** **** 7890', 'to': 'Visa **3456'},
        {'id': 2, 'state': 'CANCELED', 'from': 'Visa 1234 56** **** 3456', 'to': 'Счет **7890'},
    ]
    assert hide_sensitive_info(test_file) == final_result
    assert final_result is not None


def test_program_launch(monkeypatch):
    test_file_1 = [
        {'id': 1, 'date': '12.12.2019 10:10:10', 'description': '1', 'from': '1', 'to': '1',
         'operationAmount': {'amount': '1', 'currency': {'name': '1', 'code': '1'}}},
        {'id': 2, 'date': '11.12.2019 10:10:10', 'description': '2', 'from': '2', 'to': '2',
         'operationAmount': {'amount': '2', 'currency': {'name': '2', 'code': '2'}}},
        {'id': 3, 'date': '09.12.2019 10:10:10', 'description': '3', 'from': '3', 'to': '3',
         'operationAmount': {'amount': '3', 'currency': {'name': '3', 'code': '3'}}},
        {'id': 4, 'date': '08.12.2019 10:10:10', 'description': '4', 'from': '4', 'to': '4',
         'operationAmount': {'amount': '4', 'currency': {'name': '4', 'code': '4'}}},
        {'id': 5, 'date': '07.12.2019 10:10:10', 'description': '5', 'to': '5',
         'operationAmount': {'amount': '5', 'currency': {'name': '5', 'code': '5'}}},
    ]

    final_result_1 = "12.12.2019  1\n1 -> 1\n1 1\n11.12.2019  2\n2 -> 2\n2 2\n09.12.2019  3\n3 -> 3\n3 3\n"
    monkeypatch.setattr('builtins.input', lambda _: '3')
    assert program_launch(test_file_1) == final_result_1




