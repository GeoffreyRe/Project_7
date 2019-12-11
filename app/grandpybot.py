"""
This module contains GrandpyBot class
"""
import app.utils.Parser as parser
import app.utils.ApiUser as apiuser
class GrandpyBot():
    """
    This class will use instances from Parser and ApiUser to collect informations from APIs.
    It manages cases where APIs dont give informations
    """

    def __init__(self):
        """ it init instances from Parser and ApiUser class"""
        self.parser = parser.Parser()
        self.api_user = apiuser.ApiUser()

    def try_to_parse_question(self, question):
        """
        Try to parse question and check if parse is succesfull or not
        """
        self.parser.initialize_parser(question)
        parsed = self.parser.parse()
        return parsed

    def try_to_get_infos_from_api(self, place):
        """
        try to get informations from api's with parsed question
        """
        api_response = self.api_user.give_informations(place)
        self.api_user.clear_attributes()
        return api_response

    def answer_to_user(self, question):
        """
        It return a dict with all informations
        """
        parsed = self.try_to_parse_question(question)
        if parsed:
            api_infos = self.try_to_get_infos_from_api(self.parser.parsed_question)
        else:
            api_infos = {}
        return {"parsed" : parsed, "api_infos" : api_infos}
