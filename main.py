from googletrans import Translator
import requests
import platform
import subprocess
import os
import schedule
import time

tmp_path = "./tmp.txt"


def open_editor(str):
    text_file = open(tmp_path, "w")
    text_file.write(str)
    text_file.close()
    subprocess.call(['open', '-a', 'TextEdit', tmp_path])


def push(title, message):
    plt = platform.system()

    if plt == 'Darwin':
        command = f'''
		osascript -e 'display notification "{message}" with title "{title}"'
		'''
    if plt == 'Linux':
        command = f'''
		notify-send "{title}" "{message}"
		'''
    else:
        return

    os.system(command)


def main():
    translator = Translator()

    # http://www.smartphrase.com/cgi-bin/randomphrase.cgi?german&serious&normal&231&93&146&49&108&175
    # is another site with good suggestions, though they'd have to be extracted from the html
    r = requests.get(
        "https://www.lexisrex.com/get_sentence.php?foreign=German")

    print(r.text)

    translation = translator.translate(r.text, dest="en", src="de")

    print(translation.text)

    open_editor(r.text + "\n" + translation.text)


schedule.every().hour.at(":00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
