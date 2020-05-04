import re
import fileinput
import numpy as np
import matplotlib.pyplot as plt
plt.rcdefaults()


def wordPolarities():
    polarities = {}
    for line in fileinput.input(['sentilex2.txt']):
        word = re.split(',', line)[0]
        aux = re.search(r'N0=(\-?\d+)', line)
        if aux:
            polarity = aux.group(1)
            polarities[word] = int(polarity)
    return polarities


def polaritiesLusiadas(file):
    polarities = wordPolarities()
    positiveByChapter = []
    negativeByChapter = []
    wordsByChapter = []
    total_pos = 0
    total_neg = 0
    chapter = 0
    palavras = 0
    chapters = []
    performance = []

    for line in file.read().split('\n'):
        word = line.split()
        if len(word) == 3:
            if word[0] == 'Canto':
                positiveByChapter.append(total_pos)
                negativeByChapter.append(total_neg)
                wordsByChapter.append(palavras)
                total_neg = 0
                total_pos = 0
                palavras = 0
                chapter += 1
                chapters.append(chapter)

            else:
                w = word[0].lower()
                x = polarities.get(w, 0)
                if x == -1:
                    total_neg += 1
                elif x == 1:
                    total_pos += 1
                palavras += 1
    positiveByChapter.append(total_pos)
    negativeByChapter.append(total_neg)
    wordsByChapter.append(palavras)
    positiveByChapter.pop(0)
    negativeByChapter.pop(0)
    wordsByChapter.pop(0)

    print('POS: ', positiveByChapter)
    print('NEG: ', negativeByChapter)
    print('WORDS: ', wordsByChapter)

    #Barplot
    i = 0

    while i < len(chapters):
        performance.append(- negativeByChapter[i] + positiveByChapter[i])
        i += 1

    objects = chapters

    y_pos = np.arange(len(objects))

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Word Polarity')
    plt.xlabel('Canto')
    plt.title('Polarity by Canto')
    plt.show()


def wordcountPronouns(file):
    wcPronouns = {}
    pronounsPersonal = ['I', 'He', 'She', 'We', 'You', 'They', 'Her', 'Him', 'Them', 'Me', 'Us', 'It']

    for w in file.read().split():
        w = w.capitalize()
        if w in pronounsPersonal:
            wcPronouns[w] = wcPronouns.get(w, 0) + 1

    return wcPronouns


def personal_pronouns(file):
    pronouns = wordcountPronouns(file)

    prs = []
    occurs = []
    for k, v in sorted(pronouns.items(), key=lambda x: x[1], reverse=True):
        prs.append(k)
        occurs.append(v)

    plt.suptitle('Personal Pronouns in Harry Potter')

    plt.subplot(121)
    plt.plot(occurs, prs, marker='o')
    plt.ylabel('Personal Pronouns')
    plt.xlabel('Number of Ocurrences')

    plt.subplot(122)
    plt.pie(occurs, labels=prs, autopct='%.2f%%')
    plt.show()


def godsLusiadas(file):
    godsOccur = {}
    gods = ['Marte', 'Neptuno', 'Júpiter', 'Baco', 'Vénus', 'Mercúrio', 'Apolo', 'Minerva', 'Juno', 'Diana',
            'Vulcano', 'Saturno']

    for w in file.read().split():
        w = re.sub(r'[^\w]', '', w)
        if w in gods:
            godsOccur[w] = godsOccur.get(w, 0) + 1

    names = list(godsOccur.keys())
    occurs = list(godsOccur.values())

    #Barplot
    plt.bar(names, occurs, width=0.5, color='orange')
    plt.title('Appearances of the Roman Gods in "Os Lusíadas"')
    plt.xlabel('Gods')
    plt.ylabel('Number of Mentions')

    #Donutplot

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(occurs, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(names[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, **kw)

    ax.set_title('Roman Gods')
    plt.show()


def mar_words(file):
    marOccur = {}
    mar_w = r'(^(mar)[^\s,;.\n]*)' 

    for w in file.read().split():
        w = re.sub(r'[^\w]', '', w)
        if re.search(mar_w, w):
            marOccur[w] = marOccur.get(w, 0) + 1

    names = list(marOccur.keys())
    occurs = list(marOccur.values())
    print(names)
    print(occurs)


def prompter():
    while 1:
        file1 = 'harryPotter.txt'
        file2 = 'Lusiadas.txt'
        file3 = 'Lusiadas.tagged'

        print('What do you which to see?')
        print('1 - Occurrences of personal pronouns in "Harry Potter"')
        print('2 - Appearances of the Gods in "Os Lusíadas"')
        print('3 - Word Polarities by canto in "Os Lusíadas"')
        print('4 - Ocurrences of words beginning with "mar" in "Os Lusíadas"')
        print('0 - Quit')
        choice = input('Option:')
        if choice == '1':
            f = open(file1, 'r', encoding='utf-8')
            personal_pronouns(f)
            f.close()
        elif choice == '2':
            f = open(file2, 'r', encoding='utf-8')
            godsLusiadas(f)
            f.close()
        elif choice == '3':
            f = open(file3, 'r', encoding='utf-8')
            polaritiesLusiadas(f)
            f.close()
        elif choice == '4':
            f = open(file2, 'r', encoding='utf-8')
            mar_words(f)
            f.close()
        elif choice == '0':
            break
        else:
            print('Wrong option!')


prompter()
