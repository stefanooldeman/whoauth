install:
	-brew install redis
	-pip install -r requirements.txt
	-mkdir etc
	awk '/^[a-z\ +]/ { print }' docs/redis.conf > etc/redis.conf

test:
	nosetests tests

run:
	redis-server
	python run.py
