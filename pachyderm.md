# Install pachyderm locally with minikube

Follow this [post](https://github.com/adrian555/DocsDump/raw/dev/minikube.md) to install minikube. Then go to pachyderm [documents](https://pachyderm.readthedocs.io/en/latest/getting_started/local_installation.html#pachctl) and install locally.

1. Install pachctl

```command line
curl -o /tmp/pachctl.tar.gz -L https://github.com/pachyderm/pachyderm/releases/download/v1.7.10/pachctl_1.7.10_linux_amd64.tar.gz && tar -xvf /tmp/pachctl.tar.gz -C /tmp && cp /tmp/pachctl_1.7.10_linux_amd64/pachctl /usr/local/bin
```

2. Deploy pachyderm

```command line
pachctl deploy local
```

Run ``kubectl get pods`` to see all the containers are running.

3. Port forwarding

```command line
pachctl port-forward &
```

If this command fails, just export the ip

```command line
export ADDRESS=`minikube ip`:30650
```

# Beginner tutorial

1. Create a repo

```command line
pachctl create-repo images
pachctl list-repo
```

2. Add data to repo

```command line
pachctl put-file images master liberty.png -f http://imgur.com/46Q8nDz.png
pachctl list-repo
pachctl list-commit images
pachctl list-file images master
```

Note: to display the image with ``pachctl get-file images master liberty.png | display``.

2. Create a pipeline

```command line
pachctl create-pipeline -f https://raw.githubusercontent.com/pachyderm/pachyderm/master/doc/examples/opencv/edges.json
```

To show the job, run ``pachctl list-job``.

Also, the following new container is running, shown by ``kubectl get pods``:

```text
pipeline-edges-v1-lx2ll           2/2     Running   0          1m
```

3. Process more data

Once the pipeline is created, it will automatically process new data coming to the repo.

```command line
pachctl put-file images master AT-AT.png -f http://imgur.com/8MN9Kg0.png
pachctl put-file images master kitten.png -f http://imgur.com/g2QnNqa.png
```

``pachctl list-job`` will show the new jobs kicked off from this pipeline.

4. Add another pipeline

```command line
pachctl create-pipeline -f https://raw.githubusercontent.com/pachyderm/pachyderm/master/doc/examples/opencv/montage.json
```

5. Explore DAG in pachyderm dashboard localhost:30080

# Pachyderm fundamentals

Pachyderm provides version control semantics for data. Data are stored in repositories through commits. Data can be stored in the object store. Data files are mounted to /pfs local to the container which runs the pipeline service.

Data analysis service is done through pipeline. First is to build a docker image with the code and dependencies and anything else. Second, create a pachyderm pipeline config file (json format) that references the docker image. In the json file, specify the operation and data input, output.

The analysis code should read and write local files in /pfs/\<repo\> directory.

DAG (multi-stage pipelines) then is formed with multiple related pipelines.

* Data sharding / parallelism

Automatically shard the input data across parallel containers. Number of workers for a pipeline is controlled by `parallelism_spec`. Use **Glob Patterns** to define data distribution. **Datums** are unit of parallelism in Pachyderm. The input `atom` repo is a file system. The `glob pattern` applies to the root of the file system. The files and directories matching the glob pattern are `datums`.

Pachyderm will never reprocess data in a datum that is has been run with the same analysis code. But if any part of a datum changes, the entire datum will be reprocessed.

* Build a docker image

Refer to [Containers](https://docs.docker.com/get-started/part2/) to build a docker image.

* Incremental processing

Two kinds of incremental processing: **Inter-Datum Incrementality** and **Intra-Datum Incrementality**.

* Autoscale pachyderm cluster

