import json


# path = json_file_path, res_name = txt_file_path


def get_conversation(json_file_path, txt_file_path):
    is_converted = False
    try:
        with open(json_file_path, 'r', encoding="utf-8") as f:
            parsed_response = json.load(f)

        print("Json file read successfully.")
        # json_data = parsed_response['AudioFileResults'][0]['SegmentResults']

        json_data = parsed_response['recognizedPhrases']

        with open(txt_file_path, "w", encoding="utf-8") as text_file:
            for speaker in json_data:
                if "speaker" in speaker.keys():
                    if speaker['speaker'] == 2:
                        text_file.write("S2 : " + speaker['nBest'][0]['display'] + '\n')
                    if speaker['speaker'] == 1:
                        text_file.write("S1 : " + speaker['nBest'][0]['display'] + '\n')

                else:
                    text_file.write("S1 : " + speaker['nBest'][0]['display'] + '\n')
        print("Text file written successfully.")
        text_file.close()
        is_converted = True
    except Exception as e:
        print("Error: Exception raised in get_conversation(). {0}".format(e))
        is_converted = True
    return is_converted
