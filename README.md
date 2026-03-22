# retro_ciphers
Frontend for retro_ciphers package which I built.



## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Cryptography**: Uses retro_ciphers package which I built.
- **Production**: Gunicorn WSGI server

## Setup

### Requirements

This project requires **Python 3.11** or newer to run.

```

pip install Flask gunicorn retro_ciphers 

```

### Initial Run

**Development mode:**

```

python app.py

```

**Production with Gunicorn:**

```

gunicorn -w 4 app:app

```

By default it runs on `127.0.0.1:8000`. You can explicitly set your desired port:

```

gunicorn -w 4 -b 0.0.0.0:5000 app:app

```

### Gunicorn Command Breakdown

| Part         | Meaning                                                                                                                                                                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **gunicorn** | Starts the **Gunicorn server**, a production-grade WSGI HTTP server for running Python web apps (Flask, Django, etc.)                                                                                                                    |
| **-w 4**     | Runs **4 worker processes** to handle requests concurrently. More workers = better performance under load (adjust based on your CPU cores)                                                                                               |
| **app:app**  | Specifies **where to find your Flask app**: <br> - First **app** = **Python filename** without `.py` extension (e.g., app.py) <br> - Second **app** = **Flask application object name** inside your file (e.g., `app = Flask(__name__)`) |

### Creating a Systemd Service

Create a systemd service file to run in the background, start on boot, and restart on failure.

**Create `/etc/systemd/system/crypto-app.service`:**

```

[Unit]
Description=Gunicorn instance to serve Crypto Tools Flask app
After=network.target

[Service]
User=root
WorkingDirectory=/usr/share/caddy/crypto-app
ExecStart=/usr/local/bin/gunicorn -w 4 app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

```

### Start and Enable the Service

```

sudo systemctl start crypto-app
sudo systemctl enable crypto-app
sudo systemctl status crypto-app

```

⚠️ **Educational Purpose**: These implementations are for learning and demonstration. Classical ciphers are not suitable for real-world security applications.
