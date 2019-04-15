import nltk
from nltk.corpus import stopwords
import simplejson as json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
from sklearn.model_selection import KFold
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV

def get_keywords(dic):
    output=[]
    for word in dic:
        output.append(word)
    return output

def append_words_from_sentences(sentence, output):
    for word in sentence.split():
        word=word.lower()
        if word not in stops:
            output.append(word)
    return output

def map_back_category(value, dic):
    for category, number in dic.items():
        if number == value:
            return category


if __name__ == "__main__":

    data_file = "/Users/jingyuanpan/CS4242_final_project/data/wikihow_with_keywords2.txt"
    porter = nltk.PorterStemmer()
    stops = set(stopwords.words('english'))
    categories = []
    sub_categories = []
    project_ids=[]
    text=[]
    view_counts=[]

    with open(data_file, encoding="utf-8") as f:
        articles=json.load(f)

    for article in articles:
        try:
            project_ids.append(article['project_id'])
            sub_categories.append(article['sub_category'])
            text_feature=[]
            text_feature = append_words_from_sentences(article['category'], text_feature)
            text_feature = append_words_from_sentences(article['title'], text_feature)
            for keyword in get_keywords(article['keywords']):
                text_feature.append(keyword)
            text.append(' '.join(text_feature))
        except:
            pass

    data = pd.DataFrame(list(zip(project_ids,sub_categories, text)))
    data= data.rename(columns={0: 'id', 1:'sub_category',2:'text'})
    train_df = data[data['sub_category'].notnull()]
    test_df = data[data['sub_category'].isnull()]['text']
    print(test_df.shape)

    all_subcat = set(train_df['sub_category'])
    subcat_maps = {}
    for index, cat in enumerate(all_subcat):
        subcat_maps.update({cat:index})

    train_df['sub_category'] = train_df['sub_category'].apply(lambda x: subcat_maps[x])
    y = train_df['sub_category']
    y_train = np.array(y)

    x = data['text']
    feats = TfidfVectorizer().fit_transform(x).toarray()
    x_feats = pd.DataFrame(feats)
    merged_x = pd.concat([data, x_feats], axis=1)

    x_train = np.array(merged_x[merged_x['sub_category'].notnull()].drop(['id', 'sub_category', 'text'], axis=1))
    x_test = np.array(merged_x[merged_x['sub_category'].isnull()].drop(['id', 'sub_category', 'text'], axis=1))

    # param_grid={
    #     'alpha':[0.0006, 0.0007, 0.0008],
    #     'epsilon': [0.002, 0.003, 0.004],
    #     'l1_ratio': [0.7, 0.8, 0.9]
    # }
    #
    # grid_search = GridSearchCV(estimator=linear_model.SGDClassifier(loss='hinge', alpha=0.0007, max_iter=1000, epsilon=0.002, tol=0.1, l1_ratio=0.8, penalty='l2'),param_grid=param_grid, scoring=None, n_jobs=-1, iid=False, cv=10)
    # grid_search.fit(merged_x[merged_x['sub_category'].notnull()].drop(['id', 'sub_category', 'text'], axis=1), y)
    # print(grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_)




    kf = KFold(n_splits=10)
    avg_p = 0
    avg_r = 0
    avg_f1 = 0

    for train, test in kf.split(x_train):

        # model_NB = MultinomialNB().fit(x_train[train], y_train[train])
        # predicts = model_NB.predict(x_train[test])

        model_SVM = linear_model.SGDClassifier(loss='hinge', alpha=0.0007, max_iter=1000, epsilon=0.002, tol=0.1, l1_ratio=0.8, penalty='l2').fit(x_train[train], y_train[train])
        predicts = model_SVM.predict(x_train[test])


        avg_p += precision_score(y_train[test], predicts, average='macro')
        avg_r += recall_score(y_train[test], predicts, average='macro')
        avg_f1 += f1_score(y_train[test], predicts, average='macro')

    average_precision = avg_p / 10.0
    average_recall = avg_r / 10.0
    average_f1_score = avg_f1 / 10.0
    print('Average Precision is %f.' % average_precision)
    print('Average Recall is %f.' % average_recall)
    print('Average F1 is %f' % average_f1_score)


    result = pd.concat([data[data['sub_category'].isnull()].reset_index(drop=True), pd.DataFrame(predicts)], axis=1, ignore_index=True)
    result.drop(1, axis=1, inplace=True)
    result = result.rename({0: 'project_id', 2: 'category', 3: 'predicted_number'}, axis=1)
    result['predicted_category'] = result['predicted_number'].apply(lambda x: map_back_category(x, subcat_maps))

    prediction_map = {}
    for index, row in result.iterrows():
        prediction_map.update({row.project_id:row.predicted_category})

    output_articles=[]
    for index, article in enumerate(articles):
        if article['sub_category'] is None:
            try:
                article.update({"sub_category": prediction_map[str(article['project_id'])]})
            except:
                pass
        output_articles.append(article)

    ### add key_words to data and output it
    with open("/Users/jingyuanpan/CS4242_final_project/data/wikihow_predicted_subcategories2.txt", 'a', encoding="utf-8") as fout:
        json.dump(output_articles, fout)





