#!/usr/bin/env bash
# ==============================================================================
# IELTS Master - 1-Command Local to Oracle VM Deployer & Sync Script
# Usage: ./sync_to_oracle_vm.sh <VM_PUBLIC_IP> <SSH_PRIVATE_KEY_PATH> [USERNAME]
# Example: ./sync_to_oracle_vm.sh 152.67.12.34 ~/.ssh/oracle_key.key ubuntu
# ==============================================================================

set -e

VM_IP="$1"
SSH_KEY="$2"
SSH_USER="${3:-ubuntu}"

if [ -z "$VM_IP" ] || [ -z "$SSH_KEY" ]; then
    echo "=========================================================="
    echo " 🚀 IELTS Master - Oracle VM Deployer"
    echo "=========================================================="
    echo "Usage: $0 <VM_PUBLIC_IP> <SSH_KEY_PATH> [USERNAME]"
    echo ""
    echo "Examples:"
    echo "  Ubuntu VM:       $0 129.153.12.34 ~/.ssh/ssh-key-2026.key ubuntu"
    echo "  Oracle Linux VM: $0 129.153.12.34 ~/.ssh/ssh-key-2026.key opc"
    echo "=========================================================="
    exit 1
fi

if [ ! -f "$SSH_KEY" ]; then
    echo "Error: Private key file '$SSH_KEY' does not exist."
    exit 1
fi

# Ensure correct key permissions
chmod 400 "$SSH_KEY"

echo "--> Testing SSH connection to ${SSH_USER}@${VM_IP}..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 -i "$SSH_KEY" "${SSH_USER}@${VM_IP}" "echo 'SSH Connection successful!'"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_TMP="/home/${SSH_USER}/ielts-gemini-prep"

echo "--> Uploading application files to VM (${REMOTE_TMP})..."
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude 'server.log' \
    -e "ssh -o StrictHostKeyChecking=no -i $SSH_KEY" \
    "$SCRIPT_DIR/" "${SSH_USER}@${VM_IP}:${REMOTE_TMP}/"

echo "--> Executing automated deployment script on Oracle VM..."
ssh -o StrictHostKeyChecking=no -t -i "$SSH_KEY" "${SSH_USER}@${VM_IP}" "chmod +x ${REMOTE_TMP}/deploy_oracle.sh && sudo ${REMOTE_TMP}/deploy_oracle.sh"

echo ""
echo "=========================================================="
echo " Deployment completed!"
echo " Visit your live application at: http://${VM_IP}"
echo "=========================================================="
