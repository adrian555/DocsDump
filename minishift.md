# Install minishift on centos

Install docker:

```command line
yum install docker -y
systemctl restart docker
```

Generate ssh key if not yet:

```command line
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
ssh-copy-id root@localhost 
```

Install minishift from [link](https://github.com/minishift/minishift/releases)

```command line
curl -L -o minishift.tgz https://github.com/minishift/minishift/releases/download/v1.31.0/minishift-1.31.0-linux-amd64.tgz
tar zxvf minishift.tgz
cp minishift*linux*/minishift /usr/local/bin
```

Start minishift with generic vm-driver:

```command line
export VM_IP=<vm_ip_address>
minishift start --vm-driver=generic --remote-ipaddress=$VM_IP --remote-ssh-user=root --remote-ssh-key=/root/.ssh/id_rsa --cpus 6 --memory 12G --disk-size 240g
```

Note, if got `403 API rate limit` error, set following and try to restart minishift.

```command line
export MINISHIFT_GITHUB_API_TOKEN=552aa53883753a95a91e5a43b367624310cb6dd5
```

Add path to `oc` in .bash_profile `/var/lib/minishift/bin`.

Log in to minishift with admin:

```command line
oc login -u system:admin
```

# Install minishift on ubuntu

[link](https://docs.okd.io/latest/minishift/getting-started/setting-up-virtualization-environment.html)

Set up kvm:

```command line
apt update
apt install -y libvirt-bin qemu-kvm
```

Add self to libvirt(d) group

```command line
usermod -a -G libvirtd $(whoami)
newgrp libvirtd
```

Install kvm driver

```command line
curl -L https://github.com/dhiltgen/docker-machine-kvm/releases/download/v0.10.0/docker-machine-driver-kvm-ubuntu16.04 -o /usr/local/bin/docker-machine-driver-kvm
chmod +x /usr/local/bin/docker-machine-driver-kvm
```

Check the status of libvirtd with `systemctl is-active libvirtd`, if not, start it with `systemctl start libvirtd`.

Check default libvirt network with `virsh net-list --all`. If no default network is active, run `virsh net-start default` followed by `virsh net-autostart default`.

Install minishift from [link](https://github.com/minishift/minishift/releases)

```command line
curl -L -o minishift.tgz https://github.com/minishift/minishift/releases/download/v1.30.0/minishift-1.30.0-linux-amd64.tgz
tar zxvf minishift.tgz
cp minishift*linux*/minishift /usr/local/bin
```

Install `docker-machine`

```command line
base=https://github.com/docker/machine/releases/download/v0.16.0 &&
  curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine &&
  install /tmp/docker-machine /usr/local/bin/docker-machine
```

Start minishift cluster

```command line
minishift start --vm-driver kvm --cpus 6 --memory 12G --disk-size 120g
```

With kvm, failed at `Failed to decode dnsmasq lease status: unexpected end of JSON input`.

# Install minishift with `virtualbox`

Install virtualbox [link](https://linuxize.com/post/how-to-install-virtualbox-on-ubuntu-18-04/)

```command line
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -
add-apt-repository "deb [arch=amd64] http://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib"
apt update
apt install virtualbox-6.0
```

(optional) Install virtualbox extension pack

```command line
wget https://download.virtualbox.org/virtualbox/6.0.0/Oracle_VM_VirtualBox_Extension_Pack-6.0.0.vbox-extpack
VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-6.0.0.vbox-extpack
```

After minishift is installed (refer to above), then start the minishift cluster as follow:

```command line
minishift start --vm-driver virtualbox --cpus 6 --memory 12G --disk-size 120g
```

to list the logs, run with `--show-libmachine-logs -v10`.


install with generic

The server is accessible via web console at:
    https://9.30.250.151:8443/console

You are logged in as:
    User:     developer
    Password: <any value>

To login as administrator:
    oc login -u system:admin

