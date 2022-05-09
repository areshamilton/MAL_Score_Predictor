import csv
import anime

# Reads csv contents and returns as a list of Anime objects
def read_csv(filename):
    result = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        #next(csvfile) #skips the header
        for row in reader:
            temp = anime.Anime()
            temp.title = row[0]
            temp.info = set(row[2:])
            temp.rating = row[1].lstrip(' \'').rstrip('\'')
            result.append(temp)
    return result

# Returns average rating shows in filename
def find_avg(filename):
    data = read_csv(filename)
    sum = 0
    count = 0
    for each in data:
        value = float(each.rating)
        if value > 0:
            sum += value
            count += 1

    print(sum)
    return sum / count

def main():
    file = 'predictions.csv'
    avg = find_avg(file)
    print('The average rating for {0} is: {1:.2f}'.format(file,avg))


if __name__=="__main__":
    main()