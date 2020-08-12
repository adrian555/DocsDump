Follow instructions on this [link](https://github.com/operator-framework/community-operators/blob/master/docs/testing-operators.md).

### Prereq:

* make sure you are in python3 env with pip

### Register the operator

```shell
# into your working directory
cd $WORKBENCH

mkdir test-kubeflow-operator
cd test-kubeflow-operator

# clone several operator-framework repos
git clone https://github.com/operator-framework/operator-marketplace.git
git clone https://github.com/operator-framework/operator-courier.git
git clone https://github.com/operator-framework/operator-lifecycle-manager.git

# copy over the kubeflow olm-catalog directory
# for openshift, you can download directly from https://github.com/adrian555/community-operators/tree/openshift/community-operators/kubeflow
# or
git clone https://github.com/adrian555/community-operators.git
git checkout openshift
cd community-operators/community-operators
cp -r kubeflow ../..
cd -

# install operator-courier
pip install operator-courier --upgrade

# retrieve your quay.io access token
./operator-courier/scripts/get-quay-token
export QUAY_TOKEN="basic yyyyy"

# verify operator package following the OLM standard
operator-courier verify --ui_validate_io kubeflow

# register the operator to OLM by pushing to quay.io
export OPERATOR_DIR=kubeflow
export QUAY_NAMESPACE=<quay_username>
export PACKAGE_NAME=kubeflow
export PACKAGE_VERSION=1.0.0
export TOKEN=$QUAY_TOKEN
operator-courier push "$OPERATOR_DIR" "$QUAY_NAMESPACE" "$PACKAGE_NAME" "$PACKAGE_VERSION" "$TOKEN"
```

You should be able to see the `kubeflow` in your quay.io account's `Applications` tab. If it is private, make it public.

### Create the OperatorSource

```shell
cat <<EOF > os.yaml
apiVersion: operators.coreos.com/v1
kind: OperatorSource
metadata:
  name: kubeflow-operators
  namespace: openshift-marketplace
spec:
  type: appregistry
  endpoint: https://quay.io/cnr
  registryNamespace: <quay_username>
  displayName: "Kubeflow Operators"
  publisher: "Kubeflow"
EOF
oc apply -f os.yaml
```

### Test the operator

From your OCP web console, you should be able to find it from the `Operators | OperatorHub` tab. Follow the [instruction](https://github.com/operator-framework/community-operators/blob/master/docs/testing-operators.md#testing-operator-deployment-on-openshift) to install and create a deployment.

You can also delete the deployment and the operator through the web console.

### Misc

If you have modified the operator code and rebuild the image, you should update the image in this [line](https://github.com/adrian555/community-operators/blob/openshift/community-operators/kubeflow/1.0.0/kubeflow.v1.0.0.clusterserviceversion.yaml#L562).
