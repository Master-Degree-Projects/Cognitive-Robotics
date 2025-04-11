from typing import Any, Text, Dict, List

from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import json
from utils.check_requirements import *

# name of the two regions of interest
roi1_name = "bar"
roi2_name = "market"


def debug(info):
    print("DEBUG:")
    for key, value in info:
        print(f"ENTITY: {key} - EXTRACTED VALUE: {value} - TYPE: {type(value)}")


class ActionSubmitCount(Action):
    def name(self) -> Text:
        return "action_submit_count"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
                dispatcher.utter_message(f"There is only one person that satisfies your requirements.")
                dispatcher.utter_message(response="utter_ask_new_search")
            elif len(datastore) > 1:
                dispatcher.utter_message(f"I found {len(datastore)} people that satisfy the description.")
            else:  # if no person was found
                dispatcher.utter_message("I'm so sorry, I've not found any person that satisfies the requirements...")
                dispatcher.utter_message(response="utter_ask_new_search")



        except Exception as e:
            # if an exception is found, it utters a "don't understand" message and resets all the slots
            dispatcher.utter_message(response="utter_dont_understand")
            return [AllSlotsReset()]
            # dispatcher.utter_message("Error during the loading of the file...")

        return []
