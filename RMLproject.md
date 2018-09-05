# Set up and run a R project in MLflow

In this [story](https://medium.com/@dsml4real/tracking-machine-learning-models-in-r-with-mlflow-9ccce342ce91) I have described how to use [*MLflow*](https://mlflow.org/) to track machine learning model training. *MLflow* also comes with a [`Projects`](https://mlflow.org/docs/latest/projects.html) component that packs data, source code with commands, parameters and execution environment setup together as a self-contained specification. Once a *MLproject* is defined, users can run it everywhere. Currently *MLproject* can run Python code or shell command. It can also set up the Python environment for the project specified in the `conda.yaml` file defined by users.

For R users, it is common to load some packages in the R source codes. These packages need to installed for the R code to run. In the future, it could be a good enhancement for *MLflow* to add something similar to `conda.yaml` to set up R package dependencies. But we do not have to wait for it. I will show how to create a *MLproject* containing R source code and run it with `mlflow run` command.

First, create a directory and copy the data and R source codes to that directory. For example,

```text
.
└── R
    ├── MLproject
    ├── prep.R
    ├── rpart-example.R
    └── wine-quality.csv
```
In this example, the data to be learned is [`wine-quality.csv`](https://github.com/adrian555/DocsDump/raw/dev/files/mlflow.projects/R/wine-quality.csv). The example is to run the [`rpart-example.R`](https://github.com/adrian555/DocsDump/raw/dev/files/mlflow.projects/R/rpart-example.R) to fit a tree model:

```r
# Source prep.R file to install the dependencies
source("prep.R")

# Import mlflow python package for tracking
library(reticulate)
mlflow <- import("mlflow")

# Load rpart to build a tree model
library(rpart)

# Read in data
wine <- read.csv("wine-quality.csv")

# Build the model
fit <- rpart(quality ~ ., wine)

# Save the model that can be loaded later
saveRDS(fit, "fit.rpart")

# Save the model to mlflow tracking server
mlflow$log_artifact("fit.rpart")

# Plot
jpeg("rplot.jpg")
par(xpd=TRUE)
plot(fit)
text(fit, use.n=TRUE)
dev.off()

# Save the plot to mlflow tracking server
mlflow$log_artifact("rplot.jpg")
```

The R code above includes three parts: the model training, the artifacts logging through *MLflow*, and the R package dependencies installation.

Any specific R package needed for the project is going to be installed through [`prep.R`](https://github.com/adrian555/DocsDump/raw/dev/files/mlflow.projects/R/prep.R) with these codes:

```r
# Accept parameters, args[6] is the R package repo url
args <- commandArgs()

# All installed packages
pkgs <- installed.packages()

# List of required packages for this project
reqs <- c("reticulate", "rpart")

# Try to install the dependencies if not installed
sapply(reqs, function(x){
  if (!x %in% rownames(pkgs)) {
    install.packages(x, repos=c(args[6]))
  }
})
```

Before packaging these into a *MLproject*, try to test by directly invoking `Rscript` command as follow:

```commandline
Rscript rpart-example.R https://cran.r-project.org/
```

From the *MLflow* UI, you should see this run been tracked like this screen [snapshot](https://github.com/adrian555/DocsDump/raw/dev/images/r-mlproject-bare.png):