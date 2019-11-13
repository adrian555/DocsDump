
Challenge:

OpenShift Container Platform (OCP) is a leading hybrid cloud, enterprise container platform. On top of Kubernetes, OCP is focused on security that enterprise customers require. Alluxio enables data orchestration for analytics and machine learning in the cloud. Being able to simplify the deployment, monitoring and management of Alluxio cluster on OCP is critical for customers to adopt Alluxio on OCP, as well as to expand OCP in the hybrid cloud space.

Solution:

OpenShift offers Operator SDK toolset and Operator Lifecycle Manager service through Operator Framework open source project to help develop and manage Operators for cloud applications and services running on OCP. An Alluxio operator will be built and published to operatorhub.io for sharing among open source communities. 

Benefit:

With the Alluxio operator, cumstomers can easily deploy the Alluxio cluster in OCP and connect to various under stores. The operator also provides the customization and configuration capabilities to add/remove under stores, manage secrets and scale up/down Alluxio cluster, and more. Furthermore, when the operator is published to operatorhub.io, it becomes a built-in operator for OCP and can be installed with just a few clicks through OpenShift console.

Title:

Automate installation and manage lifecycle of Alluxio Cluster on OpenShift Container Platform with Operators

Abstract:

Alluxio provides data orchestration to bring data close to the compute nodes and so accelerate the analytics and machine learning. Especially more and more enterprises focus on the data privacy and security, running, monitoring and managing Alluxio clusters on OpenShift Container Platform could be proved a better option. 

An Alluxio operator is built with the tool and service offered by the Operator Framework open source project. The operator is focused on automating the installation of an Alluxio cluster, as well as provides configuration knobs to customize and scale the cluster. Through OpenShift console, customers will be able to monitor and manage the Alluxio cluster. The Alluxio operator is planned to be published to operatorhub.io for sharing among open source communities. 

Finally, a use case on machine learning with Spark and Alluxio running on clusters deployed with Alluxio operator will be demonstrated.
