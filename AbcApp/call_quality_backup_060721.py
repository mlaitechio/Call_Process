from AbcApp import config
#import config
import pandas as pd
import re


def read_file_and_extract_agent_speech(file_path):
    clean_agent_speech_lines = []
    with open(file_path, 'r') as speech_file:
        for line in speech_file.readlines():
            if line.startswith("Agent") or line.startswith("agent"):
                clean_line = "".join(line.split("=")).lower().replace("agent :", "").strip()
                clean_agent_speech_lines.append(clean_line)

    return clean_agent_speech_lines


def apply_regex_logic(clean_agent_speech_lines):
    final_output_list = []
    for speech in clean_agent_speech_lines:
        fl_match_found = 0
        for speech_class, regex_patten in config.CONFIG_DICT.items():
            if re.search(regex_patten.lower(), speech.lower()):
                fl_match_found = 1
                break

        if fl_match_found:
            final_output_list.append({"speech": speech, "class": speech_class,
                                      "fatality": config.FATALITY_MAPPING[speech_class]})
        else:
            final_output_list.append({"speech": speech, "class": "", "fatality": ""})

    final_df = pd.DataFrame(final_output_list)
    return final_df


def create_final_score(final_df):
    counts = final_df["class"].value_counts()
    score_dict = counts.to_dict()
    # print(score_dict)

    fatal_score = 0
    non_fatal_score = 0
    final_score = "0/0"
    fl_escalation_found = 0

    speech_class_details = []

    for key, value in score_dict.items():
        if key:
            if config.FATALITY_MAPPING[key] == "fatal":
                if key == "verification":
                    fatal_score += config.SCORE_MAPPING[key]
                elif key == "escalation":
                    fl_escalation_found = 1
                    fatal_score += 0
            else:
                non_fatal_score += config.SCORE_MAPPING[key]

    # adding default 5 numbers for cannot be done fatal case
    fatal_score += 5
    if fl_escalation_found == 0:
        fatal_score += 5

    # making final grid

    # fatal_score = 15
    # non_fatal_score = 65

    if fatal_score < 15:
        final_score = "0/0"
    else:
        final_score = "{}/{}".format(fatal_score, fatal_score+non_fatal_score)

    final_colour = "Red"
    if fatal_score == 15 and fatal_score+non_fatal_score > 69:
        final_colour = "Green"
    else:
        if fatal_score < 15:
            final_colour = "Red"
        elif 0 < fatal_score+non_fatal_score <= 45:
            final_colour = "Yellow"
        else:
            final_colour = "Blue"

    final_score_dict = {
        "final_colour":  final_colour,
        "final_score": final_score
    }

    # print("Fatal score: ", fatal_score)
    # print("Non Fatal score: ", non_fatal_score)

    score_lookup = pd.DataFrame(config.SCORE_MAPPING.items(), columns=["speech_class", "score"])
    found_speech = pd.DataFrame(score_dict.items(), columns=["speech_class", "score"])
    # print(score_lookup)
    # print(found_speech)

    final_df = pd.merge(score_lookup, found_speech, how="left", on="speech_class")
    final_df.fillna(0, inplace=True)
    final_df['score_y'] = final_df['score_y'].apply(lambda x: 1 if x > 1 else x)
    final_df = final_df.rename(columns={"score_x": "score", "score_y": "found"})

    final_df["final_score"] = final_df["score"]*final_df["found"]
    # print(final_df.to_dict("records"))
    final_score_dict["score_details"] = final_df.to_dict("records")

    return final_score_dict


def qa_main(txt_filename_with_full_path):
    # change file path
    file_path = txt_filename_with_full_path
    clean_agent_speech_lines = read_file_and_extract_agent_speech(file_path)
    # print(clean_agent_speech_lines)
    final_df = apply_regex_logic(clean_agent_speech_lines)
    # print(final_df)
    """uncomment if want to see output classification"""
    # final_df.to_csv("output.csv", index=False)
    final_score_dict = final_score_details = create_final_score(final_df)
    print(final_score_dict)
    txt_filename_with_full_path_qa = txt_filename_with_full_path.split(".")[0]+"_qa.txt"
    with open(txt_filename_with_full_path_qa,"w+", encoding='utf8') as file:
        file.write("\nQuality Analysis of Call:\n")
        file.write(f"\nFinal Score: {final_score_dict['final_score']}\n")
        file.write(f"\nScore Details:-\n")
        file.write("{:<25} {:<10} {:<10} {:<10}\n".format("Speech Class","Score","Found","Final Score"))
        for x in final_score_dict['score_details']:
            file.write("{:<25} {:<10} {:<10} {:<10}\n".format(x['speech_class'],x['score'],x['found'],x['final_score']))
    
    return final_score_dict

#qa = qa_main('/home/mayank/Documents/abc/speech/abcstt/media/1622758434405.txt')

