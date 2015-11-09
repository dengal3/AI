# -*- coding: UTF-8 -*-
# author: ailin
# output some random numbers to test.txt

import random
import sys
import getopt

def random_generate():
    opts = getopt.getopt(sys.argv[1:], "n:t:", [])
    amount = 0
    print opts
    t = ""
    for op, value in opts[0]:
        if op == '-n':
            amount = int(value)
        elif op == '-t':
            t = value
    if t == "queen":
        eight_queens_random_generate(amount)


def eight_queens_random_generate(amount):
    f = open("test.txt", "w")
    for k in xrange(amount):
        for num in random.sample([i for i in xrange(8)], 8):
            f.writelines(str(num) + " ")
        f.writelines("\r\n")
    f.close()


if __name__ == "__main__":
    eight_queens_random_generate()