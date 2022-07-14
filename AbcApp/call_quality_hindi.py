from AbcApp import config
#import config
#import config
import pandas as pd
import re


def read_file_and_extract_agent_speech(file_path):
    """
    Function to clean transcription file into Agent and Customer Speech
    """
    clean_agent_speech_lines = []
    clean_customer_speech_lines = []

    with open(file_path, 'r') as speech_file:
        for line in speech_file.readlines():
            if line.lower().startswith("agent"):
                clean_line = "".join(line.split("=")[0]).lower().replace("agent :", "").strip()
                clean_agent_speech_lines.append(clean_line)

            if line.lower().startswith("customer"):
                clean_line = "".join(line.split("=")[0]).lower().replace("agent :", "").strip()
                clean_customer_speech_lines.append(clean_line)

    return clean_agent_speech_lines, clean_customer_speech_lines


def apply_regex_logic(clean_agent_speech_lines, clean_customer_speech_lines):
    """
    Funtion to apply regex basis speech classes
    """
    final_output_list = []
    for speech in clean_agent_speech_lines:
        fl_match_found = 0
        for speech_class, regex_patten in config.AGENT_CONFIG_DICT_NEW_HINDI.items():
            if re.search(regex_patten.lower(), speech.lower()):
                fl_match_found = 1
                if fl_match_found:
                    if fl_match_found:
                        if speech_class != "escalation_process":
                            final_output_list.append({"speech": speech, "class": speech_class,
                                                      "fatality": config.FATALITY_MAPPING[speech_class]})
                    else:
                        final_output_list.append({"speech": speech, "class": "", "fatality": ""})

        # applying regex on customer speech
    for speech in clean_customer_speech_lines:
        fl_match_found = 0
        for speech_class, regex_patten in config.CUSTOMER_CONFIG_DICT.items():
            if re.search(regex_patten.lower(), speech.lower()):
                fl_match_found = 1
                if fl_match_found:
                    if speech_class in ("escalation_process", "patience", "wow_call"):
                        final_output_list.append({"speech": speech, "class": speech_class,
                                                  "fatality": config.FATALITY_MAPPING[speech_class]})
                    else:
                        final_output_list.append({"speech": speech, "class": "", "fatality": ""})

    print(final_output_list)
    final_df = pd.DataFrame(final_output_list)
    return final_df


def create_final_score(final_df):
    counts = final_df["class"].value_counts()
    print(counts)
    score_dict = counts.to_dict()

    # # making found to always true for below speech classes
    # score_dict["professionalism"] = 1
    # score_dict["interruption"] = 1
    # score_dict["apology"] = 1

    '''comment uncomment to test'''
    # score_dict["escalation"] = 1

    print(score_dict)

    # initializing with default 5, bcz of professionalism
    fatal_score = 0
    non_fatal_score = 0
    fl_escalation_found = 0

    # for key, value in score_dict.items():
    #     if key:
    #         if config.FATALITY_MAPPING[key] == "fatal":
    #             if key == "escalation_process":
    #                 fl_escalation_found = 1
    #                 fatal_score += 0
    #
    #             else:
    #                 fatal_score += config.SCORE_MAPPING_NEW[key]
    #
    #         else:
    #             non_fatal_score += config.SCORE_MAPPING_NEW[key]

    for key, value in score_dict.items():
        if key:
            if config.FATALITY_MAPPING[key] == "fatal":
                if key == "escalation_process":
                    fl_escalation_found = 1
                    fatal_score += 0

                else:
                    fatal_score += config.SCORE_MAPPING_NEW[key]

    for key, value in score_dict.items():
        if key:
            if config.FATALITY_MAPPING[key] == "non_fatal":
                if fatal_score == 15 and key == "acknowledgement":
                    non_fatal_score += 2
                if fatal_score == 15 and key == "apology":
                    non_fatal_score += 2
                if fatal_score == 15 and key == "empathy":
                    non_fatal_score += 2
                if fatal_score == 15 and key == "interruption":
                    non_fatal_score += 2
                if fatal_score == 15 and key == "personalisation":
                    non_fatal_score += 2
                if fatal_score == 15 and key == "further_assistance":
                    non_fatal_score += 2
                if fatal_score == 15 and key == "patience":
                    non_fatal_score += 5

                else:
                    non_fatal_score += config.SCORE_MAPPING_NEW[key]

    if fl_escalation_found == 0:
        fatal_score += 5

    # making final grid
    if fatal_score < 15:
        final_score = "0/0"
    else:
        final_score = "{}/{}".format(fatal_score, fatal_score + non_fatal_score)

    if fatal_score == 15 and fatal_score + non_fatal_score > 69:
        final_colour = "Green"
    else:
        if fatal_score < 15:
            final_colour = "Red"
        elif 0 < fatal_score + non_fatal_score <= 45:
            final_colour = "Yellow"
        else:
            final_colour = "Blue"

    final_score_dict = {
        "final_colour": final_colour,
        "final_score": final_score
    }


    score_lookup = pd.DataFrame(config.SCORE_MAPPING_NEW.items(), columns=["speech_class", "score"])
    found_speech = pd.DataFrame(score_dict.items(), columns=["speech_class", "score"])

    final_df = pd.merge(score_lookup, found_speech, how="left", on="speech_class")
    final_df.fillna(0, inplace=True)
    final_df['score_y'] = final_df['score_y'].apply(lambda x: 1 if x > 1 else x)
    final_df = final_df.rename(columns={"score_x": "score", "score_y": "found"})

    final_df["final_score"] = final_df["score"] * final_df["found"]

    # adjusting escalation score
    if fl_escalation_found:
        final_df.loc[final_df["speech_class"] == "escalation_process", "final_score"] = 0
    else:
        final_df.loc[final_df["speech_class"] == "escalation", "final_score"] = config.SCORE_MAPPING_NEW[
            "escalation_process"]
    # print(final_df)
    final_score_dict["score_details"] = final_df.to_dict("records")

    for i in final_score_dict["score_details"]:

        if i["speech_class"] == "escalation_process" and i["found"] == 0.0:
            i["final_score"] = 5.0

    for i in final_score_dict["score_details"]:
        if fatal_score == 15 and i["speech_class"] == "acknowledgement":
            i["final_score"] = 2.0
        if fatal_score == 15 and i["speech_class"] == "apology":
            i["final_score"] = 2.0
        if fatal_score == 15 and i["speech_class"] == "empathy":
            i["final_score"] = 2.0
        if fatal_score == 15 and i["speech_class"] == "interruption":
            i["final_score"] = 2.0
        if fatal_score == 15 and i["speech_class"] == "personalisation":
            i["final_score"] = 2.0
        if fatal_score == 15 and i["speech_class"] == "further_assistance":
            i["final_score"] = 2.0
        if fatal_score == 15 and i["speech_class"] == "patience":
            i["final_score"] = 5.0

    final_score_dict["fl_escalation_found"] = fl_escalation_found


    return final_score_dict


def qa_main_hindi(txt_filename_with_full_path):
    # change file path
    file_path = txt_filename_with_full_path
    clean_agent_speech_lines, clean_customer_speech_lines = read_file_and_extract_agent_speech(file_path)
    # print(clean_agent_speech_lines)
    final_df = apply_regex_logic(clean_agent_speech_lines, clean_customer_speech_lines)
    # print(final_df)
    """uncomment if want to see output classification"""
    # final_df.to_csv("output.csv", index=False)
    final_score_dict = final_score_details = create_final_score(final_df)

    txt_filename_with_full_path_qa = txt_filename_with_full_path.split(".")[0] + "_qa.txt"
    with open(txt_filename_with_full_path_qa, "w+", encoding='utf8') as file:
        file.write("\nQuality Analysis of Call:\n")
        file.write(f"\nFinal Score: {final_score_dict['final_score']}\n")
        file.write(f"\nScore Details:-\n")
        file.write("{:<25} {:<10} {:<10} {:<10}\n".format("Speech Class", "Score", "Found", "Final Score"))
        for x in final_score_dict['score_details']:
            file.write(
                "{:<25} {:<10} {:<10} {:<10}\n".format(x['speech_class'], x['score'], x['found'], x['final_score']))

    return final_score_dict