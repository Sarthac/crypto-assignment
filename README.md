# Crypto Tools

A comprehensive cryptography toolkit built with Flask that provides implementations of classical ciphers and steganography techniques.

## Features

### 🔐 Ciphers Currently Implemented

| Substitution Ciphers       | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| Shift cipher               | Configurable character rotation (Caesar cipher variant) |
| Mixed-alphabet             | Keyword-based alphabet substitution                     |
| Atbash                     | Ancient Hebrew cipher using alphabet reversal           |
| Simple substitution cipher | Custom alphabet substitution with random generation     |
| ROT13                      | Special case of Caesar cipher with 13-character shift   |
| Baconian                   | Binary encoding cipher using A/B patterns               |
| Polybius square            | Grid-based substitution cipher                          |

### 🖼️ Steganography

- **LSB Steganography** - Hide secret messages within image files
- **Message Hiding** - Embed text into PNG images using least significant bit manipulation
- **Message Extraction** - Retrieve hidden messages from steganographic images

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Cryptography**: Custom cipher implementations
- **Steganography**: Stegano library with PIL/Pillow
- **Production**: Gunicorn WSGI server
- **Proxy**: Caddy/Nginx reverse proxy support

## Setup

### Requirements

This project requires **Python 3.11** or newer to run.

```

pip install Flask gunicorn stegano pillow

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

### Setup Reverse Proxy

You can set up a reverse proxy using **nginx** or **caddy**. But I have used caddy

**Using Caddy web server:**

```

crypto.sarthak.co.in {
reverse_proxy localhost:8000
}

```

## Usage

### Cipher Tools

1. Navigate to the **Ciphers** section from the home page
2. Select your desired cipher algorithm
3. Enter text to encrypt or decrypt
4. Configure algorithm-specific parameters (shift values, keywords, etc.)
5. Choose encrypt/decrypt action
6. View results instantly

### Steganography

1. Go to the **Steganography** section
2. Upload a cover image (PNG format recommended)
3. Enter your secret message
4. Generate steganographic image with hidden message
5. Extract hidden messages from steganographic images

## API Endpoints

- `GET /` - Home page with tool selection
- `GET/POST /cipher` - Cipher encryption/decryption interface
- `GET/POST /steganography` - Steganography tools
- `GET /api` - API documentation

##Security Notes

⚠️ **Educational Purpose**: These implementations are for learning and demonstration. Classical ciphers are not suitable for real-world security applications.

⚠️ **Steganography Limitations**: LSB steganography can be detected by steganalysis tools. Use only for educational purposes.
