# Install dind cluster

Refer to the [instruction](https://github.com/kubernetes-sigs/kubeadm-dind-cluster#using-preconfigured-scripts).

* Using preconfigured scripts

Prereq: install docker first. Refer to [minikue.md](./minikube.md) for docker installation on Ubuntu 18.04.

```command line
wget https://cdn.rawgit.com/kubernetes-sigs/kubeadm-dind-cluster/master/fixed/dind-cluster-v1.12.sh
chmod +x dind-cluster-v1.12.sh
```

To start the cluster:

```command line
./dind-cluster-v1.12.sh up
```

To stop the cluster:

```command line
./dind-cluster-v1.12.sh down
```

To remove the cluster:

```command line
./dind-cluster-v1.12.sh clean
```

Add these to .profile:

```command line
export PATH=".:$HOME/.kubeadm-dind-cluster:$PATH"
```

# Install FfDL

Refer to the [instruction](https://github.com/IBM/FfDL/blob/master/docs/detailed-installation-guide.md).

* Clone th repo

```command line
git clone https://github.com/IBM/FfDL.git
```

* Install helm

```command line
apt-get install snap
snap install helm --classic
```

* Init helm

```command line
cd $FFDL_PATH
helm init
# Make sure the tiller pod is Running before proceeding to the next step.
kubectl get pods --all-namespaces | grep tiller-deploy
```

* Export env

```command line
cd $FFDL_PATH
source env.txt
export $(cut -d= -f1 env.txt)
```

or add following to .profile

```text
export FFDL_PATH=/root/FfDL
export SHARED_VOLUME_STORAGE_CLASS=""
export VM_TYPE=dind
export PUBLIC_IP=localhost
export NAMESPACE=default
```

* Install Object Storage

```command line
cd $FFDL_PATH
./bin/s3_driver.sh
helm install storage-plugin --set dind=true,cloud=false,namespace=$NAMESPACE
```

* Create static volume

```command line
pushd bin
./create_static_volumes.sh
./create_static_volumes_config.sh
# Wait while kubectl get pvc shows static-volume-1 in state Pending
popd
```

* Install FfDL components

```command line
helm install . --set lcm.shared_volume_storage_class=$SHARED_VOLUME_STORAGE_CLASS,namespace=$NAMESPACE
```

Make sure all components are up and running

```command line
kubectl config set-context $(kubectl config current-context) --namespace=$NAMESPACE
kubectl get pods
helm status $(helm list | grep ffdl | awk '{print $1}' | head -n 1) | grep STATUS:
```

* Obtain and forward the ports

```command line
grafana_port=$(kubectl get service grafana -o jsonpath='{.spec.ports[0].nodePort}')
ui_port=$(kubectl get service ffdl-ui -o jsonpath='{.spec.ports[0].nodePort}')
restapi_port=$(kubectl get service ffdl-restapi -o jsonpath='{.spec.ports[0].nodePort}')
s3_port=$(kubectl get service s3 -o jsonpath='{.spec.ports[0].nodePort}')

./bin/dind-port-forward.sh
```

* Obtain endpoints

```command line
# Note: $(make --no-print-directory kubernetes-ip) simply gets the Public IP for your cluster.
node_ip=$PUBLIC_IP

# Echo statements to print out Grafana and Web UI URLs.
echo "Monitoring dashboard: http://$node_ip:$grafana_port/ (login: admin/admin)"
echo "Web UI: http://$node_ip:$ui_port/#/login?endpoint=$node_ip:$restapi_port&username=test-user"
```

# Kubernetes basic

```command line
kubectl version
kubectl cluster-info
kubectl get nodes
```

**Kubernetes Deployment**

```command line
# two examples
kubectl run hello-node --image=gcr.io/hello-minikube-zero-install/hello-node --port=8080
# kubectl run kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1 --port=8080
kubectl get deployments
kubectl get pods
kubectl get events
kubectl config view
```

Expose the pod to public internet using ``kubectl expose`` command.

```command line
kubectl expose deployment hello-node --type=LoadBalancer
kubectl get services
```

```command line
kubectl proxy
```

Get pod name

```command line
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
echo Name of the Pod: $POD_NAME
```

Access the service through API proxy
```command line
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/proxy/
```

Troubleshooting with kubectl

``kubectl get`` list resources<br>
``kubectl describe`` show detailed info about a resource<br>
``kubectl logs`` print the logs from a container in a pod<br>
``kubectl exec`` execute a command on a container in a pod

```command line
kubectl exec -ti $POD_NAME bash
```

**ReplicationController**<br>
**Service** contains a group of pods.

```command line
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
kubectl get services
```

``kubectl delete service`` to delete a service<br>

**Scaling deployments**<br>

```command line
kubectl scale deployments/kubernetes-bootcamp --replicas=4
```
