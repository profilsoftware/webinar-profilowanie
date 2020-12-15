import csv
import gzip


@profile
def find_title_in_file(title, filename):
    categories = []
    with gzip.open(filename, 'rt') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row[2] == title:
                categories = row[-1]
    return categories




print(find_title_in_file("The Root of Evil", "title.basics-3m.tsv.gz"))
pass

