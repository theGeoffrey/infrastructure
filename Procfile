web: twistd -n web --class server.resource --port 5000
worker: celery -A tasks worker --loglevel=info