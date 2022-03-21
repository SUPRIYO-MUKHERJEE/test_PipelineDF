sudo docker pull 3107e6123ca042ca8691f618af7d5dd2.azurecr.io/diabetes-model-score:11
sudo su
echo '{ "insecure-registries":["20.51.225.57:1200"] }' > /etc/docker/daemon.json
sudo service docker restart
sudo docker login 20.51.225.57:1200 -u admin -p master123
sudo docker tag 3107e6123ca042ca8691f618af7d5dd2.azurecr.io/diabetes-model-score:11 20.51.225.57:1200/repository/qdap-mlops/3107e6123ca042ca8691f618af7d5dd2.azurecr.io/diabetes-model-score:11
sudo docker push 20.51.225.57:1200/repository/qdap-mlops/3107e6123ca042ca8691f618af7d5dd2.azurecr.io/diabetes-model-score:11
