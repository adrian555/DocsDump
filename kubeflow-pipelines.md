# Kubeflow pipelines

* UI for managing and tracking `experiments`, `jobs` and `runs`.
* Engine for scheduling multi-step ML workflows.
* SDK for defining and manipulating `pipelines` and `components`.
* Notebooks for interacting with the system using the SDK.

## Deploy kubeflow pipelines

* Install minikube
* Install socat

```command line
apt-get install socat
```

* Deploy kubeflow pipelines
[0.1.6 link](https://github.com/kubeflow/pipelines/releases)

```command line
PIPELINE_VERSION=0.1.6
wget https://storage.googleapis.com/ml-pipeline/release/$PIPELINE_VERSION/bootstrapper.yaml
```

Edit the bootstrapper.yaml file as such

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: deploy-ml-pipeline-
spec:
  backoffLimit: 1
  template:
    metadata:
      name: deploy-ml-pipeline
    spec:
      containers:
      - name: deploy
        env:
        - name: GITHUB_TOKEN
          value: 703fcd79bfab9ae1f8c29e7fd5135fd92d1224c3
```

above add the GITHUB_TOKEN to the depoly-ml-pipeline container.

Once it is done, run `kubectl create -f bootstrapper.yaml` to deploy the pipeline service.

* kubectl port forward:

```command line
export NAMESPACE=kubeflow
kubectl port-forward -n ${NAMESPACE} $(kubectl get pods -n ${NAMESPACE} --selector=service=ambassador -o jsonpath='{.items[0].metadata.name}') 8080:80 --address 0.0.0.0&
```

* Troubleshooting:

[rate limit 403](https://www.kubeflow.org/docs/guides/troubleshooting/)

Provide Jupyter Notebook support.

* Pipeline

A description of a machine learning (ML) workflow, including all of its different components, and how they come together in the form of a graph, as well as a list of the parameters. This is the main shareable artifact in the Kubeflow Pipelines service. You create and edit a pipeline separately from the pipelines UI, although you can upload and list pipelines on the UI.

* Pipeline component

A building block in the pipeline template; self-contained user code that performs one step in the pipeline, such as preprocessing, transformation, training, etc. A component must be packaged as a Docker image. See the guide to building your own components.

* Experiment

A workspace where you can try different configurations of your pipelines. You can use experiments to organize your runs to logical groups. Experiments can contain arbitrary runs, and you can add recurring runs there as well.

* Run

A single execution of a pipeline. Runs comprise an immutable log of all e xperiments that you attempt, and are designed to be self-contained to allow for reproducibility. You can track the progress of a run by looking at its details page, where you can see its runtime graph, as well as output artifacts and logs for each of its steps.

* Recurring run config

A copy of the pipeline with all fields (parameters) specified, plus a run trigger. You can start a recurring run inside any experiment, and it will periodically start a new copy of the run config. You can enable/disable the recurring run from the UI.

* Run trigger

You select one of multiple types of triggers to tell the system when a recurring run config spawns a new run:

Periodic: for an interval-based scheduling of runs (for example: every 2 hours or every 45 minutes).
Cron: for specifying cron semantics for scheduling runs. The UI also has an option for you to manually enter a cron expression.

* Step

An execution of one of the components in the pipeline. The relationship of a step to its component is much like that of a run to its pipeline: an instantiation relationship. In a complex pipeline, components can execute multiple times in loops, or conditionally after resolving an if/else like clause in the pipeline code.

* Step output artifacts

Artifacts are outputs emitted by the pipeline’s steps, which the Kubeflow pipelines UI understands, and can render as rich visualizations. It’s useful for pipeline components to include artifacts so that you can provide for performance evaluation, quick decision making for the run, or comparison across different runs. Artifacts also make it possible to understand how the pipeline’s different components work. This can range from a plain textual view of the data to rich interactive visualizations.

* Back end

A REST API server supports the front end. For user data stored in external services (for example, Google Cloud Storage), the front end makes requests directly to those services using their client libraries.

