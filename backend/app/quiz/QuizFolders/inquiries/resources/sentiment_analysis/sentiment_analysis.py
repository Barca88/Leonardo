# sentence sentiment analysis
from .utils import convert_scale
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def get_polarity_from_comment(comment):
    fc = ' '.join(comment)
    vs = analyser.polarity_scores(fc)
    scaled_compound = convert_scale(vs['compound'])
    return scaled_compound

def get_important_words(comment):
    important_words = []

    for f_word in comment:
        word_score = analyser.polarity_scores(f_word)
        if word_score['compound'] >= 0.05 or word_score['compound'] <= -0.05:
            important_words.append(f_word)

    return important_words
