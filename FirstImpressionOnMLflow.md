# First Impression on MLflow

[***MLflow***](https://mlflow.org/) is one of the latest open source projects added to the [**Apache Spark**](https://spark.apache.org/) ecosystem by [databricks](https://databricks.com/). It first debut in the [Spark + AI Summit 2018](https://databricks.com/session/unifying-data-and-ai-for-better-data-products). The source code is hosted in the [mlflow-github](https://github.com/databricks/mlflow) and is still in the alpha release stage. The current version is 0.4.1 released on 08/03/2018.

Blogs and meetups from databricks describe *MLflow* and its roadmap, including [Introducing MLflow: an Open Source Machine Learning Platform](https://databricks.com/blog/2018/06/05/introducing-mlflow-an-open-source-machine-learning-platform.html) and [MLflow: Infrastructure for a Complete Machine Learning Life Cycle](https://www.slideshare.net/databricks/mlflow-infrastructure-for-a-complete-machine-learning-life-cycle). Users and developers can find useful information to try out *MLflow* and further contribute to the project.

This blog, however, will show the values of *MLflow* and describe the internals of the *MLflow* based on the firsthand experience and the study of the source code. It will also look for places *MLflow* can be enhanced by some comparison with other similar projects.

## What is MLflow
***MLflow*** is targeted as an open source platform for the complete machine learning lifecycle. A complete machine learning lifecycle at least includes raw data ingestion, data analysis and preparing, model training, model evaluation, model deployment and finally model maintenance. *MLflow* is built as a Python package and provides open REST APIs and commands to

* log important parameters, metrics and other data that are mattered to the machine learning model
* track the environment a model is run on 
* run any machine learning codes on that environment 
* deploy and export models to various platforms with multiple packaging formats 

*MLflow* is implemented as several modules, where each module supports a specific function.

### MLflow components
Currently *MLflow* has three components as follow (source: [Introducing MLflow: an Open Source Machine Learning Platform](https://databricks.com/blog/2018/06/05/introducing-mlflow-an-open-source-machine-learning-platform.html))
![*MLflow* components](https://databricks.com/wp-content/uploads/2018/06/mlflow.png)

Further description of each component can be found in the blog mentioned above and the link to the [*MLflow* Documentation](https://mlflow.org/docs/latest/index.html). Rest of the section will give a high level overview of the internals and implementation of each component. 

#### Tracking
Tracking implements REST APIs and UI for parameters, metrics, artifacts and source logging and viewing. The backend is implemented with [Flask](http://flask.pocoo.org/) and run on [gunicorn](http://gunicorn.org/) HTTP server while the UI is implemented with [React](https://reactjs.org/).

The Python module for tracking is `mlflow.tracking`.

Every time users train a model on the machine learning platform *MLflow* creates a `Run`  and save the `RunInfo` meta info onto disk. Python APIs are provided to log parameters and metrics for a `Run`. The output of the run such as the model are saved in the `artifacts` for a `Run`. Each individual `Run` is grouped into an `Experiment`. Following class diagram shows classes defined in *MLflow* to support tracking function.
![*MLflow* objects](images/mlflowObjects.jpg)

The model training source code needs to call *MLflow* APIs to log the data to be tracked. For example, calling `log_metric` to log the metrics and `log_param` to log the parameters.

*MLflow* tracking server currently uses file system to persist all `Experiment` data. The directory structure looks like below:
```
mlruns
└── 0
    ├── 7003d550294e4755a65569dd846a7ca6
    │   ├── artifacts
    │   │   └── test.txt
    │   ├── meta.yaml
    │   ├── metrics
    │   │   └── foo
    │   └── params
    │       └── param1
    └── meta.yaml
```

Every `Run` can be viewed through UI browser that connects to the tracking server. 
![*MLflow* UI](images/mlflow-ui.jpg)

Users can search and filter models with `metrics` and `params`, and compare and retrieve model details.

#### Projects
Projects component defines the specification on how to run the model training code. It includes the platform configuration, the source code, the data and others that 
#### Models

![packages](images/packages.jpg)
## Experience MLflow
### Comparison
## What can make MLflow do better
