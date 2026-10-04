ARG BASE_IMAGE=paperclip-asp:sideflash-local-test
FROM ${BASE_IMAGE}
USER root
COPY runtime /opt/startos
COPY operator-web /opt/paperclip/operator-web
ENTRYPOINT ["/usr/bin/tini","--","python3","/opt/startos/start.py"]
