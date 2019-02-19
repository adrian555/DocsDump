# Access to IBM Cloud

* Download and install CLI tools

```command line
curl -sL https://ibm.biz/idt-installer | bash
```

* Login

```command line
ibmcloud login -a https://api.ng.bluemix.net --sso
```

* Set target

```command line
ibmcloud cs region-set us-south
```

* Configure the environment to use k8s configuration files

```command line
ibmcloud cs cluster-config KFP-WML
```

* Set KUBECONFIG env

```comamnd line
export KUBECONFIG=/Users/$USER/.bluemix/plugins/container-service/clusters/KFP-WML/kube-config-sjc03-KFP-WML.yml
```

Create a service

```command line
# create a Watson Machine Learning service
ibmcloud cf create-service pm-20 lite wml-my-service

# create a Cloud Object Storage
ibmcloud cf create-service cloud-object-storage Lite cos-my-service
```

List all services available

```command line
ibmcloud cf m
```

Create service credential for a service

```command line
# list current service keys
ibmcloud cf service-keys wml-my-service

# create a service key
ibmcloud cf create-service-key wml-my-service wml-my-service-key

# create a service key with HMAC
ibmcloud cf create-service-key cos-my-service cos-my-service-key -c '{"HMAC":true}'

# get service credential
ibmcloud cf service-key wml-my-service wml-my-service-key
```

To retrive the service credential for Watson Machine Learning service

```command line
ibmcloud cf service-key wml-my-service wml-my-service-key | sed '1,4d' | jq
```

To retrieve the service credential for Cloud Object Storage

```command line
ibmcloud cf service-key cos-my-service cos-my-service-key | sed '1,4d' | jq '{"keys":.cos_hmac_keys,"endpoints":.endpoints}'
```

Retrieve one endpoint for the Cloud Object Storage

```command line
