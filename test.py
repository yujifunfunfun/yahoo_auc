import csv
import re

with open('item.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    l = [row for row in reader]

for i in l:
    description = i[2]
    p = r'<font color="#660000" size="3">(.*)<br><br></font><br><br></td></tr></table> </td>'
    description = re.search(p, description).group(1)
    description = description.replace('<br>','\n')
    description = re.sub('<(.*)>','',description)
    print(description)


