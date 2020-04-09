import matplotlib.pyplot as plt


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

    plt.suptitle('Personal Pronouns')

    plt.subplot(121)
    # plt.plot(list(pronouns.values()), list(pronouns.keys()), marker='o')
    # desta maneira n fica uma curva direita pq n esta ordenado
    plt.plot(occurs, prs, marker='o')
    plt.ylabel('Personal Pronouns')
    plt.xlabel('Number of Ocurrences')

    plt.subplot(122)
    plt.pie(occurs, labels=prs, autopct='%.2f%%')
    plt.show()


def prompter():
    while 1:
        file = input('Insert the name of the file to be processed: ')
        file = 'harryPotter.txt' ## just to be easier to test

        f = open(file, 'r', encoding='utf-8')

        print('What do you which to see?')
        print('1 - PieChart and BarPlot about occurrences of personal pronouns')
        print('2 - Stuff')
        ##Polarities maybe? use stacked or side by side barplots
        # something to draw scatterplot, histogram and maybe a table
        # 3d graphics is not worth it
        print('0 - Quit')
        choice = input('Option:')
        if choice == '1':
            personal_pronouns(f)
        elif choice == '2':
            print('Not available')
        elif choice == '0':
            f.close()
            break
        else:
            print('Wrong option!')
        f.close()


prompter()

