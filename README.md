# Flask Rest Upload API

Flask file upload API with pause, resume and stop capability.
Endpoints:
  - /
  - /upload GET, POST, PUT
  - /pause GET, POST, PUT
  - /stop GET, POST, PUT
  - /resume GET, POST, PUT
  - /status GET, POST, PUT

#### Running image (hosted on https://hub.docker.com/repository/docker/stupidlylogical/flask-rest-upload):
Create deployment:
  - kubectl create deployment flask-rest-upload --image=stupidlylogical/flask-rest-upload:latest

#### Running image locally on kubectl (hosted on https://hub.docker.com/repository/docker/stupidlylogical/flask-rest-upload):
Create deployment:
  - kubectl create deployment flask-rest-upload --image=stupidlylogical/flask-rest-upload:latest
Create service:
  - kubectl expose deployment flask-rest-upload --type=LoadBalancer --port=5000
Create tunnel:
  - minikube tunnel

API can be accessed by the resulting IP