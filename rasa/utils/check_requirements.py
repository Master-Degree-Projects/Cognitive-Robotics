from rasa_sdk import Tracker
import re

doubt_string = "doubt"


def check_gender(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the gender requirement.
    :param person: The person to check the gender
    :param tracker: Tracker used to get the gender
    :return: True if the person satisfies the gender requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person gender attribute and gender requirement
    gender: str = tracker.get_slot("gender")
    gender = gender.lower() if gender is not None else None
    person_gender: str = person["gender"].lower()

    # checking if the person satisfies the gender requirement
    if gender is not None:
        if gender == doubt_string:
            return True
        if gender != person_gender:
            return False

    return True


def check_upper_color(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the upper color requirement.
    :param person: The person to check the upper color
    :param tracker: Tracker used to get the upper color
    :return: True if the person satisfies the upper color requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person gender attribute and gender requirement
    upper_color: str = tracker.get_slot("upper_color")
    upper_color = upper_color.lower() if upper_color is not None else None
    person_upper_color: str = person["upper_color"].lower()

    # checking if the person satisfies the upper color requirement
    if upper_color is not None:
        if upper_color == doubt_string:
            return True

        is_with_string = tracker.get_slot("is_with_upper")

        # getting is_with value
        is_with: bool = True
        if is_with_string is None:
            is_with = True
        else:
            if is_with_string == "true":
                is_with = True
            elif is_with_string == "false":
                is_with = False

        # if is_with is true checks if the person has the same upper color
        # otherwise checks if the person does not have the same upper color
        if is_with:
            if upper_color != person_upper_color:
                return False
        else:
            if upper_color == person_upper_color:
                return False

    return True


def check_lower_color(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the lower color requirement.
    :param person: The person to check the lower color
    :param tracker: Tracker used to get the lower color
    :return: True if the person satisfies the lower color requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person gender attribute and gender requirement
    lower_color: str = tracker.get_slot("lower_color")
    lower_color = lower_color.lower() if lower_color is not None else None
    person_lower_color: str = person["lower_color"].lower()

    # checking if the person satisfies the gender requirement
    if lower_color is not None:
        if lower_color == doubt_string:
            return True

        is_with_string = tracker.get_slot("is_with_lower")

        # getting is_with value
        is_with: bool = True
        if is_with_string is None:
            is_with = True
        else:
            if is_with_string == "true":
                is_with = True
            elif is_with_string == "false":
                is_with = False

        # if is_with is true checks if the person has the same lower color
        # otherwise checks if the person does not have the same lower color
        if is_with:
            if lower_color != person_lower_color:
                return False
        else:
            if lower_color == person_lower_color:
                return False

    return True


def check_hat(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the hat requirement.
    :param person: The person to check the hat
    :param tracker: Tracker used to get the hat
    :return: True if the person satisfies the hat requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person hat attribute and hat requirement
    hat: str = tracker.get_slot("hat")
    hat = str(hat).lower() if hat is not None else None
    person_hat: str = person["hat"].lower()

    if hat is not None:
        if hat == doubt_string:
            return True

    is_with_hat = tracker.get_slot("is_with_hat")

    if hat is not None and is_with_hat is None:
        is_with_hat = "true"

    # checking if the person satisfies the hat requirement
    if is_with_hat is not None:
        if is_with_hat != person_hat:
            return False

    return True


def check_bag(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the bag requirement.
    :param person: The person to check the bag
    :param tracker: Tracker used to get the bag
    :return: True if the person satisfies the bag requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person bag attribute and bag requirement
    bag: str = tracker.get_slot("bag")
    bag = str(bag).lower() if bag is not None else None
    person_bag: str = person["bag"].lower()

    if bag is not None:
        if bag == doubt_string:
            return True

    is_with_bag = tracker.get_slot("is_with_bag")

    if bag is not None and is_with_bag is None:
        is_with_bag = "true"

    # checking if the person satisfies the bag requirement
    if is_with_bag is not None:
        if is_with_bag != person_bag:
            return False

    return True


def convert_time_in_seconds(string: str) -> int:
    """
    Converts the string in input in seconds, the string must contain a integer number and also the type of time (e.g.
    seconds, hour, minute).
    :param string: The string to convert the value of
    :return: An integer representing the time in seconds
    """
    regex = re.findall(r'\d+', string)

    # setting the time initially and checking if at least one occurrence of the regex exists,
    # if so takes the first value
    time: int = 0
    if len(regex) > 0:
        time = int(regex[0])

    # check if time is in seconds, minutes or hours
    if "second" in string:
        return time
    elif "minute" in string:
        return time*60
    elif "hour" in string:
        return time*60*60
    else:
        # if no type is given, return the time
        return time


def check_bar(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the bar requiremnt.
    :param person: The person to check the bar requirement
    :param tracker: Tracker used to get the bar requirement
    :return: True if the person satisfies the bar requirement or if no requirement about this attribute is given,
    otherwise False
    """
    # is_with_bar, time of persistence bar, bar passages, bar
    bar: str = tracker.get_slot("bar")
    if bar is None:
        return True

    bar = str(bar).lower()

    is_with_bar = tracker.get_slot("is_with_bar")

    # in person form the bar slot is set to true or false in case of affirm or deny
    if bar == "true":
        is_with_bar = "true"
    elif bar == "false":
        is_with_bar = "false"
    elif bar == doubt_string:  # in case of doubt from the user, it does not perform the check on this requirement
        return True

    if bar == "bar" and is_with_bar is None:
        is_with_bar = "true"

    if is_with_bar == "true":
        string_bar_passages: str = tracker.get_slot("bar_passages")
        string_time_of_persistence: str = tracker.get_slot("time_of_persistence_bar")

        # analyzing first the number of passages
        if string_bar_passages is not None:
            aux: str = tracker.get_slot("aux_time_of_persistence")

            # if no aux is found, sets to "for"
            if aux is None:
                aux = "for"

            try:
                bar_passages: int = int(string_bar_passages)
            except Exception as e:
                bar_passages: int = 0
            if aux == "for":
                if bar_passages != int(person["roi1_passages"]):
                    return False
            elif aux == "more":
                if bar_passages >= int(person["roi1_passages"]):
                    return False
            elif aux == "less":
                if bar_passages <= int(person["roi1_passages"]):
                    return False

        # then the time of persistence
        elif string_time_of_persistence is not None:
            # trying to convert the string to integer, if it launches an exception it sets the time to 0
            try:
                time_of_persistence: int = int(string_time_of_persistence)
            except Exception as e:
                time_of_persistence: int = 0

            aux: str = tracker.get_slot("aux_time_of_persistence")
            if aux is None:
                aux = "for"

            if aux == "for":
                if time_of_persistence != int(person["roi1_persistence_time"]):
                    return False
            elif aux == "more":
                if time_of_persistence >= int(person["roi1_persistence_time"]):
                    return False
            elif aux == "less":
                if time_of_persistence <= int(person["roi1_persistence_time"]):
                    return False

        # and last if the person is passed at least one time
        else:
            if int(person["roi1_passages"]) == 0:
                return False
    else:
        # if the person didn't pass near the bar its number of passages must be equal to 0
        if int(person["roi1_passages"]) != 0:
            return False

    return True


def check_market(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the market requiremnt.
    :param person: The person to check the market requirement
    :param tracker: Tracker used to get the market requirement
    :return: True if the person satisfies the market requirement or if no requirement about this attribute is given,
    otherwise False
    """
    # is_with_market, time of persistence market, market passages, market
    market: str = tracker.get_slot("market")
    if market is None:
        return True

    market = str(market).lower()

    is_with_market = tracker.get_slot("is_with_market")

    # in person form the market slot is set to true or false in case of affirm or deny
    if market == "true":
        is_with_market = "true"
    elif market == "false":
        is_with_market = "false"
    elif market == doubt_string:  # in case of doubt from the user, it does not perform the check on this requirement
        return True

    if market == "market" and is_with_market is None:
        is_with_market = "true"

    if is_with_market == "true":
        string_market_passages: str = tracker.get_slot("market_passages")
        string_time_of_persistence: str = tracker.get_slot("time_of_persistence_market")

        # analyzing first the number of passages
        if string_market_passages is not None:
            aux: str = tracker.get_slot("aux_time_of_persistence")

            # if no aux is found, sets to "for"
            if aux is None:
                aux = "for"

            try:
                market_passages: int = int(string_market_passages)
            except Exception as e:
                market_passages: int = 0

            if aux == "for":
                if market_passages != int(person["roi2_passages"]):
                    return False
            elif aux == "more":
                if market_passages >= int(person["roi2_passages"]):
                    return False
            elif aux == "less":
                if market_passages <= int(person["roi2_passages"]):
                    return False

        # then the time of persistence
        elif string_time_of_persistence is not None:
            # trying to convert the string to integer, if it launches an exception it sets the time to 0
            try:
                time_of_persistence: int = int(string_time_of_persistence)
            except Exception as e:
                time_of_persistence: int = 0

            aux: str = tracker.get_slot("aux_time_of_persistence")
            if aux is None:
                aux = "for"

            if aux == "for":
                if time_of_persistence != int(person["roi2_persistence_time"]):
                    return False
            elif aux == "more":
                if time_of_persistence >= int(person["roi2_persistence_time"]):
                    return False
            elif aux == "less":
                if time_of_persistence <= int(person["roi2_persistence_time"]):
                    return False

        # and last if the person is passed at least one time
        else:
            if int(person["roi2_passages"]) == 0:
                return False

    else:
        # if the person didn't pass near the market its number of passages must be equal to 0
        if int(person["roi2_passages"]) != 0:
            return False

    return True


def check_person(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies all the requirements.
    :param person: The person to check the requirements
    :param tracker: Contains the information given by the user
    :return: True if the person satisfies all the requirements, otherwise False
    """
    if not check_gender(person=person, tracker=tracker):
        return False

    if not check_upper_color(person=person, tracker=tracker):
        return False

    if not check_lower_color(person=person, tracker=tracker):
        return False

    if not check_hat(person=person, tracker=tracker):
        return False

    if not check_bag(person=person, tracker=tracker):
        return False

    if not check_bar(person=person, tracker=tracker):
        return False

    if not check_market(person=person, tracker=tracker):
        return False

    return True


def check_all_doubt(tracker: Tracker):
    """
    Checks if all the slots are set to the doubt string.
    :param tracker: Contains the information given by the user
    :return: True if all the doubt slots are set to the doubt string, otherwise False
    """
    doubt_slots = ["gender", "upper_color", "lower_color", "hat", "bag", "bar", "market"]

    for slot in doubt_slots:
        slot_value: str = tracker.get_slot(slot)
        if slot_value is None:
            return False
        if str(slot_value).lower() != doubt_string:
            return False

    return True
