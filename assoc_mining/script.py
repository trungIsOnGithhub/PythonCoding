from pycaret.datasets import get_data
from pycaret.arules import *

dataset = get_data("france")

print(dataset)

s = setup(data = data, transaction_id = 'InvoiceNo', item_id = 'Description')

print(s)

arules = create_model(metric='confidence', threshold=0.5, min_support=0.05)

print(arules)

plot_model(arules, plot = '2d')