# Use an Python3.6 official image as base image
FROM python:3.6-slim

# Developer information
MAINTAINER Samuel Xu <samuelxu999@gmail.com>

# ========================== Dependencies and tools installation =============================
# Install system tools and dependencies
RUN apt-get update && \
		apt-get install -y \
		build-essential libssl-dev libffi-dev \
		libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev \
		python3 python-dev python3-dev \
		python3-pip \
        cmake \
        git \
        wget \
        unzip \
        nano \
        jq


# Install pip tools and configurations
RUN python3 -m pip install --upgrade pip


# ===================================== golang configuration ================================
# ----------------------------- install go1.9.3 -------------------------------
ARG GO_PKG9=go1.9.3.linux-amd64.tar.gz

COPY ./"$GO_PKG9" /opt/

RUN cd /opt && \
	tar -C /usr/local -xzf /opt/"$GO_PKG9" && \
	rm -f /opt/"$GO_PKG9"


# =================================== ethereum configuration ===============================
# ------------------- build go-ethereum from source code -------------------

ARG GETH_VERSION="v1.7.3"

RUN export GOROOT=/usr/local/go && \
	export PATH=$PATH:$GOROOT/bin && \
	export GOPATH=/opt/go_proj && \
	export PATH=$PATH:$GOPATH/bin && \
	mkdir -p $GOPATH/src/github.com/ethereum && \
	cd $GOPATH/src/github.com/ethereum && \
	git clone https://github.com/ethereum/go-ethereum.git && \
	cd go-ethereum && \
	git checkout ${GETH_VERSION} && \
	make geth


# =================================== Swarm configuration ===============================
# ----------------------------- install go1.13.7 -------------------------------
ARG GO_PKG13=go1.13.7.linux-amd64.tar.gz

COPY ./"$GO_PKG13" /opt/

RUN cd /opt && \
	rm -rf /usr/local/go && \
	tar -C /usr/local -xzf /opt/"$GO_PKG13" && \
	rm -f /opt/"$GO_PKG13"

# ------------------------- build go-swarm from source code -----------------------
ARG SWARM_VERSION="v0.5.8"

RUN export GOROOT=/usr/local/go && \
	export PATH=$PATH:$GOROOT/bin && \
	export GOPATH=/opt/go_proj && \
	export PATH=$PATH:$GOPATH/bin && \	
	cd $GOPATH/src/github.com/ethereum && \
	git clone https://github.com/ethersphere/swarm && \
	cd swarm && \
	git checkout ${SWARM_VERSION} && \
	make swarm

# =================================== PATH Configure for root ===============================
# ------------------------- Add GOROOT and GOPATH to PATH ---------------
RUN echo 'export GOROOT=/usr/local/go' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOROOT/bin' >> ~/.bashrc

RUN echo 'export GOPATH=/opt/go_proj' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
	
# ------------------- Add GOETHEREUM to PATH -----------------
RUN echo 'export GOETHEREUM=$GOPATH/src/github.com/ethereum/go-ethereum/build' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOETHEREUM/bin' >> ~/.bashrc

# ------------------- Add GOSWARM to PATH -----------------
RUN echo 'export GOSWARM=$GOPATH/src/github.com/ethereum/swarm/build' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOSWARM/bin' >> ~/.bashrc


# =========================== Setup docker account ==================================
# Add user so that container does not run as root 
RUN useradd -m docker 
RUN echo "docker:samuelxu999" | chpasswd 
RUN usermod -s /bin/bash docker 
RUN usermod -aG sudo docker 
ENV HOME /home/docker

# =================================== PATH Configure for docker ===============================
# ------------------------- Add GOROOT and GOPATH to PATH ---------------
RUN echo 'export GOROOT=/usr/local/go' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOROOT/bin' >> ~/.bashrc

RUN echo 'export GOPATH=/opt/go_proj' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
	
# ------------------- Add GOETHEREUM to PATH -----------------
RUN echo 'export GOETHEREUM=$GOPATH/src/github.com/ethereum/go-ethereum/build' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOETHEREUM/bin' >> ~/.bashrc

# ------------------- Add GOSWARM to PATH -----------------
RUN echo 'export GOSWARM=$GOPATH/src/github.com/ethereum/swarm/build' >> ~/.bashrc && \
	echo 'export PATH=$PATH:$GOSWARM/bin' >> ~/.bashrc


## ============================ swarm node directory setup =============================
RUN mkdir -p ${HOME}/swarm/node
RUN mkdir -p ${HOME}/swarm/cmd

## change owner to docker
RUN chown -R docker:docker ${HOME}/swarm

## ============================ app work directory setup =============================
RUN mkdir ${HOME}/app

## --------- app code and files ---------
COPY ./app/ ${HOME}/app/
COPY ./requirements.txt ${HOME}/app/

## change owner to docker
RUN chown -R docker:docker ${HOME}/app

## ----------- Install app requirements ------------
# Install PycURL
RUN	apt-get install -y libcurl4-gnutls-dev libgnutls28-dev python3-pycurl

RUN  python3 -m pip install -r ${HOME}/app/requirements.txt

## Minimize image size 
RUN apt-get autoremove -y && apt-get autoclean -y

WORKDIR ${HOME}/app
