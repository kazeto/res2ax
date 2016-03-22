TARGET = out
DIR_WN = $(TARGET)/wn
DIR_CN = $(TARGET)/cn
URL_CN5 = http://conceptnet5.media.mit.edu/downloads/current/conceptnet5_flat_csv_5.3.tar.bz2

wn:
	mkdir -p $(DIR_WN)
	python bin/wn.synset.py $(DIR_WN)
	python bin/wn.hypernym.py $(DIR_WN)
	python bin/wn.antonym.py $(DIR_WN)
	python bin/wn.multiword.py $(DIR_WN)
	python bin/wn.lemma.synonym.py $(DIR_WN)
	python bin/wn.lemma.hypernym.py $(DIR_WN)
	python bin/wn.derivation.py $(DIR_WN)
	python bin/wn.deriv2axiom.py $(DIR_WN)

cn:
	mkdir tmp
	mv tmp
	wget $(URL_CN5)
	tar xvf *.tar.bz2
	mv ../
	mkdir -p $(DIR_CN)
	python bin/cn.py $(shell find tmp -name "*.csv") $(DIR_CN)
	rm -rf tmp

cn2:
	mkdir -p $(DIR_CN)
	python bin/cn.py $(shell find tmp -name "*.csv") $(DIR_CN)
