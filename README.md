
**Ciphers that are currrently implemented**

| Substitution ciphers |
| ------ | 
| Shift cipher | 
| mixed-alphabet |
| Atbash |

# Setup 

```
pip install Flask gunicorn

```
### Intial run 

```
gunicorn -w 4 app:app

```

by default it will run on 127.0.0.1:8000, you can explicitly set your desired port in gunicorn

```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```


| Part         | Meaning                                                                                                                                                                                                                                                         |  
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **gunicorn** | Starts the **Gunicorn server**, a production-grade WSGI HTTP server for running Python web apps (Flask, Django, etc.).                                                                                                                                          |
| **-w 4**     | Runs **4 worker processes** to handle requests concurrently. More workers = better performance under load (adjust based on your CPU cores).                                                                                                                     |
| **app\:app** | This specifies **where to find your Flask app**: <br> - The first **app** is the **Python filename without `.py` extension** (e.g. app.py). <br> - The second **app** is the **Flask application object name** inside your file (e.g. `app = Flask(__name__)`). |


### creating a systemd service file to run in the background, starts on boots, and restarts on failure.

create a systemd file on /etc/systemd/system i.e crypto-app.service

```
[Unit]
Description="Gunicorn instance to serve Caesar Flask app"
After=network.target

[Service]
User=root
WorkingDirectory=/usr/share/caddy/crypto-app
ExecStart=/usr/local/bin/gunicorn -w 1 app:app

[Install]
WantedBy=multi-user.target
```
### Start and enable the service
```
sudo systemctl start caesar
sudo systemctl enable caesar
```



### Setup proxy

You can setup reverse proxy using nginx or caddy, I am using caddy web server so, 
```
crypto.sarthak.co.in {
    reverse_proxy localhost:8000
}

```
