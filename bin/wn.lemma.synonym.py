## This program needs nltk 2.0

import sys, itertools
from nltk.corpus import wordnet as wn


## Write axioms of synsets and lemmas.
def getSynonyms(pos):
    print ' -> getting synonyms (pos=%s)' % (pos)
    out = []
    
    is_multi_word = lambda l: ('-' in l.name) or ('_' in l.name)
    
    for ss in list(wn.all_synsets(pos)):
        idx = 0
        for l1, l2 in itertools.combinations(ss.lemmas, 2):

            # MULTI-WORD EXPRESSIONS ARE EXCLUDED!
            if is_multi_word(l1) or is_multi_word(l2):
                continue
            
            kb = '(B (name synset.%s.%02d) ' % (ss.name, idx)

            if pos == 'n':
                kb += '(<=> (%s-nn x) (%s-nn x))' % (l1.name, l2.name)
            elif pos == 'v':
                kb += '(<=> (%s-vb e) (%s-vb e))' % (l1.name, l2.name)
            elif pos == 'a':
                kb += '(<=> (%s-jj e) (%s-jj e))' % (l1.name, l2.name)
            elif pos == 'r':
                kb += '(<=> (%s-rb e) (%s-rb e))' % (l1.name, l2.name)
            
            kb += ')'
            out.append(kb)
            idx += 1

    return out


def main():
    with open('%s/wn.lemma.synset.lisp' % sys.argv[1], 'w') as fo:
        for pos in ('n', 'v', 'a', 'r'):
            for ax in getSynonyms(pos):
                fo.write(ax + '\n')
            fo.write('\n')

    
if(__name__=='__main__'):
    main()
