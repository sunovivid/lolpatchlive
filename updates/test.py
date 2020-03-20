import re

e = """<div>
<a class="reference-link" href="https://am-a.akamaihd.net/image?f=https://news-a.akamaihd.net/public/images/articles/2019/december/pn24/Aphelios.png?v=1"><img src="https://am-a.akamaihd.net/image?f=https://news-a.akamaihd.net/public/images/articles/2019/december/pn24/Aphelios.png?v=1&amp;resize=64:"></a>
<h3 class="change-title" id="patch-aphelios"><a href="https://am-a.akamaihd.net/image?f=https://news-a.akamaihd.net/public/images/articles/2019/december/pn24/Aphelios.png?v=1">아펠리오스</a></h3>
<p class="summary">신념의 무기</p>
<blockquote class="blockquote context">9.24 패치 기간 중 아펠리오스와 알룬이 달빛의 속삭임 아래 승리를 쟁취하기 위해 소환사의 협곡에 모습을 드러냅니다.</blockquote>
<ul>
<li><a href="https://www.youtube.com/watch?v=p1_yfM5QFgo">챔피언 트레일러</a></li>
<li><a href="https://universe.leagueoflegends.com/ko_KR/champion/aphelios/">유니버스 페이지</a></li>
<li><a href="https://nexus.leagueoflegends.com/ko-kr/2019/11/champion-insights-aphelios/">챔피언 기획 해설</a></li>
<li><a href="https://www.leagueoflegends.co.kr/ko/update/doc/6c08d29b-9f77-4ad8-93d9-f3bfeaaffcc7">기본 가이드</a></li>
</ul>
<blockquote class="blockquote context">아펠리오스 스킨의 고화질 일러스트를 <a href="http://event.leagueoflegends.co.kr/league-displays/">LoL 디스플레이</a>에서 감상해 보세요!</blockquote>
</div>"""


def removeTag(tag, html):
    p = re.compile("<{}.*>.*</{}>".format(tag, tag))
    m = p.search(html)
    if m is not None:
        html = html[:m.start()] + html[m.end():]
    return html

print(removeTag("h3",removeTag("a", e)))