from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_script import Manager, Command, Shell
from flask_mail import Mail, Message
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk import word_tokenize, pos_tag
from tenseflow import change_tense
from win10toast import ToastNotifier
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it is not readable'
manager = Manager(app)

EmailTemplate = [
    {
        'id': 0,
        'Route': 'GOTO http://127.0.0.1:5000/Intro/',
        'Name': 'Introduction Email Template'
    },
    {
        'id': 1,
        'Route': 'GOTO http://127.0.0.1:5000/FollowUp/',
        'Name': 'Follow-Up Email Template'
    },
    {
        'id': 2,
        'Route': 'GOTO http://127.0.0.1:5000/Reengagement/',
        'Name': 'Reengagement Email Template'
    },
    {
        'id': 3,
        'Route': 'GOTO http://127.0.0.1:5000/CustomerApp/',
        'Name': 'Customer-Appreciation Email Template'
    },
    {
        'id': 4,
        'Route': 'GOTO http://127.0.0.1:5000/EventInvite/',
        'Name': 'Event-Invite Email Template'
    },
    {
        'id': 5,
        'Route': 'GOTO http://127.0.0.1:5000/SpecialDiscount/',
        'Name': 'Discount-Offer Email Template'
    },
    {
        'id': 6,
        'Route': 'GOTO http://127.0.0.1:5000/ServiceUpdate/',
        'Name': 'Service-Update Template'
    },
    {
        'id': 7,
        'Route': 'GOTO http://127.0.0.1:5000/ThankPurchase/',
        'Name' : 'Thank you for Purchase Email Template'
    },
    {
        'id': 8,
        'Route': 'GOTO http://127.0.0.1:5000/Testimonial/',
        'Name': 'Testimonial Request Email Template'
    },
    {
        'id': 9,
        'Route': 'GOTO http://127.0.0.1:5000/Review/',
        'Name' : 'Review Request Email Template'
    },
    {
        'id': 10,
        'Route': 'GOTO http://127.0.0.1:5000/Blog/',
        'Name': 'Blog-Update Email Template'
    },
    {
        'id': 11,
        'Route': 'GOTO http://127.0.0.1:5000/UpcEvent/',
        'Name': 'Upcoming-Event Email Template'
    },
    {
        'id': 12,
        'Route': 'GOTO http://127.0.0.1:5000/SickLeave/',
        'Name': 'Sick Leave Mail'
    },
    {
        'id': 13,
        'Route': 'GOTO http://127.0.0.1:5000/DayLongMeetings/',
        'Name': 'Day Long Meeting Mail'
    },
    {
        'id': 14,
        'Route': 'GOTO http://127.0.0.1:5000/Meeting1/',
        'Name': 'Meeting1 Mail'
    },
    {
        'id': 15,
        'Route': 'GOTO http://127.0.0.1:5000/Meeting2/',
        'Name': 'Meeting2 Mail'
    },
    {
        'id': 16,
        'Route': 'GOTO http://127.0.0.1:5000/Leave/',
        'Name': 'Leave Mail '
    },
    {
        'id': 17,
        'Route': 'GOTO http://127.0.0.1:5000/Deliverable/',
        'Name' : 'Deliverable Sent Revision Mail'
    },
    {
        'id': 18,
        'Route': 'GOTO http://127.0.0.1:5000/DeliverableSent/',
        'Name': 'Deliverable Sent Mail'
    },
    {
        'id': 19,
        'Route': 'GOTO http://127.0.0.1:5000/SickLeave1/',
        'Name' : 'Sick Leave 1'
    },
    {
        'id': 20,
        'Route': 'GOTO http://127.0.0.1:5000/SickLeave2/',
        'Name' : 'Sick Leave 2'
    },
    {
        'id': 21,
        'Route': 'GOTO http://127.0.0.1:5000/SickLeave3/',
        'Name' : 'Sick Leave 3'
    },
    {
        'id': 22,
        'Route': 'GOTO http://127.0.0.1:5000/AnnualLeave/',
        'Name' : 'Annual Leave'
    },
    {
        'id': 23,
        'Route': 'GOTO http://127.0.0.1:5000/Resignation/',
        'Name': 'Resignation Mail'
    },
    {
        'id': 24,
        'Route': 'GOTO http://127.0.0.1:5000/Farewell/',
        'Name': 'Farewell/Last Working Day mail'
    },
    {
        'id': 25,
        'Route': 'GOTO http://127.0.0.1:5000/Reminder/',
        'Name': 'Reminder'
    }
]


def findtense(find_tense):  # find tense of sentense
    train_text = state_union.raw("2005-GWBush.txt")
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(find_tense)
    for i in tokenized:
        words = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(words)
        # print(tagged)
        for j in tagged:
            j = list(j)
            if (j[1] == "MD"):
                return ("future")
                break
            elif (j[1] in ["VBP", "VBZ", "VBG"]):
                return ("present")
                break
            elif (j[1] in ["VBD", "VBN"]):
                return ("past")
                break

def Convert(string):  # function of converting string into list
    li = list(string.split("  "))
    return li

def listToString(s):  # function of converting list to string
    str1 = " "
    # return string
    return (str1.join(s))


def SendMail(sub,body):
    mail = Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'hblocks001@gmail.com'
    app.config['MAIL_PASSWORD'] = 'hacker#blocks09'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True    
    msg = Message(sub, sender='hblocks001@gmail.com', recipients=['anujnamdev40@gmail.com'])
    msg.body = body
    mail.send(msg)

@app.route('/')
def api_all():
    return jsonify(EmailTemplate)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

#IntroEmail
@app.route('/Intro/', methods=['POST'])
def Intro():
    req_data = request.get_json()

    string = "Hi  [name]  ,\n Thank you for showing interest in  [your product/service]  .  By taking this initial step, you are already well on your way to meeting your  [goals your business can help your prospect meet]  . \n  For our prospective customers, we  [describe a special offer]  .  [Describe the unique value and benefits of your offer for your audience.]  .  Please let us know if you would like us to help you find a  [solution]  ! Give us a call/Email us at  [Insert your contact information]  . \n Best regards, \n   [Your name]  "
    new = Convert(string)
    
    sub = req_data['sub']  # subject
    rname = req_data['rname'] # recipientname
    prod = req_data['prod']  # product
    spo = req_data['spo']  # specialoffer
    unv = req_data['unv'] # uniquevalue
    sol = req_data['sol'] # solution
    con = req_data['con']  # contact
    sname = req_data['sname']   # sendername
    gyb = req_data['gyb']  # goals your business

    new.remove(new[1])
    new.insert(1, sname)
    new.remove(new[3])
    new.insert(3, prod)
    new.remove(new[6])
    if findtense(gyb) is not None:

        tense1 = findtense(gyb)
        aaa1 = new[5]
        try:
            new_string1 = change_tense(aaa1 + gyb, tense1)

        except:
            new_string1 = aaa1 + gyb
        new.remove(new[5])
        new.insert(5, new_string1)

    else:
        aaa1 = new[5]
        new_string1 = aaa1 + gyb
        new.remove(new[5])
        new.insert(5, new_string1)
    new.remove(new[8])
    if findtense(spo) is not None:

        tense2 = findtense(spo)
        aaa2 = new[7]
        try:
            new_string2 = change_tense(aaa2 + spo, tense2)
        except:
            new_string2 = aaa2 + spo
        new.remove(new[7])
        new.insert(7, new_string2)
    else:
        aaa2 = new[7]
        new_string2 = aaa2 + spo
        new.remove(new[7])
        new.insert(7, new_string2)

    new.remove(new[9])
    new.insert(9, unv)
    new.remove(new[12])
    if findtense(sol) is not None:

        tense3 = findtense(sol)
        aaa3 = new[11]
        try:
            new_string3 = change_tense(aaa3 + sol, tense3)
        except:
            new_string3 = aaa3 + sol
        new.remove(new[11])
        new.insert(11, new_string3)
    else:
        aaa3 = new[11]
        new_string3 = aaa3 + sol
        new.remove(new[11])
        new.insert(11, new_string3)
    new.remove(new[13])
    new.insert(13, con)
    new.remove(new[15])
    new.insert(15, rname)

    body = listToString(new)
    print(body)
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.data
    col = db.dataemail
    db.dataemail.insert_many([{"subject": subject, "recipient": rname, "Contact": scont, "Sender":sname,"Topic": "Introduction Email Template", "Body": new}])
    '''
    return '<h1>Body: {}</h1>'.format(body)

#FollowUp
@app.route('/FollowUp/', methods=['POST'])
def FollowUp():
    req_data = request.get_json()

    string = "Dear  [name]  ,\nYou  [how and when the person approached your business initially]  and  we hope you were able to  [insert the value of your prospect gained from your last offer]  .This week, we are excited to introduce to you  [new offer such as valuable content or a discount]  .  [Describe the value of your offer]  .  \n[Define the problem or concern your audience faces]  .  [Represent your product or service’s unique solution to your prospective customer’s problem]  .  [Brief reiteration of your product/service’s answer to your audience’s needs]  .\nPlease let us know how we can help you by  [insert your contact information]  .\nWe hope to hear from you soon. \nBest regards,\n  [Name]  "
    new = Convert(string)

    rname = req_data['rname']   #[name]
    tp = req_data['tp']    #[how and when the person approached your business initially]
    aut = req_data['aut']   # [insert the value of your prospect gained from your last offer]
    link = req_data['link']     #[new offer such as valuable content or a discount]
    firstpa = req_data['firstpa']   #[Describe the value of your offer]
    pblog = req_data['pblog']   #[Define the problem or concern your audience faces]
    blgtle = req_data['blgtle']     #[Represent your product or service’s unique solution to your prospective customer’s problem]
    freq = req_data['freq']     #[Brief reiteration of your product/service’s answer to your audience’s needs]
    sub = req_data['sub']   #[insert your contact information]
    sname = req_data['sname']   #[Name]

    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, tp)

    new.remove(new[6])
    if findtense(aut) is not None:

        tense1 = findtense(aut)
        aaa1 = new[5]
        try:
            new_string1 = change_tense(aaa1 + aut, tense1)

        except:
            new_string1 = aaa1 + aut
        new.remove(new[5])
        new.insert(5, new_string1)

    else:
        aaa1 = new[5]
        new_string1 = aaa1 + aut
        new.remove(new[5])
        new.insert(5, new_string1)

    new.remove(new[7])
    if findtense(link) is not None:

        tense1 = findtense(link)
        aaa1 = new[6]
        try:
            new_string1 = change_tense(aaa1 + link, tense1)

        except:
            new_string1 = aaa1 + link
        new.remove(new[6])
        new.insert(6, new_string1)

    else:
        aaa1 = new[6]
        new_string1 = aaa1 + link
        new.remove(new[6])
        new.insert(6, new_string1)

    new.remove(new[8])
    new.insert(8, firstpa)
    new.remove(new[10])

    new.insert(10, pblog)
    new.remove(new[12])
    new.insert(12, blgtle)
    new.remove(new[14])
    new.insert(14, freq)
    new.remove(new[16])
    new.insert(16, sub)
    new.remove(new[18])
    new.insert(18, sname)
    
    body = listToString(new)
    SendMail(sub,body)#sendmail
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d4
    col = db.dataemaildb.dataemail.insert_many([{"recipient": rname, "TimePeriod": tp, "Link": link, "Author": aut, "Description": descp, "PreviousBlogDescription": pblog, "Sender": sname}])
    '''
    return '<h1>Body: {}</h1>'.format(body)

#ReengagementEmail
@app.route('/Reengagement/', methods=['POST'])
def Reengagement():
    req_data = request.get_json()
    
    string="Subject Line: Following up on  [last encounter]\n  Hi  [name]  ,\nI  [insert contact method]  you  [insert last time you reached out]  in response to  [how your potential customer initially reached out to you]  .  [Refresh their memory of what you talked about]  .\n  [Send your prospects an additional offer that would address questions or concerns them had during your conversation with them]  . I hope you will find it helpful and informative. Please feel free to let me know if you had any questions or feedback.\nIf you are currently looking for better ways to  [what is the problem that your prospect is looking to solve with your product or service]  , I believe that  [your business’s/product’s name]  may be a great solution for you and here is why:\n  [Make a bulleted list of your business’s unique selling points. Bold or highlight any key words to make the email easier to scan for your audience]  .\nIf you would like to discuss your business in greater detail, you can reach me directly at  [Insert your contact information]  .\nBest regards,\n  [Name]  "
    new = Convert(string)
    
    sub = req_data['sub'] #[last encounter]
    rname = req_data['rname'] #[name]
    conn = req_data['conn'] #[insert contact method]
    ltc = req_data['ltc']   #[insert last time you reached out]
    adoff = req_data['adoff'] #[how your potential customer initially reached out to you]
    bmsg = req_data['bmsg']  #[Refresh their memory of what you talked about]
    fback = req_data['fback']  #[Send your prospects an additional offer that would address questions or concerns them had during your conversation with them]
    mkey = req_data['mkey']  #[what is the problem that your prospect is looking to solve with your product or service]
    product_name = req_data['product_name']
    selling_point = req_data['selling_point']
    contact_info = req_data['contact_info']
    sname = req_data['sname'] #[Name]

    new.remove(new[1])
    new.insert(1, sub)
    new.remove(new[3])
    new.insert(3, rname)
    new.remove(new[5])
    new.insert(5, conn)
    new.remove(new[7])
    new.insert(7, ltc)
    new.remove(new[9])
    new.insert(9, adoff)
    new.remove(new[11])
    new.insert(11, bmsg)
    new.remove(new[13])
    new.insert(13, fback)

    new.remove(new[15])
    if findtense(mkey) is not None:

        tense1 = findtense(mkey)
        aaa1 = new[14]
        try:
            new_string1 = change_tense(aaa1 + mkey, tense1)

        except:
            new_string1 = aaa1 + mkey
        new.remove(new[14])
        new.insert(14, new_string1)

    else:
        aaa1 = new[14]
        new_string1 = aaa1 + mkey
        new.remove(new[14])
        new.insert(14, mkey)

    new.remove(new[16])
    new.insert(16, product_name)
    new.remove(new[18])
    new.insert(18, selling_point)
    new.remove(new[20])
    new.insert(20, contact_info)
    new.remove(new[22])
    new.insert(22, sname)
    
    body = listToString(new)
    SendMail(sub, body)  # sendmail
    print(body)
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d2
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "recipient": rname, "ContactMethod": conn, "LatTimeContacted": ltc, "AddtionalOffer": adoff, "Message": bmsg, "feedback": fback, "MainKeywords": mkey, "Sender": sname,"SellingPoint":selling_point,"ContactInfo":contact_info,"ProductName":product_name}])
    '''
    return '<h1>Body: {}</h1>'.format(body, rname, conn, ltc, adoff, bmsg, selling_point, contact_info, product_name, body)
    

#EventInvite
@app.route('/EventInvite/', methods=['POST'])
def EventInvite():
    req_data = request.get_json()
    
    string = "Dear  [rname]  ,\nYou are invited to attend  [event name]  to  [briefly describe the value of your event]  .\n  [If your event is featuring an industry expert, include information here]  .\nDate/Time/Venue  [Date, Time and time zone, Venue]  \nCost  [Cost if applicable]  . \nWe will be discussing:  [List 1]  ,  [List 2]  ,  [List 3]  and more to go. \nSign up now!, If you cannot attend this event, be sure to check out  [special offer]  for additional resources.\nHope you see you soon!\nBest regards,\n  [sname]  "
    sub = req_data['sub']
    rname = req_data['rname']
    ename = req_data['ename']
    bmsg = req_data['bmsg']
    exp = req_data['exp']
    tm = req_data['tm']
    cost = req_data['cost']
    ben1 = req_data['ben1']
    ben2 = req_data['ben2']
    ben3 = req_data['ben3']
    sof = req_data['sof']
    sname = req_data['sname']
    new = Convert(string)
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, ename)
    new.remove(new[5])
    new.insert(5, bmsg)
    new.remove(new[7])
    new.insert(7, exp)
    new.remove(new[9])
    new.insert(9, tm)
    new.remove(new[11])
    new.insert(11, cost)
    new.remove(new[13])
    new.insert(13, ben1)
    new.remove(new[15])
    new.insert(15, ben2)
    new.remove(new[17])
    new.insert(17, ben3)
    new.remove(new[19])
    new.insert(19, sof)
    new.remove(new[21])
    new.insert(21, sname)
    
    body = listToString(new)
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d4
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "recipient": rname, "Event": ename, "Message": msg, "Venue/Date": tm, "Cost": cost, "Benefit1": ben1, "Benefit2": ben2, "Benefit3": ben3, "SpecialOffer": sof, "Sender": sname}])
    '''
    return '''<h1>Body: {}</h1>'''.format(body)

    
# SpecialDiscount
@app.route('/SpecialDiscount/', methods=['POST'])
def SpecialDiscount():
    req_data = request.get_json()
    
    string = "Dear  [name]  ,\n As a valued customer, we would like to offer you a  [Special discount offer]  for  [State length of time offer is valid for]  . \n We hope you will take advantage of our special offer.  [State the unique value of your offer]  . \n As always, do not hesitate to reach out to us if you need any help by emailing us at  [your email]  or calling us directly  [your phone number]  . \nThanks, \n  [Name]  "
    new = Convert(string)
    print(new)
    sub = req_data['sub']  # subject
    rname = req_data['rname']  # recipientname
    spo = req_data['spo']  # specialoffer
    tov = req_data['tov']  # timeofferisvalid
    unv = req_data['unv']  # uniquevalue
    mail = req_data['mail']  # email
    phn = req_data['phn']  # phonenumber
    sname = req_data['sname']  # sendername

    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    if findtense(spo) is not None:
        tense = findtense(spo)
        aaa = new[2]
        try:
            new_string = change_tense(aaa + spo, tense)
        except:
            new_string = aaa + spo
        new.remove(new[2])
        new.insert(2, new_string)
    else:
        aaa = new[2]
        new_string = aaa + spo
        new.remove(new[2])
        new.insert(3, spo)
    new.remove(new[4])
    new.insert(4, tov)

    new.remove(new[6])
    new.insert(6, unv)
    new.remove(new[8])
    new.insert(8, mail)
    new.remove(new[10])
    new.insert(10, phn)
    new.remove(new[12])
    new.insert(12, sname)

    body = listToString(new)
    print(body)
    SendMail(sub, body)


    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.data
    col = db.dataemail
    db.dataemail.insert_many([{"subject": subject, "recipient": rname, "Contact": scont, "Sender":sname,"Topic": "Special Discount Email Template", "Body": new}])
    '''
    return '<h1>Body: {}</h1>'.format(body)
    

#ServiceUpdate
@app.route('/ServiceUpdate/', methods=['POST'])
def ServiceUpdate():
    req_data = request.get_json()

    string = "Dear  [Name]  , \n We are excited to introduce to you our latest  [Brief outline of new product or service]  .  [Give a brief description of your new offering and bold or underline any key points]  .  [Describe the benefits of your new offering]  .  [Tell people how to get the new offering]  . \n  [Closing remarks about the new offering]  . Please get in touch  [Insert contact information]  , if you have any questions or if there is anything else we can do to help you  [Your audience’s goal]  ! \n Best regards, \n  [Name]  "
    new = Convert(string)

    sub = req_data['sub']#subject
    rname = req_data['rname']#recipientname
    onp = req_data['onp']#outlineofnewproduct
    bdsc = req_data['bdsc']#briefdesctiption
    bno = req_data['bno']#benifitsofnewofferings
    howt = req_data['howt']#howtogetofferings
    rem = req_data['rem']#remarks
    con = req_data['con']#contact
    agoal = req_data['agoal']#audience'sgoal
    sname = req_data['sname']#sendername

    new.remove(new[1])
    new.insert(1, sname)
    new.remove(new[3])
    if findtense(onp) is not None:

        tense = findtense(onp)
        aaa = new[2]
        try:
            new_string = change_tense(aaa + onp, tense)
        except:
            new_string = aaa + onp
        new.remove(new[2])
        new.insert(2, new_string)
    else:
        aaa = new[2]
        new_string = aaa + onp
        new.remove(new[2])
        new.insert(2, new_string)

    new.remove(new[4])
    if findtense(bdsc) is not None:

        tense = findtense(bdsc)
        aaa = new[3]
        try:
            new_string = change_tense(aaa + bdsc, tense)
        except:
            new_string = aaa + bdsc
        new.remove(new[3])
        new.insert(3, new_string)
    else:
        aaa = new[3]
        new_string = aaa + bdsc
        new.remove(new[3])
        new.insert(3,new_string)

    new.remove(new[5])
    if findtense(bno) is not None:
        tense = findtense(bno)
        aaa = new[4]
        try:
            new_string = change_tense(aaa + bno, tense)
        except:
            new_string = aaa + bno
        new.remove(new[4])
        new.insert(4, new_string)
    else:
        aaa = new[4]
        new_string = aaa + bno
        new.remove(new[4])
        new.insert(4, new_string)

    new.remove(new[6])
    new.insert(6, howt)
    new.remove(new[8])
    new.insert(8, rem)
    new.remove(new[10])
    new.insert(10, con)
    new.remove(new[12])

    if findtense(agoal) is not None:

        tense = findtense(agoal)
        aaa = new[11]
        try:
            new_string = change_tense(aaa + agoal, tense)
        except:
            new_string = aaa + agoal
        new.remove(new[11])
        new.insert(11, new_string)
    else:
        aaa = new[11]
        new_string = aaa + agoal
        new.remove(new[11])
        new.insert(11, new_string)

    new.remove(new[13])
    new.insert(13, rname)

    body = listToString(new)
    print(body)
    SendMail(sub, body)  # sendmail

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.data
    col = db.dataemail
    db.dataemail.insert_many([{"subject": subject, "recipient": rname, "Contact": scont, "Sender":sname,"Topic": "Introduction Email Template", "Body": new}])
    '''
    return '''<h1>Body: {}</h1>'''.format(body)


#ThankPurchase
@app.route('/ThankPurchase/', methods=['POST'])
def ThankPurchase():
    req_data = request.get_json()
    
    string = "Dear  [name]  ,\nOn behalf of  [your business name]  , I would like to thank you for purchasing   [buying/using your product/service]  . We sincerely hope that you will continue to enjoy our  [name of your product/service]  and use it to for  [your product/service’s unique selling point]  .\nIf you have any questions or if we can further assist you in any way, please feel free to contact on  [insert contact method]  me.\n  [Promote any upcoming events/new products or services/related products/services]  .\nI hope to hear from you soon!\nThank you once again,\n  [Name]"
    new = Convert(string)

    sub = req_data['sub']
    rname = req_data['rname']
    cname = req_data['cname']
    np = req_data['np']
    msg = req_data['msg']
    cont = req_data['cont']
    prom = req_data['prom']
    sname = req_data['sname']
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, cname)
    new.remove(new[5])
    new.insert(5, np)
    new.remove(new[7])
    new.insert(7, np)
    new.remove(new[9])
    new.insert(9, msg)
    new.remove(new[11])
    new.insert(11, cont)
    new.remove(new[13])
    new.insert(13, prom)
    new.remove(new[15])
    new.insert(15, sname)

    body = listToString(new)
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d11
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "CompanyName": cname, "Event": ename, "Description": descp, "Location": loc, "Date": ddt, "time": tm, "Link": link, "Sender": sname}])
    '''
    return '''<h1>Mail Body: {}</h1>'''.format(body)

#Testimonial
@app.route('/Testimonial/', methods=['POST'])
def Testimonial():
    req_data = request.get_json()

    string = "Dear  [Name]  ,\n We hope that you are enjoying your experience with  [Insert your product/company name]  .  [Add any specifics about your business or the customer to personalize the email]  .\nBecause your opinion means a great deal to us, we would appreciate your feedback. With your permission, we would also love to share your insights about our product/service with potential customers/clients.\nSimply reply to this email with your story. Feel free to write whatever you like, but we have included a couple of questions that you can use as a guideline.\n1. What was the reason why you approached us?\n  [r1]  \n2. What’s one specific feature you like most about our product/service?\n  [r2]  \n3. What was the outcome you found from buying this product/using this service?\n  [r3]  \nWe appreciate your time and thank you again for your business. \nBest regards, \n  [Your name]  "
    new = Convert(string)
    
    sub = "Testimonal"
    rname = req_data['rname']  # recipient name
    cname = req_data['cname']  # company name
    syb = req_data['syb']  # specifics about business/customers
    rto = req_data['rto']  # reason to contact
    sop = req_data['sop']  # specific feature of product
    ofb = req_data['ofb']  # outcome from buying product
    sname = req_data['sname']  # senders name
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, cname)
    new.remove(new[5])
    new.insert(5, syb)
    new.remove(new[7])
    new.insert(7, rto)
    new.remove(new[9])
    new.insert(9, sop)
    new.remove(new[11])
    new.insert(11, ofb)
    new.remove(new[13])
    new.insert(13, sname)

    body = listToString(new)
    SendMail(sub, body)

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d8
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "Company": cname, "Message": msg, "ReasonToContact": rto, "Sender": sname}])
    '''
    return '<h1>Body: {}</h1>'.format(body)

#Review
@app.route('/Review/', methods=['POST'])
def Review():
    req_data = request.get_json()

    string = "Dear  [NAME]  ,\n  [A personalized greeting]  . We appreciate the trust that you have placed in our  [YOUR BUSINESS’S NAME]  and we will continue to strive to provide you with  [Description of what your objective is]  . Online reviews are an important part of our business so that we get your insightful feedback and continue to deliver the best service to all of our customers.\nWe would love for you to share your comments with us by leaving a review on  [Link to the site or platform you would like your recipient to leave a review on e.g Yelp and Google Maps]  .\n  [Your business name]  welcomes unbiased and informative reviews. If we have not fulfilled your expectations of us, we would like to take this opportunity to do what we can to correct any issues that might have arisen and continue to build our relationship with you.\nThank you for your continued patronage of our business and we look forward to hearing from you.\nBest Regards,\n  [Name]"
    new = Convert(string)
    
    sub = 'Your Feedback Means a Lot'
    rname = req_data['rname']
    grt = req_data['grt']
    bname = req_data['bname']
    msg = req_data['msg']
    link = req_data['link']
    sname = req_data['sname']

    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, grt)
    new.remove(new[5])
    new.insert(5, bname)
    new.remove(new[7])
    if findtense(msg) is not None:

        tense1 = findtense(msg)
        aaa1 = new[6]
        try:
            new_string1 = change_tense(aaa1 + msg, tense1)

        except:
            new_string1 = aaa1 + msg
        new.remove(new[6])
        new.insert(6, new_string1)

    else:
        aaa1 = new[6]
        new_string1 = aaa1 + msg
        new.remove(new[6])
        new.insert(6, msg)
    new.remove(new[8])
    new.insert(8, link)
    new.remove(new[10])
    new.insert(10, bname)
    new.remove(new[12])
    new.insert(12, sname)
    
    body = listToString(new)
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d11
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "CompanyName": cname, "Event": ename, "Description": descp, "Location": loc, "Date": ddt, "time": tm, "Link": link, "Sender": sname}])
    '''
    return '''<h1>Mail Body: {}</h1>'''.format(body)

#Blog
@app.route('/Blog/', methods=['POST'])
def Blog():
    req_data = request.get_json()

    string = "Subject Line:  [Frequency]  Blog Post Roundup \n Dear  [Name]  , \n  Here’s what we’ve been working on for blog posts this  [Time period]  .Whether you re-read your favorites or catch up on ones you missed, we hope you’ll get something out of them! \n  [Insert blog post title hyperlinked to blog URL]  \n By:  [Author’s name]  \n  [First paragraph or quick snippet]  \n Read full post  [Hyperlink to blog post]  \n  [Insert up to 3 blog posts]  \n Best Regards, \n  [ Name]  "
    new = Convert(string)
    
    sub = req_data['sub']
    rname = req_data['rname']   #[Name]
    tp = req_data['tp'] #timeperiod
    link = req_data['link'] #hyperlink
    aut = req_data['aut']   #author
    firstpa = req_data['firstpa']   #[First paragraph or quick snippet
    pblog = req_data['pblog']   #[Insert up to 3 blog posts]
    freq= req_data['freq']  #[Frequency]
    blgtle = req_data['blgtle'] #[Insert blog post title hyperlinked to blog URL]
    sname = req_data['sname']   #[ name]

    new.remove(new[1])
    new.insert(1,freq)
    new.remove(new[3])
    new.insert(3,rname)
    new.remove(new[6])
    new.insert(6,tp)
    new.remove(new[8])
    new.insert(8,blgtle)
    new.remove(new[10])
    new.insert(10,aut)
    new.remove(new[12])
    new.insert(12,firstpa)
    new.remove(new[14])
    new.insert(14,link)
    new.remove(new[16])
    new.insert(16,pblog)
    new.remove(new[18])
    new.insert(18,sname)
    
    body = listToString(new)    
    SendMail(sub,body)

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d10
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "TimePeriod": tp, "Link": link, "Author": aut, "Description": descp, "PreviousBlogDescription": pblog, "Sender": sname}])
    '''
    return '''<h1>Body:{}</h1>'''.format(body)


#UpcEvent
@app.route('/UpcEvent/', methods=['POST'])
def UpcEvent():
    req_data = request.get_json()
    
    string = "Dear  [rname]  ,\nHere at  [your company name]  , we are committed to providing regular workshops and live practical opportunities to continue learning, grow your network, and get involved with the community. \nAs a valued customer, we want to let you know about our upcoming events. \n•  [Event title]  :  [Brief description of event]  \n•  Location:  [Location]  \n•  Date:  [Event date]  \n•  When:  [time]  \nLearn more details and register here  [Link to event page]  \nWe hope to see you there! Feel free to reply back with questions regarding these events!\nBest regards,\n  [sname]  "
    new = Convert(string)
    
    rname = req_data['rname']
    cname = req_data['cname']
    ename = req_data['ename']
    descp = req_data['descp']
    loc = req_data['loc']
    ddt = req_data['ddt']
    tm = req_data['tm']
    link = req_data['link']
    sname = req_data['sname']
    sub = "UP coming event"
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, cname)
    new.remove(new[5])
    new.insert(5, ename)
    new.remove(new[7])
    new.insert(7, descp)
    new.remove(new[10])
    new.insert(10, loc)
    new.remove(new[13])
    new.insert(13, ddt)
    new.remove(new[16])
    new.insert(16, tm)
    new.remove(new[18])
    new.insert(18, link)
    new.remove(new[20])
    new.insert(20, link)

    body = listToString(new)
    SendMail(sub,body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d11
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "CompanyName": cname, "Event": ename, "Description": descp, "Location": loc, "Date": ddt, "time": tm, "Link": link, "Sender": sname}])
    '''
    return '''<h1>Mail Body: {}</h1>'''.format(body)
    


#SickLeave
@app.route('/SickLeave/', methods=['POST'])
#DayLongMeetings
def SickLeave():
        req_data = request.get_json()
        string = "Dear  [rname]  ,\n \n Thank you for your email! \n \n I am on a sick leave today with no access to mails. \n \n Please expect a delay in response. In case of anything urgent, please reach out to  [pname]  [email]  or I will respond once I am back in the office. \n \n For anything urgent, please message me on  [conn]  and I will try to get back to you as soon as I can. \n \n Regards, \n  [sname]  "
        # variables
        sub = 'Leave application - Sick Leave'  # subject
        rname = req_data['rname']  # recipientname
        pname = req_data['pname']  # person'sname
        email = req_data['email']  # email
        conn = req_data['conn']  # contact
        sname = req_data['sname']  # sendername

        new = Convert(string)  # converting string into list
        new.remove(new[1])
        new.insert(1, rname)
        new.remove(new[3])
        new.insert(3, pname)
        new.remove(new[4])
        new.insert(4, email)
        new.remove(new[6])
        new.insert(6, conn)
        new.remove(new[8])
        new.insert(8, sname)

        body = listToString(new)
        print(body)

        # db logic
        '''client = MongoClient("localhost", 27017)
        db = client.d1
        col = db.dataemail
        db.dataemail.insert_many([{"subject": sub, "Recipient Name": rname, "Alternate contact Name": pname, "Contact": conn, "Sender": sname}])
        '''
        return '''<h1>Mail Body: {}</h1>'''.format(body)



@app.route('/DayLongMeetings/', methods=['POST'])
#Meeting1
def Daylongmeeting():
        req_data = request.get_json()
        string = "Hi  [rname]  \n Thank you for your email. \n \n I am in back to back meetings today and so I may revert late on your email. For live projects, please get in touch with the respective team members –  [tm1]  [ email1]  ,  [tm2]  [ email2]  or  [tm3]  [ email3]  .\n \n For anything urgent, please message me on  [conn]  and I will try to get back to you as soon as I can. \n \n Thanks, \n  [sname]  "
        # variables
        sub = req_data['sub']  # subject
        rname = req_data['rname']  # recipientname
        tm1 = req_data['tm1']  # teammember1
        email1 = req_data['email1']  # email1
        tm2 = req_data['tm2']  # teammember2
        email2 = req_data['email2']  # email2
        tm3 = req_data['tm3']  # teammember3
        email3 = req_data['email3']  # email3
        conn = req_data['conn']  # contact
        sname = req_data['sname']  # sendername
        new = Convert(string)  # converting string into list

        new.remove(new[1])
        new.insert(1, rname)
        new.remove(new[3])
        new.insert(3, tm1)
        new.remove(new[4])
        new.insert(4, email1)
        new.remove(new[6])
        new.insert(6, tm2)
        new.remove(new[7])
        new.insert(7, email2)
        new.remove(new[9])
        new.insert(9, tm3)
        new.remove(new[10])
        new.insert(10, email3)
        new.remove(new[12])
        new.insert(12, conn)
        new.remove(new[14])
        new.insert(14, sname)

        body = listToString(new)
        print(body)

        SendMail(sub, body)

        return '''<h1>subject: {}</h1>
                            <h1>recipientname: {}</h1>
                            <h1>team member1: {}</h1>
                            <h1>email1: {}</h1>
                            <h1>team member2: {}</h1>
                            <h1>email2: {}</h1>
                            <h1>team member3: {}</h1>
                            <h1>email3: {}</h1>
                            <h1>sendername: {}</h1>
                            <h1>Body: {}</h1>'''.format(sub, rname, tm1, email1, tm2, email2, tm3, email3, sname, body)



@app.route('/Meeting1/', methods=['POST'])
#Meeting1
def Meeting1():
        req_data = request.get_json()

        string = "Hi  [rname]  , \n We have a meeting scheduled tomorrow with the  [cname]  Team  [tname]  . Hence, we need to share the issues that we have faced recently. Request everyone to plan your work accordingly in order to attend the meeting. \n The meeting is scheduled on  [mdate]  -  [mtime]  . \n \n Regards,  [sname]  "
        # variables
        sub = req_data['sub']  # subject
        rname = req_data['rname']  # recipientname
        cname = req_data['cname']  # company name
        tname = req_data['tname']  # team name
        mdate = req_data['mdate']  # meeting date
        mtime = req_data['mtime']  # meeting time
        sname = req_data['sname']  # sendername
        new = Convert(string)  # converting string into list

        new.remove(new[1])
        new.insert(1, rname)
        new.remove(new[3])
        new.insert(3, cname)
        new.remove(new[5])
        new.insert(5, tname)
        new.remove(new[7])
        new.insert(7, mdate)
        new.remove(new[9])
        new.insert(9, mtime)
        new.remove(new[11])
        new.insert(11, sname)

        body = listToString(new)
        print(body)

        SendMail(sub, body)

        return '''<h1>subject: {}</h1>
                            <h1>recipientname: {}</h1>
                            <h1>company name: {}</h1>
                            <h1>team name: {}</h1>
                            <h1>meeting date: {}</h1>
                            <h1>meeting time: {}</h1>
                            <h1>sendername: {}</h1>
                            <h1>Body: {}</h1>'''.format(sub, rname, cname, tname, mdate, mtime, sname, body)


        return render_template('index.html', form=form)

@app.route('/Meeting2/', methods=['POST'])
def Meeting2():
        req_data = request.get_json()
        string = "Dear  [rname]  , \n Sharing the calendar invite for the face to face presentation at  [cname]  ,  [cadd]  office on  [mDate]  -  [mTime]  . \n Regards,  [sname]  \n  ([conn])  "
        # variables
        sub = req_data['sub']  # subject
        rname =req_data['rname']  # recipientname
        cname = req_data['cname']  # company name
        cadd = req_data['cadd']  # company address
        mdate = req_data['mdate']  # meeting date
        mtime = req_data['mtime']  # meeting time
        sname = req_data['sname']  # sendername
        conn = req_data['conn']  # contact
        new = Convert(string)  # converting string into list

        new.remove(new[1])
        new.insert(1, rname)
        new.remove(new[3])
        new.insert(3, cname)
        new.remove(new[5])
        new.insert(5, cadd)
        new.remove(new[7])
        new.insert(7, mdate)
        new.remove(new[9])
        new.insert(9, mtime)
        new.remove(new[11])
        new.insert(11, sname)
        new.remove(new[13])
        new.insert(13, conn)

        body = listToString(new)
        print(body)

        SendMail(sub, body)

        return '''<h1>subject: {}</h1>
                            <h1>recipientname: {}</h1>
                            <h1>company name: {}</h1>
                            <h1>company address: {}</h1>
                            <h1>meeting date: {}</h1>
                            <h1>meeting time: {}</h1>
                            <h1>sendername: {}</h1>
                            <h1>contact: {}</h1>
                            <h1>Body: {}</h1>'''.format(sub, rname, cname, cadd, mdate, mtime, sname, conn, body)




#LeaveMail
@app.route('/LeaveMail/', methods=['POST'])
def LeaveMail():
    req_data = request.get_json()
    
    string = "Dear  Sender  ,\nI am on personal leave from  14th Oct to 17th Oct  with no access to mails or calls. Kindly expect certain delay in reply.\nIn case of anything urgent kindly connect with  FirstnameLastname1  on  firstname.lastname@companyname1.com  \nIn case of anything related to  Businessfunction1  Businessfunction2  Businessfunction3  please reach out to  FirstnameLastname2  firstname.lastname@companyname2.com;  +91 XXXXX XXXXX  \nRegards,\n  FirstnameLastname"
    new = Convert(string)

    sub = 'Leave Mail - Out of Office 3'
    rname = req_data['rname']
    leavedate = req_data['leavedate']
    name1 = req_data['name1']
    email = req_data['email']
    bfunc1 = req_data['bfunc1']
    bfunc2 = req_data['bfunc2']
    bfunc3 = req_data['bfunc3']
    name2 = req_data['name2']
    bemail = req_data['bemail']
    conn = req_data['conn']
    sname = req_data['sname']
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, leavedate)
    new.remove(new[5])
    new.insert(5, name1)
    new.remove(new[7])
    new.insert(7, email)
    new.remove(new[9])
    new.insert(9, bfunc1)
    new.remove(new[10])
    new.insert(10, bfunc2)
    new.remove(new[11])
    new.insert(11, bfunc3)
    new.remove(new[13])
    new.insert(13, name2)
    new.remove(new[14])
    new.insert(14, bemail)
    new.remove(new[15])
    new.insert(15, conn)
    new.remove(new[17])
    new.insert(17, sname)
    
    body = listToString(new)
    
    SendMail(sub,body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d11
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "CompanyName": cname, "Event": ename, "Description": descp, "Location": loc, "Date": ddt, "time": tm, "Link": link, "Sender": sname}])
    '''
    return '''<h1>Mail Body: {}</h1>'''.format(body)

#Deliverablesentrevision
@app.route('/Deliverable/', methods=['get', 'post'])
def Deliverable():
    req_data = request.get_json()

    string=" Subject: Deliverable sent with revisions \n Hi  [name]  ,\n Sharing the revised deliverable for all the changes as discussed over the call- \n 1.Have mentioned Change  [1]  \n2. Have mentioned Change  [2]  \n3.Have checked Change  [3]  \n4. Also, we have included the Change  [4]  .\nPlease do let me know in case of any clarifications.\nRegards,  [name]  "
    new = Convert(string)
    
    sub = 'Deliverable'
    rname = req_data['rname']
    change1= req_data['change1']
    change2 = req_data['change2']
    Checked_Change = req_data['Checked_Change']
    Change_included = req_data['Change_included']
    sname = req_data['Name']
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, change1)
    new.remove(new[5])
    new.insert(5, change2)
    new.remove(new[7])
    new.insert(7, Checked_Change)
    new.remove(new[9])
    new.insert(9, Change_included)
    new.remove(new[11])
    new.insert(11, sname)
    
    body = listToString(new)    
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d9
    col = db.dataemail
    db.dataemail.insert_many([{"Recipient-Name:": rname, "Change 1: ": change1, "Change 2:": change2, "Checked Change": Checked_Change, "Change Included": Change_included, "Sender-Name": sname}])
    '''
    return '''<h1>Body:{}</h1>'''.format(body)


# DeliverableSent
@app.route('/DeliverableSent/', methods=['POST'])
def DeliverableSent():
    req_data = request.get_json()
    
    string = "Hi  [Name]  ,\nSharing the deliverable for the project.\nPlease let us know when we can connect to discuss the same.\nRegards,\n  [Your name]  "
    new = Convert(string)

    sub = 'Deliverable'
    rname = req_data['rname']   # recipient name
    sname = req_data['sname']   # senders name
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, sname)

    body = listToString(new)        
    SendMail(sub,body)

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d8
    col = db.dataemail
    db.dataemail.insert_many([{"recipient": rname, "Sender": sname}])'''
    return '''<h1>Mail Body: {}</h1>'''.format(body)


# SickLeave1
@app.route('/SickLeave1/', methods=['POST'])
def SickLeave1():
    req_data = request.get_json()
    
    string = "Hi  [name]  ,\n Today I am not keeping well as I am having through stomach upset and fever. Would be taking leave for today.\nHope this is fine.\nRegards,\n  [Your name]"
    new = Convert(string)

    sub = "Sick leave"
    rname = req_data['rname']
    sname = req_data['sname']
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, sname)
    
    body = listToString(new)    
    SendMail(sub,body)

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d1
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "ManagerName": rname, "Sender": sname}])
    '''    
    return '''<h1>Mail body:{}</h1>'''.format(body)


# SickLeave2
@app.route('/SickLeave2/', methods=['POST'])
def SickLeave2():
    req_data = request.get_json()
    
    string = "Dear  (Managername)  \nWanted to inform you that I am down with fever and diarrhoea and hence will be taking a leave today.\nI shall complete all the pending tasks once I resume office back tomorrow.\nRegards,\n  employee name"
    new = Convert(string)
    
    rname = req_data['rname']   # Manager-Name
    sname = req_data['sname']   # Employee-Name
    sub = "Leave application - Sick Leave 2"  # subject
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, sname)
    
    body = listToString(new)    
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d1
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "ManagerName": rname, "Sender": sname}])
    '''
    return '''<h1>Mail Body: {}</h1>'''.format(body)


# SickLeave3
@app.route('/SickLeave3/', methods=['POST'])
def SickLeave3():
    req_data = request.get_json()
    
    string = "Dear  (Manager Name)  ,\nJust wanted to inform you that I will be taking a leave due to some unavoidable personal circumstances.\nWill be reachable over the calls in case of any queries.\nThanks,\n  Employee"
    new = Convert(string)

    rname = req_data['rname']  # Manager-Name
    sname = req_data['sname']  # Employee-Name
    sub = 'Leave application - Sick Leave 3'  # subject
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, sname)
    
    body = listToString(new)    
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d1
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "ManagerName": rname, "Sender": sname}])
    '''
    return '''<h1>Mail Body: {}</h1>'''.format(body)


#AnnualLeave
@app.route('/AnnualLeave/', methods=['POST'])
def AnnualLeave():
    req_data = request.get_json()        
    
    string = "Hi  (Manager name)  \nWanted to inform you that I am planning to take the annual leave from  DD/MM/YY to DD/MM/YY  for  X  working days.\nWould request you to approve the same. We can discuss the pending tasks and plan the same accordingly to avoid any last-minute rush.\nI shall also be applying the same in the system as well.\nRegards,\n  employeename"
    new = Convert(string)
    
    rname = req_data['rname']   #Manager-Name
    tp = req_data['tp']         #Time-Period
    nod = req_data['nod']      #number-of-days
    sname = req_data['sname']   #Employee-Name
    sub = 'Leave application - Annual Leave'    #subject
    
    new.remove(new[1])
    new.insert(1, rname)
    new.remove(new[3])
    new.insert(3, tp)
    new.remove(new[5])
    new.insert(5, nod)
    new.remove(new[7])
    new.insert(7, sname)
    
    body = listToString(new)
    SendMail(sub, body)
    
    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d1
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "ManagerName": rname, "TimePeriod": tp, "Numberofdays": nod, "Sender": sname}])
    '''
    return  '''<h1>Mail Body: {}</h1>'''.format(body)

#Resignation
@app.route('/Resignation/', methods=['POST'])
def Resignation():
    req_data = request.get_json()
    
    string = "Subject: Re: Resignation MailDear  (Manager's Name)  , \n Please accept this as formal notification of resigning from my position as  (Mention Designation)  with  (Mention Company Name)  . \n I enjoyed working under you and have learnt a lot, which will definitely help me in my career ahead. \n This was not an easy decision on my part, however, I have considered this option as the new opportunity provides better prospects of learning and growth. \n I wish you and  (Mention Company name/Team)  all the best. I do hope our paths cross again in the future.\n Regards,"
    new = Convert(string)
    
    sub = "Resignation Mail"
    mname = req_data['mname']
    des = req_data['des']
    comp = req_data['comp']
    
    new.remove(new[1])
    new.insert(1,mname)
    new.remove(new[3])
    new.insert(3,des)
    new.remove(new[5])
    new.insert(5,comp)
    new.remove(new[7])
    new.insert(7,comp)
    
    body = listToString(new)
    SendMail(sub, body)

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d1
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "ManagerName": rname, "TimePeriod": tp, "Numberofdays": nod, "Sender": sname}])
    '''
    return  '''<h1>Mail Body: {}</h1>'''.format(body)


#Farewell
@app.route('/Farewell/', methods=['POST'])
def Farewell():
    req_data = request.get_json()
    
    string = "Hello Everyone, \n I would like to take this moment and inform you that today is my last day at  (mention comapany name)  and I wanted to take a moment to let you know how grateful I am to have had the opportunity to work with all of you.\n Though I never expected my stint to be short, I has an enriching experience and learnings I have got during my tenure here. These learnings will always hold me in good stead - both professionally & personally. I have made some life- long friends at  (mention comapany name)  , with whom I connected beyond work. I am sure that our friendship will endure forever. \n  While I am excited about what lies ahead of me, leaving behind such an amazing people is definitely bittersweet. \n  I also wish to thank the maagement for giving me the opportunity to learn, grow and become part of this organization. \n Since it is a small world and as I move on, I am sure that our paths will cross again. Till then you can reach me at  (+91XXXXXXXXXX)  and  (mention personal email address)  \nLinkedin:  (pasteprofile link here)  \n  Thank you all for the support and help. Keep rocking! Cheers!!!  \n Warm Regards,"
    new = Convert(string)
    
    sub = "Farewell/Last Working Day mail"
    comp = req_data['comp']
    email = req_data['email']
    lkd = req_data['lkd']
    con = req_data['con']
    
    new.remove(new[1])
    new.insert(1,comp)
    new.remove(new[3])
    new.insert(3,comp)
    new.remove(new[7])
    new.insert(7,con)
    new.remove(new[9])
    new.insert(9,email)
    new.remove((new[11]))
    new.insert(11,lkd)
    
    body = listToString(new)
    SendMail(sub, body)

    '''db logic
    client = MongoClient("localhost", 27017)
    db = client.d1
    col = db.dataemail
    db.dataemail.insert_many([{"subject": sub, "ManagerName": rname, "TimePeriod": tp, "Numberofdays": nod, "Sender": sname}])
    '''
    return  '''<h1>Mail Body: {}</h1>'''.format(body)

@app.route('/Reminder/', methods=['POST'])
def Reminder():
    req_data = request.get_json()
    
    msg = req_data['msg']
    tm = req_data['tm']        
    #str to int()
    n = int(tm)
    n = n * 60
    
    time.sleep(n) #sleep
    
    #notification
    toaster = ToastNotifier()
    toaster.show_toast("Notification",
                msg,
                icon_path="custom.ico",
                duration=5)
    return  '''<h1>Message: {}</h1>'''.format(msg)

app.run()