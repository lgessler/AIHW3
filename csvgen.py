from random import shuffle, choice
import string
import os
import sys

if len(sys.argv) < 2:
    print("Usage: \t $ python csvgen.py <NUM FILES> <NUM ITEMS>")
    sys.exit(1)

NUM_ROUNDS = 10
LENGTH = int(sys.argv[2])
NUM_CSVS = int(sys.argv[1])
PATH = '%s-items' % LENGTH

# clean previous cases
for i in os.listdir(PATH):
    os.remove(os.path.join(PATH,i))

# write new ones
words = open('words','r').read().split('\n')
words = [filter(lambda x: x in string.printable, s).lower() for s in words if "'" not in s]
words = [choice(words) for i in range(LENGTH)]

for i in range(NUM_CSVS):
    order1 = [str(i) for i in range(1,LENGTH+1)]
    order2 = [str(i) for i in range(1,LENGTH+1)]
    shuffle(order1)
    shuffle(order2)

    with open('%s/%s_%s_%s.csv'%(PATH,choice(words),LENGTH,choice(words)),'w') as f:
        f.write(str(NUM_ROUNDS) + '\n')
        for i in range(LENGTH):
            f.write(', '.join([words[i], order1[i], order2[i]]) + '\n')

