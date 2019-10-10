# Install Pachyderm on openshift

1. create an nfs storageclass if not other storageclass exists.

```shell
# replace nfs.server and nfs.path with the NFS server config
helm install stable/nfs-client-provisioner --name nfs  --set nfs.server=10.16.3.220,nfs.path=/data,storageClass.defaultClass=true,storageClass.provisionerName=nfs-provisioner,storageClass.archiveOnDelete=false
```

2. if there is not a S3 object store to be used, run following to deploy minio service.

```shell
helm install --name oc --set accessKey=minio,secretKey=minio123 stable/minio
```

3. create a dry-run of Pachyderm deployment as follow:

```shell
# pachctl deploy custom --dry-run --persistent-disk aws --object-store s3 \
#   <pv-storage-name> <pv-storage-size> \
#    <s3-bucket-name> <s3-access-key-id> <s3-access-secret-key> <s3-access-endpoint-url> \
#   --static-etcd-volume=<pv-storage-name> --no-expose-docker-socket -o yaml > pach.yaml
pachctl deploy custom --dry-run --persistent-disk aws --object-store s3 pach-pv 2000000 pach minio minio3 http://oc-minio-default.apps.ddoc.os.fyre.ibm.com --static-etcd-volume=pach-pv --no-expose-docker-socket -o yaml > pach.yaml
```

4. modify `pach.yaml` file to update the volumes to use PVC through storageclass such as the file [pach.yaml](files/pachyderm/pach.yaml).

5. now deploy the Pachyderm by running

```shell
oc apply -f pach.yaml
```

## Troubleshooting

* No docker runtime or limit the user privilege to docker.sock, use `--no-expose-docker-socket` when deploying pachyderm.

* Uninstall Pachyderm

```shell
pachctl undeploy --all
```
