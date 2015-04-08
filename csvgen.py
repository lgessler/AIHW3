from random import shuffle, choice
import string

NUM_ROUNDS = 10
LENGTH = 7

words = open('/usr/share/dict/words','r').read().split('\n')
words = [filter(lambda x: x in string.printable, s) for s in words if "'" not in s]

order1 = [str(i) for i in range(1,LENGTH+1)]
order2 = [str(i) for i in range(1,LENGTH+1)]
shuffle(order1)
shuffle(order2)

with open('test_cases/%s_%s_%s.csv'%(choice(words),LENGTH,choice(words)),'w') as f:
    f.write(str(NUM_ROUNDS) + '\n')
    for i in range(LENGTH):
        f.write(', '.join([choice(words), order1[i], order2[i]]) + '\n')

print "Wrote new csv file to test_cases"
