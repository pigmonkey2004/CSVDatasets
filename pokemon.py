import math
import re
import csv
from collections import defaultdict
from collections import Counter

def readem(f):
    with open(f) as file:
        reader = csv.DictReader(file)
        data = list(reader)
        fire_pokemon = [(index,row) for index,row in enumerate(data) if row['type'] == 'fire']
        aboveforty = [(index,row) for index,row in fire_pokemon if float(row['level']) >= 40.0]
        percent = (len(aboveforty) / len(fire_pokemon)) * 100
        rounded = round(percent)
    with open('pokemon1.txt', 'w') as outfile:
            outfilds = []
            outfilds.append("Percentage of fire type Pokemons at or above level 40 = " + str(rounded))
            outfile.write(''.join(outfilds))
    return
    pass

def fillmissing(f):
    with open(f, newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for row in data:
            if row['type'] == 'NaN':
                typefreq = defaultdict(int)
                for index1,row1 in enumerate(data): 
                    if row1['weakness'] == row['weakness'] and row1['type'] != 'NaN':
                        typefreq[row1['type']] += 1   
                row['type'] = max(typefreq, key=lambda x: (typefreq[x], x), default=None)
        abv40atkSum = 0
        abv40atkCnt = 0
        abv40defSum = 0
        abv40defCnt = 0
        abv40hpSum = 0
        abv40hpCnt = 0
        bel40atkSum = 0
        bel40atkCnt = 0
        bel40defSum = 0
        bel40defCnt = 0
        bel40hpSum = 0
        bel40hpCnt = 0
        for row in data:
            if float(row['level']) >= 40.0:
                if row['atk'] != 'NaN':
                    abv40atkSum += float(row['atk'])
                    abv40atkCnt += 1
                if row['def'] != 'NaN':
                    abv40defSum += float(row['def'])
                    abv40defCnt += 1
                if row['hp'] != 'NaN':
                    abv40hpSum += float(row['hp'])
                    abv40hpCnt += 1
            if float(row['level']) < 40.0:
                if row['atk'] != 'NaN':
                    bel40atkSum += float(row['atk'])
                    bel40atkCnt += 1
                if row['def'] != 'NaN':
                    bel40defSum += float(row['def'])
                    bel40defCnt += 1
                if row['hp'] != 'NaN':
                    bel40hpSum += float(row['hp'])
                    bel40hpCnt += 1
        abv40atkavg = round(abv40atkSum/abv40atkCnt, 1)
        abv40defavg = round(abv40defSum/abv40defCnt, 1)
        abv40hpavg = round(abv40hpSum/abv40hpCnt, 1)
        bel40atkavg = round(bel40atkSum/bel40atkCnt, 1)
        bel40defavg = round(bel40defSum/bel40defCnt, 1)
        bel40hpavg = round(bel40hpSum/bel40hpCnt, 1)
        for row in data:
            if float(row['level']) >= 40.0:
                if row['atk'] == 'NaN':
                    row['atk'] = str(abv40atkavg)
                if row['def'] == 'NaN':
                    row['def'] = str(abv40defavg)
                if row['hp'] == 'NaN':
                    row['hp'] = str(abv40hpavg)
            if float(row['level']) < 40.0:
                if row['atk'] == 'NaN':
                    row['atk'] = str(bel40atkavg)
                if row['def'] == 'NaN':
                    row['def'] = str(bel40defavg)
                if row['hp'] == 'NaN':
                    row['hp'] = str(bel40hpavg)
    
    with open('pokemonResult.csv', 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return data

    pass

def personality(f):
    persite = defaultdict(list)
    with open(f) as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for row in data:
            if row['personality'] not in persite[row['type']]:
                persite[row['type']].append(row['personality'])
    with open('pokemon4.txt', 'w') as outfile:
        for key in persite:
            outfilds = []
            outfilds.append(key + ': ')
            for value in persite[key]:
                outfilds.append(value)
            outfile.write(''.join(outfilds[:1]))
            outfile.write(', '.join(outfilds[1:])+'\n')
    return persite

    pass

def average(f):
    persite = defaultdict(list)
    with open(f) as file:
        reader = csv.DictReader(file)
        data = list(reader)
        hpsum = 0
        hpcount = 0
        stagethree = [(index,row) for index,row in enumerate(data) if float(row['stage']) == 3.0]
        for index,row in stagethree:
            hpsum += float(row['hp'])
            hpcount += 1
        avghp = round(hpsum / hpcount)
        with open('pokemon5.txt', 'w') as outfile:
            outfilds = []
            outfilds.append('Average hit point for Pokemons of stage 3.0 = ' + str(avghp))
            outfile.write(''.join(outfilds))

        return avghp

def main():
    wow = readem('pokemonTrain.csv')
    woah = fillmissing('pokemonTrain.csv')
    persons = personality('pokemonResult.csv')
    avghp = average('pokemonResult.csv')

    
    pass
    
main()
