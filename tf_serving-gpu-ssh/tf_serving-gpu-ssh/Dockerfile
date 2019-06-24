FROM tf-serving-gpu-apt:v1
ENV PASSWORD="123456"
ENV XRDP_PORT=3389 SSH_PORT=22
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /root
RUN mv /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/cuda.list.bak
RUN mv /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/nvidia-ml.list.bak
RUN apt-get update && apt-get purge tightvncserver xrdp && \
apt-get install -y \
xrdp xfce4 xfce4-goodies vnc4server tightvncserver \
vim curl net-tools iputils-ping firefox sudo supervisor wget python-pip python-dev \
gedit \
python-software-properties software-properties-common aptitude locales \
ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy fcitx fcitx-googlepinyin \
openssh-server
RUN mkdir /var/run/sshd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
#config xrdp
RUN sed -i '/param7=/a\param8=-SecurityTypes' /etc/xrdp/sesman.ini
RUN sed -i '/param8=-SecurityTypes/a\param9=None' /etc/xrdp/sesman.ini
RUN mkdir /root/.ssh
RUN mkdir /root/.init
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "xfce4-session" > ~/.xsession
#set env config
RUN echo 'export PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/sbin:/sbin:$PATH' >> /root/.bashrc
ADD ./startup.sh /root/.init
ADD ./config.sh /root/.init
ADD ./models /models
RUN chmod a+x /root/.init/startup.sh && chmod a+x /root/.init/config.sh
EXPOSE $XRDP_PORT $SSH_PORT
RUN apt-get clean && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENTRYPOINT ["/root/.init/startup.sh"]