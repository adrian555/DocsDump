# Install **minikue** without hypervisor on Ubuntu 18.04

[minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) provides a [kubernetes](https://kubernetes.io/) cluster on a local or vm machine. Such cluster can help dev and test when they are not ready to deploy on a k8s cluster on cloud. Normally minikube requires a hypervisor to be installed, such as KVM2 or VirtualBox. But it also provides a no-driver mode which bases on the docker.

Following is how to set up such minikube cluster on Ubuntu 18.04.

1. install docker-ce

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

2. install kubectl

Follow the official instruction [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/)


```command line
# refresh Ubuntu packages
apt-get update

# add official GPG key
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# add repositories
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list

# refresh packages again
apt-get update

# install kubectl
apt-get install -y kubectl
```

3. install minikube

Follow the official instruction [here](https://github.com/kubernetes/minikube/releases).

```command line
# download minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.30.0/minikube-linux-amd64

# move to /usr/local/bin directory
chmod +x minikube
cp minikube /usr/local/bin/
rm minikube
```

Now minikube can be start as follow:

```command line
minikube start --vm-driver=none --cpus 4 --memory 8192 --disk-size=40g
```

The minikube cluster should now be up and running. To test, run following service:

```command line
kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.10 --port=8080
kubectl expose deployment hello-minikube --type=NodePort
kubectl get pod
curl $(minikube service hello-minikube --url)
```

To delete the service, run

```command line
kubectl delete services hello-minikube
kubectl delete deployment hello-minikube
```

To stop the minikube cluster, run

```command line
minikue stop
```

List addons

```command line
minikue addons list
```

To see the dashboard from remote, run following

```command line
kubectl proxy --address="0.0.0.0" --port=9090 --accept-hosts '.*'&
```

with [link](http://9.30.213.76:9090/api/v1/namespaces/kube-system/services/http:kubernetes-dashboard:/proxy/).

# Docker local registry

Run a local registry

```command line
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

Build a docker image with Dockerfile

```command line
docker build . -t minikube1.fyre.ibm.com:5000/ffdl:latest
```

Push the image to the registry

```command line
docker push minikube1.fyre.ibm.com:5000/ffdl
```

Run the image as kubectl pod

```command line
kubectl run --image=minikube1.fyre.ibm.com:5000/ffdl:latest ffdl
```

Delete a k8s deployment

```command line
kubectl delete deployment ffdl
```

