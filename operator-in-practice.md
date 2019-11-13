# Operator Framework in Practice

Since [Red Hat](https://www.redhat.com/en) announced [Operator Framework](https://coreos.com/blog/introducing-operator-framework) back in early 2018, there has been many articles and tutorials on what the framework is and how to benefit from it. However, we have not seen any article covers the complete cycle from writing to installing operators. This could be partly because the open source project itself evolves very fast. The documentation on the open source project's [`github`](https://github.com/operator-framework) site sometime was out of date. Even the official documentation for [OpenShift Container Platform](https://docs.openshift.com/container-platform/4.2/welcome/index.html) has some outdated contents.

This tutorial, however, aims to provide hands-on exercise with step-by-step instruction and demonstrate how to create, register, install an operator and finally deploy the application managed by the operator. Basic concepts, tools and services offered by the Operator Framework will be briefly explained followed by a workable example.

## Basic concepts

### Opertaor

**Operator** was introduced in 2016 by [CoreOS](https://coreos.com/blog/introducing-operators.html). Operators are a method of packaging, deploying, and managing a Kubernetes application. An operator has its custom controller watching the custom resources specifically defined for the applications. Hence an operator mainly consists of Kubernetes CustomResourceDefinitions (CRDs) and Controller logic. Operator extends the K8S API with CRDs. When you create a new CRD, the K8S API Server creates a new set of RESTful endpoints, eg. `/apis/os.ibm.com/v1alpha1/namespaces/default/SparkCluster`, to manage the custom resource. Operator itself is a Kubernetes application as well. So to run an operator on the OpenShift cluster is to create a Kubernetes deployment to deploy an operator pod which may run one of more containers with pre-built images.

With operators, it is easy to manage complex stateful applications. Database application is one example of stateful applications. It is also good for day 2 operations, such as patch, update, upgrade and scale, when the application is managed by an operator. 

But creating an operator is not easy until the open source project [Operator Framework](https://github.com/operator-framework) was introduced.

### Operator Framework

**Operator Framework** offers open source toolkit to build, test, package Operators and manage lifecycle of Operators. Tools are:

* [operator-sdk](https://github.com/operator-framework/operator-sdk) — write, test and package operators
* [operator-courier](https://github.com/operator-framework/operator-courier) — build, verify and push operator manifests (CRDs and CSVs)
* [operator-registry](https://github.com/operator-framework/operator-registry) — store the manifest data in database and provide operator catalog data to Operator Lifecycle Manager
* [operator-lifecycle-manager](https://github.com/operator-framework/operator-lifecycle-manager) — install, upgrade and RBAC control operators (aka. operator of operators)
* [operator-metering](https://github.com/operator-framework/operator-lifecycle-manager) — collect operational metrics of operators for day 2 management
* [operator-marketplace](https://github.com/operator-framework/operator-marketplace) — an operator to register off-cluster operators
* [community-operators](https://github.com/operator-framework/community-operators) — host community created operators and publish to operatorhub.io

This tutorial covers the two main components `Operator SDK` and `Operator Lifecycle Manager`, which are essential for creating and managing operators. **Operator SDK** provides SDK for building operators, while **Operator Lifecycle Manager (OLM)** provides service to discover, install and manage operators.

An operator watches on the custom resources through CustomResourceDefinitions (CRDs). The OLM runs a version of operator with a ClusterServiceVersion (CSV), which contains all resources, including CRDs and RBAC rules to run the operator.

## Create SparkCluster operator with Operator SDK

This tutorial will build an operator to create a standalone [Spark](https://spark.apache.org/) cluster running on an OpenShift cluster. A Spark standalone cluster consists of one or more master and worker nodes. Each node runs Spark binary in a daemon process. The master node provides `SPARK_MASTER` URL for Spark drivers to submit applications to run on. The worker node receives jobs from the master and spawn exectuors to run tasks.

The application managed by the operator is to create such a Spark cluster.
 
To try out this tutorial, you should have the `git` installed and have access to this tutorial's [`github repo`](https://github.com/adrian555/ofip). First, run following command to clone this repo:

```command line
git clone https://github.com/adrian555/ofip.git
```

Now, follow steps below to build and install the Spark operator.

1. Build Spark docker image

Since we are running on an OpenShift Kubernetes cluster, the first thing is to prepare the container image for Spark master and worker nodes. We use Spark's `docker-image-tool` to build and push the docker image, with some tweaks to install `pyspark` and make the image for both master and worker node.

```command line
# download the original Spark binary
wget http://ftp.wayne.edu/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar zxvf spark-2.4.4-bin-hadoop2.7.tgz

# modify Dockerfile
cd spark-2.4.4-bin-hadoop2.7
cp ../patch/run.sh sbin
cp ../patch/Dockerfile kubernetes/dockerfiles/spark

# build and push the docker image
# NOTE: replace the repository with the one you owned
./bin/docker-image-tool.sh -r docker.io/dsml4real -t v2.4.4 build
./bin/docker-image-tool.sh -r docker.io/dsml4real -t v2.4.4 push
cd ..
```

2. Create Spark operator with Operator SDK

`Operator SDK` can help build one of `Go`, `Helm` and `Ansible` types of operators. The difference among these three types of operators is the maturity of an operator's encapsulated operations as shown following:

![Operator maturity model](https://github.com/adrian555/DocsDump/raw/dev/images/OperatorMaturityModel.png)
*Operator maturity model* from [OpenShift Container Platform document](https://docs.openshift.com/container-platform/4.2/operators/olm-what-operators-are.html)

This tutorial chooses `Ansible` as the mechanism to write the controller logic for the Spark operator.

`Operator SDK` can be installed through `brew` on macOS or downloaded as binary from this [link](https://github.com/operator-framework/operator-sdk/blob/master/doc/user/install-operator-sdk.md).

Once the SDK is installed, run following command to create the operator:

```command line
mkdir temp
operator-sdk new spark-operator --api-version=ibm.com/v1alpha1 --kind=Spark --type=ansible
cd ..
```

This creates the scaffolding code for the operator under the `spark-operator` directory, including the manifests of CRDs, example custom resource, RBAC role and rolebinding, and the Ansible playbook role and tasks, as well as the Dockerfile to build the image for the operator. The directory structure and contents are similar to the [one](https://github.com/adrian555/ofip/tree/master/scratch/spark-operator) included in the repo.

Once an Ansible type of operator is installed on the OpenShift cluster, a pod is created and runs with two containers: `ansible` and `operator`. The `ansible-runner` process executes the `role` or playbook provided in the [`spark-operator/roles/spark`](https://github.com/adrian555/ofip/tree/master/scratch/spark-operator/roles/spark) directory. Refer to this [link](https://github.com/operator-framework/operator-sdk/blob/master/doc/ansible/information-flow-ansible-operator.md) for more details.

3. Add Ansible tasks to install a Spark cluster

The application managed by this operator is to install a Spark cluster. This can be done through Ansible playbook tasks. This tutorial already implements the code in the [`spark-operator/roles/spark`](https://github.com/adrian555/ofip/tree/master/spark-operator/roles/spark) directory.

The main tasks are in the [`tasks/main.yml`](https://github.com/adrian555/ofip/blob/master/spark-operator/roles/spark/tasks/main.yml) file. It creates a `spark-master` Kubernetes Deployment to run Spark master pod, a `spark-worker` Kubernetes Deployment to run one or more Spark worker pods and a `spark-cluster` Kubernetes Service to access the Spark driver requests to the Spark master. It can also create a `spark-worker-pvc` Kubernetes PersistentVolumeClaim used in the Spark worker pods if the access to a distributed NFS server is provided. The number of pods created by the `spark-worker` deployment can be specified by the `worker-size`, which is a parameter passed in through the CustomResource when creating a Spark cluster from the Spark operator.

It is worth mentioning that these tasks are the same one when you use to install a Spark cluster without an operator. All we do here is to rewrite them with [Ansible](https://docs.ansible.com/ansible/latest/index.html) automation tool.

4. Update RBAC roles

The Operator SDK command creates a `spark-operator` service account with certain [role](https://github.com/adrian555/ofip/blob/master/spark-operator/deploy/role.yaml) and [role binding](https://github.com/adrian555/ofip/blob/master/spark-operator/deploy/role_binding.yaml). The application is installed and managed by this service account. And the role defines the RBAC restriction for the service account. Users should carefully choose what roles to be granted for this service account for security reasons. Also, if an operator is watching resources from other namespaces accross the OpenShift cluster, you may need to choose appropriate cluster roles instead. This tutorial just binds the `cluster-admin` role to the `spark-operator` service account for simplification purpose.

5. Create Spark manifest

An operator creates and watches custom resource definitions. These CRDs are saved in the [`spark-operator/deploy/crds`](https://github.com/adrian555/ofip/tree/master/spark-operator/deploy/crds) directory. To create an instance of the CRD, you will need to create a manifest file. You can specify parameters for the custom resource as well.

The Spark operator in this tutorial creates the `Spark` custom resource. One example of the manifest to create an application of the `Spark` custom resource is this [file](https://github.com/adrian555/ofip/blob/master/spark-operator/deploy/crds/ibm_v1alpha1_spark_pv_cr.yaml).

6. Build docker image for operator and update operator deployment to use the image

The Operator SDK command already generates a [`Dockerfile`](https://github.com/adrian555/ofip/blob/master/spark-operator/build/Dockerfile) for the operator image. Run following command to build the docker image:

```command line
cd spark-operator

# build the docker image
operator-sdk build dsml4real/spark-operator:v0.0.1

# push the docker image
docker push dsml4real/spark-operator:v0.0.1
cd ..
```

As mentioned earlier, operator code is run through a deployment defined in the [`spark-operator/deploy/operator.yaml`](https://github.com/adrian555/ofip/blob/master/spark-operator/deploy/operator.yaml). Update that file and make sure that the image for both `ansible` and `operator` containers will run with the image built above.

So far, we have prepared the artifacts for the application - standalone Spark cluster, created Ansible type of operator `spark-operator` with Operator SDK tool, added the CRDs and controller logic to deploy a Spark cluster, and built the docker image for the operator. These are the common steps for writing an operator. Now the Spark operator is ready. We can either test the operator locally or install it on the cluster.

7. Install Spark operator

There are two approaches to install an operator. One is to run some OpenShift client `oc` commands to create service account, role binding and then the operator itself. The other one is to package the resources into a cluster service version (CSV) and then let Operator Lifecycle Manager (OLM) install.

* install manually

Here are the commands to install the Spark operator:

```command line
cd spark-operator

# create a new project (optional)
oc new-project tutorial

# create CRDs
oc apply -f deploy/crds/ibm_v1alpha1_spark_crd.yaml

# create service account
oc apply -f deploy/service_account.yaml

# create role and role binding
oc apply -f deploy/role.yaml
oc apply -f deploy/role_binding.yaml

# create the operator deployment
oc apply -f deploy/operator.yaml

cd ..
```

A pod such as following should be created now

```command line
oc get pods -n tutorial
### NAME                              READY   STATUS    RESTARTS   AGE
### spark-operator-7477ff4c94-lgb6z   2/2     Running   0          40s
```

To check the progress, run following to view the logs from the `operator` container of the `spark-operator` pod.

```command line
kubectl logs deployment/spark-operator operator -n tutorial -f
```

* install through OLM

Before an operator can be installed through OLM, two things must happen. First a CSV manifest must be generated to include the metadata, CRDs and install strategy for the operator. Secondly it has to register itself to a catalog for the OLM to discover.

![OLM and catalog source](https://github.com/adrian555/DocsDump/raw/dev/images/catalogsource.jpg)
*Add operators to registry and use in catalog source*

The Operator SDK tool also helps generate the CSV. Run following command:

```command line
cd spark-operator
operator-sdk olm-catalog gen-csv --csv-version 0.0.1 --update-crds
cd ..
```

The CSV maniefest is generated in the [`spark-operator/deploy/olm-catalog`](https://github.com/adrian555/ofip/tree/master/spark-operator/deploy/olm-catalog/spark-operator) directory. The directory contains different versions of CSVs and dependent CRDs, together with a package manifest describing the channels for different install path for application (such as alpha vs stable). It is used in the Subscription manifest when create or upgrade the CustomResource (ie. application).

Operator scope
namespace scoped: watches and manages resources in a single namespace
cluster scoped: watches and manages cluster-wide



Once a CatalogSource resource is created in its namespace (the sourceNamespace later used to install the operators), a service will be running on a defined port so that OLM can discover all operators included in this catalog.

Each operator watches and manages these resources respectively.

OperatorGroup provides multitenant configuration to Operators registered through CatalogSource. An OperatorGroup selects a set of target namespaces (olm.targetNamespaces in CSV) in which to generate required RBAC access for its member Operators. If an operator’s  CSV is in the same namespace as the OperatorGroup, and its InstallMode support the same of namespaces targeted by the OperatorGroup, then this operator is a member of this OG and may be installed by this OG. We can see one example of CSV during the demo.

Two operators
OLM operator — operator of operators
ClusterServiceVersion, ClusterResourceDefinition, OperatorGroup
Deployments, (Cluster)Role, (Cluster)RoleBinding, ServiceAccount
Catalog operator — discover and install CSVs and CRDs
InstallPlan, CatalogSource, Subscription
Metrics
csv_count, install_plan_count, subscription_count, csv_upgrade_count

Each operator watches and manages these resources respectively.

OperatorGroup provides multitenant configuration to Operators registered through CatalogSource. An OperatorGroup selects a set of target namespaces (olm.targetNamespaces in CSV) in which to generate required RBAC access for its member Operators. If an operator’s  CSV is in the same namespace as the OperatorGroup, and its InstallMode support the same of namespaces targeted by the OperatorGroup, then this operator is a member of this OG and may be installed by this OG. We can see one example of CSV during the demo.


learn.openshift.com/operatorframework

Two main components are `operator sdk` and `operator lifecycle manager`.

1. Two approaches to install the operator and deploy application.
- Install manually
  - create serviceaccount
  - create role and rolebinding
  - create the operator deployment
  - deploy the application with customresource
- Install through OLM
  - generate clusterserviceversion
  - update csv and verify with operator-courier
  - build image for operator-registry
  - create catalogsource using the registry image
    - if the sourcenamespace has an operatorgroup watching the targetnamespaces, then the operator can be installed to the targetnamespace
    - otherwise, need to create an operatorgroup
  - create the operator deployment with a subscription
  - deploy the application by creating an instance of the provided API