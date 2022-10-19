# Prometheus GPU Exporter
Including Dockerfile,Docker-compose,Ansible playbook

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Ansible](https://img.shields.io/badge/ansible-%231A1918.svg?style=for-the-badge&logo=ansible&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

>This repository contains:
- python script for custom prometheus exporter form nvitop
- docker compose for running exporters 
- ansible playbook for running compose on gpu servers



## Usage

```sh
ansible-playbook -i hosts.ini exporter-play.yaml
```
