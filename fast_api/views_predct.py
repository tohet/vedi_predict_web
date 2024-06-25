import pandas as pd
import numpy as np
import re

from pymorphy3 import MorphAnalyzer

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords

from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

class ModelHolder:
    def __init__(self, data_path, y_name):
        data = pd.read_csv(data_path)
        y = data[y_name]
        X = data.drop(y_name, axis = 1)

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        self.linreg = Lasso(alpha = 5, tol = 100).fit(X, y)
    
    # sets text priorities based on views - unused
    def classify_by_views(self, views):
        if views > 100000:
            return 0
        elif views <= 100000 and views > 50000:
            return 1
        elif views <= 50000 and views > 30000:
            return 2
        else:
            return 3

    def predict(self, parsed_input):
        pred_views = self.linreg.predict(parsed_input)
        return pred_views



class InputManager:
    def __init__(self, data_path):
        data = pd.read_csv(data_path)
        # create a df with the same structure as original ved_5mon with only one row
        # all the values in row set to 0
        self.df = pd.DataFrame(0, index=range(1), columns=data.columns)
        self.df = self.df.drop('открытия материала', axis = 1)

        self.morph = MorphAnalyzer()
        self.patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.stopwords_ru = stopwords.words("russian")

    def return_as_pd_df(self, title, authors, topics):
        result_df = self.df.copy(deep=True)
        # parse the tite
        if title == None or authors == None or topics == None:
            title = 'ЕЦБ назвал главные риски европейской финансовой системы'
            authors = 'Антон Козлов'
            topics = 'Экономика'
            print("None data got")
        
        title_tokens = self.preprocess(title)
        title_tokens = self.lemmatize(title_tokens)

        for token in title_tokens:
            # try to match each token with a column
            # if match set to 1
            if token in result_df.columns:
                result_df.loc[0, token] = 1
        
        # save authors as list of tokens
        authors_tokens = authors.split(", ")
        for author in authors_tokens:
            if author in result_df.columns:
                result_df.loc[0, author] = 1

        # same for topics
        topics_tokens = topics.split(", ")
        for topic in topics_tokens:
            if topic in result_df.columns:
                result_df.loc[0, topic] = 1
        
        # return the resulting df
        #result_df = result_df.drop('Unnamed: 0', axis = 1)
        return result_df
    
    # functions for tokenizing the title

    def preprocess(self, text):
        stop_words = set(stopwords.words('russian'))
        lemmatizer = WordNetLemmatizer()

        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token not in stop_words]
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(tokens)
    
    def lemmatize(self, doc):
        doc = re.sub(self.patterns, ' ', doc)
        tokens = []
        for token in doc.split():
            if token and token not in self.stopwords_ru:
                token = token.strip()
                token = self.morph.normal_forms(token)[0]

                tokens.append(token)

        return tokens

# a class to store predictions
class PredScore():
    def __init__(self, score):
        self.score = score
        self.label = ''

    # sets labels
    def update(self, new_score):
        self.score = new_score
        if new_score >= 15000:
            self.label = 'Хит'
        elif new_score < 15000 and new_score >= 14500:
            self.label = 'Успех'
        elif new_score < 14500 and new_score >= 14000:
            self.label = 'Проходной'
        elif new_score < 14000 and new_score >= 13500:
            self.label = 'Неинтересный'
        elif new_score < 13500 and new_score >= 13000:
            self.label = 'Нишевой'
        elif new_score < 13000:
            self.label = 'Провал'
