import hashlib
from typing import Callable
import multiprocessing as mp
import logging
from random import randint

logger = logging.getLogger()
logger.setLevel('INFO')


def is_valid(hash: str, number: str) -> bool:
    return hashlib.sha224(number.encode()).hexdigest() == hash


def get_number(hash: str, last_numerals: str, 
               bins: tuple, cores: int = mp.cpu_count()) -> list:
    result_list = []
    with mp.Pool(processes=cores) as p:
        for j in bins:
            numbers = [(hash, f'{j}{str(i).zfill(6)}{last_numerals}')
                       for i in range(0, 1000000)]
            results = p.starmap(is_valid, numbers)
            for index, result in enumerate(results):
                if result:
                    result_list.append(int(numbers[index][1]))
                    logging.info('Card valid number found')
    return result_list


def luhn_algorithm(number: str) -> bool:
    last = number[-1]
    reverse_number = number[:len(number)-1]
    reverse_number = reverse_number[::-1]
    sum = 0
    for index, el in enumerate(reverse_number):
        if index % 2 == 0:
            s = int(el) * 2
            if s >= 10:
                s -= 9
            sum += s
        else:
            sum += int(el)
    sum = (10 - ((sum % 10) % 10))
    logging.info(f' Сard number:{number} is verified using Luhn algorithm')
    return sum == last
