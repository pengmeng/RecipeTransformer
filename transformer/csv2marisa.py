__author__ = 'mengpeng'
import sys
import os
import marisa_trie


def outfile(filename):
    outfilename = filename if '/' not in filename else filename.split('/')[-1]
    outfilename = outfilename.split('.')[0]
    if not os.path.exists('./marisa'):
            os.mkdir('./marisa')
    outfilename = './marisa/' + outfilename + '.marisa'
    return outfilename


def tomarisa(filename):
    outfilename = outfile(filename)
    valuelist = []
    with open(filename, 'r') as infile:
        for line in infile:
            l = line.strip().split(',')
            try:
                valuelist.extend([unicode(x.strip().lower()) for x in l if x])
            except UnicodeDecodeError:
                print('Unexpected characters occured in file. Please remove them with English characers.')
    trie = marisa_trie.Trie(valuelist)
    trie.save(outfilename)
    print('{0} items read from {1} and saved as {2} with {3} items.'
          .format(len(valuelist), filename, outfilename, len(trie.items())))


def tobytestrie(filename):
    outfilename = outfile(filename)
    keys, values = [], []
    with open(filename, 'r') as infile:
        for line in infile:
            l = line.strip().split(',')
            try:
                keys.append(unicode(l[0].strip().lower()))
                values.append(bytes.encode(l[1].strip().lower()))
            except UnicodeDecodeError:
                print('Unexpected characters occured in file. Please remove them with English characers.')
    trie = marisa_trie.BytesTrie(zip(keys, values))
    trie.save(outfilename)
    print('{0} items read from {1} and saved as {2} with {3} items.'
          .format(len(keys), filename, outfilename, len(trie.items())))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing arguments. Using like this:')
        print('python csv2marisa.py [bytes] csvfile1 csvfile2 ..')
        print('If the second argument is "bytes", will build a BytesTrie.')
    elif sys.argv[1] == 'bytes':
        for each in sys.argv[2:]:
            tobytestrie(each)
    else:
        for each in sys.argv[1:]:
            tomarisa(each)