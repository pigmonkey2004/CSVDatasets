import math
import re
import csv
from collections import defaultdict
from collections import Counter

def readem(f):
    with open(f) as file:
        reader = csv.DictReader(file)
        data = list(reader)
        latitudeSum = 0
        latitudeCount = 0
        longitudeSum = 0
        longitudeCount = 0
        for row in data:
             if row['age'].__contains__('-'):
                nums = re.findall(r'\d+', row['age'])
                start = int(nums[0])
                end = int(nums[1])
                avg = (start + end) / 2
                row['age'] = round(avg)
             for date in ['date_onset_symptoms', 'date_admission_hospital', 'date_confirmation']: 
                sel = nums = re.findall(r'\d+', row[date])
                dd = sel[0]
                mm = sel[1]
                yyyy = sel[2]
                newdate = mm + '.' + dd + '.' + yyyy
                row[date] = newdate
        for row in data:  
            if row['latitude'] != 'NaN':
                latitudeSum += float(row['latitude'])
                latitudeCount += 1
            if row['longitude'] != 'NaN':
                longitudeSum += float(row['longitude'])
                longitudeCount += 1
        latitudeavg = round(latitudeSum/latitudeCount, 2)  
        longitudeavg = round(longitudeSum/longitudeCount, 2)  
        for row in data:
            if row['latitude'] == 'NaN':
                row['latitude'] = latitudeavg
            if row['longitude'] == 'NaN':
                row['longitude'] = longitudeavg
        province_city_counts = defaultdict(lambda: defaultdict(int))

        for row in data:
            province = row['province']
            city = row['city']
            if province != 'NaN' and city != 'NaN':
                province_city_counts[province][city] += 1

        # Determine the most occurring city for each province
        most_common_cities = {}
        for province, cities in province_city_counts.items():
            most_common_city = max(cities, key=lambda x: (cities[x], x), default=None)
            most_common_cities[province] = most_common_city

        for row in data:
            if row['city'] == 'NaN':
                row['city'] = most_common_cities[row['province']]

        province_symptom_counter = defaultdict(lambda: defaultdict(int))
        for row in data:
            province = row['province']
            symptom = row['symptoms']
            if province != 'NaN' and symptom != 'NaN':
                if row['symptoms'].__contains__(';'):
                    symps = re.findall('[a-zA-Z]+', row['symptoms'])
                    for symp in symps:
                        province_symptom_counter[province][symp] += 1
                else:
                    province_symptom_counter[province][symptom] += 1
         
        most_common_symptoms = {}
        for province, symptoms in province_symptom_counter.items():
            most_common_symptom = max(symptoms, key=lambda x: (symptoms[x], x), default=None)
            most_common_symptoms[province] = most_common_symptom

        for row in data:
            if row['symptoms'] == 'NaN':
                row['symptoms'] = most_common_symptoms[row['province']]

    with open('covidResult.csv', 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return data
    pass

def main():
    wow = readem('covidTrain.csv')
    pass
    
main()