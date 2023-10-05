#!/usr/bin/env bash
# Task0
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<html><head></head><body>Test Page</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null
sudo ln -sf /data/web_static/releases/test/  /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/web_static
nginx_config="/etc/nginx/sites-available/default"
nginx_alias="location /hbnb_static { alias /data/web_static/current/; }"
if ! grep -q "$nginx_alias" "$nginx_config"; then
    sudo sed -i "/server_name _;/ a $nginx_alias" "$nginx_config"
fi
sudo service nginx restart
