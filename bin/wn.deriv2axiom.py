# -*- coding: utf-8 -*-

import sys
from itertools import combinations

INPUT = '%s/wn.derivation.tsv' % sys.argv[1]
OUTPUT = '%s/wn.derivation.lisp' % sys.argv[1]


CONVENTION = {
    'NN_ADJ'   : ['(=> ($W1 x) (^ ($W2 e) (nsubj e x)) :deriv)'],
    'ADJ_NN_1' : ['(=> ($W1 e) (^ ($W2 e.n) (nsubj e e.n)) :deriv)'],
    'ADJ_NN_2' : ['(=> ($W1 e) ($W2 e) :deriv)'],
    'VB_ADJ_1' : ['(=> (^ ($W1 e) (nsubj e x)) ($W2 x) :deriv)'],
    'VB_ADJ_2' : ['(=> (^ ($W1 e) (dobj e y)) ($W2 y) :deriv)'],
    # 'VB_ADJ_3' : ['(=> ($W1 e) ($W2 e.dr) :deriv)'],
    'VB_ADJ'   : ['(=> (^ ($W1 e1) (nsubj x)) (^ ($W2 e2) (nsubj x)) :deriv)',
                  '(=> (^ ($W1 e1) (dobj y)) (^ ($W2 e2) (nsubj y)) :deriv)'],
    'VB_NN_EVN' : ['(=> ($W1 e1) ($W2 e1) :deriv)'],
    'VB_NN_AGT' : ['(=> (^ ($W1 e) (nsubj x)) ($W2 x) :deriv)'],
    'VB_NN_OBJ' : ['(=> (^ ($W1 e) (dobj y)) ($W2 y) :deriv)'],
    # 'NN_VB' : ['(=> ($W1 x) ($W2 e) :deriv)'],
    # 'NN_NN' : ['(=> ($W1 x) ($W2 y) :deriv)'],
    # 'NN_NN_2' : ['(=> ($W1 x) ($W2 y) :deriv)']
    }


def formatWord(w):
    splitted = w.rsplit('.', 1)
    
    if len(splitted) != 2:
        print '#ERROR: ', w
        raise ValueError
    
    word = splitted[0]
    pos = splitted[1]

    if pos == 'n':
        return '%s-nn' % word
    elif pos == 'v':
        return '%s-vb' % word
    elif pos == 'a':
        return '%s-jj' % word
    elif pos == 'r':
        return '%s-rb' % word
    else:
        print '#ERROR:', w
        raise ValueError


def convertDerivationToAxiom(w1, w2, deriv_type):
    if not CONVENTION.has_key(deriv_type):
        return ''

    word1 = formatWord(w1)
    word2 = formatWord(w2)
    out = []
    
    for i, conv in enumerate(CONVENTION[deriv_type]):
        axiom = conv.replace('$W1', word1).replace('$W2', word2)
        out.append('(B (name wn.deriv.%s.%s.%s.%d) %s)' %
                   (deriv_type.lower(), word1, word2, i, axiom))
        
    return '\n'.join(out)


def convert(filename):
    print ' -> converting derivations'
    
    fout = open(OUTPUT, 'w')
    with open(INPUT) as fin:
        for line in fin:
            spl = line.strip().split('\t')
            if len(spl) == 3:
                disp = convertDerivationToAxiom(spl[0], spl[1], spl[2])
                if disp:
                    fout.write(disp + '\n')
    fout.close()


def main():
    convert(OUTPUT)
                
    
if(__name__=='__main__'):
    main()
