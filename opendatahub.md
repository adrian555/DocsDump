# Deploy Open Data Hub services

[Link](https://gitlab.com/opendatahub/jupyterhub-ansible) to the Ansible installation.

Install `apb` cli on centos:

```command line
yum install -y dnf
dnf -y install dnf-plugins-core
dnf -y copr enable @ansible-service-broker/ansible-service-broker-latest
dnf -y install apb
```

Add registry:

```command line
apb registry add opendatahub --type quay --org opendatahub
apb bundle list
```

If going to install `dev` instead of `prod` plan, run following to grant the permission to `Ceph`:

```command line
oc --as system:admin adm policy add-scc-to-user anyuid system:serviceaccount:myproject:default
```

Install and provision jupyter-apb-bundle:

```command line
apb bundle provision jupyterhub-apb -s admin -f
```

Forward the `Ceph` port:

```comamnd line
oc port-forward ceph-nano-0 8000 &
```

Get the jupyter-hub url with following command:

```command line
oc status
```

(optional) Install awscli:

```command line
yum install -y epel-release
yum install -y python-pip
pip install awscli
```