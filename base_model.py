import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only

def read_corpus(corpus_name, split_character):
    """
    corpus_name: string; name of text file, which should be readed.
    split_characer: string; corpus should be splitted with respect to the symbol.
    
    return: list; list of all sentences.
    """
    
    with open(corpus_name, 'r', errors = 'ignore') as file:
        corpus = file.read().lower().split(split_character)
        
    return corpus


def lem_words(sentence):
    """
    sentence: list; list of words.  
    
    return string;
    """
    
    return ' '.join([lemmer.lemmatize(word) for word in sentence])


def clean_corpus(sentence):
    """
    sentence: string;  
    
    return string;
    """
    
    text = re.sub(r"\’", "'", sentence)
    text = ' '.join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', text).split())
    text = re.sub(r"what's", "what is ", text.lower())
    text = re.sub(r"\ 's", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r"\u200a", " ", text)
    text = re.sub(r"[^a-z ]", " ", text)
    text = re.sub(r" [a-z]{1} ", " ", text)
    text = re.sub(r"[ ]{2,}", '', text)
    return text

def lem_normalize(text):
    return lem_words(clean_corpus(text).split(' '))


def get_response(message):
    response = ''
    corpus.append(message)
    
    TfidfVec = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(corpus)
    
    matrix = cosine_similarity(tfidf[-1], tfidf)
    index = matrix.argsort()[0][-2]
    matrix = matrix.flatten()
    matrix.sort()
    req_tfidf = matrix[-2]
    
    if req_tfidf == 0:
        response = response + ". I don't understand you"
    else:
        response = response + corpus[index]
        
    return response

lemmer = nltk.stem.WordNetLemmatizer()
corpus = read_corpus('ML_1.txt', '.')

