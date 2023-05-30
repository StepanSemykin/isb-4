import hashlib
import multiprocessing as mp
import logging
from collections.abc import Callable

logger = logging.getLogger()
logger.setLevel('INFO')


def is_valid(hash: str, number: str) -> bool:
    """Compares the hash of the card with the number.
    Args:
        hash (str): Hash cards.
        number (str): Card number.
    Returns:
        bool: Verification result.
    """
    return hashlib.sha224(number.encode()).hexdigest() == hash


def get_number(hash: str, last_numerals: str,
               bins: tuple, cores: int = mp.cpu_count(), 
               func: Callable[[int], None] = None) -> list:
    """Gets correct card numbers by hash.
    Args:
        hash (str): Hash cards.
        last_numerals (str): Last 4 digits of the card.
        bins (tuple): Bins card.
        cores (int, optional): Number of processor cores. 
        Defaults to mp.cpu_count().
        func (Callable[[int], None], optional): 
        Annotation of the function to increase the progress bar. 
        Defaults to None.
    Returns:
        list: List of correct numbers.
    """
    result_list = []
    count_bins = 0
    with mp.Pool(processes=cores) as p:
        for j in bins:
            numbers = [(hash, f'{j}{str(i).zfill(6)}{last_numerals}')
                       for i in range(0, 1000000)]
            results = p.starmap(is_valid, numbers)
            for index, result in enumerate(results):
                if result:
                    result_list.append(int(numbers[index][1]))
            count_bins += 1
            func(count_bins)
    return result_list


def luhn_algorithm(number: str) -> bool:
    """Сhecks if the card number is real.
    Args:
        number (str): Card number.
    Returns:
        bool: Verification result.
    """
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
