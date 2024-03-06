#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static
if ! dpkg -l | grep -qw nginx; then
	sudo apt-get update
	sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "<html>
<head>
</head>
<body>
I Wish I Was A Cat Just MeoMeo 
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i "38i \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n" /etc/nginx/sites-available/default
sudo service nginx restart

