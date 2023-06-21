cd "$(dirname "$0")"

read -p "User to run on (root not recommended): " uservar 

# Edit the sudoers file to allow us to read the certificate
sudo tee -a /etc/sudoers > /dev/null <<EOT
$uservar ALL = (root:root) NOPASSWD: /usr/bin/cat /etc/elasticsearch/certs/http_ca.crt
EOT

# Add a file to cron to run this project continually
sudo tee /etc/cron.d/cradlepoint_middleware > /dev/null <<EOT
SHELL="/bin/bash"

*/5 * * * * $uservar $PWD/run.cron.bash > $PWD/cron/recent-cron.log
EOT
