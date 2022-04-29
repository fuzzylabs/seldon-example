
## Setup

```shell
kubectl create namespace seldon
```

```shell
s2i build . seldonio/seldon-core-s2i-python3:1.14.0-dev audio-image
kubectl apply -f audio_server.yaml
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
```

There's an error `fatal error: sndfile.h: No such file or directory`on `pip install sndfile` which is a dependency
of librosa, for me this was fixed with `sudo apt-get install libsndfile1`

