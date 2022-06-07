import os
from UploadFileBlob import upload_file_to_azure_storage
from Transcribe import transcribe
from ExtractConversation import get_conversation


def main():
    # Please give the path in same as wav_files_directory_path with forward slash and no trailing slash.
    # Otherwise it will fail.
    wav_files_directory_path = r"C:/Users/vikas/Downloads/mlai/Audio_Hindi_Calls/WAV"
    all_wav_files = [f for f in os.listdir(wav_files_directory_path) if f.endswith('.wav')]
    for wav_file in all_wav_files:
        json_file_name = wav_files_directory_path + "/" + wav_file.split(".")[0] + ".json"
        txt_file_name = wav_files_directory_path + "/" + wav_file.split(".")[0] + ".txt"
        print("=" * 20)
        print("{0} Started..".format(wav_file))
        upload_blob_result = upload_file_to_azure_storage(wav_file, wav_files_directory_path)
        if "url" in upload_blob_result:
            audio_uri = upload_blob_result["url"]
            transcribe_result = transcribe(audio_uri, json_file_name)
            if transcribe_result:
                write_data_to_txt_from_json = get_conversation(json_file_name, txt_file_name)
                if write_data_to_txt_from_json:
                    print("=" * 20)
                    print("{0} converted successfully".format(wav_file))
                else:
                    print("{0} Unable to get conversation from json or text.".format(wav_file))
            else:
                print("{0} Transcribed Failed.".format(wav_file))
        else:
            print("{0} Unable to upload file to Blob".format(wav_file))


if __name__ == '__main__':
    main()
