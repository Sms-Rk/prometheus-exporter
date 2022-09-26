#ARG basetag="515-signed-ubuntu22.04"  # Ubuntu only
FROM nvcr.io/nvidia/driver:515-signed-ubuntu22.04

LABEL creator="SmsRk" \
      company="Targoman" \
      discription="dockerfile for prometheus exporter"


ENV DEBIAN_FRONTEND=noninteractive

# Update APT sources
RUN . /etc/os-release && [ "${NAME}" = "Ubuntu" ] && \
  echo "deb [arch=amd64] http://archive.ubuntu.com/ubuntu ${UBUNTU_CODENAME} main universe" > /etc/apt/sources.list && \
  echo "deb [arch=amd64] http://archive.ubuntu.com/ubuntu ${UBUNTU_CODENAME}-updates main universe" >> /etc/apt/sources.list && \
  echo "deb [arch=amd64] http://archive.ubuntu.com/ubuntu ${UBUNTU_CODENAME}-security main universe" >> /etc/apt/sources.list

# Install Python 3
RUN apt-get update && \
  apt-get install --quiet --yes --no-install-recommends \
  python3-dev python3-pip python3-setuptools python3-wheel locales && \
  rm -rf /var/lib/apt/lists/*

RUN pip install prometheus-client

# Setup locale
ENV LC_ALL=C.UTF-8
RUN update-locale LC_ALL="C.UTF-8"

COPY nvitop-sm-exporter.py requierments.txt ./
RUN pip3 install -r requierments.txt
RUN pip install nvitop

EXPOSE 9000

# Entrypoint
ENTRYPOINT [ "python3","nvitop-sm-exporter.py" ]
