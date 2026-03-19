# --- Project API Endpoints (from swagger_v3.yaml) ---

ENDPOINT_TEMPLATES_PROJECTS = "/templates/projects"
# GET: Project templates list
# Headers:
#   - Accept: application/json
# Params: None

ENDPOINT_TEMPLATES_PROJECT_ICON = "/templates/projects/{project_name}/icon"
# GET: Get project icon for template
# Headers:
#   - Accept: image/*
# Params (path): project_name (str, required)

ENDPOINT_PUBLIC_PROJECTS_ACTIVITY = "/templates/projects/{project_name}/models/{model_name}/{activity_type}"
# GET: Get public project activity file contents
# Headers:
#   - Accept: application/json
# Params (path): project_name, model_name, activity_type (all str, required)
# Params (query): type (str, optional), name (str, optional)

ENDPOINT_PROJECTS = "/projects"
# GET: List projects
# Headers:
#   - Authorization: Bearer <token>
#   - Accept: application/json
# Params (query): as_org (str, optional)
# POST: Create new project
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (query): is_user_project (bool, optional), as_org (str, optional)
# Body: NewProject (JSON)

ENDPOINT_PROJECT = "/projects/{project_name}"
# GET: Get project by name
# Headers:
#   - Authorization: Bearer <token>
#   - Accept: application/json
# Params (path): project_name (str, required)
# Params (query): as_org (str, optional)
# DELETE: Delete project by name
# Headers:
#   - Authorization: Bearer <token>
# Params (path): project_name (str, required)
# Params (query): as_org (str, optional)

ENDPOINT_PROJECT_ICON = "/projects/{project_name}/icon"
# GET: Get project icon
# Headers:
#   - Authorization: Bearer <token>
#   - Accept: image/*
# Params (path): project_name (str, required)
# Params (query): as_org (str, optional)

ENDPOINT_MODELS = "/projects/{project_name}/models"
# POST: Create new model
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name (str, required)
# Params (query): as_org (str, optional)
# Body: NewModel (JSON)

ENDPOINT_MODEL = "/projects/{project_name}/models/{model_name}"
# DELETE: Delete model
# Headers:
#   - Authorization: Bearer <token>
# Params (path): project_name, model_name (str, required)
# Params (query): as_org (str, optional)
# PATCH: Patch model
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name, model_name (str, required)
# Params (query): as_org (str, optional)
# Body: NewModel (JSON)

ENDPOINT_ACTIVITY = "/projects/{project_name}/models/{model_name}/{activity_type}"
# POST: Create new activity
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name, model_name, activity_type (str, required)
# Params (query): as_org (str, optional)
# Body: NewTraining (JSON)
# PUT: Update activity JSON
# PATCH: Update partial activity JSON
# DELETE: Delete activity
# GET: Get activity file contents
# Headers:
#   - Authorization: Bearer <token>
#   - Accept: application/json
# Params (query): type (str, optional), name (str, optional), as_org (str, optional)

ENDPOINT_ACTIVITY_JOB = "/projects/{project_name}/models/{model_name}/{activity_type}/job"
# POST: Create new activity job
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name, model_name, activity_type (str, required)
# Params (query): as_org (str, optional)
# Body: Job (JSON)

ENDPOINT_ACTIVITY_ARTIFACTS = "/projects/{project_name}/models/{model_name}/{activity_type}/artifacts"
# POST: Download activity job artifacts
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name, model_name, activity_type (str, required)
# Params (query): as_org (str, optional)
# Body: JobArtifact (JSON)

ENDPOINT_ACTIVITY_CONFIGURATION = "/projects/{project_name}/models/{model_name}/{activity_type}/configuration"
# POST: Create activity configuration file
# PATCH: Update activity configuration file
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name, model_name, activity_type (str, required)
# Params (query): as_org (str, optional)
# Body: TrainingMLCConfiguration (JSON)

ENDPOINT_DEPLOYMENT_LEAF = "/projects/{project_name}/deployments/{deployment_id}/leaf/{device_id}"
# GET: Get files for a leaf device
# Headers:
#   - Authorization: Bearer <token>
# Params (path): project_name, deployment_id, device_id (str, required)
# Params (query): resource (str, required), as_org (str, optional)

ENDPOINT_DEPLOYMENT_GATEWAY = "/projects/{project_name}/deployments/{deployment_id}/gateway/{device_id}"
# GET: Get files for a gateway device
# Headers:
#   - Authorization: Bearer <token>
# Params (path): project_name, deployment_id, device_id (str, required)
# Params (query): resource (str, required), as_org (str, optional)

ENDPOINT_DEPLOYMENTS = "/projects/{project_name}/deployments"
# POST: Create deployment
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json
# Params (path): project_name (str, required)
# Params (query): as_org (str, optional)
# Body: deployment (JSON)

ENDPOINT_DEPLOYMENT_ID = "/projects/{project_name}/deployments/{deployment_id}"
# PUT: Update deployment
# DELETE: Delete deployment
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json (PUT)
# Params (path): project_name, deployment_id (str, required)
# Params (query): as_org (str, optional)
# Body: deployment (JSON, PUT)

ENDPOINT_DEPLOYMENT_ARTIFACTS = "/projects/{project_name}/deployments/{deployment_name}/devices/{device_id}/artifacts"
# GET: Get deployment artifacts
# Headers:
#   - Authorization: Bearer <token>
# Params (path): project_name, deployment_name, device_id (str, required)
# Params (query): log_uuid (str, required), as_org (str, optional)

ENDPOINT_APPLICATION_ID = "/projects/{project_name}/applications/{application_id}"
# DELETE: Delete application
# PATCH: Patch application
# Headers:
#   - Authorization: Bearer <token>
#   - Content-Type: application/json (PATCH)
# Params (path): project_name, application_id (str, required)
# Params (query): as_org (str, optional)
# Body: application (JSON, PATCH)