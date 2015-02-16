## This program needs nltk 2.0

import sys, re
from nltk.corpus import wordnet as wn

PATTERN_SEEDS = [
    # NN_ADJ : ADJ means being related with NN.
    ('~',    'n', '~y',     'a', 'NN_ADJ'),  # fault-faulty
    ('~e',   'n', '~y',     'a', 'NN_ADJ'),  # sponge-spongy
    ('~',    'n', '~ary',   'a', 'NN_ADJ'),  # complement-complementary
    ('~g',   'n', '~ggy',   'a', 'NN_ADJ'),  # pig-piggy
    ('~e',   'n', '~ic',    'a', 'NN_ADJ'),  # hygroscope-hygroscopic
    ('~y',   'n', '~ic',    'a', 'NN_ADJ'),  # ideology-ideologic
    ('~i',   'n', '~ic',    'a', 'NN_ADJ'),  # alkali-alkalic
    ('~l',   'n', '~lic',   'a', 'NN_ADJ'),  # acidophil-acidophilic
    ('~ra',  'n', '~ric',   'a', 'NN_ADJ'),  # plethora-plethoric
    ('~c',   'n', '~cal',   'a', 'NN_ADJ'),  # ascetic-ascetical
    ('~cs',  'n', '~cal',   'a', 'NN_ADJ'),  # genetics-genetical
    ('~y',   'n', '~ical',  'a', 'NN_ADJ'),  # ideology-ideological
    ('~',    'n', '~ual',   'a', 'NN_ADJ'),  # concept-conceptual
    ('~',    'n', '~al',    'a', 'NN_ADJ'),  # complement-complemental
    ('~a',   'n', '~al',    'a', 'NN_ADJ'),  # gingiva-gingival
    ('~a',   'n', '~ar',    'a', 'NN_ADJ'),  # glabella-glabellar
    ('~',    'n', '~ial',   'a', 'NN_ADJ'),  # torrent-torrential
    ('~cy',  'n', '~tial',  'a', 'NN_ADJ'),  # potency-potential
    ('~ea',  'n', '~eal',   'a', 'NN_ADJ'),  # idea-ideal
    ('~ion', 'n', '~ional', 'a', 'NN_ADJ'),  # conception-conceptional
    
    # ADJ_NN_1 : NN means something being ADJ.
    ('~',     'a', '~',      'n', 'ADJ_NN_1'),  # absolute-absolute
    
    # ADJ_NN_2 : NN means being ADJ.
    ('~le',   'a', '~ility', 'n', 'ADJ_NN_2'),  # able-ability
    ('~al',   'a', '~ality', 'n', 'ADJ_NN_2'),  # conceptual-conceptuality
    ('~',     'a', '~ity',   'n', 'ADJ_NN_2'),  # acid-acidity
    ('~e',    'a', '~ity',   'n', 'ADJ_NN_2'),  # active-activity
    ('~y',    'a', '~ity',   'n', 'ADJ_NN_2'),  # complementary-complementarity
    ('~ent',  'a', '~ency',  'n', 'ADJ_NN_2'),  # efficient-efficiency
    ('~ent',  'a', '~ence',  'n', 'ADJ_NN_2'),  # emergent-emergence
    ('~ant',  'a', '~ancy',  'n', 'ADJ_NN_2'),  # verdant-verdancy
    ('~ant',  'a', '~ance',  'n', 'ADJ_NN_2'),  # luxuriant-luxuriance
    ('~ous',  'a', '~',      'n', 'ADJ_NN_2'),  # gluttonous-glutton
    ('~ous',  'a', '~ty',    'n', 'ADJ_NN_2'),  # rapacious-rapacity
    ('~ous',  'a', '~ence',  'n', 'ADJ_NN_2'),  # crapulous-crapulence
    ('~ous',  'a', '~osity', 'n', 'ADJ_NN_2'),  # voluminous-voluminosity
    ('~eous', 'a', '~y',     'n', 'ADJ_NN_2'),  # plenteous-plenty
    ('~',     'a', '~ness',  'n', 'ADJ_NN_2'),  # rapacious-rapaciousness
    ('~y',    'a', '~iness', 'n', 'ADJ_NN_2'),  # spongy-sponginess

    # VB_ADJ_1 : ADJ means being likely to be agent of VB.
    ('~',     'v', '~ant',    'a', 'VB_ADJ_1'),  # resist-resistant
    ('~ate',  'v', '~ant',    'a', 'VB_ADJ_1'),  # luxuriate-luxuriant
    ('~ound', 'v', '~undant', 'a', 'VB_ADJ_1'),  # abound-abundant
    ('~',     'v', '~ent',    'a', 'VB_ADJ_1'),  # absorb-absorbent
    ('~e',    'v', '~ent',    'a', 'VB_ADJ_1'),  # emerge-emergent
    ('~ain',  'v', '~inent',  'a', 'VB_ADJ_1'),  # abstain-abstinent
    
    # VB_ADJ_2 : ADJ means being likely to be object of VB.
    ('~ize',  'v', '~',      'a', 'VB_ADJ_2'),  # realize-real
    ('~',     'v', '~able',  'a', 'VB_ADJ_2'),  # absorb-absorbable
    ('~',     'v', '~ible',  'a', 'VB_ADJ_2'),  # access-accessible

    # VB_ADJ_3 : ADJ means being related with event of VB.
    ('~ate',  'v', '~atory', 'a', 'VB_ADJ_3'),  # assimilate-assimilatory
    
    # VB_ADJ : ADJ means being likely to be agent or object of VB.
    ('~',    'v', '~ive',   'a', 'VB_ADJ'),  # adduct-adductive
    ('~',    'v', '~itive', 'a', 'VB_ADJ'),  # add-additive
    ('~',    'v', '~ative', 'a', 'VB_ADJ'),  # adapt-adaptative
    ('~e',   'v', '~ative', 'a', 'VB_ADJ'),  # compare-comparative
    ('~ate', 'v', '~ative', 'a', 'VB_ADJ'),  # accommodate-accommodative
    ('~b',   'v', '~ptive', 'a', 'VB_ADJ'),  # absorb-absorptive
    ('~e',   'v', '~ptive', 'a', 'VB_ADJ'),  # assume-assumptive

    # VB_NN_EVN : NN means event of VB.
    ('~',     'v', '~',        'n', 'VB_NN_EVN'),  # rescue-rescue
    ('~',     'v', '~ing',     'n', 'VB_NN_EVN'),  # foil-foiling
    ('~e',    'v', '~ing',     'n', 'VB_NN_EVN'),  # shine-shining
    ('~n',    'v', '~nning',   'n', 'VB_NN_EVN'),  # sin-sinning
    ('~m',    'v', '~mming',   'n', 'VB_NN_EVN'),  # trim-trimming
    ('~b',    'v', '~bbing',   'n', 'VB_NN_EVN'),  # rub-rubbing
    ('~g',    'v', '~gging',   'n', 'VB_NN_EVN'),  # log-logging
    ('~p',    'v', '~pping',   'n', 'VB_NN_EVN'),  # chop-chopping
    ('~t',    'v', '~tting',   'n', 'VB_NN_EVN'),  # cut-cutting
    ('~e',    'v', '~age',     'n', 'VB_NN_EVN'),  # pave-pavage
    ('~x',    'v', '~xure',    'n', 'VB_NN_EVN'),  # flex-flexure
    ('~',     'v', '~ment',    'n', 'VB_NN_EVN'),  # employ-employment
    ('~er',   'v', '~erance',  'n', 'VB_NN_EVN'),  # deliver-deliverance
    ('~e',    'v', '~ence',    'n', 'VB_NN_EVN'),  # effervesce-effervescence
    ('~t',    'v', '~tion',    'n', 'VB_NN_EVN'),  # except-exception
    ('~t',    'v', '~sion',    'n', 'VB_NN_EVN'),  # introvert-introversion
    ('~te',   'v', '~tion',    'n', 'VB_NN_EVN'),  # affiliate-affiliation
    ('~ne',   'v', '~ntion',   'n', 'VB_NN_EVN'),  # contravene-contravention
    ('~y',    'v', '~ication', 'n', 'VB_NN_EVN'),  # mistify-mistification
    ('~lve',  'v', '~lution',  'n', 'VB_NN_EVN'),  # convolve-convolution
    ('~ize',  'v', '~ization', 'n', 'VB_NN_EVN'),  # sanitize-sanitization
    ('~ise',  'v', '~isation', 'n', 'VB_NN_EVN'),  # sanitize-sanitization
    ('~ise',  'v', '~ision',   'n', 'VB_NN_EVN'),  # circumcise-circumcision
    ('~ise',  'v', '~ission',  'n', 'VB_NN_EVN'),  # abscise-abscission
    ('~ize',  'v', '~ysis',    'n', 'VB_NN_EVN'),  # hydrolize-hydrolysis
    ('~ise',  'v', '~ysis',    'n', 'VB_NN_EVN'),  # hydrolise-hydrolysis
    ('~ose',  'v', '~osition', 'n', 'VB_NN_EVN'),  # postpose-postposition
    ('~ade',  'v', '~asion',   'n', 'VB_NN_EVN'),  # abrade-abrasion
    ('~ne',   'v', '~neasion', 'n', 'VB_NN_EVN'),  # line-lineation
    ('~ribe', 'v', '~ription', 'n', 'VB_NN_EVN'),  # transcribe-transcription

    # VB_NN_AGT : NN means agent of VB.
    ('~',     'v', '~er',    'n', 'VB_NN_AGT'),  # play-player
    ('~',     'v', '~eer',   'n', 'VB_NN_AGT'),  # profit-profiteer
    ('~',     'v', '~or',    'n', 'VB_NN_AGT'),  # effect-effector
    ('~',     'v', '~ry',    'n', 'VB_NN_AGT'),  # spice-spicery
    ('~e',    'v', '~er',    'n', 'VB_NN_AGT'),  # rescue-rescuer
    ('~e',    'v', '~or',    'n', 'VB_NN_AGT'),  # defibrillate-defibrillator
    ('~e',    'v', '~ior',   'n', 'VB_NN_AGT'),  # save-savior
    ('~n',    'v', '~nner',  'n', 'VB_NN_AGT'),  # sin-sinner
    ('~b',    'v', '~bber',  'n', 'VB_NN_AGT'),  # scrub-scrubber
    ('~p',    'v', '~pper',  'n', 'VB_NN_AGT'),  # chop-chopper
    ('~m',    'v', '~mmer',  'n', 'VB_NN_AGT'),  # trim-trimmer
    ('~t',    'v', '~tter',  'n', 'VB_NN_AGT'),  # cut-cutter
    ('~ure',  'v', '~urant', 'n', 'VB_NN_AGT'),  # denature-denaturant
    ('~ade',  'v', '~adant', 'n', 'VB_NN_AGT'),  # abrade-abradant
    ('~ize',  'v', '~ist',   'n', 'VB_NN_AGT'),  # archaize-archaist
    ('~ise',  'v', '~ist',   'n', 'VB_NN_AGT'),  # archaise-archaist

    # VB_NN_OBJ : NN means object of VB.
    ('~',     'v', '~ee',    'n', 'VB_NN_OBJ'),  # employ-employee

    # NN_VB : VB means act derived from NN.
    ('~',    'n', '~ate',   'v', 'NN_VB'),  # acetyl-acetylate
    ('~il',  'n', '~liate', 'v', 'NN_VB'),  # foil-foliate
    ('~',    'n', '~ize',   'v', 'NN_VB'),  # marble-marbleize
    ('~',    'n', '~ise',   'v', 'NN_VB'),  # glamour-glamourise
    ('~y',   'n', '~ize',   'v', 'NN_VB'),  # symmetry-symmetrize
    ('~y',   'n', '~ise',   'v', 'NN_VB'),  # symmetry-symmetrise
    ('~is',  'n', '~ize',   'v', 'NN_VB'),  # hypothesize-hypothesis
    ('~na',  'n', '~nize',  'v', 'NN_VB'),  # patina-patinize
    ('~na',  'n', '~nate',  'v', 'NN_VB'),  # patina-patinate
    ('~ne',  'n', '~nize',  'v', 'NN_VB'),  # agene-agenize
    ('~ne',  'n', '~nise',  'v', 'NN_VB'),  # agene-agenise
    ('~al',  'n', '~alize', 'v', 'NN_VB'),  # diagonal-diagonalize
    ('~al',  'n', '~alise', 'v', 'NN_VB'),  # diagonal-diagonalise
    ('~ism', 'n', '~ize',   'v', 'NN_VB'),  # archaism-archaize
    ('~ism', 'n', '~ise',   'v', 'NN_VB'),  # archaism-archaise
    ('~',    'n', '~ify',   'v', 'NN_VB'),  # object-objectify
    ('~y',   'n', '~ify',   'v', 'NN_VB'),  # ruby-rubify
    ('~ce',  'n', '~fy',    'v', 'NN_VB'),  # justice-justify
    ('~ery', 'n', '~ify',   'v', 'NN_VB'),  # mistery-mistify

    # NN_NN_1 : A concept and people who are related with the concept.
    ('~ist',   'n', '~',     'n', 'NN_NN_1'),  # colorist-color
    ('~ist',   'n', '~e',    'n', 'NN_NN_1'),  # sericultuist-sericulture
    ('~ist',   'n', '~y',    'n', 'NN_NN_1'),  # anarchist-anarchy
    ('~ist',   'n', '~ism',  'n', 'NN_NN_1'),  # nihilist-nihilism
    ('~gist',  'n', '~gue',  'n', 'NN_NN_1'),  # monologist-monologue
    ('~ician', 'n', '~ics',  'n', 'NN_NN_1'),  # politician-politics
    ('~er',    'n', '~',     'n', 'NN_NN_1'),  # freeholder-freehold
    ('~er',    'n', '~e',    'n', 'NN_NN_1'),  # mainer-maine
    ('~ster',  'n', '~',     'n', 'NN_NN_1'),  # punster-pun
    ('~pher',  'n', '~phy',  'n', 'NN_NN_1'),  # radiographer-radiography
    ('~',      'n', '~hood', 'n', 'NN_NN_1'),  # bachelor-bachelorhood
    ('~',      'n', '~ship', 'n', 'NN_NN_1'),  # friend-friendship
    ('~',      'n', '~dom',  'n', 'NN_NN_1'),  # serf-serfdom
    ('~ll',    'n', '~ldom', 'n', 'NN_NN_1'),  # thrall-thraldom
    ('~ant',   'n', '~ancy', 'n', 'NN_NN_1'),  # infant-infancy
    ('~ling',  'n', '~',     'n', 'NN_NN_1'),  # earthling-earth

    # NN_NN_2 : A concept and its hyponym
    ('~',   'n', '~let', 'n', 'NN_NN_2'),  # tree-treelet
    ('~le', 'n', '~let', 'n', 'NN_NN_2'),  # isle-islet
    ]

patterns = []
is_word = lambda w: (w.name.find('_') < 0)

for ps in PATTERN_SEEDS:
    rex = '%s.%s;%s.%s' % (
        ps[0].replace('~', '(?P<x>.*)'), ps[1],
        ps[2].replace('~', '(?P=x)'), ps[3])
    add = (re.compile(rex), ps[4])
    patterns.append(add);


class DerivationalPair:
    def __init__(self, lemma1, lemma2):
        if lemma1 < lemma2:
            self.__lemma1 = lemma1
            self.__lemma2 = lemma2
        else:
            self.__lemma1 = lemma2
            self.__lemma2 = lemma1
        self.name1 = self.__lemma1.name.lower()
        self.name2 = self.__lemma2.name.lower()
        self.pos1 = self.__lemma1.synset.pos
        self.pos2 = self.__lemma2.synset.pos
        if self.pos1 == 's':
            self.pos1 = 'a'
        if self.pos2 == 's':
            self.pos2 = 'a'

    def string(self, reverse = False):
        if reverse:
            return '%s.%s\t%s.%s' % \
                   (self.name2, self.pos2, self.name1, self.pos1)
        else:
            return '%s.%s\t%s.%s' % \
                   (self.name1, self.pos1, self.name2, self.pos2)


def matchPattern(pair, pattern):
    key1 = '%s.%s;%s.%s' % (pair.name1, pair.pos1, pair.name2, pair.pos2)
    key2 = '%s.%s;%s.%s' % (pair.name2, pair.pos2, pair.name1, pair.pos1)
    if pattern[0].match(key1): return 1;
    if pattern[0].match(key2): return 2;
    return 0


def writeDerivations(filename):
    print ' -> getting derivation patterns'
    
    processed = set()
    fout = open(filename, 'w')
    
    for ss in list(wn.all_synsets()):
        for lemma in ss.lemmas:
            if not is_word(lemma):
                continue
            
            for deriv in lemma.derivationally_related_forms():
                if not is_word(deriv):
                    continue
                
                pair = DerivationalPair(lemma, deriv)
                if pair.string() in processed:
                    continue
                else:
                    processed.add(pair.string())

                for pat in patterns:
                    ret = matchPattern(pair, pat)
                    if ret == 1:
                        do_match_with_any_pattern = True
                        disp = '%s\t%s\n' % (pair.string(False), pat[1])
                        fout.write(disp)
                    if ret == 2:
                        do_match_with_any_pattern = True
                        disp = '%s\t%s\n' % (pair.string(True), pat[1])
                        fout.write(disp)
                    if ret > 0:
                        break
                else:
                    disp = '%s\tUNKNOWN\n' % pair.string()
                    fout.write(disp)


def main():
    writeDerivations('%s/wn.derivation.tsv' % sys.argv[1])
    
    
if(__name__=='__main__'):
    main()
