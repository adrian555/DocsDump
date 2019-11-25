* add following to .bashrc

```command line
export PATH=.:$HOME/bin:$PATH
export PUBLIC_IP=`wget http://ipecho.net/plain -O - -q ; echo`
```

* stop `httpd`

```command line
systemctl stop httpd
```

* install docker latest ce version

```command line
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
systemctl enable docker
systemctl start docker
cat << EOF >/etc/docker/daemon.json
{
 "insecure-registries": [
 "172.30.0.0/16"
 ]
}
EOF
systemctl restart docker
```

* install dependencies

```command line
yum install -y wget git net-tools httpd-tools bind-utils iptables-services bridge-utils bash-completion
yum install -y  https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```

* download oc client tool

```command line
wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
tar -xzvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
cp openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/local/bin/
cp ./openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/kubectl /usr/local/bin/
```

* start the cluster

```command line
oc cluster up --public-hostname=${PUBLIC_IP} --base-dir=/var/lib/origin/openshift.local.clusterup --enable=service-catalog,router,registry,web-console,persistent-volumes,rhel-imagestreams
```

* install `helm`

```command line
curl -LO https://git.io/get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
oc create sa tiller -n kube-system
oc adm policy add-cluster-role-to-user cluster-admin -z tiller -n kube-system
helm init --service-account tiller --upgrade
```

* create `nfs-client` storageClass

```command line
# start nfs service
mkdir -p /storage/nfs
chmod -R 777 /storage/nfs/
yum install -y nfs-utils rpcbind
cat >> /etc/exports << EOF
/storage/nfs  *(rw,sync,no_subtree_check,no_root_squash,no_all_squash)
EOF
exportfs
systemctl restart nfs

# deploy nfs-client storage class
oc login -u system:admin
oc project default
oc adm policy add-scc-to-user hostmount-anyuid -z nfs-nfs-client-provisioner
helm install --name nfs --set nfs.server=$PUBLIC_IP,nfs.path=/storage/nfs,storageClass.defaultClass=true,storageClass.provisionerName=nfs-provisioner,storageClass.archiveOnDelete=false stable/nfs-client-provisioner
```

* `ocup` command

```command line
oc cluster up --public-hostname=${PUBLIC_IP} --base-dir=/var/lib/origin/openshift.local.clusterup --enable=service-catalog,router,registry,web-console,persistent-volumes,rhel-imagestreams
```

* `ocdown` command

```command line
oc cluster down
for x in `df |grep /var/lib/origin |awk '{print $6}'`
do
  umount $x
done
rm -rf /var/lib/origin
```

* install python3

```command line
yum install -y python3
python3 -m venv p3
source p3/bin/activate
```

* install openaihub

```command line
pip install openaihub==v0.0.1.dev1
openaihub install --openshift --namespace kubeflow --verbose
```

