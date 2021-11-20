import csv

source_file = open('data/presidents-wikipedia-clean.txt', 'r')
Lines = source_file.readlines()

def convert_date(s):
  if not s:
    return '2021-11-20'
  pieces = s.split('|')
  year = pieces[0]
  month = pieces[1] if int(pieces[1]) >= 10 else '0' + pieces[1]
  day = pieces[2] if int(pieces[2]) >= 10 else '0' + pieces[2]
  return year + '-' + month + '-' + day

presidents=[ ['Name', 'Lastname', 'Born', 'Start', 'End'] ]
next_name = 0
for index, line in enumerate(Lines):
  if line.strip() == '--' or index < next_name:
    continue
  else:
    who = line.strip()
    born = Lines[index+1].strip()
    start = Lines[index+2].strip()
    end = Lines[index+3].strip()
    next_name = index+4
    president = who.split("|")[::-1] + [convert_date(born), convert_date(start), convert_date(end)]
    presidents.append(president)

print(presidents)

with open('data/presidents.csv', mode='w') as presidents_file:
  presidents_writer = csv.writer(presidents_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for president in presidents:
    presidents_writer.writerow(president)
