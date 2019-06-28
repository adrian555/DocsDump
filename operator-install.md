# Install custom operators through OLM

[OLM](https://github.com/operator-framework/operator-lifecycle-manager) will be the default operator package management tool. OLM is installed default from Openshift 4.0. On Kubernetes cluster, deploying OLM is also very easy with one command:

```command line
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/0.10.0/install.sh | bash -s 0.10.0
```

This installation create namespaces `olm` and `operators` and other resources

```text
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
deployment "olm-operator" successfully rolled out
deployment "catalog-operator" successfully rolled out
Package server phase: Waiting for CSV to appear
Package server phase: Pending
Package server phase: Installing
Package server phase: Succeeded
deployment "packageserver" successfully rolled out
```

In `olm` namespace, `olm-operators` service is looking for any operator from catalog sources and will install the operator. `olm-operator` is the operator for OLM itself. OLM installation also deploys the catalog source of all upstream community operators from [`operatorhub.io`](http://operatorhub.io). Run 

```commandline
kubectl get packagemanifests
```

to see all available operators. When an operator exists in the catalog source, one only needs to create a `subscription` and OLM will take care of deployment of the operator. For example, to install the `istio` operator, create following subscription

```yaml istio-operator.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: my-istio
  namespace: operators
spec:
  channel: beta
  name: istio
  source: operatorhubio-catalog
  sourceNamespace: olm
```

Run the command 

```command line
kubectl create -f istio-operator.yaml
```

to install the operator. The operator is running in the `operators` namespace

```text
NAME                              READY   STATUS    RESTARTS   AGE
istio-operator-85dd8b8c84-vqm4z   1/1     Running   0          5s
```

To further deploy the istio application, one will need to create the CustomResource for it.

Following this model, we can build our own registry server and catalog source for any operators we build or uploaded.

Here is the process:

1. Make sure each operator is supplied with these three files `<operator>.package.yaml`, `<operator>.clusterserviceversion.yaml` and `<operator>.crd.yaml`.

Below we will use `openaihub` as an example. In `openaihub` directory

```command line
cd openaihub
ls
##openaihub-operator.package.yaml
##openaihub-operator.v0.0.1.clusterserviceversion.yaml
##openaihub_v1alpha1_openaihub_crd.yaml
```

2. A catalog source can contain multiple operators, organize all these operators in to one directory `operators`

```command line
cd operators
ls
##openaihub
##pipelines
```

3. Create `Dockerfile` as follow to pack all these operators into a database for the registry server to look up

```Dockerfile
FROM python:3 as manifests

RUN pip3 install operator-courier==1.0.2
COPY operators operators
RUN for file in ./operators/*; do operator-courier nest $file /manifests/$(basename $file); done

FROM quay.io/operator-framework/upstream-registry-builder:v1.1.0 as builder
COPY --from=manifests /manifests manifests
RUN ./bin/initializer -o ./bundles.db

FROM scratch
COPY --from=builder /build/bundles.db /bundles.db
COPY --from=builder /build/bin/registry-server /registry-server
COPY --from=builder /bin/grpc_health_probe /bin/grpc_health_probe
EXPOSE 50051
ENTRYPOINT ["/registry-server"]
CMD ["--database", "bundles.db"]
```

4. Build and push the image

```command line
docker build . -t ffdlops/operators:v0.0.2
docker push ffdlops/operators:v0.0.2
```

5. Now create a `catalogsource` resource to use this image

```yaml openaihub.catalogsource.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: openaihub-catalog
  namespace: olm
spec:
  sourceType: grpc
  image: ffdlops/operators:v0.0.2
  displayName: OpenAIHub Operators
  publisher: IBM
```

6. Deploy the catalogsource

```command line
kubectl create -f openaihub.catalogsource.yaml
```

Once complete, we should see the `openaihub-catalog` pod and service is running. And from the `kubectl get packagemanifests` command, we should see all new operators included in the catalog.

7. Install the operators from the catalog

Same, create the subscription and deploy.

```yaml openaihub-operator.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: my-openaihub
  namespace: operators
spec:
  channel: alpha
  name: openaihub
  source: openaihub-catalog
  sourceNamespace: olm
```

```command line
kubectl create -f openaihub-operator.yaml
```

Once complete, we should see the `openaihub-operator` is running

```text
kubectl get pods -n operators
##NAME                                  READY   STATUS    RESTARTS   AGE
##istio-operator-85dd8b8c84-vqm4z       1/1     Running   0          22m
##openaihub-operator-85bb946d45-wwb5g   2/2     Running   0          21s
```

## automate the process to install a custom operator

The idea is to install a custom operator through a component that can be run through a pipeline. The following define the component to create the catalogsource for operators.

```yaml component.yaml
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

name: 'Create catalogsource for operators'
description: |
  Create catalogsource, registry server for custom operators
inputs:
  - {name: url,             description: 'Required. Github repo where the custom operators '}
outputs:
  - {name: name,     description: 'Name of the created catalogsource'}
implementation:
  container:
    image: docker.io/aipipeline/wml-config:latest
    command: ['python3']
    args: [
      /app/config.py,
      --token, {inputValue: token},
      --url, {inputValue: url},
      --name, {inputValue: name},
      --output-secret-name-file, {outputPath: secret_name},
    ]
```

## Interface with API backend

The above installation steps will be packed into a python script and built into a component. A pipeline (named `operator-install-pipeline`) will be created for OpenAIHub. Once an operator is to be installed through OpenAIHub API, the API backend will call the REST API `POST /apis/v1beta1/runs` to initiate a run with the pipeline to install the operator. The parameters for the `operator-install-pipeline` will have

| parameter | value |
|-----------|-------|
| repo | the repo where the operator is hosted, ie. `git@github.ibm.com:OpenAIHub/openaihub.git` |
| operator | name of the operator |
| parameters | the parameters for the operator, ie. `NAMESPACE:default,KUBECTL_VERSION:v1.13.1`|