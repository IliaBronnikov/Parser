import pytest
from bs4 import BeautifulSoup

from parser import chunk_string, clean_bs_item, get_page

def test_chunk_string():
    string = 'Модули должны иметь короткие, строчные имена. Подчеркивания могут использоваться в имени модуля, ' \
             'если это улучшает читабельность. Пакеты Python также должны иметь короткие, строчные имена, ' \
             'хотя использование подчеркивания не рекомендуется.'

    assert len(string)//80 +1 == len(list(chunk_string(string, 80)))


def test_clean_bs_item():
    html_str = '<div class="fe10c23a">' \
               '<head class="aab058a7">This is a title</head>' \
               '<p>This is some text content</p>' \
               '</div>'

    bs = BeautifulSoup(html_str, "html.parser")

    assert "<head>" not in clean_bs_item(bs, 5)

