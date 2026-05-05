FROM jenkins/jenkins:lts

USER root

RUN apt update && \
    apt install -y python3 python3-venv python3-pip && \
    apt clean


USER jenkins