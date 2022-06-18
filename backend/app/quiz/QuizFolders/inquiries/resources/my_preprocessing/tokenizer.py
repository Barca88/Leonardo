# sentence tokenizer and word tokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import app.quiz.QuizFolders.inquiries.resources.my_preprocessing.nltk_modules

stop_words = set(stopwords.words("english"))

def word_tokenizer(comment):
    words = word_tokenize(comment)
    return words

def remove_stop_words(tokenized_comment):
    filtered_comment = []

    for word in tokenized_comment:
        if word not in stop_words and len(word)>1:
            filtered_comment.append(word)
            
    return filtered_comment

def filtered_comment(comment):
    tokenized_comment = word_tokenizer(comment)
    filtered_comment = remove_stop_words(tokenized_comment)
    return filtered_comment