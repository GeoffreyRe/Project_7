class Parser():
    def __init__(self):
        self.question_to_analyse = None # this value will get a value when "get_question" method will be called

    def get_question(self):
        """
        ask to user a question
        """
        question = input("Posez votre question à grandPy: ")
        self.question_to_analyse = question
    