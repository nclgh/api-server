gunicorn -w 1 server:app -b 0.0.0.0:8080 --reload
# gunicorn -w 3 server:app -b 0.0.0.0:8080 --reload