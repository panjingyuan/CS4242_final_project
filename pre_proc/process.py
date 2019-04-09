# Manually parse the json files to be uploadable
import json
import os

DIR_NAME = "fixtures/"
WH_FILENAME = "wikihow.json"
IN_FILENAME = "instructables.json"
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
# modifies and outputs the data.
# site_type: WH, IN
def unify(site_type, entry):
    result_obj = {}

    # Unify if they have the same fields
    for fieldname in SAME_FIELDS:
        result_obj[fieldname] = entry[fieldname]

    #If this is a WikiHow article
    if site_type == "WH":
        result_obj["summary"] = entry["introduction"]
        #find sub_categories if they exist
        sub_categories = parse_subcat(entry["introduction"])
        if entry["sub_category"]:
            sub_categories.append(entry["sub_category"])

        result_obj["sub_category"] = sub_categories
    #If this is an Instructables article
    else:
        result_obj["summary"] = shorten(''.join(entry["raw_text"]))

        sub_categories = parse_subcat(entry["raw_text"])
        result_obj["sub_category"] = sub_categories

    return result_obj

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
with open(WH_FILENAME) as json_file:
    data_WH = json.load(json_file)
    values = json.dumps(data_WH, indent=4)
    print(data_WH[0].keys())
    print(data_WH[0])
    print(unify("WH",data_WH[0]))


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
u'raw_text': [u'I have been working on converting my bicycle to an electric one using a DC motor for automatic door mechanism and for that I have also made a battery pack thats rated at 84v DC. '
, u'Now we need a speed controller that can limit the amounbt of energy delivered to the motor from the battery pack. Most of the speed controller avliable online are not rated for that much high voltage so I decided to built one for myself. So thats whats this project is going to be, to design and built a customized PWM speed controller to controll the speed of large scale DC motors.', u'For this project you need basic soldering tools such as:', u'The schematic, Gerber files and the list of comonents is avliable ', u'.', u'Since we are aiming to con trol the speed of a DC motor for which we can use two techinquies, A buck converter which will stepdown the input voltage buts its a rather complicated one so what we have decided to go with is PWM Control (Pulse Width Modulation). The approach is simple, to control the speed the battery power is switched on and off at a high frequency. To change the speed the duty cycle or the on off time period of the switch is changed.', u'Now mechanical switches are not expected to undergo such high stress so an appropriate choice for such application is an N-Channel Mosfet that are specifically made to handle moderate amount of current at high frequency.', u'To switch the mosfets we need a PWM signal which is produced by a 555 timer IC and the duty cycle of the switching signal is varied using a 100k potentiometer.', u'Since we cant operate 555 timer above 15v so we incorporated a lm5008 Buck converter IC which steps down the input voltage from 84VDC to 10VDC which is used to power the timer IC and the cooling fan.', u'Now to handle the large amount of current, I have used four N-Channel Mosfets that are connected in parallel.', u'Besided that I have added all the complimentary components as described in the datasheets.', u'As I finished the schematic I have decided to go with designing a dedicated PCB for the speed controller as it will not only help us to keep everything neat but I intended to design this unit so thats its capable of further modifications for my other DIY projects that uses large DC motors.', u'The idea of designing a PCB might seems to take a whole lot of efforts but believe me it worth that all when you get your hands on customized boards. So with that in mind I designed the PCB for the speed controller unit. Always try to define particular regions such as the control circuitry and the power on the other side so that when you are connecting everything together you are good to go with appropriate track width specially on the power side.', u'I have also added four mounting holes which will be helpful to mount the controller and also hold the colling fan along with the heat sink above the MOSFETs.', u'Unlike any other customized part for your DIY Project, PCBs are surely the easiest one to get. Yes Now once we generated gerber files of our finilized PCB layout we are jjust a few clicks away from ordering our customized PCBs.', u'What all I did is to head upto ', u' and after going through a bunch of options there I uploaded my gerber files. Once the deisgn is checked for any errors by their techinical team your design is forwarded to the manufacturing line. The whole process will take two days to completa and hopefully you will get your PCBs within ust a week.', u' have made this project possible by their support so take your time and have a look at their website. They are offering Standard PCB, Quick-turn PCB, SMD etc so for discounts of upto 30% on your PCBs visit this ', u'.', u'Gerber files,schematic and the BOM(Bill Of Material) for the speed controller PCB is avliable ', u'.', u'As expected the PCBs arrived within a week and the finish is just too good. The quality of the PCBs is absolutely flawless. Now time to gather all the components as mentioned in the BOM(Bill of Material) and drop them in place. ', u'To keep things flowing we need to start with the smallest component on the PCB which in our case is LM5008 Buck converter, an SMP component. Once we sottered it using soldering braid as we dont have a hot gun to deal with SMD component, we than sottered the inductor next to it and moved towards larger components.', u'Once we are done assembling the boards, Its time to drop the 555 timer in place with the notch in correct direction.', u'With this much amount of power that we are going to deal with, obviously things are expected to heat up. So to deal with that we are going to bend the MOSFETs and mounted a 12v fan with the heat sink sandwitched inbetween.', u'With that being done, the beast of a PWM speed controller is ready to roll.', u'To test the controller we are goint to use an 84v customized battery pack that we have built for our electric bicycle. The controller is temporarily connected to the battery pack and the motor that is attached to the bicycle to drive the rear wheel.', u'As I toggled the switch, the controller is powered on with the fan blowing air over the MOSFETs. As I turned the potentiometer clockwise, the motor started to rotated and gradually increasing the speed proportional to the rotation of knob.', u'At this stage the speed controller is ready and it went way beyound my expectations as far as the finish is concerned. The controller seems to operate easily on 84v battery pack and controlls the speed of the motor smoothly.', u'But to test this speed controller on load we need to finish our bicycle project and mount everything in place. So guys for on load performance stay tuned for the upcoming project video which is a DIY electric bicycle conversion project.', u' and stay tuned for upcoming project video.', u'Regards.', u'DIY King'],
u'channel': u'Electronics'}
'''
with open(IN_FILENAME) as json_file:
    data_IN = json.load(json_file)
    #values = json.dumps(data, indent=4)
    print(data_IN[0].keys())
    print(data_IN[0])
    print(unify("IN",data_IN[0]))
