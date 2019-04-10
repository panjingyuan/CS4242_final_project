# Manually parse the json files to be uploadable
import json
import os, sys
from mysite.models import Article, Category, Subcat
#from django.core.serializers import serialize
#from django.core.serializers.json import DjangoJSONEncoder

DIR_NAME = "fixtures/"
WH_FILENAME = "wikihow.json"
IN_FILENAME = "instructables.json"
OUT_FILENAME = "unified.json"
APP_NAME = "mysite"
ARTICLE_NAME = "article"
CURR_PK = 0
os.chdir(DIR_NAME)


SAME_FIELDS =  ["category", "view_count", "url",
                "image", "title", "project_id"]

# TODO:
# Add function that parses introduction/raw_text
# and extracts sub_categories from them
# https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34
# Returns sub_categories as a list
def parse_subcat(text):
    return None

# Function to shorten a string to
# the character limit and keep the last word
# https://djangosnippets.org/snippets/1259/
def shorten(str, CHAR_LIM = 500):
    if len(str) < CHAR_LIM:
        return str
    else:
        str = str[:CHAR_LIM]
        trunc_str = str.split(' ')[:-1]
        print(' '.join(trunc_str[:-1]))
        return ' '.join(trunc_str[:-1])+"..."

# Receives a JSON entry
# based on the field it encounters,
# modifies and outputs the data in a unified format.
# site_type: WH, IN
def unify(site_type, entry, CURR_PK):
    result_obj = {}
    fields_obj = {}

    # Unify if they have the same fields
    for fieldname in SAME_FIELDS:
        if fieldname == "view_count":
            fields_obj[fieldname] = int(entry[fieldname].replace(",","" ))
        else:
            fields_obj[fieldname] = entry[fieldname]

    fields_obj["site_type"] = site_type

    #If this is a WikiHow article
    if site_type == "WH":
        fields_obj["summary"] = entry["introduction"]
        #find sub_categories if they exist
        sub_categories = parse_subcat(entry["introduction"])
        if entry["sub_category"]:
            sub_categories.append(entry["sub_category"])

        fields_obj["sub_category"] = sub_categories
        fields_obj["site"] = "WH"
    #If this is an Instructables article
    else:
        fields_obj["summary"] = shorten(''.join(entry["raw_text"]))

        sub_categories = parse_subcat(entry["raw_text"])
        fields_obj["sub_category"] = sub_categories
        fields_obj["site"] = "IN"

    CURR_PK += 1
    result_obj["pk"] = CURR_PK
    result_obj["model"] = APP_NAME + "." + ARTICLE_NAME
    result_obj["fields"] = fields_obj

    return result_obj

records = []

#========================
# Parse wikihow
#========================
'''
WIKIHOW
same: category, view_count, url, image, title, project_id
(These fields will remain the same)

modify: - introduction, (SUMMARY)
        - rating, vote_count (might have to divide this by view_count)
        - publish_date (DATE, change to DDMMYYYY)
        - sub_category (only some have sub_category)

exclusive: -co_authors (there's no specific author)

{u'category': u'Computers and Electronics',
u'view_count': u'959,808', u'rating': None, u'sub_category': None,
u'title': u'How to Guess a Password',
u'introduction': u"Though there's no guaranteed way to guess a password, there are several methods that can lead you in the right direction. If you want to know how to guess a password, just follow these steps and you'll be on your way.",
u'image': u'https://www.wikihow.com/images/c/ca/Guess-a-Password-Step-8.jpg',
u'co_authors': u'77', u'vote_count': None,
u'publish_date': u'March 29, 2019',
u'url': u'https://www.wikihow.com/Guess-a-Password', u'project_id': u'555407'}
'''
with open(WH_FILENAME) as WH_file:
    data_WH = json.load(WH_file)
    values = json.dumps(data_WH, indent=4)
    print(data_WH[0].keys())
    print(data_WH[0])
    WH_unified = unify("WH",data_WH[0], CURR_PK)
    print(WH_unified)
    records.append(WH_unified)

#========================
# Parse Instructables
#========================
'''
==Fields==
same: category, view_count, url, image, title, project_id

modify:     -publish_date (DATE, contains time and date)
            -raw_text (SUMMARY, choose text )
            -channel (SUBCATERGORY, has a meaning somewhat between category and sub_category)

exclusive: comment_count, favourite_count, author, author_id

{u'category': u'technology',
u'view_count': u'251',
u'author': u'DIY KING 00',
u'url': u'https://www.instructables.com/id/DIY-PWM-SPEED-CONTROLLER/',
u'image': u'https://cdn.instructables.com/ORIG/FCM/XP9O/JTYNGO13/FCMXP9OJTYNGO13.jpg?width=2100',
u'title': u'DIY 2000 Watts PWM Speed Controller',
u'comment_count': u'0',
u'publish_date': u'2019-04-03 09:01:31.0',
u'favourite_count': u'5',
u'author_id': u'MZFJ2UDG3TDVHKI', u'project_id': u'E74OQR1JTENEKA4',
u'raw_text': [u'I have been working on converting ...'],
u'channel': u'Electronics'}
'''
with open(IN_FILENAME) as IN_file:
    data_IN = json.load(IN_file)
    #values = json.dumps(data, indent=4)
    print(data_IN[0].keys())
    print(data_IN[0])
    IN_unified = unify("IN",data_IN[0], CURR_PK)
    print(IN_unified)
    records.append(IN_unified)

with open(OUT_FILENAME, 'w') as outfile:
    json.dump(records, outfile)
