import app.Parser

def test_class_Parser_exists():
    assert hasattr(app.Parser, "Parser")

def test_get_question_method_add_value_to_question_to_analyse_attribute(monkeypatch):
    user_question = "Bonjour GrandPy, j'espère que tu vas bien, sais-tu où se trouve la tour eiffel?"
    def mock_input(string=None):
        return user_question
    
    parser = app.Parser.Parser()
    monkeypatch.setattr("builtins.input", mock_input)
    parser.get_question()

    assert parser.question_to_analyse == user_question

