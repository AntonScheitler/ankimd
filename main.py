import sys
import os


END_OF_FRONT = "!\\" # signals end of front of flashcard
END_OF_BACK = "!\\\\" # signals end of back of flashcard

def parse_special_chars(line: str) -> str:
    return line.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

def parse_newline_front_back(line: str) -> str:
    if line[:-1].endswith(END_OF_FRONT) or line[:-1].endswith(END_OF_BACK):
        line = line.replace("\n", "")
    line = line.replace("\n", "<br>")
    line = line.replace(END_OF_BACK, "\n").replace(END_OF_FRONT, ";")
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

def main():
    md_path = sys.argv[1]
    pure_path, extension = os.path.splitext(md_path)
    curr_flashcards = "" # the current parsed text

    in_list = False # is an unordered list currently being processed

    try:
        if extension != ".md":
            raise FileNotFoundError

        with open(md_path, "r") as f:
            for line in f.readlines():
                if line == "\n":
                    continue

                line = parse_special_chars(line)
                line = parse_newline_front_back(line)
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



if __name__ == "__main__":
    main()

