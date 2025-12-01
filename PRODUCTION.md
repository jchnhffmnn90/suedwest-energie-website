# Südwest-Energie Website - Production Deployment

This document describes how to deploy the Südwest-Energie website in a production environment.

## Production Features Added

- **Security enhancements**: Form validation, input sanitization, security headers
- **Error handling & logging**: Comprehensive error tracking and logging system
- **Performance optimization**: Caching mechanisms and compression
- **Analytics**: Google Analytics integration for monitoring
- **Environment configuration**: Secure environment variable management
- **Production deployment**: Docker and docker-compose setup for production

## Prerequisites

- Docker and Docker Compose
- A domain name (recommended for production)
- SSL certificates (for HTTPS)
- SMTP server credentials for contact form emails
- Google Analytics 4 property ID (optional)

## Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your production values:
   - Set `ENVIRONMENT=production`
   - Set `SECRET_KEY` to a strong, unique value
   - Configure your database connection (`DB_URL`)
   - Set up SMTP settings for contact form emails
   - Add Google Analytics ID if using analytics

## Deployment Options

### Option 1: Docker Compose (Recommended)

1. Build and start the services:
   ```bash
   docker-compose up -d --build
   ```

2. The application will be available at `http://localhost:8000` (or your configured domain)

### Option 2: Using the Deployment Script

1. Make the script executable:
   ```bash
   chmod +x deploy.sh
   ```

2. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

## Database Configuration

By default, the application uses PostgreSQL in production. Update the `DB_URL` in your environment variables to point to your production database.

For local development, the default is SQLite, but for production it's recommended to use PostgreSQL.

## SSL/HTTPS Configuration

To enable HTTPS:

1. Place your SSL certificate and private key in the `ssl/` directory
2. Update `nginx.conf` with the correct paths to your certificates
3. The nginx configuration is set up to redirect HTTP to HTTPS automatically

## Email Configuration

The contact form can send notifications via email. To enable this:

1. Configure SMTP settings in your environment variables
2. Make sure `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` are set
3. Test the contact form to ensure emails are being sent

## Analytics Configuration

To enable Google Analytics:

1. Set `GOOGLE_ANALYTICS_ID` in your environment variables
2. The tracking code will be automatically added to all pages
3. The implementation includes IP anonymization for GDPR compliance

## Monitoring and Logging

- Application logs are stored in the `logs/` directory
- You can view logs with: `docker-compose logs -f`
- Error logs help with debugging in production

## Backup Strategy

For production deployments, implement a regular backup strategy for:
- Database (PostgreSQL)
- Application logs
- Static assets

## Security Considerations

- Always use HTTPS in production
- Set a strong, unique `SECRET_KEY`
- Regularly update dependencies
- Monitor logs for suspicious activity
- Use environment variables for all sensitive data
- Implement rate limiting for forms (consider adding additional middleware)

## Scaling

For high-traffic sites, consider:
- Adding a load balancer
- Using multiple application containers
- Database read replicas
- CDN for static assets