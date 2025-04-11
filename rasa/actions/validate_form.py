from typing import Any,Optional, Text, Dict, List

from rasa_sdk.events import EventType, SlotSet
from rasa_sdk import Tracker
from rasa_sdk import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from utils.correct_entities import validate_input_form


class ValidatePersonForm(FormValidationAction):
    _ask_intent = "ask_with_info"
    _unknown = "DOUBT"
    _unknown_intent = "doubt"
    _affirm_intent = ["affirm_with_entity", "affirm"]
    _deny_intent = ["deny_with_entity", "deny"]
    _no_passages = "0"

    def name(self) -> Text:
        return "validate_person_form"

    def validate_gender(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if self._intent_not_know(user_intent):
            return {"gender": self._unknown}
        else:
            return {"gender": validate_input_form("gender", slot_value)}

    def validate_bag(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if user_intent in self._affirm_intent:
            return {"bag": True}
        elif user_intent in self._deny_intent:
            return {"bag": False}

        if self._intent_not_know(user_intent):
            return {"bag": self._unknown}
        else:
            return {"bag": validate_input_form("bag", slot_value)}

    def validate_hat(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if user_intent in self._affirm_intent:
            return {"hat": True}
        elif user_intent in self._deny_intent:
            return {"hat": False}

        if self._intent_not_know(user_intent):
            return {"hat": self._unknown}
        else:

            return {"hat": validate_input_form("hat", slot_value)}

    def validate_upper_color(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if self._intent_not_know(user_intent):
            return {"upper_color": self._unknown}
        else:
            slot_value = validate_input_form("upper_color", slot_value)
            return self._found_suit(tracker.get_slot("suit"), slot_color=slot_value, slot_name="upper_color")

    def validate_lower_color(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if self._intent_not_know(user_intent):
            return {"lower_color": self._unknown}
        else:
            slot_value = validate_input_form("lower_color", slot_value)
            return self._found_suit(tracker.get_slot("suit"), slot_color=slot_value, slot_name="lower_color")

    def validate_bar(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if self._intent_not_know(user_intent):
            return {"bar": self._unknown, "bar_passages": self._unknown,
                    "time_of_persistence_bar": self._unknown}

        elif user_intent in self._deny_intent:
            return {"bar": False, "bar_passages": self._no_passages, "time_of_persistence_bar": self._no_passages}

        else:
            return {"bar": slot_value}

    def validate_market(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if self._intent_not_know(user_intent):
            return {"market": self._unknown, "market_passages": self._unknown,
                    "time_of_persistence_market": self._unknown}

        elif user_intent in self._deny_intent:
            return {"market": False, "market_passages": self._no_passages, "time_of_persistence_market": self._no_passages}

        else:
            return {"market": slot_value}

    def validate_time_of_persistence_market(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if self._intent_not_know(user_intent):
            return {"time_of_persistence_market": self._unknown}
        else:
            return {"time_of_persistence_market": self._value_duckling_second(tracker.latest_message["entities"], slot_value)}

    def validate_time_of_persistence_bar(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)


        if self._intent_not_know(user_intent):
            return {"time_of_persistence_bar": self._unknown}
        else:
            return {"time_of_persistence_bar": self._value_duckling_second(tracker.latest_message["entities"], slot_value)}

    def _intent_not_know(self, intent) -> bool:

        return True if self._unknown_intent in intent else False

    def _found_suit(self, slot_suit, slot_color, slot_name):
        synonyms_suit = ("clothing", "duds", "dress", "suit and tie", "suit")

        if slot_suit in synonyms_suit:
            if "upper" in slot_name:
                return {"lower_color": slot_color}
            elif "lower" in slot_name:
                return {"upper_color": slot_color}

        return {slot_name: slot_color}

    def _value_duckling_second(self, values, slot_value):

        for element in values:
            if element["entity"] == "duration":
                if "additional_info" in element.keys():
                    return element["additional_info"]["normalized"]["value"]

        return slot_value