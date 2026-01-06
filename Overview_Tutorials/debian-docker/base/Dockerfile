# SPDX-License-Identifier: BSD-3-Clause

# This Source Code Form is subject to the terms of the BSD-3-Clause License.
# If a copy of the BSD-3-Clause License was not distributed with this file, You can obtain one at https://opensource.org/licenses/BSD-3-Clause.
#
# Stefan Zintgraf, stefan@zintgraf.de

# Docker Image for AI ready C/C++ and Python Development

FROM debian:latest

# Update and install packages
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get -y update \
  && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade \
  && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
    # Base essentials
    locales \
    ca-certificates \
    bash \
    bash-completion \
    gpg \
    less \
    sudo \
    nano \
    mousepad \
    curl \
    wget \
    git \
    iproute2 \
    net-tools \
    \
    # C/C++ build essentials
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    gdb \
    \
    # Python development environment
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libssl-dev \
    libffi-dev \
    pkg-config\
    \
    # Windows development environment
    binutils-mingw-w64 \
    mingw-w64 \
    mingw-w64-tools \
    \
    # GUI Desktop Environment (XFCE4 - lightweight)
    dbus-x11 \
    x11-xserver-utils \
    xorgxrdp \
    xrdp \
    tigervnc-standalone-server \
    tigervnc-common \
    xfce4 \
    xfce4-goodies \
    xfce4-clipman-plugin \
    xfce4-cpugraph-plugin \
    xfce4-netload-plugin \
    xfce4-screenshooter \
    xfce4-taskmanager \
    xfce4-terminal \
    xfce4-xkb-plugin \
    xfwm4-theme-breeze \
    gvfs \
    libglib2.0-bin \
    \
    # Clean up to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Set locales
RUN \
     sed -i -e 's/# \(en_US\.UTF-8 .*\)/\1/' /etc/locale.gen \
  && sed -i -e 's/# \(de_DE\.UTF-8 .*\)/\1/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Accept build arguments for user credentials
ARG DOCKER_USERNAME=dev
ARG DOCKER_PASSWORD=dev
ARG VNC_PASSWORD=password
# Optional: Set USE_SSH=1 to enable SSH server, USE_SMB=1 to enable SMB server
ARG USE_SSH=
ARG USE_SMB=

# Set up VNC environment
ENV VNC_RESOLUTION=1920x1080
ENV VNC_PASSWORD=${VNC_PASSWORD}

# Create User and set password
# add git config to allow access to not owned git repositories
RUN \
  useradd --create-home --shell /bin/bash --comment "defaultuser" --groups sudo,adm ${DOCKER_USERNAME} \
  && echo "${DOCKER_USERNAME}:${DOCKER_PASSWORD}" | chpasswd \
  && git config --system --add safe.directory '*' \
  && /bin/dbus-uuidgen > /etc/machine-id # XFCE Config

# Conditionally install and configure SSH server
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  if [ -n "${USE_SSH}" ]; then \
    apt-get -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install openssh-server \
    && mkdir -p /var/run/sshd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config \
    && rm -rf /var/lib/apt/lists/*; \
  fi

# Conditionally install and configure Samba server
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  if [ -n "${USE_SMB}" ]; then \
    apt-get -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install samba \
    && mkdir -p /var/lib/samba/private \
    && mkdir -p /var/run/samba \
    && mkdir -p /home/${DOCKER_USERNAME}/share \
    && chown ${DOCKER_USERNAME}:${DOCKER_USERNAME} /home/${DOCKER_USERNAME}/share \
    && chmod 755 /home/${DOCKER_USERNAME}/share \
    && echo "[global]" > /etc/samba/smb.conf \
    && echo "   workgroup = WORKGROUP" >> /etc/samba/smb.conf \
    && echo "   server string = Debian Dev Server" >> /etc/samba/smb.conf \
    && echo "   security = user" >> /etc/samba/smb.conf \
    && echo "   map to guest = Bad User" >> /etc/samba/smb.conf \
    && echo "   dns proxy = no" >> /etc/samba/smb.conf \
    && echo "" >> /etc/samba/smb.conf \
    && echo "[share]" >> /etc/samba/smb.conf \
    && echo "   comment = Shared Folder" >> /etc/samba/smb.conf \
    && echo "   path = /home/${DOCKER_USERNAME}/share" >> /etc/samba/smb.conf \
    && echo "   browseable = yes" >> /etc/samba/smb.conf \
    && echo "   read only = no" >> /etc/samba/smb.conf \
    && echo "   guest ok = no" >> /etc/samba/smb.conf \
    && echo "   valid users = ${DOCKER_USERNAME}" >> /etc/samba/smb.conf \
    && echo "   create mask = 0664" >> /etc/samba/smb.conf \
    && echo "   directory mask = 0775" >> /etc/samba/smb.conf \
    && (echo "${DOCKER_PASSWORD}"; echo "${DOCKER_PASSWORD}") | smbpasswd -a -s ${DOCKER_USERNAME} \
    && smbpasswd -e ${DOCKER_USERNAME} \
    && rm -rf /var/lib/apt/lists/*; \
  fi

COPY start_rdp.sh /usr/bin/start_rdp.sh
RUN sed -i 's/\r$//' /usr/bin/start_rdp.sh && chmod +x /usr/bin/start_rdp.sh

COPY start_vnc.sh /usr/bin/start_vnc.sh
RUN sed -i 's/\r$//' /usr/bin/start_vnc.sh && chmod +x /usr/bin/start_vnc.sh

USER ${DOCKER_USERNAME}
WORKDIR /home/${DOCKER_USERNAME}

EXPOSE 3389/tcp
EXPOSE 5901/tcp
# SSH port (only exposed if USE_SSH is set)
# EXPOSE 22/tcp
# SMB ports (only exposed if USE_SMB is set)
# EXPOSE 139/tcp
# EXPOSE 445/tcp

ENTRYPOINT [ "/usr/bin/start_rdp.sh" ]

