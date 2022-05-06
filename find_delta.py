import anime
import csv
import find_avg


def main():
    data1 = find_avg.read_csv('test.csv')
    data2 = find_avg.read_csv('naive_prediction.csv')

    sum = 0
    count = 0

    for d1, d2 in zip(data1, data2):
        if float(d1.rating) > 0 and float(d2.rating) > 0:
            sum += abs((float(d1.rating) - float(d2.rating)))
            count += 1

    avg = sum / count
    print('The average delta is {:.2f}'.format(avg))



if __name__=="__main__":
    main()

