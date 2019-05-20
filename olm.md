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