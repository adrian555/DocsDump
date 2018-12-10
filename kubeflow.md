# Install kubeflow on minikube

Start minikube:

```command line
minikube start --vm-driver=none --cpus 4 --memory 8192
```

```command line
export KUBEFLOW_SRC=/root/kubeflow
cd $KUBEFLOW_SRC
export KUBEFLOW_TAG=v0.3.1
curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash

export KFAPP=$KUBEFLOW_SRC/kfapp
KUBEFLOW_REPO=${KUBEFLOW_SRC} ${KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform minikube
cd ${KFAPP}
${KUBEFLOW_SRC}/scripts/kfctl.sh generate all
${KUBEFLOW_SRC}/scripts/kfctl.sh apply all
