 deps/__init__.py: deps
	cp init.make deps/__init__.py
	pip install -r requirements.txt -t deps/

deps: 
	mkdir deps
