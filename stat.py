import pywikibot
import re
import pymorphy2
import progressbar
import time

def getlangs(text: str):
    return re.findall(r'= {{-(.*?)-}} =',text)

def ifexists(lang:str, title:str):
    site = pywikibot.Site()
    page = pywikibot.Page(site, title)
    if(page.exists()):
        text = page.text
        if(lang in getlangs(text)):
            return True
        else:
            return False
    else:
        return False

#if(ifexists('nl', u'dog')):
#    print("such word exists")
#else:
#    print("such word doesn't exist")

morph = pymorphy2.MorphAnalyzer()

fin = open('text.txt','r')
# l = [line.strip() for line in fin]
text = fin.read()
fin.close()

text = text.replace('.', ' ').replace(',', ' ').replace(' - ', ' ').replace('!', ' ').replace('?', ' ')
text = text.replace(':', ' ').replace(';', ' ').replace('(:)', ' ').replace(')', ' ')
words = text.split()

print('first 10 words: ',words[0:10])
lemmas = []
for word in words:
#    print(morph.parse(word)[0].inflect({'sing', 'nomn'}).word)
    lemmas.append(morph.parse(word)[0].normal_form)
print('first 10 lemmas: ',lemmas[0:10])
print('Starting seeking in Wiktionary...')

todo = []
i = 0
bar = progressbar.ProgressBar(maxval=lemmas.__len__(), term_width=100, widgets=[
   'Just a progress bar test: ', # Статический текст
   progressbar.Bar(left='[', marker='=', right=']'), # Прогресс
   progressbar.SimpleProgress(), # Надпись "6 из 10"
]).start()
for lemma in lemmas:
    i += 1
#    bar.update(i)
    if(ifexists('ru', lemma)):
        # print(lemma + " exists")
        continue
    else:
        todo.append(lemma)
        print()
        print(lemma + " doesn't exist")

bar.finish()
print('collected these non-existant lemmas: ', todo)