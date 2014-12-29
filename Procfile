web: twistd -n web --class server.resource --port 8080
worker: celery -A tasks worker --loglevel=info