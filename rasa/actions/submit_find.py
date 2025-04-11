from typing import Any, Text, Dict, List

from rasa_sdk.events import FollowupAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import json
from utils.check_requirements import *
from rasa_sdk.events import SlotSet
# name of the two regions of interest
roi1_name = "bar"
roi2_name = "market"


def debug(info):
    print("DEBUG:")
    for key, value in info:
        print(f"ENTITY: {key} - EXTRACTED VALUE: {value} - TYPE: {type(value)}")


def print_person_info(person, dispatcher: CollectingDispatcher):
    string = "I found the person you're looking for. "

    subj = "it"
    pron = "it"

    # getting information about the gender
    if person["gender"] == "male":
        subj = "he"
        pron = "him"
    else:
        subj = "she"
        pron = "her"

    # printing information about clothes
    #string += f"{subj} is wearing {person['upper_color']} on the top and {person['lower_color']} on the bottom. "

    ## printing information about hat
    #if person["hat"] == "true":
    #    string += f"{subj} is wearing a hat and "
    #else:
    #    string += f"{subj} isn't wearing a hat and "

    ## printing information aboutbag
    #if person["bag"] == "true":
    #    string += f"{subj} has a bag. "
    #else:
    #    string += f"{subj} hasn't a bag. "

    # getting information about the passages in the roi
    has_passed_roi1 = person["roi1_passages"] > 0
    roi1_persistence_time = person["roi1_persistence_time"]
    has_passed_roi2 = person["roi2_passages"] > 0
    roi2_persistence_time = person["roi2_persistence_time"]

    if has_passed_roi1 and has_passed_roi2:
        string += f"I saw {pron} near the {roi1_name.lower()} and the {roi2_name.lower()} before."
    elif has_passed_roi1:
        string += f"I saw {pron} near the {roi1_name.lower()} before, {subj} stayed there for about {roi1_persistence_time} seconds."
    elif has_passed_roi2:
        string += f"I saw {pron} near the {roi2_name.lower()} before, {subj} stayed there for about {roi2_persistence_time} seconds."
    else:
        string += f"I didn't see {pron} neither near the {roi1_name.lower()} nor near the {roi2_name.lower()}."

    dispatcher.utter_message(string)
    dispatcher.utter_message(response="utter_ask_new_search")


class ActionSubmitFind(Action):
    def name(self) -> Text:
        return "action_submit_find"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(tracker.get_intent_of_latest_message())

        # extracting info from the slots that are set
        info = [(key, tracker.get_slot(key)) for key in tracker.slots]

        # ----- TO REMOVE -----
        debug(info)

        if check_all_doubt(tracker):
            dispatcher.utter_message(response="utter_dont_understand")
            return [AllSlotsReset()]

        # if no info is extracted, the search in the database is not performed
        if len(info) == 0:
            dispatcher.utter_message(response="utter_dont_understand")
            return []

        try:
            filename = "output.json"

            with open(filename, 'r') as f:
                datastore = json.load(f)["people"]

            tmp_datastore = datastore.copy()

            for person in datastore:
                if not check_person(person=person, tracker=tracker):
                    tmp_datastore.remove(person)
            datastore = tmp_datastore.copy()

            # bot says the results of the research
            if len(datastore) == 1:
                person = datastore[0]
                print_person_info(person=person, dispatcher=dispatcher)

                return [AllSlotsReset()]
            elif len(datastore) > 1:
                dispatcher.utter_message(f"I found {len(datastore)} people that satisfy the description.")
                for person in datastore:
                    print(person)

                if tracker.get_intent_of_latest_message() == "stop_form":
                    return[SlotSet("requested_slot", None)]

                return [FollowupAction("utter_ask_other_info")]
            else:  # if no person was found
                dispatcher.utter_message("I'm so sorry, I've not found any person that satisfies the requirements...")

                dispatcher.utter_message(response="utter_ask_new_search")
                return [AllSlotsReset()]

        except Exception as e:
            # if an exception is found, it utters a "don't understand" message and resets all the slots
            print(e)
            dispatcher.utter_message(response="utter_dont_understand")
            return [AllSlotsReset()]

        return []
