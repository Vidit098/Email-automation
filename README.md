# Email-automation
Automatically genrate different emails after passing required information.There are various kind of email in this project like sick leave , follow up letter etc. and to send that email user donot have to write full email else he have to pass just the required information as asked in the code and rest the body formation grammer etc is automatically done .
# Guidelines
1.	Install tensflow from github link:- https://github.com/bendichter/tenseflow
2.	Python 2.7 or 3.6 is mandatory
3.	To install tenseflow in command Prompt (windows)
  
    •	Need git+ in windows
  
    •	Then command(git+ pip install:- https://github.com/bendichter/tenseflow@master)
 
    •	 Pip install spacy
  
    •	python -m spacy download en_core_web_sm
  
    •	then import rest of the packages written in _init_.py which includes:-
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
    
  
  4.Then run the _init_.py file 
