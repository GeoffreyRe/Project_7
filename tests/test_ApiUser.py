import app.utils.ApiUser as ApiUser
import pytest
def test_class_ApiUser_exists():
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
    api_user.binary_image = "test"
    api_user.clear_attributes()
    attributes_list = [api_user.place_to_find, api_user.wiki_id, api_user.wiki_infos,
                       api_user.lon, api_user.lat, api_user.binary_image]
    for attr in attributes_list:
        assert attr == None

def test_construct_http_request_for_geocoords():
    api_user = ApiUser.ApiUser()
    api_user.set_place_to_find("example_test")
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(find_geocoords=True)
    assert http_request == api_user.HTTP_BASE_REQUEST_API_HERE_GEOCOORDS + "app_id=user1&app_code=abc1234&q=example_test&at=0,0"

def test_construct_http_request_for_image():
    api_user = ApiUser.ApiUser()
    api_user.lon, api_user.lat = 2,4
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(find_map=True)
    assert http_request == api_user.HTTP_BASE_REQUEST_API_HERE_IMAGE + "app_id=user1&app_code=abc1234&c=2,4&z=14"

def test_construct_http_request_for_wiki_to_find_id():
    api_user = ApiUser.ApiUser()
    api_user.lon, api_user.lat = 2,4
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(get_wiki_id=True)
    assert http_request == api_user.HTTP_BASE_REQUEST_API_WIKIPEDIA + "action=query&list=geosearch&gscoord=2|4&gsradius=10000&gslimit=10&format=json"

def test_construct_http_request_for_wiki_to_find_infos():
    api_user = ApiUser.ApiUser()
    api_user.wiki_id = 45293
    api_user.app_id, api_user.app_code = "user1", "abc1234"
    http_request = api_user.construct_http_request(find_wiki_infos=True)
    assert http_request == api_user.HTTP_BASE_REQUEST_API_WIKIPEDIA + "action=query&pageids=45293&prop=extracts&explaintext=true&exsectionformat=wiki&format=json"

def test_send_http_request_return_response_with_mock_request_get(monkeypatch):
    class MockResponse():
        pass

    def mock_construct_http_request(object, find_geocoords=False, find_map=False, find_wiki_infos=False, get_wiki_id=False):
        return "https://api/test.com"

    def mock_requests_get(url):
        return MockResponse()
    
    monkeypatch.setattr("app.utils.ApiUser.ApiUser.construct_http_request", mock_construct_http_request)
    monkeypatch.setattr("requests.get", mock_requests_get )
    api_user = ApiUser.ApiUser()
    response_object = api_user.send_http_request({"find_geocoords" : False, "find_map" : True, "find_wiki_infos" : False, "get_wiki_id" : False})
    assert type(response_object) == MockResponse

def test_trait_http_request():
    pass


    
    
