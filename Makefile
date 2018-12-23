.PHONY: clean

src/deps/__init__.py: src/deps
	cp src/init.make src/deps/__init__.py
	pip install -r src/requirements.txt -t src/deps/ || rm -f src/deps/__init__.py

src/deps: 
	mkdir src/deps

clean:
	rm -rf src/deps
	find . -iname "*.pyc" -exec rm -f {} ";"