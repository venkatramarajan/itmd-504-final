#!/bin/bash

# Update system
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv nodejs npm mysql-server nginx

# Install Node.js 18.x (LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Create MySQL database and user
sudo mysql -e "CREATE DATABASE IF NOT EXISTS address_book;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'address_book_user'@'localhost' IDENTIFIED BY 'your_secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON address_book.* TO 'address_book_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create application directory
sudo mkdir -p /var/www/address_book
sudo chown -R $USER:$USER /var/www/address_book

# Copy application files
cp -r backend /var/www/address_book/
cp -r frontend /var/www/address_book/
cp requirements.txt /var/www/address_book/

# Set up Python virtual environment
cd /var/www/address_book
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up frontend
cd /var/www/address_book/frontend
npm install
npm run build

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/address_book << EOF
server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain

    # Frontend
    location / {
        root /var/www/address_book/frontend/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/address_book /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Create PM2 ecosystem file
cd /var/www/address_book
tee ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: "address_book_backend",
    script: "backend/app.py",
    interpreter: "/var/www/address_book/venv/bin/python3",
    env: {
      FLASK_APP: "backend/app.py",
      FLASK_ENV: "production",
      DATABASE_URL: "mysql://address_book_user:your_secure_password@localhost/address_book"
    }
  }]
}
EOF

# Start the application with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Set up SSL with Certbot (optional)
# sudo apt install -y certbot python3-certbot-nginx
# sudo certbot --nginx -d your_domain.com 