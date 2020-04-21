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

2. Clone the repository.
```
git clone git@github.com:guadr/frontend.git
```

3. Install dependencies
```python3
pip install -r requirements.txt
```

4. Create instance Folder for DB
```
mkdir instance
```

5. run the application 
```
python3 frontend.py
```

6. We currently have a 'dummy' secret key on this repository. We change this when it is actually deployed. Make sure to make a good secrey key when deploying. Learn more here 
https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY

## Running on an ubuntu webserver
1. Follow this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)
2. Clone this repository
3. Create a python3 virtual environment
4. Activate virtual environment & install everything in requirements.txt
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```
4. Create database as shown in "Setting Up Frontend"
5. Run nginx and frontend services
```
sudo systemctl start nginx;
sudo systemctl start frontend;
```

# Expansions To Take On
1. Add Payment Capabilities
2. Add Notification Sysytem
