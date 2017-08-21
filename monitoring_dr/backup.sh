#!/bin/bash
#
# BACKUP GALAXY APPLICATION and some miscellaneous files
#
# 1. Other files
cd /home/ubuntu && tar -czf /mnt/tmp/galaxy_qld-ubuntu.tar.gz -T Backup.txt

# 2. Galaxy application files
cd /mnt/galaxy && sudo tar -czf /mnt/tmp/galaxy_qld-galaxy.tar.gz -T Backup.txt

# 3. Backup Database
sudo -u galaxy pg_dump -p 5930 galaxy >/mnt/tmp/galaxy.sql
