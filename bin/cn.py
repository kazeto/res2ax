# -*- coding: utf-8 -*-

import sys
from nltk.corpus import wordnet as wn


CN_FILES = sys.argv[1:-1]
OUTPUT_DIR = sys.argv[-1]

CONVENTIONS = {
    'Antonym|nn|nn' : '(xor ($W1 x) ($W2 x))',
    'Antonym|vb|vb' : '(xor ($W1 e) ($W2 e))',
    'Antonym|jj|jj' : '(xor ($W1 e) ($W2 e))',
    'Antonym|rb|rb' : '(xor ($W1 e) ($W2 e))',
    'NotIsA|nn|nn' : '(xor ($W1 x) ($W2 x))',
    'NotIsA|vb|vb' : '(xor ($W1 e) ($W2 e))',
    'NotIsA|jj|jj' : '(xor ($W1 e) ($W2 e))',
    'NotIsA|rb|rb' : '(xor ($W1 e) ($W2 e))',
    'AtLocation|nn|nn' : '(=> ($W1 x) (^ ($W2 y) (in-prep d x y)))',
    'HasPrerequisite|nn|nn' : '(=> ($W1 x) ($W2 y))',
    'HasPrerequisite|vb|nn' : '(=> ($W1 e1) (^ ($W2 x) (own-vb e2) (dobj d e2 x)))',
    'HasPrerequisite|vb|vb' : '(=> (^ ($W1 e1) (nsubj d1 e1 x)) (^ ($W2 e2) (nsubj d2 e2 x)))',
    'HasProperty|nn|nn' : '(=> ($W1 e1 x1) ($W2 e2 x2))',
    'HasProperty|vb|nn' : '(=> ($W1 e1 x1 x2) ($W2 e2 x3))',
    'HasProperty|vb|vb' : '(=> ($W1 e1 x y) ($W2 e2 x y))',
    'IsA|nn|nn' : '(=> ($W1 x) ($W2 x))',
    'IsA|vb|vb' : '(=> ($W1 e) ($W2 e))',
    'HasA|nn|nn' : '(=> ($W1 x1) (^ ($W2 x2) (own-vb e) (nsubj d1 e x1) (dobj d2 e x2)))',
    'LocatedNear|nn|nn' : '(=> ($W1 e1 x) ($W2 e2 y))',
    'LocatedNear|nn|vb' : '(=> ($W1 e1 x) ($W2 e2 y z))',
    'LocatedNear|vb|vb' : '(=> ($W1 e1 x1 y1) ($W2 e2 x2 y2))',
    'PartOf|nn|nn' : '(=> ($W1 e1 x1) (^ ($W2 e2 x2) (own-vb e3 x2 x1)))',
    'RelatedTo|nn|nn' : '(=> ($W1 e1 x1) ($W2 e2 x2))',
    'RelatedTo|nn|jj' : '(=> ($W1 e1 x1) ($W2 e2 x2))',
    'RelatedTo|vb|nn' : '(=> ($W1 e1 x1 x2) ($W2 e2 x3))',
    'RelatedTo|vb|jj' : '(=> ($W1 e1 x1 x2) ($W2 e2 x3))',
    'RelatedTo|jj|jj' : '(=> ($W1 e1 x1) ($W2 e2 x2))',
    'Synonym|nn|nn' : '(=> ($W1 e x) ($W2 e x))',
    'Synonym|vb|vb' : '(=> ($W1 e x y) ($W2 e x y))',
    'Synonym|jj|jj' : '(=> ($W1 e x) ($W2 e x))',
    'Synonym|rb|rb' : '(=> ($W1 e x) ($W2 e x))',
    'SimilarTo|vb|vb' : '(=> ($W1 e x y) ($W2 e x y))',
    'SimilarTo|jj|jj' : '(=> ($W1 e x) ($W2 e x))',
    'Causes|nn|nn' : '(=> ($W1 e1 x) ($W2 e2 y))',
    'Causes|vb|nn' : '(=> ($W1 e1 x y) ($W2 e2 z))',
    'Causes|vb|vb' : '(=> ($W1 e1 x y) ($W2 e2 x y))',
    'InstanceOf|nn|nn' : '(=> ($W1 e1 x) ($W2 e2 x))'}

fouts = {}
counts = {}


class Entity:
    def __init__(self, line):
        spl = line.split('/')
        self.lang = spl[2]
        self.word = spl[3]
        self.pos = spl[4] if (len(spl) > 4) else self._guess_pos()
        self.sem = spl[5] if (len(spl) > 5) else ''

        if self.pos == 'n': self.pos = 'nn';
        if self.pos == 'v': self.pos = 'vb';
        if self.pos == 'a': self.pos = 'jj';
        if self.pos == 'r': self.pos = 'rb';

    def good(self):
        return (self.lang == 'en' and self.pos != '')

    def _guess_pos(self):
        nums = {}
        n = list(wn.synsets(self.word, 'n'))
        v = list(wn.synsets(self.word, 'v'))
        a = list(wn.synsets(self.word, 'a'))
        r = list(wn.synsets(self.word, 'r'))
        
        if n: nums['nn'] = len(n);
        if v: nums['vb'] = len(v);
        if a: nums['jj'] = len(a);
        if r: nums['rb'] = len(r);

        if nums:
            m = max(nums.values())
            out = [k for (k, n) in nums.iteritems() if n == m]
            return ';'.join(out)
        else:
            return ''


def process_sub(word1, pos1, word2, pos2, rel):
    key = '%s|%s|%s' % (rel, pos1, pos2)
    if not CONVENTIONS.has_key(key) or (word1 == word2 and pos1 == pos2):
        return

    if not fouts.has_key(rel):
        path = '%s/cn.%s.lisp' % (OUTPUT_DIR, rel)
        fouts[rel] = open(path, 'w')
        counts[rel] = 0
        
    axiom = CONVENTIONS[key] \
            .replace('$W1', '%s-%s' % (word1, pos1)) \
            .replace('$W2', '%s-%s' % (word2, pos2))
    name = 'cn.%s.%d' % (rel.lower(), counts[rel])

    fouts[rel].write('(B (name %s) %s)\n' % (name, axiom))
    counts[rel] += 1


def process(e1, e2, rel):
    for pos1 in e1.pos.split(';'):
        for pos2 in e2.pos.split(';'):
            process_sub(e1.word, pos1, e2.word, pos2, rel)
    

def main():
    for filename in CN_FILES:
        print ' -> processing', filename
        processed = 0

        with open(filename) as fin:
            for line in fin:
                splitted = line.split('\t')
                rel = splitted[1].split('/')[2]
                ent1 = Entity(splitted[2])
                ent2 = Entity(splitted[3])

                if ent1.good() and ent2.good():
                    process(ent1, ent2, rel)

                processed += 1
                if processed % 100 == 0:
                    sys.stdout.write('%d\r' % processed)
        
    for fo in fouts.itervalues():
        fo.close()

    
if(__name__=='__main__'):
    main()
