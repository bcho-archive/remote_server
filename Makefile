.PHONY: clean-pyc clean

run_server:
	python run_server.py

run_bot:
	python run_bot.py

offline:
	python run_bot.py testing

offline-weibo:
	python run_offline.py

build_db:
	python make_db.py

clean:  clean-pyc

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
