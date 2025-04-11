from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from utils.correct_entities import correct_entities, read_json


class ActionCorrectEntitiesValues(Action):
    _bar = ["time_of_persistence_bar", "bar_passages"]
    _market = ["time_of_persistence_market", "market_passages"]
    _roi = ["time_of_persistence_", "_passages"]

    def name(self) -> Text:
        return "action_correct_entities_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Update slots with correct values
        :param dispatcher:
        :param tracker:
        :param domain:
        :return: updated slots or None
        """

        all_values = tracker.current_slot_values()
        duration = next(tracker.get_latest_entity_values("duration"), None)
        number = next(tracker.get_latest_entity_values("number"), None)

        # track entity in the last intent
        market_presence = next(tracker.get_latest_entity_values("roi", entity_group="market_group"), None)
        bar_presence = next(tracker.get_latest_entity_values("roi", entity_group="bar_group"), None)

        duration_s_list = roi_passages_list = list()
        if market_presence is not None or bar_presence is not None:

            if duration is not None or number is not None:
                latest_values = self._obtain_values_entities(tracker.latest_message["entities"])
                duration_s_list = self._value_duckling_second(latest_values)
                roi_passages_list = self._roi_passages_duckling(latest_values)

        entities_values = dict()
        entities_db = read_json()

        for i in all_values:
            slot_value = tracker.get_slot(i)

            if slot_value is None:
                slot_value = "None"

            elif slot_value is True or slot_value is False:
                slot_value = str(slot_value).lower()

            if slot_value not in entities_db["values"] and i != "duration" and i != "number":
                entities_values[i] = slot_value

        if len(entities_values) > 0:
            correct_slot = correct_entities(entities_values)

            if len(duration_s_list) > 0:
                for element in duration_s_list:
                    correct_slot[element[0]] = element[2]

            if len(roi_passages_list) > 0:
                for element in roi_passages_list:
                    correct_slot[element[0]] = element[2]

            print("correct entities values: ", correct_slot)
            return [SlotSet(key, value) for key, value in correct_slot.items()]

        return []

    def _value_duckling_second(self, all_values) -> List:
        """
        Process the 'duration' and 'roi' values to update
        the ROI passages with duration information.

        :param all_values: Dictionary containing all current slot values.
        :return: A list of elements representing updated time of persistence of roi
                with duration information.
        """

        ordered_roi = all_values["roi"]

        for i, duration in enumerate(all_values["duration"]):
            for j, roi in enumerate(ordered_roi):
                if roi[-1] == duration[-1]:
                    ordered_roi[j][2] = duration[0]
                    ordered_roi[j][0] = self._roi[0] + ordered_roi[j][0]

        return [element for element in ordered_roi if element[2] != -1]

    def _roi_passages_duckling(self, all_values) -> List:
        """
        Process the 'number' entity to update
        the ROI passages with number information.

        :param all_values: Dictionary containing all current slot values.
        :return: A list of elements representing updated
                ROI passages with number information.
        """
        ordered_roi = all_values["roi"]

        for i, number in enumerate(all_values["number"]):
            for j, roi in enumerate(ordered_roi):
                if ordered_roi[j][-1] == number[-1]:
                    ordered_roi[j][2] = number[0]

                elif ordered_roi[j][2] == -1:
                    # no presence one of two roi
                    ordered_roi[j][2] = None
                ordered_roi[j][0] = ordered_roi[j][0] + self._roi[1]

        return [element for element in ordered_roi if element[2] != -1]

    def _obtain_values_entities(self, values) -> Dict[Text, Any]:
        """
        Extract and organize relevant information
        from entities in the latest message.

        :param values: List of entities extracted from the latest user message.
        :return: A dictionary containing organized information
                related to 'roi', 'duration', and 'number'.
        """
        all_values = {
            "roi": [["market", -1, -1, -1], ["bar", -1, -1, -1]],
            "duration": [],
            "number": [],
        }

        index_roi = index_duc = 0
        for i, element in enumerate(values):
            if element["entity"] == "roi" and element["group"] == "market_group":
                all_values["roi"][0] = ["market", element["start"], -1, index_roi]
                index_roi += 1
                if index_roi == 2 and index_duc == 0:
                    index_duc = 1

            elif element["entity"] == "roi" and element["group"] == "bar_group":
                all_values["roi"][1] = ["bar", element["start"], -1, index_roi]
                index_roi += 1

                # se ci stanno 2 roi e la prima non ha duration o number, mentre la seconda potrebbe esserci
                if index_roi == 2 and index_duc == 0:
                    index_duc = 1

            elif element["entity"] == "duration":
                if "additional_info" in element.keys():
                    all_values["duration"].append([element["additional_info"]["normalized"]["value"], index_duc])
                    index_duc += 1

            elif element["entity"] == "number":
                if "additional_info" in element.keys():
                    all_values["number"].append([element["value"], index_duc])
                    index_duc += 1

        return all_values



