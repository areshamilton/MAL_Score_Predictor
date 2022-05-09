import anime
import csv
import find_avg


def main():
    data1 = find_avg.read_csv('test.csv')
    data2 = find_avg.read_csv('predictions_125.csv')

    sum = 0
    mean = 0
    count = 0

    for d1, d2 in zip(data1, data2):
        if float(d1.rating) > 0 and float(d2.rating) > 0:
            sum += abs((float(d1.rating) - float(d2.rating)))
            mean += abs(((float(d1.rating)) - float(d2.rating)) / float(d1.rating))
            count += 1

    avg = sum / count
    mean_avg = mean / count
    print('The average delta is {:.2f}'.format(avg))
    print('The mean absolute percentage error is %{:.2f}'.format(mean_avg*100))



if __name__=="__main__":
    main()

