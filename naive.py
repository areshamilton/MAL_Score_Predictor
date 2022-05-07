import csv

class Anime():
    title = ''
    info = {}
    rating = 0.0

# Reads csv contents and returns as a list of Anime objects
def read_csv(filename):
    result = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        #next(csvfile) #skips the header
        for row in reader:
            anime = Anime()
            anime.title = row[0]
            anime.info = set(row[2:])
            anime.rating = row[1]
            result.append(anime)
    return result

def main():
    
    filename = 'test.csv'
    data = read_csv(filename)

    with open('fix_rating_test.csv', 'a') as writer:
        for each in data:
            line = []
            line.append(each.title)
            line.append(each.rating)
            line.append(each.info)
            print(str(line).strip('[]""'))
            #writer.write(str(line).strip('[]')+'\n')


if __name__=="__main__":
    main()