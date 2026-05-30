\# SwiftBus - Cloud-Based Bus Ticket Booking Platform



A fully functional, secure bus ticket booking web application built with Python Flask and deployed on AWS Cloud using DevSecOps best practices.



\## Live Demo

https://swiftbus.duckdns.org



\## Features

\- User registration and login with bcrypt password hashing

\- Bus search by route and date

\- Seat booking with real-time availability

\- Admin panel for managing buses, users, and bookings

\- HTTPS with SSL/TLS certificate

\- CI/CD pipeline with GitHub Actions



\## Tech Stack

\- \*\*Backend:\*\* Python Flask

\- \*\*Database:\*\* SQLite (local) / MySQL RDS (production)

\- \*\*Web Server:\*\* Nginx + Gunicorn

\- \*\*Cloud:\*\* AWS EC2, VPC, S3, CloudWatch

\- \*\*Security:\*\* bcrypt, SSL/TLS, Fail2ban, UFW

\- \*\*DevOps:\*\* Git, GitHub Actions



\## Setup Instructions



\### Local Development

1\. Clone the repository

&#x20;  git clone https://github.com/mathewanjitha2007-glitch/swiftbus-app.git



2\. Create virtual environment

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate



3\. Install dependencies

&#x20;  pip install -r requirements.txt



4\. Run the application

&#x20;  python app.py



5\. Open browser at http://127.0.0.1:5000



\### Production Deployment

Deployed on AWS EC2 (Ubuntu 22.04, t3.micro) in Mumbai region.

Domain: https://swiftbus.duckdns.org



\## Security Features

\- Password hashing with bcrypt

\- HTTPS with Let's Encrypt SSL certificate

\- SQL injection prevention with SQLAlchemy ORM

\- SSH hardening (key-based auth, no root login)

\- Fail2ban brute force protection

\- UFW firewall configuration



\## Monitoring

\- AWS CloudWatch CPU utilization alerts

\- Status check monitoring

\- Email notifications via SNS



\## Project Structure

\- app.py - Main Flask application

\- models.py - Database models

\- templates/ - HTML templates

\- requirements.txt - Python dependencies

\- .github/workflows/ - CI/CD pipeline

