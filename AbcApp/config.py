CONFIG_DICT = {
    "wow_call": r"You[.]*helped me a lot|Thanks for[.]*Help|I am very happy|Thank you so much",
    "opening": r"Thank you for calling Aditya Birla Health Insurance, how may I assist you today",
    "active_listening": r"As I have understood your concern is|Please correct me if I am wrong but your issue is",
    "interruption": r"Sorry to interrupt you in between",
    "acknowledgement": r"definitely help|rest assured",
    "verbal_handshake": r"would like to inform my name is|your full name",
    "empathy": r"I understand how you must be feeling|I am very sorry to hear that|I am sad to hear you had to go through such troubles",
    "apology": r"sorry|apologize|regret[a-z\s]*inconvenience",
    "probing": r"please tell me|when did|what did",
    "hold_procedure": r"please.*call.*hold",
    "alternative_offered": r"We are now on digital platforms like whatspp, portal & chatbot, have sent an SMS on your registered mobile number, please follow the instructions and activate the services",
    "retention_offered": r"continue|do not cancel|emergency this policy|beneficial|best in the market",
    "additional_assistance": r"any other concern|anything else",
    "call_closing": r"Thank[\s]*you for calling in Aditya birla Health insurance. Be safe and healthy|Thank[\s]*you for calling in Aditya birla Helath insurance, have a great day ahead",
    "data_enrichment": r"update any alternative number|update any alternative email id",
    "verification": r"verification is completed|thanks for.*verification",
    "escalation": r"IRDAI|Social Media|CEO|File a case|Police|Consumer Court",
    "health_intent": r"engage|yoga|gym|walk"
}

AGENT_CONFIG_DICT_NEW = {
    "wow_call": r"happy|very happy|thank|thanks|thank you[\sso much]*|bahut[\sacha]*[\sbadiya]*",
    "opening": r"(thank|welcome|dhanyawad).*?(help|assist|call|contacting|sahayata)",
    "active_listening": r"[i\s]*understood|understand|acknowledge|definitely[\shelp]*|correct me|samja|samaj sakta|jaroor|rest assured|sahayata|nishchint|yeah|no problem|right|surely|sure|right",
    "interruption": r"(sorry|kshama).*?(interrupt|mang)",
    "acknowledgement": r"acknowledge|understand|definitely help|rest assured|sahayata|nischint|yeah|right|sure|surely",
    "verbal_handshake": r"i am|my name[\sis]*|mera naam|main|aapka naam|your name",
    "empathy": r"acknowledge|understand|definitely help|rest assured|very sorry|sad to hear|sad to know|dukh hua|samaj sakta|feel pain|no problem|sorry|may i|right|help|sure|surely",
    "apology": r"sorry|apologize|regret[a-z\s]*inconvenience|kshama",
    "probing": r"please tell me|when|what|how|where|why|can i|may i",
    "hold_procedure": r"please.*call.*hold|line.*hold.*pe|sorry.*hold|call.*hold",
    "alternative_offered": r"digital[\splatform]*|whatspp|chatbot|SMS|please follow the instructions",
    "retention_offered": r"continue policy|do not cancel|beneficial|continue plan|best plan|comprehensive plan|unique benefits|additional features|additonal advantages|best in market|better than market|free coverage",
    "additional_assistance": r"Anything else|any other concern|address your concern|any other help|any other assistance|aur[\skoi]*sahayata",
    "call_closing": r"(thank you|thanks|dhanyawad).*?(calling|call|call krne ke liye).*?(good|great|be safe|nice day|subh din)",
    "data_enrichment": r"update|alternate|alternative",
    "verification": r"(unregistered number).*?(verify|verification)|thank.*verification",
    "health_intent": r"engage|yoga|gym|walk|\bfit|health|swimming|sehat"
}

CUSTOMER_CONFIG_DICT = {
    "escalation": r"|Social Media|Connect me to supervisor/Speak with your supervisor|Connect to Manager|Social Media post|Complain in consumer forum|Escalate to CEO , mail to CEO/COO|Calling again & again|You people behave badly|Customer care do not respond|Complain to manager|Unhappy|Fed up|Pathetic|Awful|Worst Service|Horrible|Escalate|Legal Action|connect to Senior Management|Poor Service|SEBI|SEBI + COMPLAINT|AMFI|AMFI + COMPLAINT|Refund|Useless|Compensation|Delay|Bad|Shameful|Grievances|Weird|Shocked|Lethargic|Uncomfortable|Not satisfied|Lazy|Irate|Irritated|Frustrated|Annoyed|Ashamed|Court|Notice|Litigation|Fraud|forgery|Misspelling|Discrepancy|Disappointed|Poor performance|Social Media|Compensation|Immediate|Discrepancy|Reminder|Complaint|Mis-behave|Mis-sell|Incorrect information|Assault|Abuse|Threaten|Mis-communication|Harassed|Harassment",
}


AGENT_CONFIG_DICT_NEW_HINDI = {
    "wow_call": "बहुत बहुत धन्यवाद|बहुत बहुत शुक्रिया|बहुत अच्छा लगा",
    "opening": "थैंक यू फॉर कॉलिंग, प्लस असिस्ट यू|कॉल करने के लिए धन्यवाद, मैं आपकी किस प्रकार सहायता कर सकता",
    "active_listening": "जी मैं जान सकता हूँ|नोट डाउन कर लीजिए|सुन रहा हूँ मैं|अपडेट करदेता हूँ|राइट|हाँ जी|जैसे मैं देख पा|आप बताइए|हो जाएगा|लाइन पे रहिएगा|मैं अभी चेक करके बता|स्टेटस जानना चाहते हैं न|आपको अपडेट आ जाएगा",
    "interruption": "सॉरी|माफ़ी चाहूंगा|जस्ट मूवमेंट|एक बार रिपीट|थोड़ा समय दीजिए|बाधित करने के लिए खेद है",
    "acknowledgement": "जी सर|जी में|जी मैडम|हाँ जी|नोट डाउन कर लीजिए|माफी चाहूंगा। मैं इसके लिए|अपडेट कर देता हूँ|ठीक है|हाँ बताइए|ठीक है|चेक करके बता|जैसे कि मैं देख पा|लाइन पे रहिएगा|स्टेटस जानना चाहते है ना|हाँ जी बिलकुल|निश्चिंत रहिए",
    "verbal_handshake": "मेरा नाम|आपका नाम|जी सर|जी मैडम|थैंक यू",
    "empathy": "बिलकुल निश्चिंत रहिए गा|जी सर माफी चाहूंगा मैं|हाँ बताइए प्लीज़|माफ़ी चाहेंगे|असुविधा हुई|हो जाएगा",
    "apology": "माफी चाहूंगा|माफ़ी चाहेंगे असुविधा हुई",
    "probing": "रजिस्टर नंबर बता दो प्लीज्|पॉलिसी नंबर बता दीजिए?|अड्रेस बता दीजिए|मुझे बताएंगे|कब कहाँ कैसे|कृप्या बताएं",
    "hold_procedure": " 2 मिनट के लिए कॉल होल्ड पे रख सकता हूँ|लाइन पे बने रहिए|लाइन पे रहिएगा",
    "alternative_offered": "वेबसाइट पे एक्टिव अप व्हाट्सएप होटल, चैटबॉट",
    "retention_offered": "जैसे आपको मैने कहा|आपको प्रॉब्लम नहीं होगी|बेनिफिट|सिक्योर लोन|सबसे अच्छा लोन|अक्सीडेंटल कवर|लाइफ कवर|अभी बंद करवाने का मतलब नहीं है|प्रदना करें",
    "additional_assistance": "इसके अलावा और कोई सहायता|और कोई जानकारी|और कोई हेल्प|कोई अलटरनेट फ़ोन नंबर",
    "call_closing": "बहुत धन्यवाद आपका|आपका दिन शुभ रहे|कॉल करने के लिए धन्यवाद थैंक यू",
    "data_enrichment": "अलटरनेट फ़ोन नंबर|कोई अलटरनेट नंबर या ईमेल आई डी अपडेट",
    "verification": "मैं आपका नाम जान सकता हूँ प्लस वेरिफिकेशन के लिए धन्यवाद|डेट ऑफ बर्थ प्लेस वेरिफिकेशन के लिए धन्यवाद|अड्रेस बता दीजिए, बस वेरिफिकेशन के लिए धन्यवाद|रजिस्टर्ड नंबर बता दीजिए लैरी विकेशन के लिए धन्यवाद",
    "health_intent": "फिट रखने के लिए कोई एक्सरसाइज करते हैं जैसे"
}

CUSTOMER_CONFIG_DICT_HINDI = {
    "escalation": "एग्जिक्यूटिव के साथ कनेक्ट|एग्ज़िक्यटिव के साथ कनेक्ट , सुपरवाइजर से बात, एग्ज़िक्यटिव से बात|मैनेजर से कनेक्ट , मैनेजर से बात|सोशल मीडिया पोस्ट|उपभोक्ता फोरम में शिकायत|सीईओ मेल|बार बार फ़ोन|बदतमीजी से बात|कस्टमर केयर वाले जवाब नहीं देते|मैनेजर से शिकायत करना|अप्रसन्न ,असंतुष्ट|सबसे खराब सेवा|सेबी|सेबी की शिकायत|एम्फी शिकायत|खराब|नाराज़|मुआवज़ा|शिकायत|एम्फी  + कोम्प्लैण्ट|फ्रोड|रेमाएण्डर|मिस्-बेहवे||मिस्-सेल्ल|वरिष्ठ अधिकारी से बात करवा दे|कॉल ट्रांसफर करे|परेशां ",
}

FATALITY_MAPPING = {
    "wow_call": "non_fatal",
    "opening": "non_fatal",
    "active_listening": "non_fatal",
    "interruption": "non_fatal",
    "acknowledgement": "non_fatal",
    "verbal_handshake": "non_fatal",
    "empathy": "non_fatal",
    "apology": "non_fatal",
    "probing": "non_fatal",
    "hold_procedure": "non_fatal",
    "alternative_offered": "non_fatal",
    "retention_offered": "non_fatal",
    "additional_assistance": "non_fatal",
    "call_closing": "non_fatal",
    "data_enrichment": "non_fatal",
    "verification": "fatal",
    "escalation": "fatal",
    "professionalism": "fatal",
    "health_intent": "non_fatal"
}

SCORE_MAPPING = {
    "wow_call": 10,
    "opening": 2,
    "active_listening": 4,
    "interruption": 4,
    "acknowledgement": 4,
    "verbal_handshake": 2,
    "empathy": 2,
    "apology": 2,
    "probing": 8,
    "hold_procedure": 3,
    "alternative_offered": 2,
    "retention_offered": 2,
    "additional_assistance": 2,
    "call_closing": 2,
    "data_enrichment": 4,
    "verification": 5,
    "escalation": 5,
    "professionalism": 5,
    "health_intent": 2
}