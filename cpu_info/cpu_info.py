import urllib2
from bs4 import BeautifulSoup

response = urllib2.urlopen('http://www.cpu-world.com/info/Intel/Intel_Xeon.html')
html = response.read()
soup = BeautifulSoup(html)

table = soup.select('#gs_sortable')[0]
rows = table.findChildren(['th', 'tr'])

for row in rows:
    cells = row.findChildren('td')

    for i, cell in enumerate(cells):
        value = cell.string

        if value is None:
            print ',',
            continue

        print value,
        if i < len(cells) -1:
            print ',',

    print ' '