import difflib

# Greetings and basic conversation
greetings_qa_pairs = {
    "uraho": "uraho neza, Amakuru yawe",
    "amakuru yanjye ni meza": "Ni byiza rwose, nagufasha iki",
    "amakuru": "Ni meza, urakoze kubaza. Nagufasha iki uyumunsi",
    "witwa nde": "Nitwa Robo, umufasha ukoresha ikinyarwanda.",
    "wakora iki": "Nshobora kumva, gusobanura, no gusubiza ikibazo waba ufite nkoresheje ururimi rw'ikinyarwanda.",
    "uba he": "Ndahari hafi yawe.",
    "mwiriwe": "Mwiriwe neza!",
    "bite": "Ni byiza, urakoze. Nagufasha iki uyumunsi",
    "ufite imyaka ingahe": "Ndi robot, sinagira imyaka.",
    "ukunda iki": "Nkunda gufasha abantu no kuvugana nabo.",
    "urikunyumva neza": "Yego, ndakumva neza.",
    "ubuzima bumeze bute": "Ubuzima ni bwiza, urakoze kubaza.",
    "ufasha iki": "Nshobora kumva, gusobanura, no gusubiza ikibazo waba ufite nkoresheje ururimi rw'ikinyarwanda.",
    "washobora kuvuga": "Yego, nshobora kuvuga neza mu Kinyarwanda.",
    "uraryama ryari": "Ndi robot, sindyama.",
    "ufite inshuti": "Ndi inshuti ya buri wese.",
    "wakora iki niba ufite ikibazo": "Nashaka ubufasha vuba.",
    "murakoze": "Nshimishijwe no kugufasha.",
}

# Combine all QA pairs
qa_pairs = {}
qa_pairs.update(greetings_qa_pairs)

class KinyarwandaNLP:
    def __init__(self, qa_database=None):
        """
        Initialize the NLP component
        
        Parameters:
        - qa_database: Dictionary of question-answer pairs
        """
        self.qa_pairs = qa_database if qa_database else qa_pairs
        self.keys = list(self.qa_pairs.keys())
    
    def find_answer(self, question):
        """
        Match question to answer using simple NLP techniques
        
        Parameters:
        - question: The input question in Kinyarwanda
        
        Returns:
        - The best matching answer or default response
        """
        # Clean the input
        question = question.lower().strip()
        
        # Exact match
        for key in self.qa_pairs:
            if key in question:
                return self.qa_pairs[key]
        
        # Fuzzy match for similar phrases
        matches = difflib.get_close_matches(question, self.keys, n=1, cutoff=0.6)
        if matches:
            return self.qa_pairs[matches[0]]
        
        # Default response if no match found
        return "Sinumva neza icyo ushaka. Ushobora kongera kubaza mu buryo butandukanye?"

    def add_qa_pair(self, question, answer):
        """Add a new question-answer pair to the database"""
        self.qa_pairs[question.lower()] = answer
        self.keys = list(self.qa_pairs.keys())

# Example usage
if __name__ == "__main__":
    nlp = KinyarwandaNLP()
    test_questions = [
        "witwa nde",
        "amakuru yawe",
        "ufite imyaka ingahe",
        "ntabwo nkwumva" # Something not in the database
    ]
    
    for question in test_questions:
        print(f"Q: {question}")
        print(f"A: {nlp.find_answer(question)}\n")