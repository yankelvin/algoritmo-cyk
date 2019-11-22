from re import findall
from math import floor, ceil

grammar = dict()

# Getting productions from the file
with open('gramatica.txt', 'r') as file:
    for row in file.readlines():
        left = findall(r'[a-zA-Z]+\s\=\>', row)[0]
        key = left.replace('=>', '').strip()
        productions = row.replace(left, '').strip().split('|')
        grammar[key] = productions


word = input('Qual palavra deseja verificar? ')

# Creating the matrix
matrix = [list() for i in range(len(word))]
word = list(word)


# Filling the matrix
def filling_matrix(word, grammar, matrix, row):
    base = matrix[len(matrix) - 1]
    if (len(base) != 0):
        if list(grammar.keys())[0] in base[0]:
            print('Essa palavra faz parte da gramática!')
        else:
            print('Essa palavra não faz parte da gramática!')
        return matrix

    combinations = generate_combinations(word, row)
    if len(combinations[0]) > 2:
        for i, comb in enumerate(combinations):
            combinations[i] = []
            for j in range(len(comb) - 1):
                combinations[i].append([comb[:j+1], comb[j+1:]])

    for comb in combinations:
        if type(comb[0]) is list:
            calc = list()
            result = ''
            for j in comb:
                verif = []
                for k in j:
                    if len(k) > 1:
                        w = ''.join(word)
                        concat = ''.join(k)
                        position = w.find(concat)
                        no_termminal = matrix[len(concat)-1][position]
                        verif.append(no_termminal)
                    else:
                        no_termminal = verify_production(k, grammar)
                        verif.append(no_termminal)
                verif = distribuction(verif[0], verif[1])
                result = verify_production(verif, grammar)
                calc.append(result)
                result = ''
            found = ''
            for c in calc:
                found += c
            matrix[row].append(found)
        else:
            verif = ''
            no_termminal = verify_production(comb, grammar)
            if len(no_termminal) > 1:
                verif = distribuction(no_termminal[:ceil(
                    len(no_termminal)/2)], no_termminal[ceil(len(no_termminal)/2):])
                verif = list(dict.fromkeys(verif))
                result = verify_production(verif, grammar)
                if result == '':
                    result = no_termminal
                matrix[row].append(result)
            else:
                matrix[row].append(no_termminal)

    row += 1
    return filling_matrix(word, grammar, matrix, row)


def verify_production(w, grammar):
    prod = ''
    if (type(w) is list):
        for i in w:
            prod += verify_production(i, grammar)
    else:
        for key, values in grammar.items():
            if w in values:
                prod += key
    return prod


def generate_combinations(w, row):
    step = row + 1
    combinations = []
    for i in range(len(w)):
        symbol = []
        try:
            if (row > 0):
                for j in range(i, step + i):
                    symbol.append(w[j])
                combinations.append(symbol)
            else:
                combinations.append(w[i:step][0])
                step += 1
        except:
            pass
    return combinations


def distribuction(ve, node):
    dist = []
    for i in ve:
        for n in node:
            dist.append(f'{i}{n}')
    return dist


result = filling_matrix(word, grammar, matrix, 0)
print(result)
