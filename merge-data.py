import csv
from datetime import datetime

def read_csv(filename):
  records = []
  with open(filename, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
      records.append(row)
  return records

def expectancy_value(expectancies, year):
  values = [y for [x,y] in expectancies if x == year]
  return values[0]

def interpolate_expectancies(expectancies):
  filtered = [[int(x[2]), float(x[4])] for x in expectancies if x[1] == "USA"]
  output = []
  for year in range(1800, 2015):
    closest_smaller = max([x for [x,y] in filtered if x < year])
    closest_bigger = min([x for [x,y] in filtered if x >= year])
    if closest_bigger == year:
      output.append([year, expectancy_value(filtered, year)])
    else:
      factor =  float(year - closest_smaller) / float(closest_bigger - closest_smaller)
      output.append([year, (1 - factor) * expectancy_value(filtered, closest_smaller) + factor * expectancy_value(filtered, closest_bigger) ])
    print(year, closest_smaller, closest_bigger)
  return output

def expand_presidents(presidents):
  output = {}
  for year in range(1861, 2021+1):
    ref_date = str(year)+'-11-20'
    closest_smaller = max([started for [lastname, firstname, born, started, ended] in presidents if started < ref_date])
    president = [x for x in presidents if x[3] == closest_smaller][0]
    date_ref_date = datetime.strptime(ref_date, "%Y-%m-%d")
    date_born = datetime.strptime(president[2], "%Y-%m-%d")
    age = (date_ref_date - date_born).days / 365.25
    birth_year = date_born.year
    output[year] = {
      'year': year,
      'lastname': president[0],
      'firstname': president[1],
      'age': age,
      'birth_year': birth_year
    }
    print(year, output[year]["lastname"], output[year]["firstname"], output[year]["age"], output[year]["birth_year"])
  return output

presidents = read_csv('data/presidents.csv')
expectancies = read_csv('data/life-expectancy-at-birth-by-sex.csv')

expectancies = interpolate_expectancies(expectancies)

presidents = expand_presidents(presidents)

records = [ ["Year", "Lastname", "Firstname", "Age", "BirthYear", "LifeExpectancy", "Exceeded"] ]
for president in presidents.values():
  print(president)
  records.append([
    president["year"],
    president["lastname"],
    president["firstname"],
    president["age"],
    president["birth_year"],
    expectancy_value(expectancies, president["birth_year"]),
    president["age"] - expectancy_value(expectancies, president["birth_year"])
  ])

with open('data/presidents-age-life-expectancy.csv', mode='w') as records_file:
  records_writer = csv.writer(records_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for record in records:
    records_writer.writerow(record)
