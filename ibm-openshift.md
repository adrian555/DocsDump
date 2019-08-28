## kubeflow on openshift

Follow the [troubleshooting](https://www.kubeflow.org/docs/other-guides/troubleshooting/) for kubeflow.

```command line
export NAMESPACE=kubeflow
oc adm policy add-scc-to-user anyuid -z ambassador -n $NAMESPACE
oc adm policy add-scc-to-group anyuid system:authenticated -n $NAMESPACE
```

Then go to deploy the [`pipelines-operator`](https://github.ibm.com/OpenAIHub/operator-source/tree/master/pipelines-operator) and create the kubeflow pipeline service.

Once it is done, run following to add the `cluster-admin` to `pipeline-runner` serviceaccount.

```command line
oc create clusterrolebinding pipeline-runner-extend --clusterrole cluster-admin --serviceaccount $NAMESPACE:pipeline-runner
```

Now, edit or patch the `argo` clusterrole so that it has following:

```yaml
- apiGroups:
  - ""
  attributeRestrictions: null
  resources:
  - pods
  - pods/exec
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
- apiGroups:
  - ""
  attributeRestrictions: null
  resources:
  - configmaps
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - ""
  attributeRestrictions: null
  resources:
  - persistentvolumeclaims
  verbs:
  - create
  - delete
- apiGroups:
  - argoproj.io
  attributeRestrictions: null
  resources:
  - workflows
  - workflows/finalizers
  verbs:
  - get
  - list
  - patch
  - update
  - watch
```
