#!/bin/sh
# SPDX-License-Identifier: BSD-3-Clause

# This Source Code Form is subject to the terms of the BSD-3-Clause License.
# If a copy of the BSD-3-Clause License was not distributed with this file, You can obtain one at https://opensource.org/licenses/BSD-3-Clause.
#
# Stefan Zintgraf, stefan@zintgraf.de

# Set up VNC password if not already set
if [ ! -f ~/.vnc/passwd ]; then
    mkdir -p ~/.vnc
    echo "${VNC_PASSWORD:-password}" | vncpasswd -f > ~/.vnc/passwd
    chmod 600 ~/.vnc/passwd
fi

# Create xstartup script for XFCE4 if it doesn't exist
if [ ! -f ~/.vnc/xstartup ]; then
    mkdir -p ~/.vnc
    cat > ~/.vnc/xstartup << 'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
startxfce4 &
EOF
    chmod +x ~/.vnc/xstartup
fi

# Start dbus (required for XFCE4)
service dbus start || true

# Start VNC server on display :1
export USER=$(whoami)
export HOME=$HOME
vncserver :1 -geometry ${VNC_RESOLUTION:-1920x1080} -depth 24 -localhost no -SecurityTypes VncAuth -passwd ~/.vnc/passwd

# Keep container running
tail -f /dev/null
