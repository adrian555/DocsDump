# Deploy FfDL on minishift (centos7)

* Install 

https://blog.openshift.com/automation-broker-discovering-helm-charts/

Install k8s service catalog: https://kubernetes.io/docs/tasks/service-catalog/install-service-catalog-using-helm/

Install helm

```command line
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
```

Install kubectl

```command line
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
yum install -y kubectl
```

Login in to docker.io

```command line
docker login -u adrian555
```

Install s3fs

```command line
yum install -y epel-release
yum install -y s3fs-fuse
ln -s /usr/bin/s3fs /usr/local/bin/s3fs
```

Install git

```command line
yum install -y git
```

Clone FfDL

```command line
git clone https://github.com/IBM/FfDL.git
```

Tiller service account

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: tiller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: tiller
    namespace: kube-system
```

Add the tiller service account:

```command line
oc apply -f sa.yaml
helm init --service-account tiller --upgrade
```

To allow ALL service accounts to act as cluster admin:

```command line
kubectl create clusterrolebinding permissive-binding \
  --clusterrole=cluster-admin \
  --user=admin \
  --user=kubelet \
  --group=system:serviceaccounts
```

```command line
# Gives the default service account in the current project access to run as UID 0 (root)
oc adm policy add-scc-to-user anyuid -z default
```

```command line
# allows images to run as the root UID if no USER is specified in the Dockerfile.
oc adm policy add-scc-to-group anyuid system:authenticated
```

```command line
oc adm policy add-scc-to-user anyuid system:serviceaccount:myproject:mysvcacct
```

```command line
oc adm policy add-scc-to-group privileged system:serviceaccounts:myproject
```

Install FfDL

```command line
cd FfDL

# switch to helm-patch branch
git checkout helm-patch

# object storage plugin
helm install docs/helm-charts/ibmcloud-object-storage-plugin-0.1.tgz --name ibmcloud-object-storage-plugin --set namespace=$NAMESPACE,cloud=false

# ffdl helper
helm install docs/helm-charts/ffdl-helper-0.1.1.tgz --name ffdl-helper --set namespace=$NAMESPACE,shared_volume_storage_class=$SHARED_VOLUME_STORAGE_CLASS,localstorage=true,prometheus.deploy=false --wait

# ffdl core
helm install docs/helm-charts/ffdl-core-0.1.1.tgz --name ffdl-core --set namespace=$NAMESPACE,lcm.shared_volume_storage_class=$SHARED_VOLUME_STORAGE_CLASS --wait
```

Other `helm` commands: `helm list` and `helm del -purge`.

Install k8s service catalog

```command line
helm repo add svc-cat https://svc-catalog-charts.storage.googleapis.com
helm search service-catalog
kubectl create clusterrolebinding tiller-cluster-admin \
    --clusterrole=cluster-admin \
    --serviceaccount=kube-system:tiller
helm install svc-cat/catalog --name catalog --namespace catalog
```

Deploy `Automation Broker`:

```command line
cat <<EOF | kubectl create -f -
---
apiVersion: v1
kind: Namespace
metadata:
  name: automation-broker-apb

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: automation-broker-apb
  namespace: automation-broker-apb

---
# Since the Broker APB will create CRDs and other privileged
# k8s objects, we need elevated permissions
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: automation-broker-apb
roleRef:
  name: cluster-admin
  kind: ClusterRole
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: automation-broker-apb
  namespace: automation-broker-apb

---
apiVersion: v1
kind: Pod
metadata:
  name: automation-broker-apb
  namespace: automation-broker-apb
spec:
  serviceAccount: automation-broker-apb
  containers:
    - name: apb
      image: docker.io/automationbroker/automation-broker-apb:latest
      args:
        - "provision"
        - "-e create_broker_namespace=true"
        - "-e broker_sandbox_role=admin"
        - "-e broker_dockerhub_tag=canary"
        - "-e broker_helm_enabled=true"
        - "-e broker_helm_url=https://kubernetes-charts.storage.googleapis.com"
        - "-e wait_for_broker=true"
      imagePullPolicy: IfNotPresent
  restartPolicy: Never
EOF
```

To allow ALL service accounts to act as cluster admin:

```command line
kubectl create clusterrolebinding permissive-binding \
  --clusterrole=cluster-admin \
  --user=admin \
  --user=kubelet \
  --group=system:serviceaccounts
```

Kubeflow pipeline on minishift:

```command line
oc adm policy add-scc-to-user anyuid -z ambassador
oc adm policy add-scc-to-user anyuid -z jupyter-hub
```
