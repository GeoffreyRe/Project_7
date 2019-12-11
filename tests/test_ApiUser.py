"""
This module contains tests of class ApiUser
"""
import pytest
import app.utils.ApiUser as ApiUser
def test_class_apiuser_exists():
    assert hasattr(ApiUser, "ApiUser")

def test_set_place_to_find_gives_value_to_attribute_place_to_find():
    api_user = ApiUser.ApiUser()
    api_user.set_place_to_find("chapelle Sixtine")
    assert api_user.place_to_find == "chapelle Sixtine"

def test_clear_attribute_method_clears_every_attributes():
    api_user = ApiUser.ApiUser()
    api_user.place_to_find = "test"
    api_user.wiki_id, api_user.wiki_infos = "test", "test"
    api_user.lon, api_user.lat = "test", "test"
    api_user.clear_attributes()
    attributes_list = [api_user.place_to_find, api_user.wiki_id, api_user.wiki_infos,
                       api_user.lon, api_user.lat]
    for attr in attributes_list:
        assert attr is None

def test_construct_http_request_for_geocoords():
    api_user = ApiUser.ApiUser()
    api_user.set_place_to_find("example_test")
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(find_geocoords=True)
    assert http_request == (api_user.HTTP_BASE_REQUEST_API_HERE_GEOCOORDS
                            + "app_id=user1&app_code=abc1234&q=example_test&at=0,0")

def test_construct_http_request_for_wiki_to_find_id():
    api_user = ApiUser.ApiUser()
    api_user.lon, api_user.lat = 2, 4
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(get_wiki_id=True)
    assert http_request == (api_user.HTTP_BASE_REQUEST_API_WIKIPEDIA
                            + "action=query&list=geosearch&gscoord=2|4&"
                              "gsradius=10000&gslimit=10&format=json")

def test_construct_http_request_for_wiki_to_find_infos():
    api_user = ApiUser.ApiUser()
    api_user.wiki_id = 45293
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(find_wiki_infos=True)
    assert http_request == (api_user.HTTP_BASE_REQUEST_API_WIKIPEDIA
                            + "action=query&pageids=45293&prop=extracts&"
                              "explaintext=true&exsectionformat=wiki&format=json")

def test_send_http_request_return_response_with_mock_request_get(monkeypatch):
    class MockResponse():
        pass

    def mock_construct_http_request(object, find_geocoords=False,
                                    find_wiki_infos=False, get_wiki_id=False):
        return "https://api/test.com"

    def mock_requests_get(url):
        return MockResponse()

    monkeypatch.setattr("app.utils.ApiUser.ApiUser.construct_http_request",
                        mock_construct_http_request)
    monkeypatch.setattr("requests.get", mock_requests_get)
    api_user = ApiUser.ApiUser()
    response_object = api_user.send_http_request({"find_geocoords" : False,
                                                  "find_wiki_infos" : False,
                                                  "get_wiki_id" : False})
    assert type(response_object) == MockResponse

def test_trait_http_request_for_geocoords():
    api_user = ApiUser.ApiUser()
    lon, lat = 2, 3

    class MockResponse():
        def json(self):
            return {"results" : {"items" : [{"position" : [lon, lat]}]}}

    api_user.trait_http_request(MockResponse(), {"find_geocoords" : True})

    assert (api_user.lon == lon and api_user.lat == lat)

def test_trait_http_request_for_wiki_id():
    api_user = ApiUser.ApiUser()
    id_wiki = 242

    class MockResponse():
        def json(self):
            return {"query" : {"geosearch" : [{"pageid" : id_wiki}]}}

    api_user.trait_http_request(MockResponse(), {"get_wiki_id" : True, "find_geocoords": False})

    assert api_user.wiki_id == id_wiki

def test_trait_http_request_for_wiki_infos(monkeypatch):
    api_user = ApiUser.ApiUser()
    api_user.wiki_id = 5
    title = "test"
    extract = "ceci est un test"
    extract_intro = "ceci"
    def mock_find_wiki_introduction(self, text):
        return extract_intro

    monkeypatch.setattr("app.utils.ApiUser.ApiUser.find_wiki_introduction",
                        mock_find_wiki_introduction)

    class MockResponse():
        def json(self):
            return {"query" : {"pages" : {str(api_user.wiki_id) : {"title": title,
                                                                   "extract" : extract}}}}

    api_user.trait_http_request(MockResponse(),
                                {"get_wiki_id" : False,
                                 "find_geocoords": False, "find_wiki_infos" : True})

    assert api_user.wiki_infos == {"title" : title, "intro" : extract_intro}

def test_give_informations_method(monkeypatch):
    api_user = ApiUser.ApiUser()
    wiki_informations = "informations"
    longitude = 25
    latitude = 15

    def mock_find_all_informations(self):
        api_user.wiki_infos = wiki_informations
        api_user.lon = longitude
        api_user.lat = latitude
        api_user.find_infos_success = True
        api_user.request_success = True
    monkeypatch.setattr("app.utils.ApiUser.ApiUser.find_all_informations",
                        mock_find_all_informations)
    infos = {"status" : True, "wiki" : wiki_informations, "longitude" : longitude,
             "latitude" : latitude}
    assert api_user.give_informations("Belgium") == infos
