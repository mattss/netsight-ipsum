from flask import Flask
from flask import render_template
import nltk.data
import requests
from bs4 import BeautifulSoup
import random
import html2text

app = Flask(__name__)
html_handler = html2text.HTML2Text()
html_handler.ignore_links = True
html_handler.ignore_images = True


def get_some_text(n_paras=5):
    tokenizer = nltk.data.load('ntlk-english.pickle')
    feed = requests.get('https://www.netsight.co.uk/insights/feed/',
                        verify=False)

    soup = BeautifulSoup(feed.text, "html.parser")

    items = soup.find_all('item')
    all_lines = []
    for item in items:
        content = item.find('content:encoded').get_text()
        plain = html_handler.handle(content)
        stripped = ' '.join(plain.split())
        lines = tokenizer.tokenize(stripped)
        for i in range(5):
            all_lines.append(random.choice(lines).strip())

    output = u""
    for para in range(n_paras):
        nlines = random.randint(3, 5)
        paratext = u""
        for i in range(nlines):
            line = random.choice(all_lines)
            paratext += line
            paratext += u" "
        output += paratext
        output += u"\n\n"

    return output


@app.route('/')
@app.route('/generate')
@app.route('/generate/<n>')
def generate(n=5):
    n = int(n)
    if n > 20:
        n = 20
    ipsum = get_some_text(n)
    return render_template('ipsum.html', ipsum=ipsum)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20601)
