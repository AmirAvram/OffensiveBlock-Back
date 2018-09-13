import pickle
import re
import string
import numpy as np
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
FILES_LOCATION = "idk/"

def tokenize(s): return re_tok.sub(r' \1 ', s).split()


label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']


def save_obj(obj, name):
    with open(FILES_LOCATION + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(FILES_LOCATION + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def load_model(path=FILES_LOCATION):
    r = [0] * 6
    m = [0] * 6
    for i in range(6):
        r[i] = np.mat(np.load(path + "r" + str(i) + ".npy"))
        m[i] = joblib.load(path + "m" + str(i) + ".sav")

    # TF-IDF vectorizer
    vec = TfidfVectorizer(ngram_range=(1, 2), tokenizer=tokenize,
                          min_df=3, max_df=0.9, strip_accents='unicode', use_idf=1,
                          smooth_idf=1, sublinear_tf=1)
    vec._tfidf._idf_diag = load_obj("idf_diag")  # sp.spdiags(idfs, diags = 0, m = len(idfs), n = len(idfs))
    vec.vocabulary_ = load_obj("vocabulary")
    return vec, m, r


vec, m, r = load_model()


def predict(sentence, col=None):
    # print(sentence)
    if col != None:
        if col not in label_cols: raise ValueError("column requested is not in label columns")
        i = label_cols.index(col)
        pred = vec.transform([sentence])
        return (m[i].predict_proba(pred.multiply(r[i]))[0, 1])
    else:
        result = [0] * 6
        pred = vec.transform([sentence])
        for i, j in enumerate(label_cols):
            result[i] = (j, m[i].predict_proba(pred.multiply(r[i]))[0, 1])
    return result
