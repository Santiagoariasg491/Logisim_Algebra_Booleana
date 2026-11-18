# Logisim Evolution en un contenedor, accesible desde el navegador (noVNC).
# Imagen base con Java 21, requerido por Logisim Evolution 3.9.x
FROM eclipse-temurin:21-jre

ARG LOGISIM_VERSION=3.9.0
ARG LOGISIM_URL=https://github.com/logisim-evolution/logisim-evolution/releases/download/v${LOGISIM_VERSION}/logisim-evolution-${LOGISIM_VERSION}-all.jar

ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:0 \
    RESOLUTION=1600x900

# Escritorio virtual (Xvfb), gestor de ventanas (openbox), servidor VNC y noVNC
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        xvfb x11vnc openbox novnc websockify \
        fonts-dejavu-core libxtst6 libxrender1 libxi6 \
        ca-certificates curl \
    && ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html \
    && rm -rf /var/lib/apt/lists/*

# Descarga de Logisim Evolution
RUN mkdir -p /opt/logisim \
    && curl -fsSL "${LOGISIM_URL}" -o /opt/logisim/logisim-evolution.jar

# Script de arranque: Xvfb -> openbox -> x11vnc -> noVNC -> Logisim
RUN cat > /usr/local/bin/start.sh <<'EOF'
#!/bin/bash
set -e

Xvfb "${DISPLAY}" -screen 0 "${RESOLUTION}x24" -nolisten tcp &

# Esperar a que el servidor X esté listo
for i in $(seq 1 50); do
  [ -S "/tmp/.X11-unix/X${DISPLAY#:}" ] && break
  sleep 0.2
done

openbox &
x11vnc -display "${DISPLAY}" -forever -shared -nopw -quiet -rfbport 5900 &
websockify --web /usr/share/novnc 6080 localhost:5900 &

echo "Logisim Evolution listo: abre http://localhost:6080/vnc.html?autoconnect=true&resize=scale"

exec java -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true \
     -jar /opt/logisim/logisim-evolution.jar
EOF
RUN chmod +x /usr/local/bin/start.sh

# Usuario sin privilegios (la imagen base puede traer ya un usuario con UID 1000)
RUN (userdel -r ubuntu 2>/dev/null || true) \
    && useradd -m -u 1000 -s /bin/bash logisim \
    && mkdir -p /workspace \
    && chown logisim:logisim /workspace

USER logisim
WORKDIR /workspace

EXPOSE 6080

CMD ["/usr/local/bin/start.sh"]
