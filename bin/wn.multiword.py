## This program needs nltk 2.0.

import sys
from nltk.corpus import wordnet as wn


## Enumerates multi-words in WordNet.
def getMultiWords(pos):
    print ' -> getting multi-words (pos=%s)' % pos
    multi_words = set()
    
    for ss in list(wn.all_synsets(pos)):
        for lemma in ss.lemmas:
            if lemma.name.find('_') >= 0:
                multi_words.add(lemma.name)

    return multi_words


def main():
    with open('%s/wn.multiword.tsv' % sys.argv[1], 'w') as fo:
        for pos in ('n', 'v', 'a', 'r'):
            for mw in sorted(getMultiWords(pos)):
                fo.write('%s\t%s\n' % (mw, pos))
            fo.write('\n')
            
    
if(__name__=='__main__'):
    main()
