# Package to unify files
import json
import os, sys
from progress.bar import IncrementalBar
from datetime import datetime as dt
from mysite.models import Article, Category, Subcat, Keyword

SAME_FIELDS =  ["category", "view_count", "url",
                "image", "title", "project_id"]

EXTRA_FIELDS = [
    "site_type",
    "summary",
    "date",
    "sub_category",
    "keywords"
]

MAX_ENTRIES = 1000

REQUIRED_FIELDS = []
REQUIRED_FIELDS.extend(SAME_FIELDS)
REQUIRED_FIELDS.extend(EXTRA_FIELDS)

# Returns keywords
def get_kw(kw_dict):
    kw_list = []
    for item in list(kw_dict.keys()):
        new_kw, created = Keyword.objects.get_or_create(pk=item)
        kw_list.append(new_kw)
    return kw_list

# Function to shorten a string to
# the character limit and keep the last word
# https://djangosnippets.org/snippets/1259/
def shorten(str, CHAR_LIM = 500):
    if len(str) < CHAR_LIM:
        return str
    else:
        str = str[:CHAR_LIM]
        trunc_str = str.split(' ')[:-1]
        #print(' '.join(trunc_str[:-1]))
        return ' '.join(trunc_str[:-1])+"..."

# changes wikihow's
# MONTH DD, YYYY into datetime
def wh_date(dt_str):
    return dt.strptime(dt_str,"%B %d, %Y")

# changes Instructables'
# YYYY-MM-DD HH:MM:SS.M into datetime
def in_date(dt_str):
    return dt.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")

def add_cat(cat_name):
    if (cat_name == None) or (cat_name == "None"):
#       ans = input("Do you want to give a name to this article? (n to cancel)")
#       if not ans == "n":
#       for item in entry:
#           print(item + ": " + str(entry[item]))
#       cat_name = input("Enter name of new category: ")
        cat_name = "Uncategorised"
    new_cat, created = Category.objects.get_or_create(pk=cat_name)
#   if created:
#        print("Created category %s" % str(new_cat))
    new_cat.save()
    return new_cat

def add_sc(cat_name):
    if (not cat_name == None) and (not cat_name == "None"):
        new_sc, created = Subcat.objects.get_or_create(pk=cat_name)
        if created:
            print("created %s" % cat_name)
            new_sc.save()
        return new_sc
    else:
        return None

# Receives a JSON entry
# based on the field it encounters,
# modifies and outputs the data in a unified format.
# site_type: WH, IN
def unify(site_type, entry):
    fields_obj = {}
    sub_categories = []
    # Unify if they have the same fields
    for fieldname in SAME_FIELDS:
        if fieldname == "view_count":
            fields_obj[fieldname] = int(entry[fieldname].replace(",","" ))
        elif fieldname == "category":
            cat_name = str(entry["category"]).strip()
            cat = add_cat(cat_name)
            fields_obj[fieldname] = cat
        else:
            fields_obj[fieldname] = entry[fieldname]

    fields_obj["site_type"] = site_type

    #If this is a WikiHow article
    if site_type == "WH":
        fields_obj["summary"] = entry["introduction"]
        fields_obj["date"] = wh_date(entry["publish_date"])
        fields_obj["sub_category"] = add_sc(entry["sub_category"])
        fields_obj["keywords"] = []
        fields_obj["keywords"].extend(get_kw(entry["keywords"]))
    #If this is an Instructables article
    else:
        fields_obj["summary"] = shorten(''.join(entry["raw_text"]))
        fields_obj["date"] = in_date(entry["publish_date"])
        fields_obj["keywords"] = []
        fields_obj["keywords"].extend(get_kw(entry["keywords"]))

    return fields_obj

#========================
# Parse wikihow
#========================
'''
WIKIHOW
same: category, view_count, url, image, title, project_id
(These fields will remain the same)

modify: - introduction, (SUMMARY)
        - publish_date (DATE, change to DDMMYYYY)
        - rating, vote_count (might have to divide this by view_count)
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
def load_wh(WH_FILEPATH):
    WH_results = []
    with open(WH_FILEPATH) as WH_file:
        data_WH = json.load(WH_file)
        count = 0
        bar = IncrementalBar('Reading WH_file: ', max=len(data_WH))
        for entry in data_WH:
            count += 1
            WH_unified = unify("WH",entry)
            #print(WH_unified)
            WH_results.append(WH_unified)
            bar.next()
            if count > MAX_ENTRIES:
                break
        bar.finish()
    WH_file.close()

    return WH_results

#========================
# Parse Instructables
#========================
'''
==Fields==
same: category, view_count, url, image, title, project_id

modify:     -publish_date (DATE, contains time and date)
            -raw_text (SUMMARY, choose text )
            -channel (SUBCATEGORY, has a meaning somewhat between category and sub_category)

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
def load_in(IN_FILEPATH):
    IN_results = []
    count = 0

    with open(IN_FILEPATH) as IN_file:
        data_IN = json.load(IN_file)
        bar = IncrementalBar('Reading IN_file: ', max=len(data_IN))
        for entry in data_IN:
            count += 1
            IN_unified = unify("IN",entry)
            IN_results.append(IN_unified)
            bar.next()
            if count > MAX_ENTRIES:
                break
        bar.finish()
    IN_file.close()

    return IN_results
