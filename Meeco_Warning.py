import re
import requests
from bs4 import BeautifulSoup

forbidden_words = []  # []안에 금지어를 적어주세요. 여러개 입력이 가능하며, 각 금지어는 콤마로 구분 합니다. ex) 금지어가 a, b, c라면 []안에 'a', 'b', 'c' 라고 적어주세요,
comment = 20  # 게시글의 댓글 수가 일정 갯수에 도달하면 미게에 뭔가 일이 있음을 감지합니다. 이 변수를 이를 위한 기준을 설정하는 변수입니다. 기본값은 20입니다.
max_page = 3  # 검색된 페이지가 설정한 값을 넘어가면 미게가 조용한걸로 판단합니다.
url = 'https://meeco.kr/mini'  # 원하는 카테고리의 주소를 넣어주세요.

# User-Agent header설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

i = 0
check = False

while True:
    if max_page == i:
        print('미게에 설정한 값을 충족하는 게시글이 없습니다.')
        break
    elif check:
        break
    else:
        i += 1
        page = {
            'page': str(i)
        }

        # 미게의 게시글을 가져오기 위한 BeautifulSoup 객체 설정
        resp = requests.get(url, page, headers=headers)
        html_src = resp.text
        soup = BeautifulSoup(html_src, 'html.parser')

        post_list = soup.select('#bBd > div.bBox > div > table > tbody > tr')

        for post in post_list:
            try:
                notice = post['class'][0]
            except KeyError:
                notice = None

            if notice == 'notice':
                continue
            else:
                name = post.select_one('a.title_a > span').text
                count_comment = post.select_one('td.title > a.ptCl.num')
                if count_comment:
                    count_comment = int(re.findall('\d+', count_comment.text)[0])
                else:
                    continue

                for forbidden_word in forbidden_words:
                    name = name.lower()

                    if count_comment >= comment:
                        if name.find(forbidden_word) != -1:
                            print('미게에 설정한 값을 충족하는 게시글이 존재합니다.')
                            check = True
                            break
