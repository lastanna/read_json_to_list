import argparse
import json
import logging
from collections.abc import Iterable
from typing import Any, List, Dict


def check_instances(value: Any, res_lst: List) -> None:
    """
    Проверяем тип, если простой тип присоединяем к листу,
    иначе отдаем в рекурсивную функцию
    :param res_lst: результирующий список
    :param value: элемент json-а, который будем проверять
    :return: None
    """
    if any([isinstance(value, typ) for typ in (str, float, int)]):
        res_lst.append(value)
    elif isinstance(value, Iterable):
        parse_json(value, res_lst)
    else:
        res_lst.append(value)


def parse_dict(dct: Dict, res_lst: List) -> None:
    """
    Проверяет каждый элемент словаря:
    присоединяет ключ к списку, проверяет значение на тип
    :param dct: словарь из json (любого уровня вложенности)
    :param res_lst: результирующий список
    :return: None
    """
    for key, value in dct.items():
        res_lst.append(key)
        check_instances(value, res_lst)


def parse_list(sublst: List, res_lst: List) -> None:
    """
    Проверяет значение каждого элемента списка на тип
    :param sublst: список из json (любого уровня вложенности)
    :param res_lst: результирующий список
    :return: None
    """
    for item in sublst:
        check_instances(item, res_lst)


def read_json(filepath: str) -> Any:
    """
    Читает json файл
    :param filepath: путь к json файлу
    :return: данные из json файла
    """
    with open(filepath, 'r') as json_file:
        return json.load(json_file)


def parse_json(item: Any, lst=[]) -> List:
    """
    Берет каждый итерируемый элемент json-a и проверяет
    является ли он словарём или списком
    Рекурсивная функция
    :param item: любой из итерируемых элементов json-а
    :param lst: результирующий список
    :return: результирующий список
    """
    if isinstance(item, dict):
        parse_dict(item, lst)
    if isinstance(item, list):
        parse_list(item, lst)
    return list(set(lst))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    args = parser.parse_args()
    if args.filepath:
        data = read_json(args.filepath)
        result = parse_json(data)
    else:
        logging.warning('''Please give a filepath
        as python script argument: python main.py --filepath''')
