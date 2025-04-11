from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionSuit(Action):
    _ask_info = "ask_with_info"

    def name(self) -> Text:
        return "action_suit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Check if entity shirt has value suit.
        :param dispatcher:
        :param tracker:
        :param domain:
        :return: set lower_color and upper_color with same value.
        """
        synonyms_unique_entity = ("clothing", "duds", "dress", "suit and tie", "suit")
        colors = ("blue", "white", "black", "red", "green", "yellow", "orange", "purple", "pink", "brown", "gray")

        user_intent = tracker.get_intent_of_latest_message()

        groups = ["lower_group", "upper_group"]

        if user_intent == self._ask_info:

            value_shirt = list(tracker.get_latest_entity_values("shirt", entity_group=groups[1]))
            value_color_upper = list(tracker.get_latest_entity_values("color", entity_group=groups[1]))
            value_with_upper = list(tracker.get_latest_entity_values("is_with", entity_group=groups[1]))

            value_pants = list(tracker.get_latest_entity_values("pants", entity_group=groups[0]))
            value_color_lower = list(tracker.get_latest_entity_values("color", entity_group=groups[0]))
            value_with_lower = list(tracker.get_latest_entity_values("is_with", entity_group=groups[0]))

            color = ""
            value_with = ""
            presence_suit = False
            if len(value_shirt) > 0:
                if value_shirt[-1] in synonyms_unique_entity:
                    presence_suit = True

            if len(value_pants) > 0:
                if value_pants[-1] in synonyms_unique_entity:
                    presence_suit = True

            if presence_suit is False:
                return []

            if len(value_color_upper) > 0 and len(value_with_upper) > 0:
                last_value_upper = value_color_upper[-1]

                if last_value_upper in colors:
                    color = last_value_upper

                last_value_upper = value_with_upper[-1]
                
                if last_value_upper == "true" or last_value_upper == "false":
                    value_with = last_value_upper

                return [SlotSet("upper_color", color), SlotSet("lower_color", color), SlotSet("is_with_lower", value_with)]

            if len(value_color_lower) > 0 and len(value_with_lower) > 0:
                value_lower = value_color_lower[-1]
                if value_lower in colors:
                    color = value_lower

                value_lower = value_with_lower[-1]
                for value_lower in value_with_lower:
                    if value_lower == "true" or value_lower == "false":
                        value_with = value_lower
                return [SlotSet("upper_color", color), SlotSet("lower_color", color), SlotSet("is_with_upper", value_with)]

            dispatcher.utter_message(text=color)

        return []

