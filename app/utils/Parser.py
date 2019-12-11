"""
This module contains Parser class
"""
import re
import json
class Parser():
    """
    This class has the responsibility to parse the user question
    """
    def __init__(self):
        """
        This method create instance attributes
        """
        self.question_to_analyse = None
        self.parsed_question = None
        self.ACCENTS_DICT = {("à", "â", "ä") : "a",
                             ("ù", "ü", "û") : "u",
                             ("é", "è", "ë", "ê"): "e",
                             ("ô", "ö") : "o",
                             ("î", "ï") : "i",
                             ("ç") : "c",
                             (",", ":", ";", "\"", "_") : "",
                             ("'", "-") : " "}
        self.part_of_regex = "([a-z0-9]*[ ])([ a-z0-9-]*)([.?!])"
        self.keywords_list = ["connais tu", "ou se trouv", "ou se situe", "se localis",
                              "l adresse", "le lieu", "l endroit", "peux tu trouve",
                              "le monument", "j aimerais trouve"]
        self.stopwords_list = None
        self.success = False

    def import_stopwords(self):
        """
        This method import json stopwords
        """
        with open("app/static/stopwords.json") as file:
            self.stopwords_list = json.load(file)


    def get_question(self, question):
        """
        This method assign value to question_to_analyse
        """
        self.question_to_analyse = question + "."

    def initialize_parser(self, question):
        """
        This method import stopword and initialize attribute
        """
        self.import_stopwords()
        self.get_question(question)

    def lower_user_question(self):
        """
        This method lower user question
        """
        return self.question_to_analyse.lower()

    def eliminate_accents_of_question(self, question):
        """
        This method check if there are accents into the question
        and change accents letters into non-accent letters
        """
        question = list(question)
        for index, letter in enumerate(question):
            for key in self.ACCENTS_DICT.keys():
                if letter in key:
                    question[index] = self.ACCENTS_DICT[key]
        question_without_accents = "".join(question)
        return question_without_accents

    def find_place_in_question(self, question):
        """
        Try to find place to question thanks to a regex
        """
        for keyword in self.keywords_list:
            regex = keyword + self.part_of_regex
            re_answer = re.search(regex, question)
            if re_answer:
                return (True, re_answer.group(2))
        return (False, "")

    def remove_stopwords(self, sentence):
        """
        The method removes stopwords from the question
        """
        words_list = sentence.split(" ")
        for index, word in enumerate(words_list):
            for stopword in self.stopwords_list:
                if word == stopword:
                    words_list[index] = ""
        words_list = [word for word in words_list if word != ""]
        return " ".join(words_list)


    def parse(self):
        """
        This method trait the question completely
        """
        question_lowed = self.lower_user_question()
        question_no_accent = self.eliminate_accents_of_question(question_lowed)
        interesting_part_of_question = self.find_place_in_question(question_no_accent)
        if interesting_part_of_question[0]:
            interesting_part_without_stopwords = self.remove_stopwords(interesting_part_of_question[1])
        elif not interesting_part_of_question[0]:
            return False
        self.parsed_question = interesting_part_without_stopwords
        return True
