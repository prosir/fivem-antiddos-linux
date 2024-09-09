import os
import subprocess
import sys

def run_command(command):
    try:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}\n{e}")
        sys.exit(1)

def install_packages():
    print("Installing necessary packages (iptables, fail2ban, iftop, nload)...")
    run_command('sudo apt-get update')
    run_command('sudo apt-get install -y iptables fail2ban iftop nload')

def configure_iptables(trusted_ip=None, mysql_secure=False):
    print("Configuring iptables rules...")
    fivem_port = "30120"
    txadmin_port = "40120"
    ssh_port = "22"
    print("Ensuring SSH is open for all connections.")
    run_command(f'sudo iptables -A INPUT -p tcp --dport {ssh_port} -j ACCEPT')
    run_command(f'sudo iptables -A INPUT -p udp --dport {fivem_port} -m limit --limit 300/second --limit-burst 600 -j ACCEPT')
    run_command(f'sudo iptables -A INPUT -p udp --dport {fivem_port} -j DROP')
    run_command(f'sudo iptables -A INPUT -p tcp --dport {fivem_port} -m limit --limit 50/second --limit-burst 100 -j ACCEPT')
    run_command(f'sudo iptables -A INPUT -p tcp --dport {fivem_port} -j DROP')
    run_command(f'sudo iptables -A INPUT -p tcp --dport {txadmin_port} -m limit --limit 10/second --limit-burst 20 -j ACCEPT')
    run_command(f'sudo iptables -A INPUT -p tcp --dport {txadmin_port} -j DROP')
    run_command('sudo iptables -A INPUT -p icmp -m limit --limit 1/second -j ACCEPT')
    run_command('sudo iptables -A INPUT -p icmp -j DROP')
    if mysql_secure:
        mysql_port = "3306"
        if trusted_ip:
            print(f"Allowing MySQL access only for trusted IP: {trusted_ip}")
            run_command(f'sudo iptables -A INPUT -p tcp --dport {mysql_port} -s {trusted_ip} -j ACCEPT')
            run_command(f'sudo iptables -A INPUT -p tcp --dport {mysql_port} -j DROP')
        else:
            print("No trusted IP provided, blocking MySQL from all external access.")
            run_command(f'sudo iptables -A INPUT -p tcp --dport {mysql_port} -j DROP')
    run_command('sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null')

def configure_fail2ban():
    print("Configuring Fail2Ban...")
    run_command('sudo systemctl enable fail2ban')
    run_command('sudo systemctl start fail2ban')
    txadmin_log_path = "/path/to/txAdminLogs.log"
    fail2ban_txadmin_config = f"""
[txadmin]
enabled = true
port = 40120
filter = txadmin
logpath = {txadmin_log_path}
maxretry = 3
bantime = 600
    """
    with open('/etc/fail2ban/jail.local', 'a') as f:
        f.write(fail2ban_txadmin_config)
    txadmin_filter = """
[Definition]
failregex = .*Login attempt failed.*
ignoreregex =
    """
    with open('/etc/fail2ban/filter.d/txadmin.conf', 'w') as f:
        f.write(txadmin_filter)
    run_command('sudo systemctl restart fail2ban')

def install_monitoring_tools():
    print("Installing and configuring monitoring tools...")
    print("To monitor real-time traffic, run 'sudo iftop' or 'sudo nload' in your terminal.")

def ask_mysql_secure():
    answer = input("Do you want to secure MySQL access (only allow specific IPs to connect)? [y/n]: ").lower()
    if answer == 'y':
        trusted_ip = input("Enter the trusted IP or VPN that can access MySQL (e.g., your home IP): ").strip()
        return True, trusted_ip
    else:
        return False, None

def setup_system():
    install_packages()
    mysql_secure, trusted_ip = ask_mysql_secure()
    configure_iptables(trusted_ip, mysql_secure)
    configure_fail2ban()
    install_monitoring_tools()

if __name__ == "__main__":
    print("Starting DDoS protection setup for FiveM server...")
    setup_system()
    print("DDoS protection setup complete! Your FiveM server is now more secure.")
