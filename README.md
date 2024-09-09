
# FiveM DDoS Protection Setup Script

## Overview
This script is designed to help you set up basic DDoS protection for your FiveM server with `txAdmin`. It configures IPTables, Fail2Ban, and installs necessary tools like `iftop` and `nload` for monitoring.

## Features
- **DDoS Protection:** Rate limits UDP and TCP traffic on FiveM ports.
- **Fail2Ban Setup:** Protects against brute-force attacks on txAdmin and SSH.
- **MySQL Access Control:** Allows you to restrict MySQL access to specific IPs (e.g., home IP or VPN).
- **SSH Access:** Ensures that SSH access is always available, preventing server lockouts.
- **Monitoring Tools:** Installs `iftop` and `nload` for real-time network traffic monitoring.

## Requirements
- A server running Linux (Debian-based systems like Ubuntu recommended)
- Python 3 installed
```bash
IF NOT INSTALLED RUN:
apt-get install python3
```

## How to Use

### Step 1: Download the Script
Clone or download the script to your server.

### Step 2: Make the Script Executable
Run the following command to make the script executable:
```bash
chmod +x main.py
```

### Step 3: Run the Script
Execute the script with:
```bash
sudo python3 main.py
```

### Step 4: Follow the Prompts
The script will ask if you want to secure MySQL access to specific IP addresses. You can enter your home IP or VPN IP to restrict access.

## Monitoring Traffic
After the script runs, you can monitor your server's traffic in real-time using the following commands:
- **iftop:** Displays active network connections
```bash
sudo iftop
```
- **nload:** Shows incoming and outgoing traffic rates
```bash
sudo nload
```

## IPTables Rules
- FiveM port (default: 30120) and txAdmin port (default: 40120) are rate-limited to prevent DDoS attacks.
- MySQL port (3306) is secured to allow access only from trusted IPs if chosen during setup.
- SSH (default: 22) is always allowed, ensuring you don’t lose server access.

## Fail2Ban Setup
- Protects txAdmin login by banning IPs after multiple failed login attempts.
- SSH brute-force protection is enabled by default.


