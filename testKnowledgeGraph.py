import time
import csv

from utils import knowledgeGraph as kg

save = 'test.json'
G = kg.Graph()

G.loadJson(save)

startTime = time.time()

# G.loadRawText("corpus/ScannerDarkly.txt")

# with open('corpus/blogtext.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     count = 0
#     try:
#         for row in reader:
#             count += 1
#             G.loadRawText(row['text'], False)
#     except:
#         pass


# G.saveJson(save)

#print(G.generateSequence())

print(G.getWordsByFrequency(30))
print("time: ", time.time()-startTime)
