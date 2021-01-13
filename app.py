from flask import Flask, request, session, redirect, url_for
from markupsafe import escape
import random
import requests
from flask import render_template
import json
from fuzzywuzzy import fuzz
import pandas as pd
from PyDictionary import PyDictionary 

app=Flask(__name__)






@app.route('/')
def root():
    return "test"

def get_search_tuple(search_word,file_location):
    df=pd.read_csv(file_location)
    aya=[]
    count_matches=0
    for index,row in df.iterrows():
        sim = fuzz.token_set_ratio(search_word,row["AyahText"])
        if sim >=95:
            trans_string=row["AyahText"]
            trans_string=trans_string.replace("&quot;","'")
            touble=(row["SuraID"],row["VerseID"],trans_string)
            aya.append(touble)
            count_matches+=1
            if count_matches>=3:
                break
    return aya

def get_similar_all_syns(word,file_location):
    dictionary=PyDictionary()
    
    le=dictionary.synonym(word)
    
    if len(le)>5:
        le=le[0:5]
    le.append(word)
    result_dict={}
    for i in range(len(le)):

        
        list_tuples=get_search_tuple(le[i],file_location)
        if len(list_tuples)!=0:
            result_dict[le[i]]=list_tuples
        else:
            continue
    return result_dict
        


@app.route('/search/<word>')
def search_word(word):
    file_location="data/English-Ahmed-Ali-100.csv"
    big_dict=get_similar_all_syns(word,file_location)
    print(big_dict)
    for word in big_dict:
        print(word)
    #return("number of synonyms = "+str(len(big_dict.keys())))
    return render_template("result.html",data=big_dict)



if __name__ == '__main__':

    app.run(host="0.0.0.0",debug=True)
    
