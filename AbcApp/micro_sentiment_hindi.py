import requests
import json
import os
import re
import requests
import json
import io
import sys
import django

sys.path.append("/".join(os.getcwd().replace("\\", "/").split("/")[0:-1]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ABC.settings'
django.setup()

from ABC.settings import BASE_DIR
from AbcApp.models import Analytic, CurrentProcessLog

# subscription_key = "e6e4681d17f748158e8cbd4325b8e161"
# #endpoint = "https://mlaitextanalyticsabc1.cognitiveservices.azure.com/"
# sentiment_url = "https://mlaitextanalyticsabc1.cognitiveservices.azure.com/text/analytics/v3.1/sentiment"


subscription_key = "de04944118374e3fa9b24decb41c8d95"
sentiment_url = "https://sentimenttextmlaianalyticsnew.cognitiveservices.azure.com/text/analytics/v3.0/sentiment"

def agent_find(txt_file_name):
    # path = os.path.join(BASE_DIR, "aditya_sentiment/transcript/")
    # print("file name ", file_name)
    # file_name = file_name.split('.json')[0] + '.txt'
    p = re.compile(r"हैल्थ इंश्योरैंस यू अर टॉकिंग|नाम जान सकता हूँ|नाम जान सकति हूँ|नाम जान सक्ती हूँ"
                   r"|ठीक है, थैंक यू फॉर कालिंग, आदित्य बिड़ला हेल्थ इन्सुरेंस|ओके सर, थैंक यू फॉर कॉलिंग आदित्य बिड़ला हेल्थ इन्शुरन्स"
                   r"|लाइन पे, है ना|1 मिनट लाइन पे बने रहिए",
                   # r"|Cyour phone number and your name|may I know you|may I know.|can.*hold|may.*hold"
                   # r"|you calling from your registered contact number|Thank you for calling.*insurance."
                   # r"|Thank you for calling Aditya Birla health insurance.|Thank you for calling"
                   # r"|welcome to|thank you for calling|Thank you for contacting|Aditya Birla health insurance."
                   # r"|How may I help you with your Aditya Birla health insurance?|Welcome to Aditya Birla health insurance."
                   # r"|How may I help you|put your call on hold.|just be on hold.|put your call on hold|May I place your call on hold"
                   # r"|Can I put your call on hold|may I place your call on hold?|Can I please call for the hold for a minute?"
                   # r"|May I put the call on hold for|Please be on line|thank you.*calling",
                   re.IGNORECASE)

    with open(txt_file_name, "r", encoding="utf8") as file:
        sentences = file.readlines()
        flag = 1
        n = len(sentences)
        a = "S1"
        b = "S2"
        for i in range(n):
            z = sentences[i].split(" : ")[1] if (len(sentences[i]) > 5) else 0
            s = sentences[i].split(" : ")[0]
            if (z and p.search(z)):
                # print(escalation.search(z))
                flag = 0
                if s == a:
                    return b
                else:
                    return a
                break
        if (flag == 1):
            return 0


def read_file(txt_file_name, language):
    sentences = []
    with open(txt_file_name, "r", encoding="utf8") as file:
        sentences = file.readlines()
    cleaned_sent = []
    i = 1
    for sent in sentences:
        # print(sent)
        if len(sent) > 5:
            cleaned_text = re.split(": ", sent)
            speaker = cleaned_text[0].strip()
            text = cleaned_text[1]
            text = text.rstrip("\n")

            cleaned_sent.append({"id": "{}".format(i), "language": language, "speaker": speaker, "text": text})
            i += 1

    return cleaned_sent


def inferencing(json_filename_with_full_path, txt_filename_with_full_path, language):
    customer = agent_find(txt_filename_with_full_path)
    agent = None
    if customer == "S2":
        agent = "S1"
    elif customer == "S1":
        agent = "S2"

    with open(txt_filename_with_full_path.split(".")[0] + "_customer.txt", "w+") as file:
        file.write("customer={0}\n".format(customer))
        file.write("agent={0}".format(agent))
    json_doc = {'document': []}
    cleaned_sentences = read_file(txt_filename_with_full_path, language)
    documents = {"documents": cleaned_sentences}
    a = len(documents["documents"])
    if (a > 10):
        n = a // 10
        r = a % 10
        j = 0
        for i in cleaned_sentences:
            # print(documents["documents"][(j*10): (j*10)+10])
            doc = {"documents": documents["documents"][(j * 10): (j * 10) + 10]}
            headers = {"Ocp-Apim-Subscription-Key": subscription_key}
            response = requests.post(sentiment_url, headers=headers, json=doc)
            sentiments = response.json()
            # print(sentiments)
            start = j * 10
            end = (j * 10) + 10
            for k in range(start, end):
                try:
                    sentiments['documents'][k % 10].update({"speaker": documents['documents'][k]['speaker']})
                except:
                    pass
                # print(sentiments)

            json_doc['document'].extend(sentiments['documents'])

            j += 1
            if (j == n):
                break

        if (r != 0):
            doc = {"documents": documents["documents"][(j) * 10: (j * 10) + r]}
            headers = {"Ocp-Apim-Subscription-Key": subscription_key}
            response = requests.post(sentiment_url, headers=headers, json=doc)
            sentiments = response.json()
            start = j * 10
            end = (j * 10) + r
            for k in range(start, end):
                sentiments['documents'][k % 10].update({"speaker": documents['documents'][k]['speaker']})
            json_doc['document'].extend(sentiments['documents'])

    else:
        doc = {"documents": documents["documents"][0:a]}
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        response = requests.post(sentiment_url, headers=headers, json=doc)
        sentiments = response.json()
        start = 0
        end = a
        for k in range(start, end):
            sentiments['documents'][k % 10].update({"speaker": documents['documents'][k]['speaker']})
        json_doc['document'].extend(sentiments['documents'])

    results = {}
    result = []
    for i in json_doc['document']:
        result_dict = {}
        if i['speaker'] == customer:
            result_dict['Prediction'] = i['sentiment'].upper()
            result_dict['Speaker'] = i['speaker']
            t = ""
            for j in i['sentences']:
                t += j['text']
                t += " "
            result_dict['Text'] = t
            result.append(result_dict)
        else:
            result_dict['Prediction'] = ""
            result_dict['Speaker'] = i["speaker"]
            t = ""
            for j in i['sentences']:
                t += j['text']
                t += " "
            result_dict['Text'] = t.strip()
            result.append(result_dict)
    results['sentiment_results'] = result
    json_filename_with_full_path = json_filename_with_full_path.split(".")[0] + "_" + "interfencing.json"
    with io.open(json_filename_with_full_path, 'w', encoding='utf8') as file:
        json_string = json.dumps(results, ensure_ascii=False, indent=4)
        file.write(json_string)
    return customer


def count(json_filename_with_full_path, txt_filename_with_full_path):
    json_filename_with_full_path = json_filename_with_full_path.split(".")[0] + "_" + "interfencing.json"
    name = open(json_filename_with_full_path, "r", encoding="utf8")
    data = json.load(name)

    S1 = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    S2 = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    for i in data["sentiment_results"]:
        if i['Prediction'] != '' and i['Prediction'] != "MIXED":
            if i["Speaker"] == 'S1':
                S1[i["Prediction"]] += 1
            else:
                S2[i["Prediction"]] += 1

    agent_name = agent_find(txt_filename_with_full_path)
    count_values = None
    flag = 0
    if agent_name == "S1":
        flag = 1
        count_values = {"Customer": S2, "Agent": S1}
    else:
        count_values = {"Customer": S1, "Agent": S2}

    txt_filename_with_full_path_count = txt_filename_with_full_path.split(".")[0] + "_" + "count.txt"
    with open(txt_filename_with_full_path_count, 'w+') as file:
        for line in count_values:
            # write line to output file
            file.write(str(line))
            file.write("\n")
            a = None
            if flag == 0:
                a = S1
            else:
                a = S2
            for i in a:
                flag = 1
                file.write(str(i))
                file.write(" : ")
                file.write(str(a[i]))
                file.write("\n")
            file.write("=========================")
            file.write("\n")

# def sentiment_txt_to_dict(txt_filename_with_full_path):
#     res_dict = {'Agent': {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0},
#                 'Customer': {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}}
#     with open(txt_filename_with_full_path, "r", encoding="utf-8") as curr_file:
#         text = curr_file.readlines()
#     sentiment_list = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
#     c = 1
#     for x in sentiment_list:
#         res_dict['Customer'][x] = text[c].split(":")[1][:-1]
#         c += 1
#     c = 6
#     for x in sentiment_list:
#         res_dict['Agent'][x] = text[c].split(":")[1][:-1]
#         c += 1
#     return res_dict
