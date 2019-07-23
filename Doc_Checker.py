#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
from datefinder import find_dates
import re
import jellyfish

##########################################################################################
#Inputs
##########################################################################################

#name of the json file
json_file = "test.json"
#place number of the certificate in the json file
row_nb = 1
#name of the txt file
txt_file = "test2"

#------------------------------------------------------------------------------------------
#Read the JSON file
#------------------------------------------------------------------------------------------

def json_reader(filename,row_nb):
    f=open(filename, 'r')
    json_data = json.load(f)
        
    # show data
    df=pd.DataFrame(json_data) 
    #print(df)
    list_var=[]
    list_str  = ['stateofregistrycode', 'Registration', 'Owner', 'DateOfRegistry', 'Serial','makemodel', 'YearOfBuild']
    for stri in list_str:
        list_var.append((df[stri][row_nb]))
    return  list_var


def find_date(filename):
    with open (filename, 'r') as myfile:  
        data = myfile.read()
    myfile.close()
    
    dates = find_dates(data)
    result = []
    for match in dates:
        temp=str(str(match)[:10])
        result.append(temp)
    return result

#------------------------------------------------------------------------------------------
#Compare the information between two files
#------------------------------------------------------------------------------------------
    
def comparison(filename_txt,json_data,debug):
    #-----txt---------------------------------------
    with open(filename_txt+'.txt', 'r') as myfile:
        data_txt = myfile.read().upper().replace("\n", " ")
        
    if (debug):
        print(data_txt)
    data_txt=''.join(re.findall("[A-Z0-9]",data_txt))
    if (debug):
        print(data_txt)
    date_txt = find_date(filename_txt+'.txt')
    if debug:
        print('text date',date_txt)
    allout=[]
    if debug:
        print('json_data',json_data)
        
    #-----json--------------------------------------
    for text in json_data:
        
        #state # can create a dictionary: state - > state code
        date_json = json_data[3] #'DateOfRegistry'
        if text == "USA":
            text = "UNITEDSTATESOFAMERICA"
            
        #makemodel
        if text == json_data[5]:
            list_model = [] # list of words descriping the model
            # temporal str
            textmodel = "" 
            for place in range(len(text)):
                if text[place] != " ":
                    textmodel += text[place]
                else :
                    list_model.append(textmodel)
                    textmodel = ""
            list_model.append(textmodel)
            if debug:
                print('list_model1',list_model)
            for word in list_model:
                if word[0] == "(" and word[-1] == ")":
                    list_model.remove(word)
                    temp_word=word[1:-1]
                    list_model.append(temp_word)
            if debug:
                print('list_model2',list_model)
                         
        #Remove all spaces, commas and other non numerical or ascii characters from the data and the search word
        newtext=''.join(re.findall("[A-Z0-9]",text.upper()))
        
        if (debug):
            print('newtext(upper,npspace)',newtext)
             
        arr=[]
        
        #Create a window of the size of the seach word and slide it over the text file
        #Calculate the levenshtein distance between the window and the search text

        for i in range(0,len(data_txt)-len(newtext)):
            window=data_txt[i:i+len(newtext)]
            d=jellyfish.levenshtein_distance(newtext, window)
            d2=jellyfish.hamming_distance(newtext, window)
            d3=jellyfish.jaro_winkler(newtext, window)
            arr.append([window,d,d2,d3])

        #Search which window has the smallest distance
        p=pd.DataFrame(arr,columns=["word","lev","hamming","jarowinkler"])
        m=p["jarowinkler"].idxmax()
        #Output that window and the match is the proportion of the matched window
        out=[p.iloc[m,0],100*p.iloc[m,3]]

        if (debug):
            print(p)
            print(p.xiloc[m])
        
        #date of registry
        if text == json_data[3]:
            if date_json in date_txt:
                out=[date_json,100]
                
        #yearofbuilt
        if text == json_data[-1]:
            if out[1] < 100:
                out[1] = 0.0
        out.insert(0,newtext)
        allout.append(out)

    #Calculate an overall score with the average of the provided text
    out=[allout,pd.DataFrame(allout).loc[:,2].mean()]
    return out


#------------------------------------------------------------------------------------------
#Display the necessary information
#------------------------------------------------------------------------------------------

def result_display(result):
    list_info = ['state of registry code', 'registration number', 'owner', 'date of registry', 'serial number','makemodel', 'year of build']
    for info in range(len(result[0])):
        if result[0][info][2] < 90:
            print("You should verify the {}.".format(list_info[info]))
    if result[1] > 90 :
        print("It seems to be the right certificate.")

##########################################################################################
#Outputs
##########################################################################################

jsondata=json_reader(json_file,row_nb)
result=comparison(txt_file,jsondata,0)
print(result)
result_display(result)

