#!/bin/bash

# Exit on error
set -e

# Update system and install required packages
echo "Updating system and installing packages..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nodejs npm mysql-server nginx
sudo apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Start and enable MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Create MySQL database and user
echo "Creating MySQL database and user..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS address_book;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'address_book_user'@'localhost' IDENTIFIED BY 'your_secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON address_book.* TO 'address_book_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create application directory
echo "Setting up application directory..."
sudo mkdir -p /var/www/address_book
sudo chown -R $USER:$USER /var/www/address_book

# Copy application files
echo "Copying application files..."
cp -r backend frontend /var/www/address_book/

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd /var/www/address_book/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build frontend
echo "Building frontend..."
cd /var/www/address_book/frontend
npm install
npm run build

# Create Nginx configuration
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/address_book << EOF
server {
    listen 80;
    server_name _;  # Replace with your domain name

    # Frontend
    location / {
        root /var/www/address_book/frontend/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;
        add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;

        if (\$request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/address_book /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Create PM2 ecosystem file
echo "Setting up PM2..."
cd /var/www/address_book/backend
tee ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: "address_book_backend",
    script: "app.py",
    interpreter: "venv/bin/python3",
    env: {
      "FLASK_APP": "app.py",
      "FLASK_ENV": "production"
    }
  }]
}
EOF

# Start the application with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo "Deployment completed successfully!"
echo "The application should now be accessible at http://your_server_ip"
echo "Default admin credentials:"
echo "Username: admin"
echo "Password: admin123"
echo "Please change these credentials after first login!" 