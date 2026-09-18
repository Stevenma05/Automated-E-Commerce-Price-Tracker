# Automated E-Commerce Price Tracker

A Python application that automates product price monitoring across multiple e-commerce platforms. Built with Selenium and deployed on AWS EC2, it checks prices and sends email reports every five hours.

## Features

- **Automated price monitoring:** Uses Selenium to collect product prices without manual browsing.
- **Multi-platform tracking:** Scans products across multiple e-commerce websites.
- **Scheduled checks:** Runs price scans every five hours.
- **Email reports:** Delivers scheduled price updates through SMTP every five hours.
- **Cloud deployment:** Runs on AWS EC2 to support ongoing monitoring.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Application logic and automation |
| Selenium | Browser automation and price collection |
| AWS EC2 | Cloud hosting |
| SMTP | Email report delivery |

## How It Works

1. The application runs a scheduled price check every five hours.
2. Selenium visits the tracked product pages and collects pricing information.
3. The collected prices are compiled into an email report.
4. SMTP delivers the report to the configured recipient.

## Results

- Replaced manual browsing with automated price checks.
- Improved tracking efficiency by **75%**.
- Achieved **100% notification reliability** during the reported project period.
