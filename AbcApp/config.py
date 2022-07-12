CONFIG_DICT = {
    "wow_call": r"You[.]*helped me a lot|Thanks for[.]*Help|I am very happy|Thank you so much|You have helped me a lot|I am very happy|I am very happy|Thank you so much",
    "opening": r"Thank you for calling Aditya Birla Health Insurance, how may I assist you today|May I have your name and folio number to assist you|May I have your name and folio number to assist you.",
    "active_listening": r"As I have understood your concern is|Please correct me if I am wrong but your issue is",
    "interruption": r"Sorry to interrupt you in between",
    "acknowledgement": r"definitely help|rest assured|I will definitely help you with your concern|Surely/ definitely will help you with With the details/Please be rest assured|Thank you for calling have a great/Nice day ahead|Thank you for calling in Aditya Birla mutual Fund| have a great/nice day ahead",
    "verbal_handshake": r"would like to inform my name is|your full name",
    "empathy": r"I understand how you must be feeling|I am very sorry to hear that|I am sad to hear you had to go through such troubles|I understand your concern completely|Be rest assured| I will definitely help you| I can understand your concern|Be rest assured|I will definitely help you",
    "apology": r"sorry|apologize|regret[a-z\s]*inconvenience|Really sorry for the inconvenence caused to you|I am very sorry|I apologize",
    "probing": r"please tell me|when did|what did",
    "hold_procedure": r"please.*call.*hold|May I please put your call on hold|Thank you for being online|May I place your call on hold|Thanks you for being on hold",
    "alternative_offered": r"We are now on digital platforms like whatspp, portal & chatbot, have sent an SMS on your registered mobile number, please follow the instructions and activate the services",
    "retention_offered": r"continue|do not cancel|emergency this policy|beneficial|best in the market",
    "additional_assistance": r"any other concern|anything else|Is there anything else I can help you with|Is there any other concern I can assist you with",
    "call_closing": r"Thank[\s]*you for calling in Aditya birla Health insurance. Be safe and healthy|Thank[\s]*you for calling in Aditya birla Helath insurance, have a great day ahead",
    "data_enrichment": r"update any alternative number|update any alternative email id",
    "verification": r"verification is completed|thanks for.*verification|For verification purpose, may I know|Thanks you for verifying your detals|Thank you for verification|",
    "escalation": r"IRDAI|Social Media|CEO|File a case|Police|Consumer Court|I will complain to SEBI or higher authorities|I will post on Social Media|Write to CEO|File a case|Police complain against you|Consumer court",
    "health_intent": r"engage|yoga|gym|walk"
}

AGENT_CONFIG_DICT_NEW = {
    "opening": r"Good|Thank|mutual fund|Help or assist",
    "call_closing": r"Thank|Calling|good daydhanyawad|call karne ke liye|shbh",
    "acknowledgement": r"Acknowledge|Understand|definitely|help|rest assured|sahayata|nischint",
    "apology": r"Sorry|incovenience|apologize|maafi|regret|kshama",
    "empathy": r"Acknowledge|Understand concern|definitely|help|rest assured|feel pain|very sorry|sad to hear|sad to know|dukh hua|samasya samaj sakta",
    "interruption": r"Sorry|Interrupt|kshama|mangi",
    "hold_procedure": r"hold|thank",
    "personalisation": r"sir|madam|mr|mrs",
    "pinching_self_care": r"Whatsapp|Chatbot|voicebot|google assistant|Whatsapp|Chatbot|voicebot|google assistant|",
    "further_assistance": r"Anything else|any other concern|address your concern|any other help|any other Assistance|aur koi sahayata|Anything else|any other concern|address your concern|any other help|any other Assistance|aur koi sahayata|Assistance|Further Assistance",
    "data_enrichment": r"update mobile number|update nominee|Not updated|Update",
    "lead_promotion": r"want to invest more |wish to invest more",
    "verification": r"verification|may I know|Thank",
    "escalation_process": r"SEBI|Socila Median|Speak to manager|Ombudsman|Complaints|Police|Consumer|Forum|Court|Sue|FIR|Escalate|CEO|supervisor|seniors|transfer the call|frustrated",
    "patience": r"Please|may i|kindly|rest assured|really sorry",
    "wow_call": r"very happy|thank you so much|bahut accha |bahut badiya|helped a lot"
}

CUSTOMER_CONFIG_DICT = {
    "escalation": r"|Connect me to supervisor/Speak with your supervisor|Connect to Manager|Social Media post|Complain in consumer forum|Escalate to CEO , mail to CEO/COO|You people behave badly|Customer care do not respond|Complain to manager|Fed up|Pathetic|Awful|Worst Service|Escalate|Legal Action|connect to Senior Management|Poor Service|SEBI|SEBI|AMFI|Refund|Useless|Compensation|Shameful|Grievances|Weird|Lethargic|Not satisfied|Lazy|Irate|Irritated|Frustrated|Annoyed|Ashamed|Court|Litigation|Fraud|forgery|Misspelling|Discrepancy|Disappointed|Poor performance|Social Media|Compensation|Immediate|Discrepancy|Reminder|Complaint|Mis-behave|Mis-sell|Incorrect information|Assault|Abuse|Threaten|Mis-communication|Harassed|Harassment",
}

AGENT_CONFIG_DICT_NEW_HINDI = {
    "opening": r"थैंक यू फॉर कॉलिंग|असिस्ट यू कॉल करने के लिए धयानवाद|मैं आपकी किस प्रकार सहायता कर सकता",
    "call_closing": r"धन्यवाद|आपका दिन शुभ रहे|कॉल करने के लिए धन्यवाद|थैंक यू",
    "acknowledgement": r"जी सर|जी माम्|जी मैडम|हाँ जी|नोट डाउन कर लीजिए|हाँ बताइए",
    "apology": r"माफ़ी चाहूंगा मैं इसके लिए|माफ़ी चाहेंगे|असुविधा हुई|लम्बे होल्ड के लिए माफ़ी चाहेंगे",
    "empathy": r"हाँ जी बिलकुल|िश्चिन्त रहिये|बिलकुल निश्चिंत रहेगा|हाँ|बताइए|प्लीज़|जी सर|माफ़ी चाहूंगा|हो जाएगा|क्या मुझे बताएंगे|कृपया बताएं|आपको प्रॉब्लम नहीं होगी|लम्बे होल्ड के लिए माफ़ी चाहेंगे",
    "interruption": r"माफ़ी चाहूंगा|जस्ट ए मोमेंट|एक बार रिपीट|थोड़ा समय दीजिए|बाधित करने के लिए खेद है",
    "hold_procedure": r"कॉल होल्ड पे रख सकता हूँ|लाइन पे बने रहिए|धन्यवादहोल्ड|लाइन पे रहिएगा|धन्यवाद",
    "personalisation": r"मिस्टर|श्री|मिस|सर|मैडम|्रीमती",
    "pinching_self_care": r"वेबसाइट पे|व्हाट्सएप|पोर्टल,चैटबॉट",
    "further_assistance": r"इसके अलावा और कोई सहायता|और कोई जानकारी|और कोई हेल्प",
    "data_enrichment": r"कोई अल्टेरनाते नंबर या ईमेल आई डी अपडेट",
    "lead_promotion": r"और इन्वेस्ट करना चाहेंगे|सेल्स टीम से कॉल बैक र्करवा दू",
    "verification": r"जान सकता हूँ|वेरिफिकेशन के लिए धन्यवाद",
    "escalation_process": r"एग्ज़िक्यटिव के साथ कनेक्ट|मैनेजर से कनेक्ट|सोशल मीडिया पोस्ट|सुपरवाइजर से बात|मैनेजर से बात|सीईओ एस्केलेट|उपभोक्ता फोरम में शिकायत|एग्ज़िक्यटिव से बात|बार बार फ़ोन करना|सेल्स के बंदे बदतमीजी से बात करते है|कस्टमर केयर वाले जवाब नहीं देते",
    "patience": r"कृपया|सहृदय निवेदन|वास्तव में खेद|क्या मैं|निश्चित",
    "wow_call": r"बहुत बहुत धन्यवाद|बहुत बहुत शुक्रिया|बहुत अच्छा लगा "

}

CUSTOMER_CONFIG_DICT_HINDI = {
    "escalation": "एग्जिक्यूटिव के साथ कनेक्ट|एग्ज़िक्यटिव के साथ कनेक्ट , सुपरवाइजर से बात, एग्ज़िक्यटिव से बात|मैनेजर से कनेक्ट , मैनेजर से बात|सोशल मीडिया पोस्ट|उपभोक्ता फोरम में शिकायत|सीईओ मेल|बार बार फ़ोन|बदतमीजी से बात|कस्टमर केयर वाले जवाब नहीं देते|मैनेजर से शिकायत करना|अप्रसन्न ,असंतुष्ट|सबसे खराब सेवा|सेबी|सेबी की शिकायत|एम्फी शिकायत|खराब|मुआवज़ा|शिकायत|एम्फी  + कोम्प्लैण्ट|फ्रोड|रेमाएण्डर|मिस्-बेहवे||मिस्-सेल्ल|वरिष्ठ अधिकारी से बात करवा दे|कॉल ट्रांसफर करे|परेशां ",
}

FATALITY_MAPPING = {
    "opening": "non_fatal",
    "call_closing": "non_fatal",
    "acknowledgement": "non_fatal",
    "apology": "non_fatal",
    "empathy": "non_fatal",
    "interruption": "non_fatal",
    "hold_procedure": "non_fatal",
    "personalisation": "non_fatal",
    "pinching_self_care": "non_fatal",
    "further_assistance": "non_fatal",
    "data_enrichment": "non_fatal",
    "lead_promotion": "non_fatal",
    "verification": "fatal",
    "escalation_process": "fatal",
    "patience": "fatal",
    "wow_call": "non_fatal"

}

SCORE_MAPPING_NEW = {
    "opening": 2,
    "call_closing": 2,
    "acknowledgement": 2,
    "apology": 2,
    "empathy": 2,
    "interruption": 2,
    "hold_procedure": 2,
    "personalisation": 2,
    "pinching_self_care": 2,
    "further_assistance": 2,
    "data_enrichment": 4,
    "lead_promotion": 4,
    "verification": 5,
    "escalation_process": 5,
    "patience": 5,
    "wow_call": 5

}
