import random, os, re, json, datetime
from flask import Flask, request, render_template, send_from_directory
from settings import VOICEMAIL_FILE_DIR
application = Flask(__name__)

@application.route('/delete_voicemail', methods=["POST"])
def delete_voicemail():
    voicemail_regex = '^'+VOICEMAIL_FILE_DIR+'/([0-9]+)/INBOX/msg([0-9]*)\.wav$'
    voicemail_urls = request.json['voicemail_urls']
    for url in voicemail_urls:
        valid_url = re.search(voicemail_regex, url)
        if valid_url:
            extension = valid_url.groups(1)[0]
            voicemail_id = valid_url.groups(1)[1]

            audio_file_url = VOICEMAIL_FILE_DIR+'/'+extension+'/INBOX/'+'msg'+voicemail_id+'.wav'
            audio_file_txt = VOICEMAIL_FILE_DIR+'/'+extension+'/INBOX/'+'msg'+voicemail_id+'.txt'
            os.remove(audio_file_url)
            os.remove(audio_file_txt)

    return "OK"

@application.route('/')
def main():
    voicemail = []
    for extension in os.listdir(VOICEMAIL_FILE_DIR):
        extension_dict = {"extension": extension, "messages": []}
        for f in os.listdir(VOICEMAIL_FILE_DIR+'/'+extension+'/INBOX'):
            is_audio_file = re.match('^msg([0-9]*)\.wav$', f)
            if is_audio_file:
                filename = VOICEMAIL_FILE_DIR+'/'+extension+'/INBOX/'+f
                creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y/%m/%d %H:%M")
                extension_dict["messages"].append({
                    "filename": filename,
                    "creation_date": creation_date
                })

        voicemail.append(extension_dict)
    voicemail = [v for v in voicemail if v['messages']]

    return render_template('main.html', voicemail=voicemail)


if __name__ == '__main__':
    application.run()

