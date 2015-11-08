# -*- coding: UTF-8 -*-
# author: ailin
# output some random numbers to test.txt

import random
import sys

def main():
    f = open("test.txt", "w")
    for k in xrange(int(sys.argv[1])):
        for num in random.sample([i for i in xrange(8)], 8):
            f.writelines(str(num) + " ")
        f.writelines("\r\n")
    f.close()

if __name__ == "__main__":
    main()