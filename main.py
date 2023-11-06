import logging
import random
import json
from typing import List, Set, Tuple

logging.basicConfig(level=logging.INFO)


class SecretSantaCalculator:
    """
    Small class which calculates secret santas for pairs
    lith the only rules, that the secret santa is not
    the partner of gifted one
    """
    def __init__(self, pair_list: List[Set]):
        """
        Constructor which initializes every iterators needed
        :param pair_list: List containing sets of pairs (of 2 strings)
        """
        self.pair_list = pair_list

        self.gifters_left = []
        for pair in pair_list:
            for person in pair:
                self.gifters_left.append(person)
        self.gifteds_left = self.gifters_left.copy()
        self.secret_santas = []

    def _get_pair_of_person(self, person: str):
        """
        Returns the pair the person is in
        :param person: person
        :return: pair of person
        """
        for pair in self.pair_list:
            if person in pair:
                return pair

    def _search_for_gifted(self, gifter: str):
        """
        Search for a possible gifted person. If None is left, raise a ValueError
        :param gifter: secret santa
        :return: person to be gifted
        """
        ensure_no_ones_left = len(self.gifteds_left) - 1
        numbers_tried = set()
        random_index = -1
        for i in range(ensure_no_ones_left + 1):  # +1 to ignore random_index's -1
            while random_index in numbers_tried:
                random_index = random.randint(a=0, b=len(self.gifteds_left) - 1)
            numbers_tried.add(random_index)

            possible_gifted = self.gifteds_left[random_index]
            if possible_gifted != gifter and possible_gifted not in self._get_pair_of_person(gifter):
                self.gifteds_left.remove(possible_gifted)
                return possible_gifted
        raise ValueError(f"Couldn't find anyone for {gifter}")

    def calculate_secret_santas(self) -> List[Tuple]:
        """
        Searches for every person a secret santa
        :return: list of
        """
        while len(self.gifters_left):
            gifter = self.gifters_left.pop()
            gifted = self._search_for_gifted(gifter)
            self.secret_santas.append((gifter, gifted))
        return self.secret_santas


if __name__ == "__main__":
    with open("pair_list.json") as pl_file:
        json_pair_list = json.load(pl_file)

    # Format into sets (json don't know sets unfortunately)
    pair_list = []
    for pair in json_pair_list:
        pair_list.append({pair[0], pair[1]})

    while True:
        ssc = SecretSantaCalculator(pair_list=pair_list)
        try:
            secret_santas = ssc.calculate_secret_santas()
        except ValueError as e:
            logging.debug(e)
        else:
            for gifter, gifted in secret_santas:
                logging.info(f"{gifter} is secret santa of {gifted}")
            break
        finally:
            logging.debug("Gifters left", ssc.gifters_left)
            logging.debug("Gifteds left", ssc.gifteds_left)
