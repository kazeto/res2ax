## This program needs nltk 2.0

import sys
from nltk.corpus import wordnet as wn


## Write axioms of hypernym.
def getHypernyms(pos):
    print ' -> getting hypernyms (pos=%s)' % pos
    out = []

    is_multi_word = lambda l: ('-' in l.name) or ('_' in l.name)
    
    for ss in list(wn.all_synsets(pos)):
        idx = 0
            
        for hyp in ss.hypernyms():
            for l1 in ss.lemmas:
                if is_multi_word(l1): continue;
                
                for l2 in hyp.lemmas:
                    if is_multi_word(l2): continue;
            
                    kb = '(B (name hypernym.%s.%02d) ' % (ss.name, idx)

                    if pos == 'n':
                        kb += '(=> (%s-nn x) (%s-nn x))' % (l1.name, l2.name)
                    elif pos == 'v':
                        kb += '(=> (%s-vb e) (%s-vb e))' % (l1.name, l2.name)
                    
                    out.append(kb + ')')
                    idx += 1
                
    return out


def main():
    with open('%s/wn.lemma.hypernym.lisp' % sys.argv[1], 'w') as fo:
        for pos in ('n', 'v'):
            for ax in getHypernyms(pos):
                fo.write(ax + '\n')
            fo.write('\n')

    
if(__name__=='__main__'):
    main()
