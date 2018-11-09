# Install **minikue** without hypervisor on Ubuntu 18.04

[minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) provides a [kubernetes](https://kubernetes.io/) cluster on a local or vm machine. Such cluster can help dev and test when they are not ready to deploy on a k8s cluster on cloud. Normally minikube requires a hypervisor to be installed, such as KVM2 or VirtualBox. But it also provides a no-driver mode which bases on the docker.

Following is how to set up such minikube cluster on Ubuntu 18.04.

1. install docker-ce
