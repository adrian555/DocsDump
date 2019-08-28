# Operator Lifecycle Management

## generate new operator

```command line
operator-sdk new openaihub-operator --api-version=openaihub.ibm.com/v1alpha1 --kind=OpenAIHub --type=ansible --cluster-scoped
```

## generate csv

```command line
operator-sdk olm-catalog gen-csv --csv-version 0.0.1 --update-crds
```

```command line
kubectl delete -f deploy/crds/openaihub_v1alpha1_ffdl_cr.yaml
kubectl delete -f deploy/operator.yaml
kubectl delete -f deploy/role_binding.yaml
kubectl delete -f deploy/role.yaml
kubectl delete -f deploy/service_account.yaml

kubectl create -f deploy/service_account.yaml
kubectl create -f deploy/role.yaml
kubectl create -f deploy/role_binding.yaml
kubectl create -f deploy/operator.yaml
kubectl create -f deploy/crds/openaihub_v1alpha1_ffdl_cr.yaml

kubectl logs deployment/ffdl-operator -f

operator-sdk build ffdlops/ffdl:v0.0.1
docker push ffdlops/ffdl:v0.0.1

kubectl create -f deploy/crds/openaihub_v1alpha1_ffdl_crd.yaml
```

## remove finalizer if the namespace or the crd can't be removed

```command line
kubectl patch crd ffdls.ffdl.ibm.com -p '{"metadata":{"finalizers": null}}'
```

```command line
export NAMESPACE=your-rogue-namespace
kubectl delete ns $NAMESPACE --force --grace-period=0
kubectl proxy &
kubectl get namespace $NAMESPACE -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
```

## helm install/uninstall

```command line
helmins() {
 kubectl -n kube-system create serviceaccount tiller
 kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
 helm init --service-account=tiller
}
helmdel() {
 kubectl -n kube-system delete deployment tiller-deploy
 kubectl delete clusterrolebinding tiller
 kubectl -n kube-system delete serviceaccount tiller
 
}
```

## install OLM

```command line
git clone https://github.com/operator-framework/operator-lifecycle-manager.git
cd operator-lifecycle-manager
kubectl create -f deploy/upstream/manifests/latest/
```

## OLM

```command line
# operator group file
cat <<EOF >operator_group.yaml
apiVersion: operators.coreos.com/v1alpha2
kind: OperatorGroup
metadata:
  annotations:
    olm.providedAPIs: openaihub.ibm.com
  name: openaihub-og
  namespace: local
spec:
  targetNamespaces:
  - local
EOF

# catalog source file
cat <<EOF >catalog_source.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  labels:
    name: openaihub
    namespace: local
  name: openaihub
spec:
  displayName: Custom Operators
  publisher: Custom
  sourceType: internal
EOF

# subscription file
cat <<EOF >subscription.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: ffdl-sub
  namespace: local
spec:
  name: ffdl
  source: ffdl-ocs
  sourceNamespace: local
  startingCSV: ffdl-operator.v0.0.1
  channel: alpha
  installPlanApproval: Automatic
EOF
```

```command line
kubectl api-resources --verbs=list -o name | xargs -n 1 kubectl get -o name
```

========================

install operator from operatorhub.io

```command line
# install OLM
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/0.10.0/install.sh | bash -s 0.10.0


====================

To create the operator in a specific namespace

1. create the catalog source in that namespace

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: openaihub-catalog
  namespace: kubeflow
spec:
  sourceType: grpc
  image: ffdlops/operators:v0.0.1
  imagePullPolicy: Always
  displayName: OpenAIHub Operators
  publisher: IBM
```

2. create an opreatorgroup in that namespace

```command line
cat << EOF | kubectl create -f -
apiVersion: operators.coreos.com/v1alpha2
kind: OperatorGroup
metadata:
  name: global-operators
EOF

3. create the subscription and point the sourceNamespace to that namespace

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: my-pachyderm
  namespace: kubeflow
spec:
  channel: alpha
  name: pachyderm
  source: openaihub-catalog
  sourceNamespace: kubeflow
```

4. create customresource with `-n` to that namespace

docker run -ti --rm -v `pwd`:/workspace -v $(PWD)/config.json:/root/.docker/config.json:ro gcr.io/kaniko-project/executor:latest --dockerfile=Dockerfile --destination=ffdlops/test-kaniko:v0.0.1

docker run -ti --entrypoint=/busybox/sh --rm -v `pwd`:/workspace -v $(PWD)/config.json:/kaniko/.docker/config.json:ro gcr.io/kaniko-project/executor:debug --dockerfile=Dockerfile --destination=docker.io/ffdlops/test 

docker run -v `pwd`:/workspace -v $(PWD)/config.json:/kaniko/config.json  --env DOCKER_CONFIG=/kaniko gcr.io/kaniko-project/executor:latest --dockerfile=Dockerfile --destination=docker.io/ffdlops/test

kubectl create configmap docker-config --from-file=config.json
kubectl create configmap build-context --from-file=Dockerfile
kubectl create -f kaniko.yaml
kubectl cp kaniko.tgz kaniko:/tmp/context.tar.gz -c kaniko-init
kubectl exec kaniko -c kaniko-init -- tar -zxf /tmp/context.tar.gz -C /kaniko/build-context
kubectl exec kaniko -c kaniko-init -- touch /tmp/complete

pip install openaihub
apk add git
apk add curl
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.13.7/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin

```text
(base) weiqiangs-mbp:temp wzhuang$ bash install.sh 0.10.0
customresourcedefinition.apiextensions.k8s.io/clusterserviceversions.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/installplans.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/subscriptions.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/catalogsources.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/operatorgroups.operators.coreos.com created
namespace/olm created
namespace/operators created
clusterrole.rbac.authorization.k8s.io/system:controller:operator-lifecycle-manager created
serviceaccount/olm-operator-serviceaccount created
clusterrolebinding.rbac.authorization.k8s.io/olm-operator-binding-olm created
deployment.apps/olm-operator created
deployment.apps/catalog-operator created
clusterrole.rbac.authorization.k8s.io/aggregate-olm-edit created
clusterrole.rbac.authorization.k8s.io/aggregate-olm-view created
configmap/olm-operators created
catalogsource.operators.coreos.com/olm-operators created
operatorgroup.operators.coreos.com/global-operators created
operatorgroup.operators.coreos.com/olm-operators created
subscription.operators.coreos.com/packageserver created
catalogsource.operators.coreos.com/operatorhubio-catalog created
Waiting for deployment "olm-operator" rollout to finish: 0 of 1 updated replicas are available...
deployment "olm-operator" successfully rolled out
Waiting for deployment "catalog-operator" rollout to finish: 0 of 1 updated replicas are available...
deployment "catalog-operator" successfully rolled out
Package server phase: Waiting for CSV to appear
Package server phase: Pending
Package server phase: InstallReady
Package server phase: Installing
Package server phase: Succeeded
deployment "packageserver" successfully rolled out
```