import csv
import gzip
import re

# @profile
def find_the_in_title(filename):
    count = 0
    pattern = re.compile(r"\bthe\b", re.IGNORECASE)
    with gzip.open(filename, 'rt') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if pattern.search(row[2]):
                count += 1
    return count


print(find_the_in_title("title.basics-3m.tsv.gz"))
