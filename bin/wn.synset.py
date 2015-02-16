## This program needs nltk 2.0

import sys
from nltk.corpus import wordnet as wn


## Write axioms of synsets and lemmas.
def getSynsets(pos):
    print ' -> getting synsets (pos=%s)' % (pos)
    out = []
    
    for ss in list(wn.all_synsets(pos)):
        idx = 0
        for lemma in ss.lemmas:                
            kb = '(B (name synset.%s.%02d) ' % (ss.name, idx)
            kb += getAxiom(ss, lemma, pos) + '))'
            out.append(kb)
            idx += 1

    return out


def getAxiom(synset, lemma, pos):
    if pos == 'n':
        return '(=> (synset.%s x) (%s-nn x)' % (synset.name, lemma.name)
    elif pos == 'v':
        return '(=> (synset.%s e) (%s-vb e)' % (synset.name, lemma.name)
    elif pos == 'a':
        return '(=> (synset.%s e) (%s-jj e)' % (synset.name, lemma.name)
    elif pos == 'r':
        return '(=> (synset.%s e) (%s-rb e)' % (synset.name, lemma.name)


def main():
    with open('%s/wn.synset.lisp' % sys.argv[1], 'w') as fo:
        for pos in ('n', 'v', 'a', 'r'):
            for ax in getSynsets(pos):
                fo.write(ax + '\n')
            fo.write('\n')

    
if(__name__=='__main__'):
    main()
