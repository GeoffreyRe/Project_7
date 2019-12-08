import requests
class ApiUser():
    def __init__(self):
        self.HTTP_BASE_REQUEST_API_HERE_GEOCOORDS = "https://places.cit.api.here.com/places/v1/discover/search?"
        self.HTTP_BASE_REQUEST_API_HERE_IMAGE = "https://image.maps.api.here.com/mia/1.6/mapview?"
        self.HTTP_BASE_REQUEST_API_WIKIPEDIA = "https://fr.wikipedia.org/w/api.php?"
        self.place_to_find = None
        self.app_id, self.app_code = "", ""
        self.wiki_id, self.wiki_infos = None, None
        self.lon, self.lat = None, None
        self.binary_image = None
        
    def set_place_to_find(self, place):
        self.place_to_find = place
    
    def clear_attributes(self):
        self.place_to_find = None
        self.wiki_id, self.wiki_infos = None, None
        self.lon, self.lat = None, None
        self.binary_image = None
    
    def construct_http_request(self, find_geocoords=False, find_map=False, find_wiki_infos=False, get_wiki_id=False):
        if find_geocoords == True:
            parameters_http_request = "app_id={0}&app_code={1}&q={2}&at=0,0".format(self.app_id, self.app_code, self.place_to_find)
            return self.HTTP_BASE_REQUEST_API_HERE_GEOCOORDS + parameters_http_request
        elif find_map == True:
            parameters_http_request = "app_id={0}&app_code={1}&c={2},{3}&z=14".format(self.app_id, self.app_code, self.lon, self.lat)
            return self.HTTP_BASE_REQUEST_API_HERE_IMAGE + parameters_http_request
        elif find_wiki_infos == True:
            parameters_http_request = "action=query&pageids={0}&prop=extracts&explaintext=true&exsectionformat=wiki&format=json".format(self.wiki_id)
            return self.HTTP_BASE_REQUEST_API_WIKIPEDIA + parameters_http_request
        elif get_wiki_id == True: 
            parameters_http_request = "action=query&list=geosearch&gscoord={0}|{1}&gsradius=10000&gslimit=10&format=json".format(self.lon, self.lat)
            return self.HTTP_BASE_REQUEST_API_WIKIPEDIA + parameters_http_request

    
    def send_http_request(self, param_dict):
        request = self.construct_http_request(**param_dict)
        try:
            response = requests.get(request)
        except:
            response = {}
        
        
        return response
    
    def trait_http_request(self, response, param_dict):
        if param_dict["find_map"] == False:
            json_response = response.json()
        if param_dict["find_geocoords"] == True:
            self.lon, self.lat = json_response["results"]["items"][0]["position"]
        elif param_dict["find_map"] == True:
            self.binary_image = response.content

        elif param_dict["get_wiki_id"] == True:
            self.wiki_id = json_response["query"]["geosearch"][0]["pageid"]

        elif param_dict["find_wiki_infos"] == True:
            self.wiki_infos = json_response["query"]["pages"][str(self.wiki_id)]
    
    def find_all_informations(self):
        modif_list = [(("find_geocoords", False), ("find_map", True)), (("find_map", False), ("get_wiki_id", True)),
                      (("get_wiki_id", False), ("find_wiki_infos", True))
                     ]
        index = -1
        param_dict = {"find_geocoords": True,
                          "find_map" : False,
                          "get_wiki_id" : False,
                          "find_wiki_infos" : False}
        while index < 4:
            response = self.send_http_request(param_dict)
            self.trait_http_request(response, param_dict)
            if index >= 0 and index < 3:
                param_dict[modif_list[index][0][0]] = modif_list[index][0][1]
                param_dict[modif_list[index][1][0]] = modif_list[index][1][1]
            index += 1
    
    def give_informations(self):
        return [self.wiki_infos, self.binary_image]
            

if __name__ == "__main__":
    api = ApiUser()
    api.set_place_to_find("la chapelle sixtinne")
    api.find_all_informations()
    print(api.give_informations())

