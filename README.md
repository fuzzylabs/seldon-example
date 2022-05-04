
## Setup

```shell
kubectl create namespace seldon
```

```shell
kubectl apply -f iris_server.yaml
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
python httprequest.py
```
