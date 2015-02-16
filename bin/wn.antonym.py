## This program needs nltk 2.0

import sys
from nltk.corpus import wordnet as wn


## Write axioms of antonyms.
def getAntonyms(pos):
    print ' -> getting antonyms (pos=%s)' % pos
    out = []
    
    for ss in list(wn.all_synsets(pos)):
        idx = 0
        for lemma in ss.lemmas:                
            for ant in lemma.antonyms():
                kb = "(B (name antonym.%s.%d) " % (lemma.name, idx)
                kb += getConsystency(lemma, ant, pos) + ')'
                out.append(kb)
                idx += 1
                    
    return out


def getConsystency(lemma, antonym, pos):
    if pos == 'n':
        return '(xor (%s-nn e) (%s-nn e))' % (antonym.name, lemma.name)
    elif pos == 'v':
        return '(xor (%s-vb e) (%s-vb e))' % (antonym.name, lemma.name)
    elif pos == 'a':
        return '(xor (%s-jj e) (%s-jj e))' % (antonym.name, lemma.name)
    elif pos == 'r':
        return '(xor (%s-rb e) (%s-rb e))' % (antonym.name, lemma.name)
                    

def main():
    with open('%s/wn.antonym.lisp' % sys.argv[1], 'w') as fo:
        for pos in ('n', 'v', 'a', 'r'):
            for a in getAntonyms(pos):
                fo.write(a + '\n')
            fo.write('\n')

    
if(__name__=='__main__'):
    main()
