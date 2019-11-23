import re
import json
class Parser():
    def __init__(self):
        self.question_to_analyse = None # this value will get a value when "get_question" method will be called
        self.parsed_question = None
        self.ACCENTS_DICT = {
                             ("à" ,"â","ä") : "a",
                             ("ù", "ü", "û") : "u",
                             ("é", "è", "ë","ê"): "e",
                             ("ô", "ö") : "o",
                             ("î", "ï") : "i",
                             ("ç") : "c",
                             (",", ":", ";", "\"", "_") : "",
                             ("'", "-") : " "
                             }
        self.part_of_regex = "([a-z0-9]*[ ])([ a-z0-9-]*)([.?!])"
        self.keywords_list = ["ou se trouv", "ou se situe", "se localis", "l adresse", "le lieu",
                              "l endroit", "peux tu trouve", "le monument", "j aimerais trouve"]
        self.stopwords_list = None
    
    def import_stopwords(self):
        with open("../static/stopwords.json") as f:
            self.stopwords_list = json.load(f)


    def get_question(self):
        """
        ask to user a question
        """
        question = input("Posez votre question à grandPy: ")
        self.question_to_analyse = question + "."

    def lower_user_question(self):
        return self.question_to_analyse.lower()
        
    def eliminate_accents_of_question(self, question):
        question = list(question)
        for index, letter in enumerate(question):
            for key in self.ACCENTS_DICT.keys():
                if letter in key:
                    question[index] = self.ACCENTS_DICT[key]
        question_without_accents = "".join(question)
        return question_without_accents
    
    def find_place_in_question(self, question):
        for keyword in self.keywords_list:
            regex = keyword + self.part_of_regex
            re_answer = re.search(regex, question)
            if re_answer:
                return (True, re_answer.group(2))
        return (False, "")

    def remove_stopwords(self, sentence):
        words_list = sentence.split(" ")
        for index, word in enumerate(words_list):
            for stopword in self.stopwords_list:
                if word == stopword:
                    words_list[index] = ""
        words_list = [word for word in words_list if word != ""]
        return " ".join(words_list)

    
    def parse(self):
        question_lowed = self.lower_user_question()
        question_no_accent = self.eliminate_accents_of_question(question_lowed)
        interesting_part_of_question = self.find_place_in_question(question_no_accent)
        if interesting_part_of_question[0]== True:
            interesting_part_without_stopwords = self.remove_stopwords(interesting_part_of_question[1])
        elif interesting_part_of_question[0] == False:
            self.parsed_question = "Désolé mais je ne comprends pas la question"
            return False
        self.parsed_question = interesting_part_without_stopwords
    
if __name__ == "__main__":
    parser = Parser()
    parser.import_stopwords()
    parser.get_question()
    parser.parse()
    print(parser.parsed_question)






    