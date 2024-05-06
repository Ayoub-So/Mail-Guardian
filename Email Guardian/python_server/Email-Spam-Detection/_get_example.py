import csv




print('spam examples : \n')
with open("spam.csv" ,'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        if row[0] == 'spam':
            print(row[1])
            print("\n\n")

