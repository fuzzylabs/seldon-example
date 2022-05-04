import base64
import requests


def base64_from_file(path: str) -> str:
    with open(path, "rb") as file:
        return str(base64.b64encode(file.read()), "utf-8")


response = requests.post(
    "http://localhost:8080/seldon/seldon/iris-model/api/v1.0/predictions",
    headers={"Content-Type": "application/json"},
    json={
        "data": {
            "ndarray": {
                "sepal_length": 1,
                "sepal_width": 2,
                "petal_length": 3,
                "petal_width": 4,
            }
        }
    },
)

print(response.json())
