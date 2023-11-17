import csv
import random
from ku_market_place.models import Product

decimal = [0.00, 0.25, 0.50, 0.75]


with open('ku_market_place/data/product-data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for line in csv_reader:
        index = random.randint(0, 3)
        x = float(format(random.randint(100, 10000) + decimal[index], '.2f'))
        formatted_x = '{:.2f}'.format(x)

        Product.objects.create(
            gender = line[1],
            masterCategory = line[2],
            subCategory = line[3],
            articleType = line[4],
            baseColour = line[5],
            season = line[6],
            year = int(line[7]),
            usage = line[8],
            productDisplayName = line[9],
            productPrice = formatted_x
        )
        Product.save()

