def createCatalogSource(args):
    # make a temp directory
    import tempfile
    tempdir = tempfile.mkdtemp()

    import os
#    os.mkdir(tempdir)

    # clone the repo containing the operators
    # the repo should have this directory structure
    # <root>
    #    |- operators
    #    |------|- operator-1
    #    |------|-----|- olm
    #    |------|-----|----|- operator-1.package.yaml
    #    |------|-----|----|- operator-1.clusterserviceversion.yaml
    #    |------|-----|----|- operator-1.crd.yaml
    #    |------|- operator-2
    from git import Repo
    basedir = os.path.join(tempdir, os.path.basename(args.repo))
    Repo.clone_from(args.repo, basedir)

    # download the Dockerfile
    import wget
    wget.download(args.dockerfile, out=basedir)

    # build the docker image
    import docker
    client = docker.from_env()
    client.images.build(path=basedir, tag=args.tag, nocache=True)q
    client.images.push(args.tag)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=str, required=False, default="git@github.ibm.com:OpenAIHub/openaihub.git") # default is OpenAIHub
    parser.add_argument('--dockerfile', type=str, required=False, default="https://raw.githubusercontent.com/adrian555/DocsDump/dev/files/operators/Dockerfile") # default is the Dockerfile in OpenAIHub
    import uuid
    parser.add_argument('--tag', type=str, required=False, default="ffdlops/operators:%s" %(100)) # default is ffdlops/operators:uuid
    args = parser.parse_args()
    createCatalogSource(args)