import csv

class Anime():
    title = ''
    info = {}
    rating = 0.0

# Reads csv contents and returns as a list of the anime object
def read_csv(filename):
    result = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        next(csvfile) #skips the header
        for row in reader:
            anime = Anime()
            anime.title = row[1]
            anime.info = set(row[3:])
            anime.rating = row[2]
            result.append(anime)
    return result

# Compares the set of info for a and b and returns the intesect
def compare(a, b):
    return len(a.info.intersection(b.info))


def main():
    training = read_csv('training.csv')
    testing = read_csv('test.csv')
    for test in testing:

        #this section should be in parallel
        for train in training:
            value = compare(train,test)
            print("Comparing \'{0}\' vs \'{1}\'. Result: {2}".format(test.title, train.title, value))


if __name__=="__main__":
    main()