# Operator in Practice

**Opertaors** was introduced in 2016 by [CoreOS](https://coreos.com/blog/introducing-operators.html). An Operator implements the Kubernetes resouce and controller with application specific domain knowledge to automate the common tasks including creating, configuring and managing instances of complex applications.

## Operator Framework

### Operator SDK
build operators with Operator SDK

### Day 2 operation

### Helm vs Operator

### Kustomize vs Operator

## Operator Lifecycle Management

install, configure, manage, upgrade, patch

Operators are automated software managers for Kubernetes clusters: Install and Lifecycle

https://onlinexperiences.com/scripts/Server.nxp?LASCmd=AI:1;F:US!100&PreviousLoginCount=0&ForceProfileToBeFilledOut=0&DisplayItem=NULL&ShowKey=66367&ShowFrameFormatOverride=NULL&RandomValue=1566934766904

learn.openshift.com/operatorframework

scaling stateless applications --- easy on k8s (kubectl scale depl/staticweb --replicas=3)
what about apps that store data?
manage stateful apps ... extend k8s
kubectl create ns kubeflow
kubectl apply -f nfs-dynamic.yaml
kubectl patch storageclass ibmc-file-bronze -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
kubectl patch storageclass nfs-dynamic -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
kubectl create -f deploy/crds/openaihub_v1alpha1_kubeflow_crd.yaml
kubectl create -f deploy/service_account.yaml -n kubeflow
kubectl create -f deploy/role.yaml
kubectl create -f deploy/role_binding.yaml
kubectl create -f deploy/operator.yaml -n kubeflow
kubectl create -f deploy/crds/openaihub_v1alpha1_kubeflow_cr.yaml -n kubeflow

kubectl logs deployment/kubeflow6-operator -n kubeflow operator -f

kubectl delete -f deploy/crds/openaihub_v1alpha1_kubeflow_cr.yaml -n kubeflow
kubectl delete -f deploy/operator.yaml -n kubeflow
kubectl delete -f deploy/role.yaml
kubectl delete -f deploy/role_binding.yaml
kubectl delete -f deploy/service_account.yaml -n kubeflow

kubectl apply -f deploy/role.yaml

kubectl delete ns istio-system