FROM python:latest

RUN echo 'root:root' | chpasswd
ENV SSH_AUTH_SOCK=/ssh-agent

# --- Create non-root user with the ability to use sudo --- #
ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN mkdir /home/developer/Dash-Website/ 
WORKDIR /home/developer/Dash-Website/

USER $USERNAME

# docker build -t website_raw .
# docker run -it -d -v /home/theovincent/HMS/docker_try/:/home/developer/website_project/ -p 8050:8050 --volume $SSH_AUTH_SOCK:/ssh-agent --env SSH_AUTH_SOCK=/ssh-agent website_raw bash
