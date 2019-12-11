"""
This module contains tests of class Parser
"""
import app.utils.Parser as Parser
import pytest

def test_class_Parser_exists():
    assert hasattr(Parser, "Parser")

@pytest.mark.parametrize("user_question", [
    "Bonjour GrandPy, j'espère que tu vas bien, sais-tu où se trouve la tour eiffel?",
    "Salut, connais-tu la grand Place à Bruxelles?",
    "Hey, j'aimerais bien avoir des infos sur le théatre de Gant."
])

def test_get_question_method_add_value_to_question_to_analyse_attribute(user_question):

    parser = Parser.Parser()
    parser.get_question(user_question)

    assert parser.question_to_analyse == user_question + "."

@pytest.mark.parametrize("user_question", [
    ("Bonjour GrandPy, j'espère que tu vas bien !"
     " Connais-tu le lieu suivant : Place de la Bastille ? Bien à toi."),
    ("BoNjoUr granDpy, j'Espère que tU vAs bien !"
     " connais-tu LE lieu suivant : place de la BasTille ? bien à toi."),
    ("BONJOUR GRANDPY, J'ESPèRE QUE TU VAS BIEN !"
     " CONNAIS-TU LE LIEU SUIVANT : PLACE DE LA BASTILLE ? BIEN à TOI.")
])
def test_lower_question_is_ok(user_question):
    """
    à demander: savoir si il faut mocker la fonction lower ou pas
    """
    parser = Parser.Parser()
    parser.question_to_analyse = user_question
    question_lowed = parser.lower_user_question()
    assert  question_lowed == ("bonjour grandpy, j'espère que tu vas bien !"
                               " connais-tu le lieu suivant : place de la bastille ? bien à toi.")

def test_method_eliminate_accents_of_questions_does_the_job():
    parser = Parser.Parser()
    question = "été soleil ça où été être cela île àâä ùüû ôö îï,,:;\""
    no_accents = "ete soleil ca ou ete etre cela ile aaa uuu oo ii"
    assert parser.eliminate_accents_of_question(question) == no_accents

def test_stopwords_list_attribute_is_assigned_well_to_attribute(monkeypatch):

    stopwords = ["a", "un", "une", "as", "des", "le", "la", "d", "et", "de", "s",
                 "il", "te", "plait"]

    class MockOpen():
        def __init__(self, directory):
            pass
        def __enter__(self):
            pass
        def __exit__(self, type, value, traceback):
            pass
    def mock_json_load(file):
        return stopwords
    parser = Parser.Parser()
    monkeypatch.setattr("builtins.open", MockOpen)
    monkeypatch.setattr("json.load", mock_json_load)
    parser.import_stopwords()
    assert parser.stopwords_list == stopwords

@pytest.mark.parametrize("question", [
    (("salut grandpy! Comment s est passe ta soiree avec grandma hier soir?"
      " au fait, pendant que j y pense,pourrais tu m indiquer ou se trouve "
      "le musee d art et d histoire de fribourg s il te plait?"),
     "le musee d art et d histoire de fribourg s il te plait"),
    (("bonsoir grandpy, j espere que tu as passe une belle semaine. est"
      " ce que tu pourrais m'indiquer l adresse de la tour eiffel?"
      " merci d avance et salutations a mamie."), "de la tour eiffel")
])

def test_find_place_in_questions_find_good__part_of_sentence(question):
    parser = Parser.Parser()
    good_part_of_question = parser.find_place_in_question(question[0])
    print(good_part_of_question)
    assert good_part_of_question[1] == question[1]


def test_remove_stopwords_removes_well_given_stopwords_of_a_sentence():
    parser = Parser.Parser()
    parser.stopwords_list = ["à", "ah", "bon", "salut", "ça", "va", "et", "de", "en"]
    parsed_sentence = parser.remove_stopwords(("salut GrandPy, comment"
                                               " ça va aujourd'hui ? ah j'ai"
                                               " oublié de te dire que je vais aller en France."))
    exc_sentence = "GrandPy, comment aujourd'hui ? j'ai oublié te dire que je vais aller France."
    assert parsed_sentence == exc_sentence

@pytest.mark.parametrize("question", [
    (("Salut grandpy! Comment s'est passé ta soirée avec Grandma hier soir? Au fait,"
      " pendant que j'y pense, pourrais-tu m'indiquer où se trouve le musée d'art et"
      " d'histoire de Fribourg, s'il te plaît?"), "musee art histoire fribourg"),
    ("""
    Bonsoir Grandpy, j'espère que tu as passé une belle semaine. Est-ce que tu pourrais m'indiquer 
    l'adresse de la tour eiffel? Merci d'avance et salutations à Mamie.""", "tour eiffel")
])

def test__method_parse_assign_expected_value_to_parsed_question_attribute(question, monkeypatch):
    def mock_import_stopwords(self):
        self.stopwords_list = ["a", "un", "une", "as", "des", "le", "la", "d", "et", "de",
                               "s", "il", "te", "plait"]
    monkeypatch.setattr("app.utils.Parser.Parser.import_stopwords", mock_import_stopwords)
    parser = Parser.Parser()
    parser.import_stopwords()
    parser.question_to_analyse = question[0]
    parser.parse()
    assert parser.parsed_question == question[1]
