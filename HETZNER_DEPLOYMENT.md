# Deploying Südwest-Energie Website to Hetzner

This guide provides comprehensive instructions for deploying the Südwest-Energie website to Hetzner web hosting.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Hetzner Account Setup](#hetzner-account-setup)
3. [Server Configuration](#server-configuration)
4. [Application Deployment](#application-deployment)
5. [Nginx Configuration](#nginx-configuration)
6. [SSL Setup](#ssl-setup)
7. [Service Management](#service-management)
8. [Post-Deployment](#post-deployment)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

- Hetzner Cloud account with billing information set up
- Domain name registered and accessible
- Local copy of the Südwest-Energie website code
- Ninox database credentials (if using Ninox integration)

## Hetzner Account Setup

### 1. Create Hetzner Account
- Go to [https://hetzner.com](https://hetzner.com)
- Sign up and complete account verification
- Add payment information

### 2. Create Server Instance
1. Log into Hetzner Cloud Console
2. Click "Projects" > "Create Project"
3. Navigate to "Servers"
4. Click "Get server"
5. Select the following configuration:
   - **Location**: Choose closest to your target audience
   - **Type**: CX22 or higher recommended (2GB RAM minimum)
   - **Image**: Ubuntu 22.04 LTS
   - **SSH Key** (optional but recommended): Add your SSH key for secure access
6. Click "Create" to provision the server

### 3. Note Server Information
- Record the **IPv4 address** for future use
- If you added SSH keys, ensure you have access to your private key

## Server Configuration

### 1. Initial Server Setup
Connect to your server via SSH:
```bash
ssh root@YOUR_SERVER_IP
```

### 2. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install Required Packages
```bash
sudo apt install python3 python3-pip python3-venv nginx git curl build-essential -y
```

### 4. Install Node.js (required for Reflex)
```bash
# Import NodeSource package signing key
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 5. Install PM2 (process manager)
```bash
sudo npm install -g pm2
```

## Application Deployment

### 1. Create Application Directory
```bash
sudo mkdir -p /var/www/suedwestenergie
sudo chown $USER:$USER /var/www/suedwestenergie
cd /var/www/suedwestenergie
```

### 2. Transfer Application Files
From your local machine, copy the application files to the server:

```bash
# Method 1: Using SCP
scp -r /path/to/your/local/suedwestenergie-reflex-projekt/* root@YOUR_SERVER_IP:/var/www/suedwestenergie/

# Method 2: Using Git (if repository exists)
git clone https://github.com/your-username/suedwestenergie-website.git .
```

### 3. Set Up Python Virtual Environment
```bash
cd /var/www/suedwestenergie

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file for production settings:
```bash
nano .env
```

Add the following content, customizing values as needed:
```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=generate-a-very-long-secret-key-here
DB_URL=postgresql://username:password@localhost:5432/suedwestenergie

# Ninox Database Configuration (add your actual credentials)
NINOX_API_KEY=your_ninox_api_key
NINOX_DATABASE_ID=your_ninox_database_id
NINOX_TABLE_ID=your_ninox_table_id

# Contact Information
COMPANY_NAME=Südwest Energie
CONTACT_EMAIL=kontakt@yourdomain.com
CONTACT_PHONE=+49 711 12345678
CONTACT_ADDRESS=Your Company Address

# Branding Colors
PRIMARY_COLOR=#00bcd4
SECONDARY_COLOR=#00acc1
ACCENT_COLOR=#26c6da
TEXT_DARK=#0d47a1
TEXT_LIGHT=#4fc3f7
BG_LIGHT=#e1f5fe
BG_DARK=#b3e5fc
CARD_BG=#ffffff
SKY_BLUE=#00bcd4
EARTH_BROWN=#ff9800

# SEO
SITE_TITLE=Südwest-Energie - Energievermittlung für Unternehmen
SITE_DESCRIPTION=Professionelle Energievermittlung für Unternehmen. Wir senken Ihre Strom- und Gaskosten um durchschnittlich 20-30% - transparent, unabhängig und kostenfrei.

# Google Analytics (if applicable)
GOOGLE_ANALYTICS_ID=your-ga4-id
```

### 5. Initialize the Reflex Application
```bash
# Activate virtual environment
source venv/bin/activate

# Initialize Reflex
reflex init

# Build the application (frontend only)
reflex export --frontend-only
```

## Nginx Configuration

### 1. Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/suedwestenergie
```

Add the following configuration, replacing `your-domain.com` with your actual domain:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase timeout for slow requests
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /_static/ {
        alias /var/www/suedwestenergie/.web/_static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security: Deny access to sensitive files
    location ~ /\. {
        deny all;
    }
}
```

### 2. Enable the Site
```bash
# Create symbolic link to enable the site
sudo ln -s /etc/nginx/sites-available/suedwestenergie /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## SSL Setup

### 1. Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Obtain SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```
Follow the interactive prompts:
- Enter your email for urgent renewal and security notices
- Agree to the terms of service
- Choose whether to share email with EFF (optional)
- Confirm redirect from HTTP to HTTPS (recommended)

### 3. Verify SSL Configuration
Check that the SSL certificate is properly installed:
```bash
sudo certbot certificates
```

## Service Management

### 1. Create PM2 Configuration
Create a process file for PM2:
```bash
nano /var/www/suedwestenergie/ecosystem.config.js
```

Add the following content:
```javascript
module.exports = {
  apps: [{
    name: 'suedwestenergie',
    script: './venv/bin/reflex',
    args: 'run',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    cwd: '/var/www/suedwestenergie',
    env: {
      NODE_ENV: 'production',
      PATH: '/var/www/suedwestenergie/venv/bin'
    }
  }]
};
```

### 2. Start Application with PM2
```bash
# Navigate to app directory
cd /var/www/suedwestenergie

# Activate virtual environment
source venv/bin/activate

# Start the application
pm2 start ecosystem.config.js

# Save PM2 configuration to start at boot
pm2 startup
pm2 save
```

### 3. Verify Service Status
```bash
# Check if app is running
pm2 status

# View application logs
pm2 logs suedwestenergie
```

## Post-Deployment

### 1. DNS Configuration
- Point your domain's DNS records to your Hetzner server IP address
- A record: `your-domain.com` → `YOUR_SERVER_IP`
- A record: `www.your-domain.com` → `YOUR_SERVER_IP`

### 2. Database Setup (if using PostgreSQL)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user (optional, only if using PostgreSQL)
sudo -u postgres psql
CREATE DATABASE suedwestenergie;
CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE suedwestenergie TO your_username;
\q
```

### 3. Firewall Configuration (recommended)
```bash
# Install and enable UFW
sudo apt install ufw -y

# Allow necessary services
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 4. Monitoring and Maintenance
```bash
# Check application status
pm2 status

# View logs
pm2 logs suedwestenergie --lines 50

# Monitor system resources
htop

# Check disk usage
df -h

# Check memory usage
free -h

# Check nginx status
sudo systemctl status nginx
```

## Troubleshooting

### Common Issues and Solutions

#### Application Not Starting
```bash
# Check PM2 logs
pm2 logs suedwestenergie

# Check if port 8000 is in use
sudo netstat -tuln | grep 8000

# Restart the application
pm2 restart suedwestenergie
```

#### Nginx Configuration Issues
```bash
# Test nginx configuration
sudo nginx -t

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check nginx access logs
sudo tail -f /var/log/nginx/access.log
```

#### SSL Certificate Issues
```bash
# Renew SSL certificate
sudo certbot renew --dry-run

# Check certificate status
sudo certbot certificates
```

#### Database Connection Issues
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
# Update your .env with correct database credentials
```

#### Performance Issues
```bash
# Check system resources
htop

# Optimize PM2 configuration if needed
pm2 reload all
```

### Useful Commands for Maintenance

```bash
# Update application
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
pm2 restart suedwestenergie

# Update SSL certificates
sudo certbot renew

# Backup environment file
cp /var/www/suedwestenergie/.env /backup/location/.env.backup

# Check all running processes
pm2 list

# Monitor application in real-time
pm2 monit
```

## Backup Strategy

### 1. Regular Backups
Set up automatic backups of your application and database:
```bash
# Create backup script directory
sudo mkdir -p /opt/backups
sudo nano /opt/backups/backup_script.sh
```

### 2. Cron Job for Automated Backups
```bash
# Edit crontab
crontab -e

# Add line for daily backups at 2 AM
0 2 * * * /opt/backups/backup_script.sh
```

## Security Best Practices

1. **Keep the system updated**: `sudo apt update && sudo apt upgrade`
2. **Secure SSH access**: Use SSH keys, disable password authentication
3. **Regular backups**: Implement automated backup strategy
4. **Monitor logs**: Regularly check application and system logs
5. **Set up monitoring**: Consider using monitoring tools for uptime alerts

Your Südwest-Energie website should now be successfully deployed to Hetzner and accessible at your domain with full functionality. The application uses the cyan/star-themed color scheme and enhanced logo placement that we implemented earlier.