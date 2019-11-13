## Preparation

* Spark k8s build and install
* Spark executors running applications
* Alluxio caching mechanism
* install Alluxio in k8s

## Goals

* A distributed file system host mounted as a persistent volume (or storage class) to be accessed by Spark executor pod/container
* First step is to support S3 file caching locally with partitions based on the node the file system is mounted to
* The Spark executor pod/container can automatically be selected to run on the node that has the file cached locally
* A catalog
* A configuration to enable the cache mounting
* A specific file descriptor if desired (such as `sparkfs://`)

## Phases

1. read Spark and Alluxio docs regarding k8s
2. set up Spark and Alluxio environment
3. manually select the executor container to run on a specific node where the Alluxio client is running
4. enable caching
5. 