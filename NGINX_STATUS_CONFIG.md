# Nginx Configuration for Status Page

To make the status page accessible at `status.suedwest-energie.de`, add the following configuration to your Nginx setup.

## Configuration Snippet

Create a new file `/etc/nginx/sites-available/status.suedwest-energie.de` (or add to your existing config):

```nginx
server {
    listen 80;
    server_name status.suedwest-energie.de;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name status.suedwest-energie.de;

    # SSL Configuration (Adjust paths to your certificates)
    ssl_certificate /etc/letsencrypt/live/suedwest-energie.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/suedwest-energie.de/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Proxy to Reflex App Status Page
    location / {
        # Proxy to the local Reflex app
        proxy_pass http://localhost:3000/status;
        
        # Standard Proxy Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket Support (for Reflex updates)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Enable Configuration

```bash
sudo ln -s /etc/nginx/sites-available/status.suedwest-energie.de /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Notes

- This configuration proxies `status.suedwest-energie.de` directly to the `/status` route of your Reflex app.
- Ensure your DNS records point `status.suedwest-energie.de` to your server's IP.
- The `proxy_pass` assumes your Reflex app is running on port 3000 (default). Adjust if running on a different port.
