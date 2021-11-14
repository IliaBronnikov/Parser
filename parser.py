from bs4 import BeautifulSoup
import requests

name_file = "fileOutput.txt"
url = "https://meduza.io/feature/2021/11/13/rossiyskie-vlasti-pytayutsya-zaschitit-pogibshego-v-berline-diplomata-ot-dikih-teoriy-pressy"


def get_page(url):
    page = requests.get(url)
    content = page.content.decode("utf-8")
    if page.status_code == 200:
        return content
    return None


def clean_bs_item(bs_item):
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
            clean_html_str += "{}\n".format(line)
    return clean_html_str


def write_data(name_file, full_text):
    with open(name_file, mode="w", encoding="utf-8") as p:
        p.write(full_text)


def main():
    page = get_page(url)
    bs = BeautifulSoup(page, "html.parser")
    parser_data = clean_bs_item(bs)
    if parser_data is None:
        print("Ошибка!")
    else:
        write_data(name_file, parser_data)


if __name__ == "__main__":
    main()
