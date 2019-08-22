import pywikibot
import re
import pymorphy2
from tqdm import tqdm
import time

lat = set('abcdefghijklmnopqrstuvwxyz')
cyr = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
cap_cyr = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
upchar_cyr = {'а':'А', 'б':'Б', 'в':'В', 'г':'Г', 'д':'Д', 'е':'Е', 'ё':'Ё', 'ж':'Ж', 'з':'З', 'и':'И', 'й':'Й', 'к':'К', 'л':'Л', 'м':'М', 'н':'Н', 'о':'О',
              'п':'П', 'р':'Р', 'с':'С', 'т':'Т', 'у':'У', 'ф':'Ф', 'х':'Х', 'ц':'Ц', 'ч':'Ч', 'ш':'Ш', 'щ':'Щ', 'э':'Э', 'ю':'Ю', 'я':'Я'}

def getlangs(text: str):
    return re.findall(r'= {{-(.*?)-}} =', text)


def ifexists(lang: str, title: str):
    site = pywikibot.Site()
    page = pywikibot.Page(site, title)
    if page.isRedirectPage():
        print ('found redirect: '+title+' to '+re.findall(r'\[\[(.*?)\]\]', page.text)[0])
        page = page.getRedirectTarget()
    if (page.exists()):
        text = page.text
        return lang in getlangs(text)
    else:
        return False


def get_lemma(word_form: str):
    #    return morph.parse(word)[0].inflect({'sing', 'nomn'}).word)
    norm = morph.parse(word_form)[0].normal_form
    return norm


def CountFrequency(words, lemmas):
    # Creating an empty dictionary
    freq = {}
    for i in range(lemmas.__len__()):
        item = lemmas[i]
        if item in freq:
            freq[item][0] += 1
            freq[item][1] = freq[item][1] | {words[i]}
        else:
            freq[item] = [1, {words[i]}]
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

fname = input("enter file name: ")
fin = open(fname, 'r')
# l = [line.strip() for line in fin]
text = fin.read()
fin.close()

text = text.replace('.', ' ').replace(',', ' ').replace(' - ', ' ').replace(' -- ', ' ').replace('!', ' ').replace('?', ' ')
text = text.replace(':', ' ').replace(';', ' ').replace('(', ' ').replace(')', ' ').replace('"', ' ')
text = text.replace('{', ' ').replace('}', ' ').replace('[', ' ').replace(']', ' ').replace('*', ' ')
words = text.split()

print(str(words.__len__()) + " words were found")
print('first 10 words: ', words[0:10])
lemmas = []
for word in words:
    lemmas.append(get_lemma(word))
print('first 10 lemmas: ', lemmas[0:10])
freq = CountFrequency(words, lemmas)

print(str(freq.__len__()) + " different lemmas were found")

sorteddict = sortFreqDict(freqdict=freq)

put_list_infile(fname.split('.')[0] + ".word_freq", sorteddict)

print('first 10 freqs: ', sorteddict[0:10])

print('Starting seeking in Wiktionary...')

todo = []
i = 0
for lemma in tqdm(freq.keys()):
    i += 1
    search = lemma
    for w in freq[i][1]:
        if w[0] in cap_cyr:
            lemma[0] = upchar_cyr[lemma[0]]
            continue
        if w[0] in cap_lat:
            lemma[0] = upchar_lat[lemma[0]]
            continue
    if ifexists('ru', lemma):
        # print(lemma + " exists")
        continue
    else:
        if set(lemma) & lat != {} :
            if ifexists('fr', lemma):
                continue
        todo.append( (freq[lemma][0], lemma, freq[lemma][1]) )
        print()
        print(lemma + " doesn't exist")

todo.sort()
todo.reverse()
print('collected these non-existant lemmas: ', todo);
put_list_infile(fname.split('.')[0] + ".todo_list", todo)
