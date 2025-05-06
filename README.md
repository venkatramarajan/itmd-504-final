# Address Book Web Application

A web-based address book application with Python Flask backend, React frontend, and MySQL database.

## Deployment Instructions for Ubuntu 24.04 LTS

### Prerequisites
- Ubuntu 24.04 LTS server
- Domain name (optional, but recommended)
- SSH access to the server

### Deployment Steps

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd address_book
   ```

2. **Make the deployment script executable**
   ```bash
   chmod +x deploy.sh
   ```

3. **Edit the configuration**
   - Open `deploy.sh` and replace `your_domain.com` with your actual domain name
   - Change `your_secure_password` to a strong password for the MySQL database
   - Update the database connection string in `backend/config.py` if needed

4. **Run the deployment script**
   ```bash
   ./deploy.sh
   ```

5. **Verify the deployment**
   - Frontend should be accessible at `http://your_domain.com`
   - Backend API should be accessible at `http://your_domain.com/api`

### Default Admin Credentials
- Username: admin
- Password: admin123

**Important**: Change the admin password after first login!

### Manual Deployment Steps (if needed)

1. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nodejs npm mysql-server nginx
   ```

2. **Set up MySQL**
   ```bash
   sudo mysql_secure_installation
   sudo mysql -e "CREATE DATABASE address_book;"
   sudo mysql -e "CREATE USER 'address_book_user'@'localhost' IDENTIFIED BY 'your_password';"
   sudo mysql -e "GRANT ALL PRIVILEGES ON address_book.* TO 'address_book_user'@'localhost';"
   ```

3. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set up frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

5. **Configure Nginx**
   - Copy the Nginx configuration from the deployment script
   - Update the domain name
   - Enable the site and restart Nginx

6. **Start the application**
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

### Maintenance

- **View logs**
  ```bash
  pm2 logs address_book_backend
  ```

- **Restart application**
  ```bash
  pm2 restart address_book_backend
  ```

- **Update application**
  ```bash
  git pull
  cd frontend && npm install && npm run build
  source venv/bin/activate && pip install -r requirements.txt
  pm2 restart address_book_backend
  ```

### Security Considerations

1. Change the default admin password immediately after deployment
2. Use strong passwords for the MySQL database
3. Enable SSL/TLS using Let's Encrypt (included in deployment script)
4. Keep the system and dependencies updated
5. Configure firewall to allow only necessary ports (80, 443)

### Troubleshooting

1. **Check application logs**
   ```bash
   pm2 logs
   ```

2. **Check Nginx logs**
   ```bash
   sudo tail -f /var/log/nginx/error.log
   sudo tail -f /var/log/nginx/access.log
   ```

3. **Check MySQL status**
   ```bash
   sudo systemctl status mysql
   ```

4. **Verify database connection**
   ```bash
   mysql -u address_book_user -p address_book
   ```
