docker ps
docker stop <id>

docker build -t test_restful_api:latest .
docker run -p 80:5000 test_restful_api 

==> URI: 0.0.0.0:80

