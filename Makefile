init:
	pip install -r requirements.txt

transmitter:
	python ./pdc_project/transmitter.py -i message.txt

receiver:
	python ./pdc_project/receiver.py

test:
	nosetests
	