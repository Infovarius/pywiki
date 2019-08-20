import pymorphy2

morph = pymorphy2.MorphAnalyzer()

fin = open('text.txt', 'r')
# l = [line.strip() for line in fin]
text = fin.read()
fin.close()

text = text.replace('.', ' ').replace(',', ' ').replace(' - ', ' ').replace('!', ' ').replace('?', ' ')
text = text.replace(':', ' ').replace('(:)', ' ').replace(')', ' ')
words = text.split()

print(words[0:100])
lemmas = []
for word in words:
    #    print(morph.parse(word)[0].inflect({'sing', 'nomn'}).word)
    lemmas.append(morph.parse(word)[0].normal_form)
print(lemmas[0:100])
