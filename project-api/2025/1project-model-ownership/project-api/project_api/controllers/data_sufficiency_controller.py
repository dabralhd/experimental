import os
from zipfile import ZipFile

import connexion
from flask import Response, send_file

from project_api.globals import GlobalObjects
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_training,
)
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)


def app_patch_datasuff(user, body, project_name, model_name):  # noqa: E501
    """Patch Data-Sufficiency

    :param body: The data-dufficiency to be patched
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """

    return Response(status=501)

def do_get_datasuff_item(user_ws_dir: str,
                         project_name: str, 
                         model_name: str,
                         artifact_type: str,
                         artifact_name: str                     
                         ):

    if artifact_type in ['config', 'runtime', 'reports'] or artifact_type == 'artifacts' and artifact_name:
        # print('case 1')
        return app_get_datasuff_items(user_ws_dir, project_name, model_name, artifact_type, artifact_name)
    elif artifact_type == 'artifacts' and artifact_name is None:
        # print('case 2')   
        model_dir_path = os.path.join(user_ws_dir, 
                                    project_name,
                                    "models",
                                    model_name)
        data_sufficiency_dir_name = 'data_sufficiency'
        data_sufficiency_dir_path = os.path.join(model_dir_path, data_sufficiency_dir_name)
        output_file_name = 'data_sufficiency.zip'
        output_file_path = os.path.join(model_dir_path, output_file_name)
        # print(f'top_dir_path: {model_dir_path}')
        # print(f'data_sufficiency_dir_name: {data_sufficiency_dir_name}')
        # print(f'data_sufficiency_dir_path: {data_sufficiency_dir_path}')
        # print(f'output_file_name: {output_file_name}')
        # print(f'output_file_path: {output_file_path}')

        if os.path.exists(data_sufficiency_dir_path):
            try:
                with ZipFile(output_file_path, 'w') as zf:
                    for root, dirs, files in os.walk(data_sufficiency_dir_path):
                        #zf.write(file_name)
                        for file_name in files:
                            zf.write(os.path.join(data_sufficiency_dir_path, file_name), os.path.relpath(os.path.join(data_sufficiency_dir_path, file_name), data_sufficiency_dir_path))

                return send_file(
                output_file_path,
                mimetype="application/octet-stream",
                as_attachment=True,
                attachment_filename=F"{output_file_name}",
                cache_timeout=0
                ) 
            except:
                return Response(status=500) # internal server error
            
        return Response(status=404) # not found
            

    elif artifact_type is None and artifact_name is None:
        # print('case 3')
        project_repo = ProjectFileRepo(user_ws_dir)        
        datasuff_domain_obj = None
        datasuff_domain_obj = project_repo.get_datasuff(project_name=project_name, model_uuid_or_name=model_name)
        datasuff_api_obj = convert_training(datasuff_domain_obj)        
        return datasuff_api_obj
    else:
        return Response(status=400) # bad request

def app_get_datasuff(user: str, project_name: str, model_name: str):  # noqa: E501
    """Get model training

    Return selected project model training from user workspace  # noqa: E501

    :param project_name: Project identifier
    :type project_name: str
    :param model_name: model identifier
    :type model_name: str

    :rtype: Training
    """
    # print('> app_get_datasuff')
    artifact_type = connexion.request.args.get('type')
    artifact_name = connexion.request.args.get('name')    
    user_ws_dir = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    
    return do_get_datasuff_item(user_ws_dir, project_name, model_name, artifact_type, artifact_name)
    
def app_get_datasuff_items(user_ws_dir: str, 
                           project_name: str, 
                           model_name: str, 
                           artifact_type: str, 
                           artifact_name: str):  # noqa: E501
    """Get activity file

    Return activity file requested (artifacts/reports/configuration)

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
                                         "data_sufficiency",
                                         os.path.basename(artifact_name))

        if os.path.exists(artifact_path):
            return send_file(
            artifact_path,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename=F"{artifact_name}",
            cache_timeout=0
            ) 
        else:
            return Response(f'artifact not found', status=404)
    elif artifact_type=='runtime':
        project_repo = ProjectFileRepo(user_ws_dir)        
        datasuff_domain_obj = None
        datasuff_domain_obj = project_repo.get_datasuff(project_name=project_name, model_uuid_or_name=model_name)
        datasuff_api_obj = convert_training(datasuff_domain_obj)
        
        return datasuff_api_obj.runtime
    else:
        return Response('wrong resource type requested', status=400)

def app_get_public_projects_datasuff(project_name: str, model_name: str):
    artifact_type = connexion.request.args.get('type')
    artifact_name = connexion.request.args.get('name')    
    public_prj_path = GlobalObjects.getInstance().getPublicProjectsPath()
    
    # print(f'artifact_type: {artifact_type}')
    # print(f'artifact_name: {artifact_name}')
    # print(f'public_prj_path: {public_prj_path}')
    
    return do_get_datasuff_item(public_prj_path, project_name, model_name, artifact_type, artifact_name)
    

