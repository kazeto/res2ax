## This program needs nltk 2.0

import sys
from nltk.corpus import wordnet as wn


## Write axioms of hypernym.
def getHypernyms(pos):
    print ' -> getting hypernyms (pos=%s)' % pos
    out = []
    
    for ss in list(wn.all_synsets(pos)):            
        idx = 0
            
        for hyp in ss.hypernyms():                
            kb = \
               '(B (name hypernym.%s.%02d) ' % (ss.name, idx) + \
               '(=> (synset.%s e) (synset.%s e)))' % \
               (ss.name, hyp.name)
            out.append(kb)
            idx += 1
                
    return out


def main():
    with open('%s/wn.hypernym.lisp' % sys.argv[1], 'w') as fo:
        for pos in ('n', 'v'):
            for ax in getHypernyms(pos):
                fo.write(ax + '\n')
            fo.write('\n')

    
if(__name__=='__main__'):
    main()
