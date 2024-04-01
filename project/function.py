import json
from datetime import datetime


def load_transactions():
    """Загружает список операций из файла """
    with open("base.json") as file:
        base = json.load(file)
        return base



def execute_transaction(base_files):
    """ Создает список успешных операций """
    good_transactions = []
    for transaction in base_files:
        if transaction.get("state") == "EXECUTED":
            good_transactions.append(transaction)
    return good_transactions


def replace_in_date(base_good_files):
    """приводит даты в соответствующий формат и сортирует дату по убыванию"""
    good_dates = []
    for stock in base_good_files:
        stock['date'] = stock['date'].replace("T", " ")
        stock["date"] = stock["date"][0:19]
        date_obj = datetime.strptime(stock["date"], '%Y-%m-%d %H:%M:%S')
        formatted_date = date_obj.strftime('%d.%m.%Y %H:%M:%S')
        stock["date"] = formatted_date
        good_dates.append(stock)
    good_dates = sorted(good_dates, key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y %H:%M:%S'), reverse=True)
    return good_dates


def hide_sensitive_info(sorted_files):
    '''скрывает информацию о счетах'''
    for item in sorted_files:
        if 'from' in item:
            account_number = item['from']
            if 'Счет' in account_number:
                hidden_account_number = account_number[:-16] + ' ' + account_number[-17:-15] +'** **** **** ' + account_number[-4:]
            else:
                hidden_account_number = account_number[:-12] + ' ' + account_number[-12:-10] + '** **** ' + account_number[-4:]
            item['from'] = hidden_account_number
        if 'to' in item:
            account_number = item['to']
            if 'Счет' in account_number:
                hidden_account_number = account_number[:-20] + '**' + account_number[-4:]
            else:
                hidden_account_number = account_number[:-16] + '**' + account_number[-4:]
            item['to'] = hidden_account_number
    return sorted_files


def program_launch(sorted_list):
    '''Выводит конечную требуемую информацию'''
    while True:
        name = input("Приветствую! Введите количество последних выполненных операций, которое необходимо вывести: ")
        try:
            name = int(name)
            if name > len(sorted_list):
                print("Вы ввели недопустимое количество выполненных операций, попробуйте ввести меньшее количество!")
            else:
                break
        except ValueError:
            print("Введите текст цифрами. Попробуйте еще раз!")
    end_result = ""
    for i in sorted_list[:name]:
        source = i.get('from', '  ')
        end_result += (f"{i['date'][0:11]} {i['description']}\n"
                       f"{source} -> {i['to']}\n"
                       f"{i['operationAmount']['amount']} {i['operationAmount']['currency']['name']}\n")
    return end_result

