# Set up OpenShift 4.1 cluster on fyre vm

* Install helm

```command line
curl -LO https://git.io/get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
oc create sa tiller -n kube-system
oc adm policy add-cluster-role-to-user cluster-admin -z tiller -n kube-system
helm init --service-account tiller --upgrade
```

* Install nfs-provisioner

```command line
helm install --name nfs --set nfs.server=10.16.11.179,nfs.path=/data,storageClass.defaultClass=true,storageClass.provisionerName=nfs-provisioner,storageClass.archiveOnDelete=false stable/nfs-client-provisioner
```

Note: replace the `nfs.server` to the `inf` node where the NFS daemon is running.

* Install the Kubeflow operator

```command line
git clone https://github.com/adrian555/operators.git
cd operators/kubeflow-operator
oc new-project kubeflow
oc create -f deploy/crds/operators_v1alpha1_kubeflow_crd.yaml
oc apply -f deploy/service_account.yaml
oc apply -f deploy/role.yaml
oc apply -f deploy/role_binding.yaml
oc apply -f deploy/operator.yaml
oc apply -f deploy/crds/operators_v1alpha1_kubeflow_cr.openshift.yaml
```

* Create a route for the `istio-system/ingressgateway` through OpenShift Web Console.

Log in through https://console-openshift-console.apps.ocdev.os.fyre.ibm.com. Once the route is created, connect to the Kubeflow dashboard http://kubeflow-istio-system.apps.ocdev.os.fyre.ibm.com.

* Update ClusterRole `argo` to add the `workflows/finalizers` resource.

* Issue: `crio` runtime instead of `docker` runtime.

Some possible solution discussed in this link https://github.com/kubeflow/pipelines/issues/1654.


