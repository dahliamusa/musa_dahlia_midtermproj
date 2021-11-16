#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from itertools import combinations
from itertools import permutations
import pandas as pd

transactions = list()
items = list()
min_support = float()
min_confidence = float()

#Support equation
def calculate_support(freq):
    return (freq / len(transactions)) * 100

#Confidence equation
def calculate_confidence(A, B):
    return (support_itemset(A.union(B)) / support_itemset(A)) * 100

#Generates the first list of itemsets
def first_itemset():
    first = list()
    for item in items:
        freq = 0
        for transaction in transactions:
            if item in transaction:
                freq += 1
        support = calculate_support(freq)
        if support >= min_support:
            first.append([item])
    return first

#Receives current list of itemsets and generates next iteration of itemsets
def next_itemset(current, k):
    #Get a list of the idividual items in "current"
    items_c = list()
    for itemset in current:
        for item in itemset:
            if item not in items_c:
                items_c.append(item)
    items_c = sorted(items_c)

    #Generate candidates
    candidates = list(combinations(items_c, k))
    
    #Keep candidates with support greater than or equal to required minimum and return result
    next = list()
    for itemset in candidates:
        freq = 0
        for transaction in transactions:
            if set(itemset).issubset(set(transaction)):
                freq += 1
        support = calculate_support(freq)
        if support >= min_support:
            next.append(itemset)   
    return next
    
#Calculates support of an itemset
def support_itemset(itemset):
    freq = 0
    for i in range(0, len(transactions)):
        if set(itemset).issubset(transactions[i]):
            freq += 1
    return calculate_support(freq)

#Generates list of association rules
def generate_rules(frequent_itemsets):
    rules = list()
    for itemset in frequent_itemsets:
        for k in range(1, len(itemset)):
            for subset in combinations(itemset, k):
                A = set()
                B = set()
                for item in subset:
                    A.add(item)
                B = set(itemset) - A
                confidence = calculate_confidence(A, B)
                if confidence >= min_confidence:
                    rules.append(str(A) + " -> " + str(B) + '\t' + str(round(confidence, 2)) + '%')
    return rules

#Apriori algorithm
def apriori():
    frequent_itemsets = list()
    l1 = first_itemset()
    l2 = next_itemset(l1, 2)
    current = l2
    length = 3
    while(current):
        frequent_itemsets += current
        next = next_itemset(current, length)
        current = next
        length += 1
    return frequent_itemsets

#Input for dataset selection
print()
while True:
    dataset = input("Enter a number from the menu: \n1 - Amazon \n2 - Best Buy \n3 - K-Mart \n4 - Nike \n5 - Generic Data \n")
    if not dataset.isdigit() or (int(dataset) != 1 and int(dataset) != 2 and int(dataset) != 3 and int(dataset) != 4 and int(dataset) != 5):
            print("Input is not valid")
    else:
        break
dataset = int(dataset)
filename = str()
if dataset == 1:
    filename = "amazon.csv"
elif dataset == 2:
    filename = "bestbuy.csv"
elif dataset == 3:
    filename = "kmart.csv"
elif dataset == 4:
    filename = "nike.csv"
elif dataset == 5:
    filename = "generic.csv"

print()
print("You chose dataset located in: " + filename)

#Load data from csv file
df = pd.read_csv(filename, sep=",")
df = df.drop('Transaction ID', 1)
transactions = df.values.tolist()
for i in range(0, len(transactions)):
    transactions[i] = transactions[i][0].split(", ")
    for item in transactions[i]:
        if item not in items:
            items.append(item)

#Display list of items in dataset
print("Dataset has the following items:")
for i in range(0, len(items)):
    print(str(i + 1) + " - " + items[i])
print()

#Input for min support
while True:
    min_support = input("Enter the support value (scale 1 to 100): ")
    try:
        if float(min_support) < 1 or float(min_support) > 100:
            print("Input is not valid")
        else:
            min_support = float(min_support)
            break
    except ValueError:
        print("Input must be a number")
print()
    
#Input for min confidence
while True:
    min_confidence = input("Enter the confidence value (scale 1 to 100): ")
    try:
        if float(min_confidence) < 1 or float(min_confidence) > 100:
            print("Input is not valid")
        else:
            min_confidence = float(min_confidence)
            break
    except ValueError:
        print("Input must be a number")
print()

#Apriori implementation

#Print frequent itemsets with support
frequent_itemsets = apriori()
if len(frequent_itemsets) == 0:
    print("No frequent itemsets found")
else:
    print("Final frequent itemsets with support:")
    print("*********************************************************")
    count = 0
    for itemset in frequent_itemsets:
        count += 1
        support = support_itemset(itemset)
        print(str(count) + " - " + str(itemset) + '\t' + str(round(support, 2)) + '%')
    print()

    #Print association rules with confidence
    association_rules = generate_rules(frequent_itemsets)
    print("Final association rules with confidence: ")
    print("*********************************************************")
    count = 0
    for rule in association_rules:
        count += 1
        print(str(count) + " - " + rule)


# In[ ]:




