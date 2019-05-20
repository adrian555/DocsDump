```command line
ibmcloud login -a https://cloud.ibm.com --sso
```

```command line
ibmcloud ks region-set us-south
```

```command line
ibmcloud ks cluster-config kfp-operations-test-16
```

```command line
export KUBECONFIG=/Users/$USER/.bluemix/plugins/container-service/clusters/kfp-operations-test-16/kube-config-dal10-kfp-operations-test-16.yml
```

```command line
ibmcloud ks cluster-config OpenShift-pipelines
```

```command line
export KUBECONFIG=/Users/$USER/.bluemix/plugins/container-service/clusters/OpenShift-pipelines/kube-config-sjc04-OpenShift-pipelines.yml
```