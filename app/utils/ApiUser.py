"""
This module contains ApiUser class
"""
import requests
class ApiUser():
    """
    This class has the responsibility of retrieve informations from api
    """
    def __init__(self):
        self.HTTP_BASE_REQUEST_API_HERE_GEOCOORDS = ("https://places.cit.api.here.com/"
                                                     "places/v1/discover/search?")
        self.HTTP_BASE_REQUEST_API_WIKIPEDIA = "https://fr.wikipedia.org/w/api.php?"
        self.place_to_find = None
        self.app_id, self.app_code = "", ""
        self.wiki_id, self.wiki_infos = None, None
        self.lon, self.lat = None, None
        self.request_success = False
        self.find_infos_success = False

    def set_place_to_find(self, place):
        """
        This method assigns value to place to find attribute
        """
        self.place_to_find = place

    def clear_attributes(self):
        """
        This method reset most of attributes
        """
        self.place_to_find = None
        self.wiki_id, self.wiki_infos = None, None
        self.lon, self.lat = None, None
        self.find_infos_success, self.request_success = False, False

    def construct_http_request(self, find_geocoords=False, find_wiki_infos=False, get_wiki_id=False):
        """
        This method construct http request wich will be send to mediawiki api and here api.
        """
        if find_geocoords:
            parameters_http_request = ("app_id={0}&app_code={1}&q={2}&at=0,"
                                       "0".format(self.app_id, self.app_code, self.place_to_find))
            return self.HTTP_BASE_REQUEST_API_HERE_GEOCOORDS + parameters_http_request
        elif find_wiki_infos:
            parameters_http_request = ("action=query&pageids={0}&prop=extracts&explaintext=true"
                                       "&exsectionformat=wiki&format=json".format(self.wiki_id))
            return self.HTTP_BASE_REQUEST_API_WIKIPEDIA + parameters_http_request
        elif get_wiki_id:
            parameters_http_request = ("action=query&list=geosearch&gscoord={0}|{1}&gsradius=10000"
                                       "&gslimit=10&format=json".format(self.lon, self.lat))
            return self.HTTP_BASE_REQUEST_API_WIKIPEDIA + parameters_http_request


    def send_http_request(self, param_dict):
        """
        This method send hhtp request with module requests
        """
        request = self.construct_http_request(**param_dict)
        try:
            response = requests.get(request)
            self.request_success = True
        except:
            response = {}
            self.request_success = False


        return response

    def find_wiki_introduction(self, full_wiki_text):
        """
        This method try to find the introduction in wiki text.
        When this method finds "==" in wiki text, it can stop
        """
        for index, letter in enumerate(full_wiki_text):
            if letter == "=":
                if full_wiki_text[index + 1] == "=":
                    return full_wiki_text[:index]
        return full_wiki_text


    def trait_http_request(self, response, param_dict):
        """
        This method has the responsibility to find every interesting information
        of a request (each information to find depend on the request)
        """
        try:
            json_response = response.json()
            if param_dict["find_geocoords"]:
                self.lon, self.lat = json_response["results"]["items"][0]["position"]
            elif param_dict["get_wiki_id"]:
                self.wiki_id = json_response["query"]["geosearch"][0]["pageid"]
            elif param_dict["find_wiki_infos"]:
                wiki_response = json_response["query"]["pages"][str(self.wiki_id)]
                self.wiki_infos = {}
                self.wiki_infos["title"] = wiki_response["title"]
                self.wiki_infos["intro"] = self.find_wiki_introduction(wiki_response["extract"])
            self.find_infos_success = True
        except:
            self.find_infos_success = False

    def find_all_informations(self):
        """
        This method try to collect every information from API
        """
        modif_list = [(("find_geocoords", False), ("get_wiki_id", True)),
                      (("get_wiki_id", False), ("find_wiki_infos", True))]
        index = 0
        param_dict = {"find_geocoords": True,
                      "get_wiki_id" : False,
                      "find_wiki_infos" : False}
        while index < 3:
            response = self.send_http_request(param_dict)
            if not self.request_success:
                break
            self.trait_http_request(response, param_dict)
            if not self.find_infos_success:
                break
            if index < 2:
                param_dict[modif_list[index][0][0]] = modif_list[index][0][1]
                param_dict[modif_list[index][1][0]] = modif_list[index][1][1]
            index += 1

    def give_informations(self, place):
        """
        This method return informations from a place in a dictionary.
        The status key gives the information if the parser understood the question
        and if APIs gave informations.
        """
        self.set_place_to_find(place)
        self.find_all_informations()
        status = self.find_infos_success and self.request_success
        informations = {"status" : status,
                        "wiki" : self.wiki_infos,
                        "longitude" : self.lon,
                        "latitude" : self.lat}
        return informations
