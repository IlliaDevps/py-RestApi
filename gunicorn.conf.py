# gunicorn.conf.py

# The number of worker processes for handling requests
workers = 4

# Bind the server to this address and port
bind = "0.0.0.0:8000"

# The Python module where your Flask/Django app is located
# Replace "your_app_module" with the actual module name
module = "app:create_app()"