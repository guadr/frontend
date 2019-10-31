# frontend
User-facing web application for guadr delivery system.

This application runs on an NGINX webserver and makes use of flask, wsgi, and OpenStreetMap

## Install dependencies
```python3
pip install -r requirements.txt
```

### Update on web server 
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```

### API
For our implementation of the API we are storing our location in a memory structure. In a move to a production environment we will need to attach to a database. 
