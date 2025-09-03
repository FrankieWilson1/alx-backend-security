# alx-backend-security

This project is a comprehensive Django application module designed to demonstrate best practices for tracking, securing, and analyzing IP addresses in a web environment. It utilizes a combination of custom middleware, background tasks, and third-party libraries to build a robust system for security and analytics.

## Features

- **IP Request Logging**: Custom middleware logs every incoming request, including the IP address and request path, to the database. This provides a detailed history of all user activity.
- **IP Blacklisting**: A custom management command allows you to add specific IP addresses to a blacklist. A middleware then automatically blocks any requests originating from these IPs, returning a 403 Forbidden response.
- **IP Geolocation**: The application integrates with a geolocation API to enrich logged IP addresses with geographical data, such as country and city. This is useful for analytics and fraud detection.
- **Rate Limiting**: Using the django-ratelimit library, views can be protected with rate limits to prevent abuse and brute-force attacks. Different limits are configured for authenticated and anonymous users.
- **Anomaly Detection**: A scheduled Celery task runs periodically to analyze the request logs. It flags suspicious IPs based on criteria like a high volume of requests or attempts to access sensitive URLs (e.g., `/admin/`).

## Setup

Follow these steps to set up and run the project locally.

1. **Clone the Repository**

   Clone the project from GitHub and navigate into the directory.

   ```bash
   git clone https://github.com/FrankieWilson1/alx-backend-security.git
   cd alx-backend-security
   ```

2. **Set up the Environment**

   Create and activate a Python virtual environment.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   Install all the required Python packages.

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Project**

   - **Database Migrations**: Apply the database migrations to create the necessary tables.

   ```bash
   python manage.py makemigrations ip_tracking
   python manage.py migrate
   ```

   - **IPinfo API Token**: Add your API token from ipinfo.io to your `alx_backend_security/settings.py` file.

   ```python
   IPINFO_TOKEN = 'YOUR_API_TOKEN'
   ```

   - **Create a Superuser**: Create a superuser to access the Django admin panel.

   ```bash
   python manage.py createsuperuser
   ```

## How to Use

1. **Run the Django Server**

   Start the Django development server.

   ```bash
   python manage.py runserver
   ```

2. **Run Celery Workers**

   To enable anomaly detection, you must run a Celery worker and the Celery Beat scheduler in separate terminal windows.

   - **Celery Worker**:

   ```bash
   celery -A alx_backend_security worker --loglevel=info
   ```

   - **Celery Beat**:

   ```bash
   celery -A alx_backend_security beat
   ```

3. **Block an IP Address**

   Use the custom management command to block an IP.

   ```bash
   python manage.py block_ip 1.2.3.4 --reason "Spam bot"
   ```

4. **Test Rate Limiting**

   Access the login page to test the rate limiting functionality.

   ```bash
   http://127.0.0.1:8000/login/
   ```

   Refresh the page more than 5 times in a minute to trigger the rate limit and receive a 429 Too Many Requests response.

## Project Structure

```
.
├── alx_backend_security/
│   ├── __init__.py
│   ├── celery.py # Celery app configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ip_tracking/
│   ├── __init__.py
│   ├── admin.py
│   ├── management/
│   │   └── commands/
│   │       └── block_ip.py # Custom command to block IPs
│   ├── migrations/
│   ├── middleware.py # IP logging and blacklisting logic
│   ├── models.py # Database models for RequestLog, BlockedIP, SuspiciousIP
│   ├── tasks.py # Celery tasks for anomaly detection
│   ├── urls.py
│   └── views.py # View to apply rate limiting
└── manage.py
```
