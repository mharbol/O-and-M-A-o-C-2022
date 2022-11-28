# Quick and easy parsing script to convert the problem text to Markdown if
# we choose to add the daily prompt to the front page. Still needs plenty
# of work and right now is more like a transcripting tool than a utility.

from sys import argv
from urllib.request import urlopen
from html.parser import HTMLParser

START = "article"

class Parser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.enter_main_flag = False
        self.md_output = ""
    
    def handle_starttag(self, tag: str, attrs = None) -> None:
        if tag == START:
            self.enter_main_flag = True
        
        if self.enter_main_flag:
            if tag == "p":
                self.md_output += "\n"
            elif tag == "h2":
                self.md_output += "###"
            elif tag == "li":
                self.md_output += "- "
            elif tag == "code":
                self.md_output += "`"
            else:
                print(tag)
            

    def handle_endtag(self, tag: str) -> None:
        if tag == START:
            self.enter_main_flag = False
        if self.enter_main_flag:
            if tag == "code":
                self.md_output += "`"

    def handle_data(self, data: str) -> None:
        if self.enter_main_flag:
           self.md_output += data

YEAR = argv[1]
DATE = argv[2]
url = f"https://adventofcode.com/{YEAR}/day/{DATE}"

with urlopen(url) as webpage:
    pageHTML = webpage.read().decode("utf8")

parser = Parser()

parser.feed(pageHTML)

print(parser.md_output)