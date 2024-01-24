import sys
import os

def parse_special_chars(line: str) -> str:
    return line.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

def parse_newline_front_back(line: str, delimiter_front: str, delimiter_back: str) -> str:
    if line[:-1].endswith(delimiter_front) or line[:-1].endswith(delimiter_back):
        line = line.replace("\n", "")
    line = line.replace("\n", "<br>")
    line = line.replace(delimiter_back, "\n").replace(delimiter_front, ";")
    return line


def parse_block_math(line: str) -> str:
    while "$$" in line:
        line = line.replace("$$", "<anki-mathjax block=\"true\">", 1)
        line = line.replace("$$", "</anki-mathjax>", 1)
    return line


def parse_inline_math(line: str) -> str:
    while "$" in line:
        line = line.replace("$", "<anki-mathjax>", 1)
        line = line.replace("$", "</anki-mathjax>", 1)
    return line


def parse_unorderd_list(line: str, in_list: bool) -> tuple[str, bool]:
    line = line.strip("\t")
    if line.startswith("- "):
        if not in_list:
            line = "<ul>" + line
            in_list = True
        line = line.replace("- ", "<li>", 1).replace("<br>", "</li>")
    else:
        if in_list:
            line = "</ul>" + line
            in_list = False
    return line, in_list

def parse(path="", delimiter_front="!\\", delimiter_back="!\\\\") -> str:
    if not path:
        path = sys.argv[1]
    pure_path, extension = os.path.splitext(path)
    curr_flashcards = "" # the current parsed text

    in_list = False # is an unordered list currently being processed

    try:
        if extension != ".md":
            raise FileNotFoundError

        with open(path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                if line == "\n":
                    continue

                line = parse_special_chars(line)
                line = parse_newline_front_back(line, delimiter_front, delimiter_back)
                line = parse_block_math(line)
                line = parse_inline_math(line)
                line, in_list = parse_unorderd_list(line, in_list)

                # add line to flashcards string 
                curr_flashcards += line



        if in_list:
            curr_flashcards += "</ul>"
        with open(pure_path + ".txt", "w") as f:
            f.write(curr_flashcards)

    except FileNotFoundError:
        print("file does not exist or does not have .md extension")

    return pure_path + ".txt"



if __name__ == "__main__":
    parse()

