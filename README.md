# frontend
User-facing web application for guadr delivery system.

This application runs on an NGINX webserver and makes use of flask, wsgi, and OpenStreetMap.

## Setting up Frontend
Here are steps to set up our Web Application on your own.

1. make a folder for the app
```
mkdir ~/Documents/GUADR_frontend
cd ~/Documents/GUADR_frontend
```

1. Clone the repository.
```
git clone git@github.com:guadr/frontend.git
```

1. Install dependencies
```python3
pip install -r requirements.txt
```

1. Create instance Folder for DB
```
mkdir instance
```

1. run the application 
```
python3 frontend.py
```

## Update on web server 
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```

