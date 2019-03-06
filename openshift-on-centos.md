```command line
yum install -y docker
systemctl enable docker
cat << EOF >/etc/docker/daemon.json
{
 "insecure-registries": [
 "172.30.0.0/16"
 ]
}
EOF
systemctl start docker
```

```command line
yum -y install centos-release-openshift-origin311
yum -y install origin-clients
```

```command line
oc cluster up --routing-suffix=$VM_IP.xip.io --public-hostname=$(hostname) --base-dir=/var/lib/origin/openshift.local.clusterup
```

```command line
yum install -y dnf
dnf -y install dnf-plugins-core
dnf -y copr enable @ansible-service-broker/ansible-service-broker-latest
dnf -y install apb
```

```command line
apb registry add opendatahub --type quay --org opendatahub
```

```command line
apb bundle list
```

```command line
yum install -y ansible
```

Build a APB

```command line
ansible-galaxy init --type=apb oah-apb
apb bundle prepare
oc new-build --binary=true --name=oah-apb
oc start-build --follow --from-dir . oah-apb
oc get is
apb registry add oconc --type local_openshift --namespaces myproject
```

```command line
apb bundle provision oah-apb --follow
```


