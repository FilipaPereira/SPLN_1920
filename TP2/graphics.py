import re

import matplotlib.pyplot as plt
import numpy as np


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
    # plt.plot(list(pronouns.values()), list(pronouns.keys()), marker='o')
    # desta maneira n fica uma curva direita pq n esta ordenado
    plt.plot(occurs, prs, marker='o')
    plt.ylabel('Personal Pronouns')
    plt.xlabel('Number of Ocurrences')

    plt.subplot(122)
    plt.pie(occurs, labels=prs, autopct='%.2f%%')
    plt.show()


def godsLusiadas(file):
    godsOccur = {}
    gods = ['Marte', 'Neptuno', 'Júpiter', 'Baco', 'Vénus', 'Mercúrio', 'Apolo', 'Minerva', 'Juno', 'Diana',
            'Vulcano', 'Saturno', 'Plutão']

    for w in file.read().split():
        w = re.sub(r'[^\w]', '', w)
        if w in gods:
            godsOccur[w] = godsOccur.get(w, 0) + 1

    print(godsOccur)
    names = list(godsOccur.keys())
    occurs = list(godsOccur.values())

    # histograma
    plt.bar(names, occurs, width=0.5, color='orange')
    plt.title('Appearances of the Roman Gods in "Os Lusíadas"')
    plt.xlabel('Gods')
    plt.ylabel('Number of Mentions')

    #grafico donut
    

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(occurs, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(names[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax.set_title("Deuses Romanos")
    plt.show()






def prompter():
    while 1:
        file1 = 'harryPotter.txt'
        file2 = 'Lusiadas.txt'

        print('What do you which to see?')
        print('1 - Piechart and Plot about occurrences of personal pronouns in Harry Potter')
        print('2 - Barplot displaying the frequency of the gods appearances in "Os Lusíadas"')
        # something to draw scatterplot, histogram and maybe a table
        ##entidades por canto --> tabela ??
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
        elif choice == '0':
            break
        else:
            print('Wrong option!')


prompter()
