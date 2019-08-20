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


def get_lemma(word_form: str):
    #    return morph.parse(word)[0].inflect({'sing', 'nomn'}).word)
    return morph.parse(word_form)[0].normal_form


def CountFrequency(my_list):
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


''' create a dict using Counter of a
flat list of words (re.findall(re.compile(r"[a-zA-Z]+"), lines)) in (lines in file->for lines in fh)'''
def _fileIndex(fh):
    return Counter(
        [wrd.lower() for wrdList in
         [words for words in
          [re.findall(re.compile(r'[a-zA-Z]+'), lines) for lines in fh]]
         for wrd in wrdList])


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


def put_list_infile(fname: str, l: list):
    fout = open(fname, 'w+')
    for fw in l:
        if fw.__len__() == 2:
            fout.write(str(fw[1]) + '\t' + str(fw[0]) + '\n')
        elif fw.__len__() == 3:
            fout.write(str(fw[1]) + '\t' + str(fw[0]) + '\t' + str(fw[2]) + '\n')
    fout.close()


# ------------------------  Begin main program -----------------------------------
# if(ifexists('nl', u'dog')):
#    print("such word exists")
# else:
#    print("such word doesn't exist")

morph = pymorphy2.MorphAnalyzer()

fname = 'text.txt'
fin = open(fname, 'r')
# l = [line.strip() for line in fin]
text = fin.read()
fin.close()

text = text.replace('.', ' ').replace(',', ' ').replace(' - ', ' ').replace('!', ' ').replace('?', ' ')
text = text.replace(':', ' ').replace(';', ' ').replace('(', ' ').replace(')', ' ')
words = text.split()

print(str(words.__len__()) + " words were found")
print('first 10 words: ', words[0:10])
lemmas = []
for word in words:
    lemmas.append(get_lemma(word))
print('first 10 lemmas: ', lemmas[0:10])
freq = CountFrequency(lemmas)
print(str(freq.__len__()) + " different lemmas were found")

sorteddict = sortFreqDict(freqdict=freq)

put_list_infile(fname.split('.')[0] + ".word_freq", sorteddict)

print('first 10 freqs: ', sorteddict[0:10])

print('Starting seeking in Wiktionary...')

todo = []
i = 0
for lemma in tqdm(freq.keys()):
    i += 1
    if (ifexists('ru', lemma)):
        # print(lemma + " exists")
        continue
    else:
        #       word = [w for w in words if get_lemma(w) == lemma]
        todo.append( (freq[lemma], lemma, set([word for word in words if get_lemma(word) == lemma])) )
        print()
        print(lemma + " doesn't exist")

todo.sort()
todo.reverse()
print('collected these non-existant lemmas: ', todo);
put_list_infile(fname.split('.')[0] + ".todo_list", todo)
