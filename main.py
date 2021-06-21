#!/usr/bin/env python3.7
import os
import re
import argparse
import sys
from collections import Counter
from datetime import datetime
from typing import Dict
from pynput import keyboard


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

LOG_FILE = os.path.join(LOGS_DIR, "words.log")


class Analyzer:
    """Basic analysis of data"""

    def __init__(self, file: str, interval: int):
        self.__file = file
        self.__size = os.stat(self.__file).st_size

        with open(self.__file, "r") as f:
            self.__data = f.readlines()

        self.__groups = self.__group(interval)

    def get_size(self) -> str:
        """
        Return size of file
        :return str
        """
        return "%.2f bytes" % self.__size

    def __group(self, interval=60) -> Dict:
        """
        Group data by interval
        :return dict
        """

        content = {}
        for entry in self.__data:
            timestamp, word, _ = entry.split(" ")
            if self.__is_word(word):
                remainder = float(timestamp) % (interval * 60 * interval)
                diff = float(timestamp) - remainder

                date_time = self.__format_datetime(diff)
                if date_time in content:
                    content[date_time].append(word)
                else:
                    content[date_time] = [word]

        return content

    def get_word_count(self):
        words = len(sum(self.__groups.values(), []))
        return words

    def get_frequently_used_words(self):
        words = sum(self.__groups.values(), [])
        frequency = Counter(words)
        return frequency.most_common(10)

    def __format_datetime(self, dt) -> str:
        date_time = datetime.fromtimestamp(dt)
        return date_time.strftime("%Y-%m-%dT%H:%M")

    def __is_word(self, word: str) -> bool:
        reg = re.compile(r"[a-zA-Z]")

        if reg.search(word):
            return True

    def get_most_active_period(self):
        sorted_groups = sorted(self.__groups.items(), key=lambda x: len(x[1]), reverse=True)
        if sorted_groups:
            period, count = sorted_groups[0]
            return (period, len(count))
        return ()

   

def commands():
    """Display command line arguments"""

    parser = argparse.ArgumentParser(description="Keyboard Word Count")
    parser.add_argument("--report", type=str,nargs="?", default="no", help="summary report - yes/no")
    parser.add_argument("--interval", type=int, nargs="?", default=20, help="interval in minutes")

    if len(sys.argv) < 1:
        parser.print_usage()
        sys.exit(2)

    args = vars(parser.parse_args())
    return args


def main():
    args = commands()

    if args["report"] == "yes":
        if not os.path.isfile(LOG_FILE):
            print("Log file not available")
            sys.exit()

        if os.stat(LOG_FILE).st_size == 0:
            print("Log file is empty.")
            sys.exit()
        interval = args["interval"]
        analyser = Analyzer(file=LOG_FILE, interval=interval)

        print('Frequently used words')
        print("%10s %10s"%("Word", "Count"), end="\n")
        print('-'*30)
        for entry in analyser.get_frequently_used_words():
            k,v = entry
            print("%10s  %10d"%(k, v))

        print('\nWord Count', analyser.get_word_count())

        active_period = analyser.get_most_active_period()
        if active_period:
            time, count = active_period
            print('Most active period %s with word count %s'%(time, count))

        file_size = analyser.get_size()
        print("File size %s"%file_size)

    else:
        word = ""
        def on_release(key) -> None:
            """
            Assumes a word until space/enter key is released
            :return None
            """

            nonlocal word
            if key in [keyboard.Key.space, keyboard.Key.enter]:
                # We have a 'word'
                now = datetime.now().timestamp()

                with open(LOG_FILE, "a+") as f:
                    f.write("%.2f %s \n" % (now, word))
                word = ""
            else:
                try:
                    if key not in [keyboard.Key.space, keyboard.key.enter]:
                        word += key.char
                except AttributeError:
                    pass

        with keyboard.Listener(on_release=on_release) as listener:
            listener.join()


if __name__ == "__main__":
    main()
