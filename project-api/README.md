# Project-API/

The Project API is an external API of STAIoTCraft to manage user projects, models, training, deployments and associated metadata.

It exposes APIs allowing the creation, modification and deletion of the following entities:

    - Projects
    - Models
    - Training
    - Deployments

The full API spec is available [here](./project_api/swagger/swagger_v3.yaml)

A user project is defined as a JSON file defined as an example [here](https://github.com/PRG-RES-UNIVERSITY/vespucci-artifacts/blob/dev/projects/get_started_asset_tracking_mlc/ai_get_started_asset_tracking_mlc.json)

### Development

Build a docker image and run the image mounted with test data.
Internally this project uses [poetry](https://python-poetry.org/) to manage dependencies.

- Build DEBUG image:
	- ```docker build --target 'run-debug' --output type=image,oci-types=true,compression=zstd,compression-level=22,push=true -t 303868523198.dkr.ecr.eu-west-1.amazonaws.com/project-api:poetryrel-debug-build1 .```
	
- Build RELEASE image:
	- ```docker build --target 'run-release' --output type=image,oci-types=true,compression=zstd,compression-level=22,push=true -t 303868523198.dkr.ecr.eu-west-1.amazonaws.com/project-api:poetryrel-build1 .```

The test data needs to be structured as in the folder ```test_vol/```. Please go through this [doc](./test_vol/README.md) to structure the test folder.

- Run the script ```create_docker_volume```: 
    -  ```[source create_docker_volume.sh]``` to create the necessary docker volume which will be mounted by the docker container.

- To run the debug container locally:
	- ```docker compose --file docker-compose-dev.yaml --env-file env.devel up -d```

Sample http routes are available in [api.http](./api.http)

### Changes to pyproject.toml file:
- Whenever we change Poetry related stuff in the ```pyproject.toml``` file, we need to run ```poetry lock --no-update``` afterwards to sync the ```poetry.lock``` file with those changes. The ```--no-update``` flag tries to preserve existing versions of dependencies. Make sure to commit the poetry.lock file after updating it.
