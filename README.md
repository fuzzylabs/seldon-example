
## Setup

```shell
kubectl create namespace seldon
```

```shell
s2i build . seldonio/seldon-core-s2i-python3:1.14.0-dev iris-image
kubectl apply -f iris_server.yaml
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
```
