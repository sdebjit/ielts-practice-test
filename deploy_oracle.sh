#!/usr/bin/env bash
# ==============================================================================
# IELTS Master - Automated Oracle Cloud Free Tier VM Deployment Script
# Supports: Ubuntu 22.04/24.04 LTS (default 'ubuntu') & Oracle Linux 8/9 ('opc')
# ==============================================================================

set -e

echo "=========================================================="
echo " 🚀 Initializing IELTS Master Deployment on Oracle Cloud VM"
echo "=========================================================="

APP_DIR="/opt/ielts-gemini-prep"
if [ -n "$SUDO_USER" ]; then
    CURRENT_USER="$SUDO_USER"
else
    CURRENT_USER=$(whoami)
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID=$ID
else
    OS_ID="unknown"
fi

echo "Detected OS: $OS_ID ($NAME), Target Service User: $CURRENT_USER"

# 1. Update packages and install prerequisites
echo "--> Installing dependencies (Python 3, Nginx, Git, Curl, UFW/Iptables)..."
if [[ "$OS_ID" == "ubuntu" || "$OS_ID" == "debian" ]]; then
    sudo apt-get update -y
    echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections || true
    echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections || true
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip nginx curl git iptables-persistent netfilter-persistent certbot python3-certbot-nginx
elif [[ "$OS_ID" == "ol" || "$OS_ID" == "rhel" || "$OS_ID" == "centos" || "$OS_ID" == "rocky" ]]; then
    sudo dnf update -y
    sudo dnf install -y python3 python3-pip nginx curl git firewalld
    sudo systemctl enable --now firewalld
fi

# 2. Setup Application Directory
echo "--> Preparing application directory at $APP_DIR..."
sudo mkdir -p "$APP_DIR"

SCRIPT_SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$SCRIPT_SOURCE_DIR" != "$APP_DIR" ]; then
    echo "--> Copying files to $APP_DIR..."
    cp -r "$SCRIPT_SOURCE_DIR"/* "$APP_DIR"/
fi

# Ensure correct permissions for application files and SQLite database
sudo chown -R "$CURRENT_USER":"$CURRENT_USER" "$APP_DIR"
if [ -d "$APP_DIR/data" ]; then
    sudo chmod -R 775 "$APP_DIR/data"
fi

# 3. Configure Oracle Cloud Host Firewall (Crucial Step on Oracle Cloud!)
echo "--> Configuring Host Firewall for Ports 80, 443, 8080..."
if [[ "$OS_ID" == "ubuntu" || "$OS_ID" == "debian" ]]; then
    # Oracle Cloud Ubuntu has pre-installed iptables rules that reject incoming traffic
    sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT || true
    sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT || true
    sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT || true
    sudo netfilter-persistent save || true

    if command -v ufw >/dev/null 2>&1; then
        sudo ufw allow 22/tcp || true
        sudo ufw allow 80/tcp || true
        sudo ufw allow 443/tcp || true
        sudo ufw allow 8080/tcp || true
        sudo ufw --force enable || true
    fi
elif [[ "$OS_ID" == "ol" || "$OS_ID" == "rhel" || "$OS_ID" == "centos" ]]; then
    sudo firewall-cmd --permanent --add-port=80/tcp || true
    sudo firewall-cmd --permanent --add-port=443/tcp || true
    sudo firewall-cmd --permanent --add-port=8080/tcp || true
    sudo firewall-cmd --reload || true
fi

# 4. Configure Systemd Service for IELTS Master
echo "--> Configuring systemd service (/etc/systemd/system/ielts-master.service)..."
cat <<EOF | sudo tee /etc/systemd/system/ielts-master.service
[Unit]
Description=IELTS Master Full-Stack Application Server
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/backend/server.py 8080
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ielts-master
sudo systemctl restart ielts-master

PUBLIC_IP=$(curl -s https://ifconfig.me || curl -s https://api.ipify.org || echo "<YOUR_VM_PUBLIC_IP>")
HEX_IP=$(echo "$PUBLIC_IP" | awk -F'.' '{printf("%02x%02x%02x%02x\n", $1, $2, $3, $4)}')
NIP_HEX_DOMAIN="${HEX_IP}.nip.io"

# 5. SSL / TLS Certificate Provisioning (Let's Encrypt / Certbot)
echo "--> Checking SSL certificate for ${NIP_HEX_DOMAIN} (nip.io hex notation)..."
if [ ! -f "/etc/letsencrypt/live/${NIP_HEX_DOMAIN}/fullchain.pem" ]; then
    echo "--> Requesting Let's Encrypt SSL certificate for ${NIP_HEX_DOMAIN}..."
    sudo certbot certonly --nginx -d "${NIP_HEX_DOMAIN}" --non-interactive --agree-tos -m debjit@ieltsmaster.com || true
fi

# 6. Configure Nginx Reverse Proxy with SSL
echo "--> Configuring Nginx reverse proxy..."
if [[ "$OS_ID" == "ubuntu" || "$OS_ID" == "debian" ]]; then
    sudo cp "$APP_DIR/nginx/ielts-master.conf" /etc/nginx/sites-available/ielts-master.conf
    sudo ln -sf /etc/nginx/sites-available/ielts-master.conf /etc/nginx/sites-enabled/ielts-master.conf
    sudo rm -f /etc/nginx/sites-enabled/default
else
    sudo cp "$APP_DIR/nginx/ielts-master.conf" /etc/nginx/conf.d/ielts-master.conf
fi

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

# 7. Verification
sleep 2
echo "--> Checking service status..."
if sudo systemctl is-active --quiet ielts-master; then
    echo "✅ ielts-master service is ACTIVE!"
else
    echo "⚠️ ielts-master service status check failed. Check logs with: journalctl -u ielts-master -n 50"
fi

echo ""
echo "=========================================================="
echo " 🎉 IELTS Master Successfully Deployed on Oracle Cloud!"
echo "=========================================================="
echo " 🔒 Secure HTTPS Access: https://${NIP_HEX_DOMAIN}"
echo " 🌐 Direct HTTP Access:   http://${PUBLIC_IP} (Redirects to HTTPS)"
echo " 🔌 Port 8080 Access:     http://${PUBLIC_IP}:8080"
echo ""
echo " Useful Management Commands:"
echo " - View logs:        sudo journalctl -u ielts-master -f"
echo " - Restart server:   sudo systemctl restart ielts-master"
echo " - Restart Nginx:    sudo systemctl restart nginx"
echo " - Check Certs:      sudo certbot certificates"
echo "=========================================================="
