import json
import re
import nltk
from nltk.corpus import stopwords
import simplejson as json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer




def rm_url(str):
    return re.sub(r'http[s]?:[/+]?[a-zA-Z0-9_\.\/]*', '', str)

def rm_repeat_chars(str):
    return re.sub(r'(.)(\1){2,}', r'\1\1', str)

def rm_time(str):
    return re.sub(r'[0-9][0-9]:[0-9][0-9]', '', str)

def rm_punctuation(current_tweet):
    return re.sub(r'[^\w\s]', '', current_tweet)


def rm_numbers(str):
    return re.sub(r"[\d+]+", '', str)

def check_noun(word):
    try:
        pos = wn.synsets(word)[0].pos()
        return pos == "n"
    except:
        return False

def rm_ing(word):
    if word[-3:]=='ing':
        word = word[:-3]
    return word


def pre_process(str, porter, stopwords):
    # do not change the preprocessing order only if you know what you're doing
    str = str.lower()
    str = rm_url(str)
    str = rm_repeat_chars(str)
    str = rm_time(str)
    str = rm_punctuation(str)
    str = rm_numbers(str)


    str = nltk.tokenize.word_tokenize(str)
    str = [lemmatizer.lemmatize(t) for t in str]
    str = [t for t in str if t not in stopwords]
    str = [rm_ing(t) for t in str]
    str = [t for t in str if check_noun(t)]

    output = ' '.join(str)

    return output

def word_count(words):
    counts = dict()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results

def get_key_words(article, title):
    tf_idf_vector = tfidf_transformer.transform(cv.transform([article]))
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(feature_names, sorted_items, 5)
    if len(keywords)==0:
        try:
            title = rm_numbers(title)
            str = title.split()
            str = [lemmatizer.lemmatize(t) for t in str]
            str = [t for t in str if t not in stops]
            str = [rm_ing(t) for t in str]
            str = [t for t in str if check_noun(t)]
            str = [t for t in str if len(t)>2]
            for s in str:
                keywords.update({s.lower():0})
            print(keywords)
        except:
            pass
    return keywords


if __name__ == "__main__":

    data_file = "/Users/jingyuanpan/CS4242_final_project/data/wikihow.json"
    porter = nltk.PorterStemmer()
    stops = set(stopwords.words('english'))

    documents=[]
    text = []
    subjects = []
    lemmatizer = WordNetLemmatizer()

    with open(data_file, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if len(line)>2:
                try:
                    article = json.loads(line[:-2])
                except:
                    article = json.loads(line)

                #flatten_text = ''.join(article['introduction'])
                flatten_text = article['introduction']
                try:
                    flatten_text = pre_process(flatten_text, porter, stops)
                    text.append(flatten_text)
                    subjects.append(article['title'])
                    documents.append(article)
                except:
                    pass

    cv=CountVectorizer(max_df=0.85)
    word_count_vector=cv.fit_transform(text)
    feature_names=cv.get_feature_names()
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True).fit(word_count_vector)

    ### add key_words to data and output it
    with open("/Users/jingyuanpan/CS4242_final_project/data/wikihow_with_keywords.txt", 'a', encoding="utf-8") as fout:
        for index, document in enumerate(documents):
            document.update({"keywords": get_key_words(text[index], subjects[index])})
            fout.write(str(document) + os.linesep)


