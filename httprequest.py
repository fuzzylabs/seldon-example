import base64
import requests


def base64_from_file(path: str) -> str:
    with open(path, "rb") as file:
        return str(base64.b64encode(file.read()), "utf-8")


response = requests.post(
    "http://localhost:8080/seldon/seldon/audio-model/api/v1.0/predictions",
    headers={"Content-Type": "application/json"},
    json={
        "data": {
            "ndarray": [
                base64_from_file("hello.wav")
            ]
        }
    },
)

# print(response.json())
# print(["Hello" if float(i[0]) < 0.5 else "Goodbye" for i in response.json()])
