# -*- coding: UTF-8 -*-
# author: ailin
# output some random numbers to test.txt

import random

def main():
    f = open("test.txt", "w")
    for k in xrange(1, 200):
        for num in random.sample([i for i in xrange(8)], 8):
            f.writelines(str(num) + " ")
        f.writelines("\r\n")
    f.close()

if __name__ == "__main__":
    main()