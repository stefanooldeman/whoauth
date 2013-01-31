install:
	-brew install redis
	-pip install -r requirements.txt
	-mkdir etc
	awk '/^[a-z\ +]/ { print }' docs/redis.conf > etc/redis.conf

test:
	nosetests tests

start:
	redis-server etc/redis.conf
	python run.py

stop:
	cat etc/redis.conf | grep redis.pid | cut -d' ' -f2 | xargs cat | xargs kill

