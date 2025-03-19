#!/bin/sh

echo "Cleaning docker volume and containers..."

docker rm project-api || true
docker volume rm project_api_data_test_volume || true

echo "Creating docker volume for 'Project API'..."

docker volume create project_api_data_test_volume
docker run -v project_api_data_test_volume:/root --name helper hello-world
#docker cp ./test_vol/project_api_data_test_folder/client_secrets.json helper:/root
docker cp ./test_vol/project_api_data_test_folder/local/workspace helper:/root
docker cp ./test_vol/project_api_data_test_folder/artifacts helper:/root
docker rm helper || true

