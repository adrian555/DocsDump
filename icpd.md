* install OLM

```command line
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/0.11.0/install.sh | bash -s 0.11.0
```

* install olm-console

```command line
oc apply -f olm-console.yaml
```

* build catalog image [link](https://github.com/operator-framework/community-operators/blob/master/upstream.Dockerfile)

```Dockerfile
FROM python:3 as manifests

RUN pip3 install operator-courier==2.1.7
COPY operators operators
RUN for file in ./operators/*; do operator-courier nest $file /manifests/$(basename $file); done

FROM quay.io/operator-framework/upstream-registry-builder as builder
COPY --from=manifests /manifests manifests
RUN ./bin/initializer -o ./bundles.db

FROM scratch
COPY --from=builder /build/bundles.db /bundles.db
COPY --from=builder /build/bin/registry-server /registry-server
COPY --from=builder /bin/grpc_health_probe /bin/grpc_health_probe
EXPOSE 50051
ENTRYPOINT ["/registry-server"]
CMD ["--database", "bundles.db"]
```

* create catalogsource

```yaml icpd-registry.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: openaihub-catalog
  namespace: olm
spec:
  sourceType: grpc
  image: ffdlops/operators:v0.0.2
  displayName: OpenAIHub Operators
  publisher: IBM
```

```command line
oc apply -f icpd-registry.yaml
```

