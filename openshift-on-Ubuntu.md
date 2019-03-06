# Install OpenShift on Ubuntu

[link](https://medium.com/@maheshacharya_44641/install-openshift-origin-on-ubuntu-18-04-7b98773c2ee6)

## Install `docker`

Follow the official install instruction [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)

```command line
# refresh Ubuntu packages
apt-get update

# install dependencies
apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# add GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# add stable release repositories
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# refresh packages again
apt-get update

# install the latest version
apt-get install -y docker-ce
```

To install a specific version of docker ce, list the available version with command

```command line
# list available versions
apt-cache madison docker-ce
### docker-ce | 18.09.0~ce-0~ubuntu | https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages

# install specific version
apt-get install -y docker-ce=<VERSION>
```

## Download OpenShift Origin

From the [release link](https://github.com/openshift/origin/releases), download the client tool to install.

```command line
wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
tar zxvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
cp oc kubectl /usr/local/bin
```

## Add Insecure registry to docker daemon and restart docker service

```command line
cat << EOF > /etc/docker/daemon.json 
{
    "insecure-registries" : [ "172.30.0.0/16" ]
}
EOF
systemctl restart docker
```

## Start OpenShift cluster

```command line
export VM_IP=<host_IP_address>
oc cluster up --routing-suffix=$VM_IP.xip.io --public-hostname=$(hostname) --base-dir=/var/lib/origin/openshift.local.clusterup --enable=service-catalog,router,registry,web-console,persistent-volumes,rhel-imagestreams,automation-service-broker