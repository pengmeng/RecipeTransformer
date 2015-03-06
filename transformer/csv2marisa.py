__author__ = 'mengpeng'
import sys
import os
import marisa_trie


def tomarisa(filename):
    outfilename = filename if '/' not in filename else filename.split('/')[-1]
    outfilename = outfilename.split('.')[0]
    if not os.path.exists('./marisa'):
            os.mkdir('./marisa')
    outfilename = './marisa/' + outfilename + '.marisa'
    valuelist = []
    with open(filename, 'r') as infile:
        for line in infile:
            l = line.strip().split(',')
            try:
                valuelist.extend([unicode(x.strip()) for x in l if x])
            except UnicodeDecodeError:
                print('Unexpected character occured in file. Please remove them with English characer.')
    trie = marisa_trie.Trie(valuelist)
    trie.save(outfilename)
    print('{0} items read from {1} and saved as {2} with {3} items.'
          .format(len(valuelist), filename, outfilename, len(trie.items())))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing arguments. Using like this:')
        print('python csv2marisa.py csvfile1 csvfile2 ..')
    else:
        for each in sys.argv[1:]:
            tomarisa(each)