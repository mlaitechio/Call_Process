# import os,json

# from requests.api import request

# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# request_id = "1622758434405"
# txt_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".txt"
# json_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".json"

# with open(txt_filename_with_full_path.split(".")[0] + "_" + "customer.txt", "r", encoding="utf8") as file:
#     result = file.readlines()
#     customer_agent = "".join(result)

# for x in result:
#     if "customer" in x:
#         customer = x.split("=")[-1].strip()

# print(customer)

# name = open(json_filename_with_full_path.split(".")[0] + "_" + "interfencing.json", "r",
#             encoding="utf8")
# data = json.load(name)
# for row in data['sentiment_results']:
#     if(row['Speaker'] == customer):
#         speaker = "Customer"
#     else:
#         speaker = "Agent"
#     print(f"{speaker} : {row['Text']}")

# print(result)
# print(customer_agent)

#####################################################################################
# def pretty(d, indent=0):
#    for key, value in d.items():
#       print('\t' * indent + str(key))
#       if isinstance(value, dict):
#          pretty(value, indent+1)
#       else:
#          print('\t' * (indent+1) + str(value))
# dic = {'final_colour': 'Yellow', 'final_score': '15/27', 'score_details': [{'speech_class': 'wow_call', 'score': 10, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'opening', 'score': 2, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'active_listening', 'score': 4, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'interruption', 'score': 4, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'acknowledgement', 'score': 4, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'verbal_handshake', 'score': 2, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'empathy', 'score': 2, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'apology', 'score': 2, 'found': 1.0, 'final_score': 2.0}, {'speech_class': 'probing', 'score': 8, 'found': 1.0, 'final_score': 8.0}, {'speech_class': 'hold_procedure', 'score': 3, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'alternative_offered', 'score': 2, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'retention_offered', 'score': 2, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'additional_assistance', 'score': 2, 'found': 1.0, 'final_score': 2.0}, {'speech_class': 'call_closing', 'score': 2, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'data_enrichment', 'score': 4, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'verification', 'score': 5, 'found': 1.0, 'final_score': 5.0}, {'speech_class': 'escalation', 'score': 5, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'professionalism', 'score': 5, 'found': 0.0, 'final_score': 0.0}, {'speech_class': 'health_intent', 'score': 2, 'found': 0.0, 'final_score': 0.0}]}
# print(pretty(dic))

######################################################################################
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# request_id = "1625025697432"
# json_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".json"
# name = open(json_filename_with_full_path.split(".")[0] + "_" + "interfencing.json", "r",
#             encoding="utf8")
# results = json.load(name)
# for each_sentiment in results['sentiment_results']:
#    if each_sentiment['Text'].replace(" ","").replace(".","").lower().strip() == "okay":
#       each_sentiment['Prediction'] = "NEUTRAL"
# print(results)

######################################################################################
# final_json = {}
# final_json["qa"] = {}
# final_json["qa"]["score"] = 20

# print(final_json)

#######################################################################################
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# request_id = "speaker_demo2"
# txt_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".txt"
# with open(txt_filename_with_full_path, "r", encoding="utf8") as file:
#     result = file.readlines()
# new_result=[]
# for res in result:
#     res = res.replace("S3","S2")
#     res = res.replace("S4","S2")
#     new_result.append(res)
# print(new_result)
# with open(txt_filename_with_full_path, "w+") as file:
#     for res in new_result:
#         file.write(res)
#######################################################################################

a = "पुलिस"
print(a == "पलिस")