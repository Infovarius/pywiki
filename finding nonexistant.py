import pywikibot
import re
import pymorphy2
from tqdm import tqdm
import time


def getlangs(text: str):
    return re.findall(r'= {{-(.*?)-}} =', text)


def ifexists(lang: str, title: str):
    site = pywikibot.Site()
    page = pywikibot.Page(site, title)
    if (page.exists()):
        text = page.text
        return lang in getlangs(text)
    else:
        return False


# if(ifexists('nl', u'dog')):
#    print("such word exists")
# else:
#    print("such word doesn't exist")

morph = pymorphy2.MorphAnalyzer()

fin = open('text.txt', 'r')
# l = [line.strip() for line in fin]
text = fin.read()
fin.close()

text = text.replace('.', ' ').replace(',', ' ').replace(' - ', ' ').replace('!', ' ').replace('?', ' ')
text = text.replace(':', ' ').replace(';', ' ').replace('(:)', ' ').replace(')', ' ')
words = text.split()

print('first 10 words: ', words[0:10])
lemmas = []
for word in words:
    #    print(morph.parse(word)[0].inflect({'sing', 'nomn'}).word)
    lemmas.append(morph.parse(word)[0].normal_form)
print('first 10 lemmas: ', lemmas[0:10])
print('Starting seeking in Wiktionary...')

todo = []
i = 0
for lemma in tqdm(lemmas):
    i += 1
    #    bar.update(i)
    if (ifexists('ru', lemma)):
        # print(lemma + " exists")
        continue
    else:
        todo.append(lemma)
        print()
        print(lemma + " doesn't exist")

print('collected these non-existant lemmas: ', todo)
