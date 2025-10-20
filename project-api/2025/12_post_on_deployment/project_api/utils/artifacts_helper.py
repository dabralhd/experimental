import json
import os
from zipfile import ZipFile

import connexion
from flask import Response
from requests import get

from project_api.globals import GlobalObjects
from project_api.models.job import Job
from project_api.models.new_training import NewTraining
from project_api.util import response_error
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_training,
)
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
import logging
import json
from project_api.utils.zipfolder import zip_directory
import shutil
import tempfile

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def download_from_s3(user, project_name, model_name, url, fpath_zip):
    """
    Downloads a zip file from an S3 URL, extracts its contents, and processes the files.
    Args:
        user (str): The user ID.
        project_name (str): The name of the project.
        model_name (str): The name of the model.
        url (str): The S3 URL to download the zip file from.
        fpath_zip (str): The file path where the downloaded zip file will be saved.
    Returns:
        bool: True if an expert mode file is found and processed, False otherwise.
    Raises:
        Response: If the download fails or if there are issues during file extraction or copying.
    """
    
    copy_configuration_json = False
    try:
        training_dir = os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                        project_name,
                                        'models',
                                        model_name,
                                        'training')
        temp_dir = os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                        project_name,
                                        'models',
                                        model_name,
                                        '_temp_training')

        logger.debug(f'url: {url},\n fpath_zip: {fpath_zip},\n dir_dest: {training_dir}\n temp_dir: {temp_dir}')
        
        try:
            response = get(url, stream=True)
            logger.info(f'response code: {response.status_code}')
            if response.status_code != 200:
                logger.error(f'NOK received while downloading from url {url}')
                return Response(status=response.status_code)             
            with open(fpath_zip, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(f'failed to download from url {url}', status=500)

        with ZipFile(fpath_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            logger.info(f'zip file extracted successfully to {temp_dir}.\n Checking for UCF file OR lsm6dsv16x_mlc.json in the downloaded artifacts.')
            for name in zip_ref.namelist():
                sensor_config_json_fname = get_sensor_name(user, project_name, model_name) + '_mlc' + '.json'
                logger.debug(f'sensor_config_json_fname: {sensor_config_json_fname}')
                if name.lower().endswith('ucf') or name.lower().startswith(sensor_config_json_fname.lower()):
                    copy_configuration_json = True
                    logger.info(f'match found in the downloaded artifacts.\n setting copy_configuration_json to: {copy_configuration_json}')

        #temp_training_dir = os.path.join(temp_dir, 'training')

        # logging.info(f'doing a walk on the extracted dir: {temp_dir}')
        # for dir_path, _, fname in os.walk(temp_dir):  
        #     logging.info(dir_path)  
        #     logging.info(fname)  
        #     for f in fname:
        #         logger.info(f'copying {f} to {training_dir}')                                   
        #         try:
        #             shutil.copy(src=os.path.join(dir_path, f), dst=os.path.join(training_dir, f))
        #         except Exception as e:
        #             logger.error(e, exc_info=True)
        #             return Response(f'failed to copy {f} after downloading trainig artifacts', status=500)
        try:
            shutil.rmtree(training_dir)   
            shutil.move(temp_dir, training_dir)
            logger.info(f"Directory '{temp_dir}' moved to '{training_dir}' successfully.")
        except Exception as e:
            logger.error(f'Error while deleting previous training contents and moving workspace contents to {training_dir}', exc_info=True)
            return Response(f'Error while deleting previous training contents and moving workspace contents to {training_dir}', status=500)

        if copy_configuration_json:
            config_file_path = os.path.join(training_dir, 'configuration.json')
            dst_file_path = os.path.join(training_dir, 'configuration_processed.json')                    
            logger.info(f'copy_configuration_json is True.\nproceeding to copy {config_file_path} to {dst_file_path}!')
            try:
                shutil.copy(src=config_file_path, dst=dst_file_path)
            except Exception as e:
                logger.error(e, exc_info=True)
                return Response('failed to copy configuration after downloading trainig artifacts', status=500)                
                
        logger.debug(f'Removing {fpath_zip}')
        os.remove(fpath_zip)               

    except Exception as e:
        logger.error(e, exc_info=True)
        return Response(status=500)
    return copy_configuration_json

def get_sensor_name(user: str, project_name: str, model_name: str):
    """
    Retrieves the sensor name from the configuration file of a specified model.
    Args:
        user (str): The user ID.
        project_name (str): The name of the project.
        model_name (str): The name of the model.
    Returns:
        str: The sensor name if found in the configuration file, otherwise an empty string.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file is not a valid JSON.
        KeyError: If the 'name' key is not present in the configuration file.
    """

    config_file_path = os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                         project_name,
                                         'models',
                                         model_name,
                                         'training',
                                         'configuration.json')
    with open(config_file_path) as f:
        obj = json.load(f)
        return obj['name']
    return ''