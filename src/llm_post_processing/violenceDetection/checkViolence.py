from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re
import spacy
import pickle
import os

class ViolenceDetector():

    def clean(self, s):
        # stop_words = stopwords.words("english")
        lemmatizer = WordNetLemmatizer()
        porter = PorterStemmer()
        s = re.sub(r'[^\w\s]','',s)
        # s = " ".join([lemmatizer.lemmatize(w) for w in s.split() if not w in stop_words])
        s = " ".join([lemmatizer.lemmatize(w) for w in s.split()])
        s = " ".join([porter.stem(w) for w in s.split()])
        return s


    def sentence_extraction(self, token, l, main):
        if token.text in main:
            main.remove(token.text)
        for token_ in token.lefts:
            if token_.dep_[0]!='c':
                self.sentence_extraction(token_, l, main)
        l.append(token.text)
        for token_ in token.rights:
            if token_.dep_[0]!='c':
                self.sentence_extraction(token_, l, main)
        return l, main


    def paragraph_to_sentence(self, p):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(p)

        main_words = []
        for token in doc:
            if token.dep_=="ROOT" or token.pos_=='VERB':
                main_words.append(token.text)
                
        if len(main_words)==0:
            return [doc.text]

        lst = []
        for token in doc:
            if token.text in main_words:
                l, main_words = self.sentence_extraction(token, [], main_words)
                lst.append(self.clean(' '.join(l)))

        return lst


    def checkViolence(self, text):

        l = self.paragraph_to_sentence(text)

        vectorizer_file = os.path.abspath('violenceDetection/vectorizer.pkl')
        vectorizer = pickle.load(open(vectorizer_file, 'rb'))

        model_file = os.path.abspath('violenceDetection/model.pkl')
        model = pickle.load(open(model_file, 'rb'))

        for s in l:
            x = vectorizer.transform([s])
            # print(s, clf.predict_proba(x)[0][1])
            if model.predict_proba(x)[0][1]>0.1:
                return 1
        return 0
    


text = "i am a good boy but i killed someone"

result = ViolenceDetector().checkViolence(text)
print(result)