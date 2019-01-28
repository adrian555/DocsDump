# Install OpenShift Origin on RedHat 7.6 VM

[OKD link](https://github.com/openshift/origin)

Download client tool from this [link](https://github.com/openshift/origin/releases)

Note: on RedHat 7.6, `python` version is 2.7. So the `ansible` comes as version 2.4.2, which does not meet the requirement of `openshift-ansible`. 

Now trying to install [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#latest-release-via-dnf-or-yum)

Note, since [`openshift-ansible`](https://github.com/openshift/openshift-ansible) does not support `ansible` version 2.7+, so we have to manually install the lower version.

```command line
yum install https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.6.9-1.el7.ans.noarch.rpm
```

Need to update to 3.6. To do so, install the `epel-release` repository first.

```command line
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```

Install `python3.6`

```command line
yum install -y python36
```

Install `pip3`

```command line
curl https://bootstrap.pypa.io/get-pip.py | python3.6
```

Now install `ansible`

```command line
pip3 install ansible==2.6.9
```

Install `virtualenv`:

```command line
pip3 install virtualenv
```

Create virtual env for openshift:

```command line
virtualenv openshift
cd openshift/bin
source activate
```

Now we are in the `openshift` python36 environment. `ansible --version` should now show it is using python3.6.

Enable NetworkManager:

```
systemctl enable NetworkManager
systemctl start NetworkManager
systemctl show NetworkManager | grep ActiveState
```

Enable SELinux, [link](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-changing_selinux_modes): 

Edit `/etc/selinux/config` file, change to `SELINUX=permissive`. Then reboot the VM.
Check for denials. If no, edit `/etc/selinux/config` file again with `SELINUX=enforcing`. Reboot the VM.

Install `openshift-ansible` v3.11.0:

```command line
cd ~
git clone https://github.com/openshift/openshift-ansible
cd openshift-ansible
ansible-playbook -i inventory/hosts.localhost playbooks/prerequisites.yml
ansible-playbook -i inventory/hosts.localhost playbooks/deploy_cluster.yml
```

