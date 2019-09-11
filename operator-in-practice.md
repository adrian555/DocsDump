# Operator in Practice

## Why another article around Operator Framework

Since [Red Hat](https://www.redhat.com/en) announced [Operator Framework](https://coreos.com/blog/introducing-operator-framework) back in early 2018, there has been many articles and tutorials on what the framework is and how to benefit from it. However those articles usually cover one aspect of the 

**Opertaors** was introduced in 2016 by [CoreOS](https://coreos.com/blog/introducing-operators.html). Operators enable users to create, configure and manage, not just the stateless but also stateful, Kubernetes applications. An operator has its custom controller watching the custom resources specifically defined for the applications. Hence an operator mainly consists of Kubernetes CustomResourceDefinitions (CRDs) and Controller logic.

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