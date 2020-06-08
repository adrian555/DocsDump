* .cshrc to include PATH and PUBLIC_IP

* systemctl stop httpd

* yum update

* install new version docker-ce
```
yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
```

* list docker version if needed
```
yum list docker-ce --showduplicates | sort -r
yum install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io
```

* start docker
```
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

* download kubectl
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.17.0/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin
```

* download minikube
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v1.6.2/minikube-linux-amd64
chmod +x minikube
mv minikube /usr/local/bin
```

* start minikube
```
minikube start --vm-driver=none --cpus 6 --memory 12288 --disk-size=120g
```

* create nfs service
```
yum install -y nfs-utils rpcbind
mkdir -p /storage/nfs
chmod -R 777 /storage/nfs/
cat >> /etc/exports << EOF
/storage/nfs  *(rw,sync,no_subtree_check,no_root_squash,no_all_squash)
EOF
exportfs
systemctl restart nfs
```

* create nfs deployment/storageclass

```
sed -e "s/%NFS_SERVER%/${PUBLIC_IP}/g" ./nfs/nfs-deployment.yaml > /tmp/nfs-dep.yaml
kubectl -n default create -f /tmp/nfs-dep.yaml
```

set_up_oc4.sh 10.16.45.186
oc patch storageclass nfs-client -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
cpd-linux adm --repo ./repo.yaml --assembly lite --namespace zen --apply
cpd-linux --repo ./repo.yaml --assembly lite --namespace zen --storageclass nfs-client
cpd-linux adm --repo wos-repo.yaml --assembly aiopenscale --namespace zen --apply
cpd-linux --repo wos-repo.yaml --assembly aiopenscale --namespace zen --storageclass nfs-client