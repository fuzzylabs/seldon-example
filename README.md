
# Seldon Core Deployment

This is an example project showing the deployment of an iris model in Seldon Core.

## Installing Seldon

This project has the same requirements as the quickstart described in the 
[Seldon docs](https://docs.seldon.io/projects/seldon-core/en/latest/install/kind.html).

##### Install Docker
First install Docker for 
[Linux](https://docs.docker.com/engine/install/ubuntu/),
[Mac](https://docs.docker.com/desktop/mac/install/),
[Windows](https://docs.docker.com/desktop/windows/install/).

##### Install Kind
[Install Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
to run kubernetes locally.

##### Install kubectl
Install kubectl for 
[Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux),
[Mac](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos),
[Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows)
to interact with kubernetes clusters.

##### Install Helm
Install [Helm](https://helm.sh/docs/intro/install/).

##### Install Istio
For Linux and macOS, the easiest way to download Istio is using the following command:
```shell
curl -L https://istio.io/downloadIstio | sh -
```
Move to the Istio package directory. For example, if the package is istio-1.11.4:
```shell
cd istio-1.11.4
```
Add the istioctl client to your path (Linux or macOS):
```shell
export PATH=$PWD/bin:$PATH
```

Istio provides a command line tool istioctl to make the installation process easy. The demo configuration profile has a
good set of defaults that will work on your local cluster. Install it with:
```shell
istioctl install --set profile=demo -y
```

The namespace label istio-injection=enabled instructs Istio to automatically inject proxies alongside anything we deploy
in that namespace. We’ll set it up for our default namespace:
```shell
kubectl label namespace default istio-injection=enabled
```

In order for Seldon Core to use Istio’s features to manage cluster traffic, we need to create an
[Istio Gateway](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/) by running the following
command:
```shell
kubectl apply -f istio_gateway.yaml
```
For custom configuration and more details on installing seldon core with Istio please see the
[Istio Ingress](https://docs.seldon.io/projects/seldon-core/en/latest/ingress/istio.html) page.

##### Install Seldon Core
First, create a new namespace for the operator to run in:
```shell
kubectl create namespace seldon-system
```

Create a new Kubernetes cluster and configure kubectl to use it with:
```shell
kind create cluster --name seldon
kubectl cluster-info --context kind-seldon
```

Then install seldon-core in our cluster
```shell
helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set istio.enabled=true \
    --namespace seldon-system
```

To check that the controller is running do:
```shell
kubectl get pods -n seldon-system
```
You should see a `seldon-controller-manager` pod with `STATUS=Running`.

##### Local Port Forwarding
Because your kubernetes cluster is running locally, we need to forward a port on your local machine to one in the
cluster for us to be able to access it externally. You can do this by running

```shell
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
```

This will forward any traffic from port 8080 on your local machine to port 80 inside your cluster.

## Deploying the iris model

Seldon provides an sklearn iris model at `gs://seldon-models/v1.14.0-dev/sklearn/iris`.
This project deploys this with the pre-packaged
[sklearn server](https://docs.seldon.io/projects/seldon-core/en/latest/servers/sklearn.html) provided by Seldon.

First we create a namespace to run our model in 
```shell
kubectl create namespace seldon
```

Then we deploy our model using config from `iris_server.yaml`:
```shell
kubectl apply -f iris_server.yaml
```
Then we port forward our server.
```shell
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
```

We can now query our server by running the httprequest.py script
```shell
pip install -r requirements.txt
python httprequest.py
```

This guide roughly follows the Seldon instructions for 
[installing locally](https://docs.seldon.io/projects/seldon-core/en/latest/install/kind.html) and
[deploying a model](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/github-readme.html)
so see those for more information.

## Clearing down the model
Run the following to clear down the kubernetes setup:
```shell
kubectl delete -f iris_server.yaml
kubectl delete -f istio_gateway.yaml
```
