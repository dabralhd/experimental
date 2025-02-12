import json
import os
from zipfile import ZipFile

import connexion
from flask import Response, send_file
from requests import get

from project_api.globals import GlobalObjects
from project_api.models.job import Job
from project_api.models.new_training import NewTraining
from project_api.util import response_error
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_training,
)
from project_api.utils.artifacts_helper import (
    download_from_s3,
)

from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
import logging
import json
from project_api.utils.zipfolder import zip_directory
import shutil
from project_api.utils.error_types import (client_side_error, ErrorType)
from project_api.utils.error_helper import (model_exists)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def app_create_training(user, body, project_name, model_name):  # noqa: E501
    """Create new training or update whole training section

    :param body: The training to be added/updated.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """ 
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    
    if connexion.request.is_json:
        new_training = NewTraining.from_dict(connexion.request.get_json())  # noqa: E501
        logger.debug(new_training)
        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)
       
        user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
        user_project_model_path_folder = os.path.join(user_project_models_path_folder, model_name)
        user_project_training_path_folder = os.path.join(user_project_model_path_folder, "training")

        project_repo.create_training(project_name=project_name, model_uuid_or_name=model_name, 
                                     type=new_training.type, configuration=new_training.configuration,
                                     artifacts=new_training.artifacts, reports=new_training.reports)

        return Response(status=201)

    return Response(status=400)

def app_update_training(user, body, project_name, model_name):  # noqa: E501
    """Create new training or update whole training section

    :param body: The training to be added/updated.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """ 
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))

    return app_create_training

def app_patch_training(user, body, project_name, model_name):  # noqa: E501
    """Create new training

    :param body: The training to be added.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """ 
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    
    if connexion.request.is_json:
        updated_training = NewTraining.from_dict(connexion.request.get_json())  # noqa: E501
        logger.debug(updated_training)
        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)

        project_repo.patch_training(project_name=project_name, model_uuid_or_name=model_name,
                                    type=updated_training.type, configuration=updated_training.configuration,
                                     artifacts=updated_training.artifacts, reports=updated_training.reports)

        return Response(status=201)

    return Response(status=400)

def do_get_training_item(user_ws_dir: str,
                         project_name: str, 
                         model_name: str,
                         artifact_type: str,
                         artifact_name: str                     
                         ):
    if artifact_type == 'artifacts':  
        if artifact_name is None:
            #logger.info(f'requested training artifacts without specifying artifact_name.')   
            model_dir_path = os.path.join(user_ws_dir, 
                                        project_name,
                                        "models",
                                        model_name)
            training_dir_name = 'training'
            training_dir_path = os.path.join(model_dir_path, training_dir_name)
            output_fname = 'training'
            zip_fname = output_fname + '.zip'
            zip_fpath = os.path.join(model_dir_path, zip_fname)
            output_file_path = os.path.join(model_dir_path, output_fname)
            logger.info(f'model_dir_path: {model_dir_path}\ntraining_dir_name: {training_dir_name}\ntraining_dir_path: {training_dir_path}')
            logger.info(f'output_fname: {output_fname}\nzip_fname: {zip_fname}\nzip_fpath: {zip_fpath}')

            try:
                zip_directory(output_file_path, training_dir_path)
                logger.info(f'zip file created successfully, now returning the file to client.')
            except Exception as e:
                logger.exception(f'Error while creating zip file: {e}')
                return Response(status=500) # internal server error

            return send_file(
            zip_fpath,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename=F"{zip_fname}",
            cache_timeout=0
            ) 
        else:
            logger.info(f'requested training artifacts with specifying artifact_name.')   
            return app_get_training_items(user_ws_dir, project_name, model_name, artifact_type, artifact_name)
    elif artifact_type in ['config', 'runtime', 'reports']:
        logger.info(f'requested training {artifact_type} without specifying artifact_name.')
        return app_get_training_items(user_ws_dir, project_name, model_name, artifact_type, artifact_name)
    elif artifact_type is None and artifact_name is None:
        logger.info(f'requested training without specifying artifact_type and artifact_name.')
        project_repo = ProjectFileRepo(user_ws_dir)

        training_domain_obj = None
        training_domain_obj = project_repo.get_training(project_name=project_name, model_uuid_or_name=model_name)

        training_api_obj = convert_training(training_domain_obj)
        return training_api_obj
    
    return Response(status=400) # bad request

def app_get_training(user: str, project_name: str, model_name: str):  # noqa: E501
    """Get model training

    Return selected project model training from user workspace  # noqa: E501

    :param project_name: Project identifier
    :type project_name: str
    :param model_name: model identifier
    :type model_name: str

    :rtype: Training
    """
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    
    artifact_type = connexion.request.args.get('type')
    artifact_name = connexion.request.args.get('name')    
    user_ws_dir = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    
    return do_get_training_item(user_ws_dir, project_name, model_name, artifact_type, artifact_name)
    
def app_delete_training(user, project_name, model_name):  # noqa: E501
    """Delete training associated to the given name

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param experiment_name: Experiment &#x60;name&#x60; identifier
    :type experiment_name: str
    :param test_name: Test &#x60;name&#x60; identifier
    :type test_name: str

    :rtype: None
    """
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    
    return Response(status=200)

def app_get_training_items(user_ws_dir: str, 
                           project_name: str, 
                           model_name: str, 
                           artifact_type: str, 
                           artifact_name: str):  # noqa: E501
    """Get output file

    Return output file generated for the test  # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param artifact_type: Artifact type (artifacts, reports or config)
    :type artifact_type: str
    :param artifact_name: Name of the Artifact file
    :type artifact_name: str

    :rtype: str
    """
    if artifact_type in ['artifacts', 'reports', 'config']:
        artifact_path = os.path.join(user_ws_dir, 
                                         project_name,
                                         "models",
                                         model_name,
                                         "training",
                                         os.path.basename(artifact_name))

        logger.info(f'artifact_path: {artifact_path}\nartifact_type: {artifact_type}\nartifact_name: {artifact_name}')
        if os.path.exists(artifact_path):
            return send_file(
            artifact_path,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename=F"{artifact_name}",
            cache_timeout=0
            ) 
        else:
            logger.error(f'artifact not found: {artifact_path}')
            return Response(f'artifact not found: {artifact_path}', status=404)
    elif artifact_type=='runtime':
        project_repo = ProjectFileRepo(user_ws_dir)        
        training_domain_obj = None
        training_domain_obj = project_repo.get_training(project_name=project_name, model_uuid_or_name=model_name)
        training_api_obj = convert_training(training_domain_obj)
        
        return training_api_obj.runtime
    else:
        logger.error(f'wrong resource type requested: {artifact_type}')
        return Response('wrong resource type requested', status=400)

def app_download_training_artifacts(user, body, project_name, model_name):
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    
    if connexion.request.is_json:
        # job_artifact = JobArtifact.from_dict(connexion.request.get_json())   
        job_artifact = connexion.request.get_json()
        
        try:                
            zip_name = 'workspace.zip'     
            model_dir = os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                         project_name,
                                         "models",
                                         model_name)

            training_dir = os.path.join(model_dir, "training")         
                 
            zip_fpath = os.path.join(model_dir, zip_name)
        
            logger.debug(f'zip_fpath: {zip_fpath} ')  

            expert_mode_flag = download_from_s3(user, 
                                                project_name, 
                                                model_name, 
                                                job_artifact["s3_url"], 
                                                zip_fpath)

            user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
            project_repo = ProjectFileRepo(user_workspace_path)
            logger.debug(f'user_workspace_path: {user_workspace_path}')
            # adapt for expert mode
            # if downloaded artifacts contains dt and ucf file than create a copy configuration.json to configuration_processed.json
            config_file_path = os.path.join(training_dir, 'configuration.json')
            dst_file_path = os.path.join(training_dir, 'configuration_processed.json')
            
            logger.debug(f'dst_file_path: {dst_file_path}\n config_file_path: {config_file_path}\n, dst_file_path: {dst_file_path}')

            # if expert_mode_flag: 
            #     logger.debug(f'expert_mode_flag is True.\nproceeding to copy {config_file_path}!')
            #     try:
            #         shutil.copy(src=config_file_path, dst=dst_file_path)
            #     except Exception as e:
            #         logger.error(e, exc_info=True)
            #         return Response('failed to copy configuration after downloading trainig artifacts', status=500)
                       
            # Add the job to the job list in the training runtime
            if "job" in job_artifact:
                new_job = Job.from_dict(job_artifact["job"])
                logger.debug(f'job version: {new_job.version}')
                logger.debug(f'job name: {new_job.name}')
                logger.debug(f'job template_id: {new_job.template_id}')

                project_repo.create_job(project_name=project_name, model_uuid_or_name=model_name, 
                                            name=new_job.name, version=new_job.version, template_id=new_job.template_id)

            # Patch runtime with the artifacts and reports array
            if "artifacts" in job_artifact:
                project_repo.patch_training(project_name=project_name, model_uuid_or_name=model_name,
                                            type=None, configuration=None,
                                            artifacts=job_artifact["artifacts"], reports=None)

            if "reports" in job_artifact:
                project_repo.patch_training(project_name=project_name, model_uuid_or_name=model_name,
                                            type=None, configuration=None,
                                            artifacts=None, reports=job_artifact["reports"])
            headers = {'Cache-Control': 'no-cache'}
            return Response(status=200, headers=headers) # disable caching for downloaded artifact
        
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=500)    

def app_create_training_configuration(user, body, project_name, model_name):
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))

    if connexion.request.is_json:
        mlc_configuration = connexion.request.get_json()  # noqa: E501
        
        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)  

        user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
        user_project_model_path_folder = os.path.join(user_project_models_path_folder, model_name)
        user_project_training_path_folder = os.path.join(user_project_model_path_folder, "training")
        
        training_domain_obj = project_repo.get_training(project_name=project_name, model_uuid_or_name=model_name)
        if training_domain_obj is None:
            project_repo.create_training(project_name=project_name, model_uuid_or_name=model_name, 
                                     type="job", configuration="configuration.json",
                                     artifacts=[], reports=[])
            training_domain_obj = project_repo.get_training(project_name=project_name, model_uuid_or_name=model_name)
        configuration_file = training_domain_obj.configuration
        configuration_file_path = os.path.join(user_project_training_path_folder, configuration_file)

        if mlc_configuration is None:
            return Response(status=400)
        
        try:
            with open(configuration_file_path, 'w') as file:
                json.dump(mlc_configuration["configuration"], file, indent=4)
        except IOError:
            return Response(status=500)

        return Response(status=201)

    return Response(status=400)

def app_patch_training_configuration(user, body, project_name, model_name):
    if not model_exists(user, project_name, model_name):
        return Response(status=client_side_error(ErrorType.NOT_FOUND))


    if connexion.request.is_json:
        patch_configuration = connexion.request.get_json()  # noqa: E501
        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)  

        user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
        user_project_model_path_folder = os.path.join(user_project_models_path_folder, model_name)
        user_project_training_path_folder = os.path.join(user_project_model_path_folder, "training")
        
        training_domain_obj = project_repo.get_training(project_name=project_name, model_uuid_or_name=model_name)
        if training_domain_obj is None:
            return response_error("Training configuration file not set", status_code=404)
        configuration_file = training_domain_obj.configuration
        configuration_file_path = os.path.join(user_project_training_path_folder, configuration_file)

        try:
            with open(configuration_file_path, 'r') as file:
                mlc_configuration = json.load(file)
        except IOError as e:
            return response_error(e.strerror, status_code=500)
        
        for key, value in patch_configuration["configuration"].items():
            mlc_configuration[key] = value
        
        try:
            with open(configuration_file_path, 'w') as file:
                json.dump(mlc_configuration, file, indent=4)
        except IOError:
            return Response(status=500)
        
        return Response(status=201)
    
    return Response(status=400)

def app_get_public_projects_training(project_name: str, model_name: str):
    artifact_type = connexion.request.args.get('type')
    artifact_name = connexion.request.args.get('name')    
    public_prj_path = GlobalObjects.getInstance().getPublicProjectsPath()
    
    logger.debug(f'artifact_type: {artifact_type}')
    logger.debug(f'artifact_name: {artifact_name}')
    logger.debug(f'public_prj_path: {public_prj_path}')
    
    return do_get_training_item(public_prj_path, project_name, model_name, artifact_type, artifact_name)
    
