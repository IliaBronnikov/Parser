import argparse
import sys

from bs4 import BeautifulSoup
import requests

name_file = "fileOutput.txt"
# url = "https://meduza.io/feature/2021/11/13/rossiyskie-vlasti-pytayutsya-zaschitit-pogibshego-v-berline-diplomata-ot-dikih-teoriy-pressy"
# length = 80
decoder_dict = {"yes": True, "no": False}


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="Input url")
    parser.add_argument("length_str", type=int, help="Input length for output string")
    parser.add_argument(
        "save_img_link",
        type=str,
        choices=["yes", "no"],
        default="no",
        help="Save image links in text?",
    )
    parser.add_argument(
        "save_to_file",
        type=str,
        choices=["yes", "no"],
        default="no",
        help="Save text to file or write in terminal?",
    )
    return parser


def get_page(url):
    page = requests.get(url)
    content = page.content.decode("utf-8")
    if page.status_code == 200:
        return content
    return None


def chunk_string(string, length):
    while len(string) > length:
        upper_bound = string.rindex(" ", 0, length)
        yield string[0:upper_bound].strip()
        string = string[upper_bound:]


def clean_bs_item(bs_item, length_string):
    lines = bs_item.find_all(text=True)
    clean_tags_str = ""
    clean_html_str = ""
    blacklist = [
        "[document]",
        "noscript",
        "header",
        "html",
        "meta",
        "head",
        "input",
        "script",
        "title",
        "style",
        "span",
        "svg",
        "href",
        "footer",
    ]
    for line in lines:
        if line.parent.name not in blacklist:
            clean_tags_str += "{}".format(line.replace(u"\xa0", u" "))
    for line in clean_tags_str.splitlines():
        if len(line) > 1:
            if len(line) > length_string:
                line = "\n".join(list(chunk_string(line, length_string)))
            clean_html_str += "{}\n".format(line)
    return clean_html_str


def write_data(name_file, full_text):
    with open(name_file, mode="w", encoding="utf-8") as p:
        p.write(full_text)


def main():
    parser = createParser()
    arg = parser.parse_args(sys.argv[1:])
    url = arg.url
    length_string = arg.length_str
    save_img_link = decoder_dict[str(arg.save_img_link)]
    save_to_file = decoder_dict[str(arg.save_to_file)]

    page = get_page(url)
    bs = BeautifulSoup(page, "html.parser")
    parser_data = clean_bs_item(bs, length_string)
    if save_to_file:
        write_data(name_file, parser_data)
    else:
        print(parser_data)

if __name__ == "__main__":
    main()
