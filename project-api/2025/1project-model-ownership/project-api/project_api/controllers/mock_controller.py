import os

import connexion
from flask import jsonify, send_file

mock_projects = [
    {
    "schema_version": "v9",
    "ai_project_name": "get_started_asset_tracking_mlc",
    "display_name": "Asset Tracking",
    "description": "Get started project for asset tracking scenario run on the MLC sensor.",
    "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35abc",
    "version": "1.0.0",
    "creation": "YYYY-MM-DDThh:mmTZD",
    "last_updated": "YYYY-MM-DDThh:mmTZD", 
    "models": [
        {
            "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35a46",
            "name": "asset_tracking_automl",
            "description": "Model to recognize position and orientation of a tracked item, with an Auto-ML based approach.",
            "creation": "YYYY-MM-DDThh:mmTZD",
            "last_updated": "YYYY-MM-DDThh:mmTZD", 
            "metadata": {
                "type": "classifier",
                "classes": [
                    "stationary_upright",
                    "stationary_not_upright",
                    "motion",
                    "shaken"
                ]
            },
            "dataset": {
                "dataset_id": "<dataset_id>",
                "name": "asset_tracking_mlc"
            },
            "target": {
                "type": "mlc",
                "component": "lsm6dsv16x",
                "device": "steval-mkboxpro"
            },
            "training": {
                "runtime": {
                    "job_id": "",
                    "tool": "mlctools",
                    "version": "1.0.0"
                },
                "configuration": "configuration.json",
                "artifacts": [
                    "lsm6dsv16x_mlc.ucf",
                    "lsm6dsv16x_mlc.h"
                ],
                "reports": [
                    "report.json"
                ]
            },
            "optimization": "",
            "building": ""
        }
    ],
    "deployments": [
		{
            "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35a47",
            "display_name": "Asset Tracking end-to-end system.",
            "description": "End-to-end system deployment for Asset Tracking scenario.",
            "last_deploy_time": "",
            "last_deploy_result": "",
            "cloud_params": {
                "type": "azure_iotc",
                "app_url": ""
            },
            "configuration": {
                "leaf": [
                    {
                        "device_id": "leaf_0",
                        "description": "Leaf device at position 0.",
                        "gateway_id": "gateway_0",
                        "models": [
                            {
                                "name": "asset_tracking_automl",
                                "datalogging": {
                                    "device_template_uri": "https://raw.githubusercontent.com/STMicroelectronics/appconfig/release/dtmi/appconfig/steval_mkboxpro/FP_SNS_DATALOG2_Datalog2-3.expanded.json",
                                    "device_template_id": "dtmi:appconfig:steval_mkboxpro:FP_SNS_DATALOG2_Datalog2;3",
                                    "protocol": 2,
                                    "firmware_uri": "https://raw.githubusercontent.com/STMicroelectronics/appconfig/release/bluestsdkv2/bin/steval-mkboxpro/FP-SNS-DATALOG2_Datalog2_2_0_1.bin"
                                },
                                "inference": {
                                    "device_template_uri": "e2e_system_deployment/leaf/steval_mkboxpro/asset_tracking_mlc-1.expanded.json",
                                    "device_template_id": "dtmi:vespucci:steval_mkboxpro:asset_tracking_mlc;1",
                                    "protocol": 1,
                                    "firmware_uri": "e2e_system_deployment/leaf/steval_mkboxpro/ai_inertial_steval_mkboxpro_mlc_release_1_0_0.bin",
                                    "ml_uri": "models/asset_tracking_automl/training/lsm6dsv16x_mlc.ucf",
                                    "firmware_update": "false"
                                }
                            }
                        ]
                    }
                ],
                "gateway": [
                    {
                        "device_id": "gateway_0",
                        "description": "Gateway device at position 0.",
                        "gateway_id": "",
                        "module_id": "edgeMLC",
                        "configuration_uri": "e2e_system_deployment/gateway/vespucci_config.ini.template",
                        "device_manifest_uri": "e2e_system_deployment/gateway/mlc_gateway-2.manifest.json",
                        "device_template_uri": "e2e_system_deployment/gateway/mlc_gateway-2.expanded.json",
                        "device_template_id": "dtmi:vespucci:gateway:mlc_gateway;1",
                        "wifi_mode": "off"
                    }
                ]
            }
        }
    ]
    },
    {
    "schema_version": "v9",
    "ai_project_name": "get_started_motor_classification_mcu",
    "display_name": "Motor Classification",
    "description": "Get started project for motor classification scenario run on the MCU.",
    "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35a50",
    "version": "1.0.0",
    "creation": "YYYY-MM-DDThh:mmTZD",
    "last_updated": "YYYY-MM-DDThh:mmTZD", 
    "models": [
        {
            "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35a51",
            "name": "motor_two_classes_mfcc",
            "description": "Model to classify vibration data in two classes, based on MFCC coefficients computation.",
            "creation": "YYYY-MM-DDThh:mmTZD",
            "last_updated": "YYYY-MM-DDThh:mmTZD", 
            "metadata": {
                "type": "classifier",
                "classes": [
                    "slow",
                    "fast"
                ]
            },
            "dataset": {
                "dataset_id": "<dataset_id>",
                "name": "motor_two_classes_mfcc"
            },
            "target": {
                "type": "mcu",
                "component": "stm32u585ai",
                "device": "steval-stwinbx1"
            },
            "training": {
                "runtime": {
                    "job_id": "",
                    "tool": "jupyter_notebook",
                    "version": "1.0.0"
                },
                "configuration": "configuration.json",
                "artifacts": [
                    "motor_two_classes_mfcc.h5"
                ],
                "reports": ""
            },
            "optimization": {
                "best_configuration": "66d185fa-d6b2-4187-8bec-944a1ae35b42",
                "configurations": [
                    {
                        "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35c46",
                        "name": "baseline_h5_c1",
                        "runtime": {
                            "job_id": "<job_id>",
                            "tool": "stm32ai",
                            "version": "7.3.0"
                        },
                        "configuration": "configuration.json",
                        "artifacts": [
                            "network.h",
                            "network.c",
                            "network_data.h",
                            "network_data.c"
                        ],
                        "reports": [
                            "analyze.json"
                        ]
                    }
                ]
            },
            "building":  {
                "configurations": [
                    {
                        "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35d46",
                        "runtime": {
                            "job_id": "<job_id>",
                            "tool": "stm32cubeide",
                            "version": "1.13.2"
                        },
                        "configuration": "configuration.json",
                        "artifacts": [
                            "motor_two_classes_mfcc.bin"
                        ],
                        "reports": ""
                    }
                ]
            }
        },
        {
            "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35i46",
            "name": "motor_four_classes_mfcc",
            "description": "Model to classify vibration data in four classes, based on MFCC coefficients computation.",
            "creation": "YYYY-MM-DDThh:mmTZD",
            "last_updated": "YYYY-MM-DDThh:mmTZD", 
            "metadata": {
                "type": "classifier",
                "classes": [
                    "slow",
                    "fast",
                    "slow_with_disturbance",
                    "fast_with_disturbance"
                ]
            },
            "dataset": {
                "dataset_id": "<dataset_id>",
                "name": "motor_four_classes_mfcc"
            },
            "target": {
                "type": "mcu",
                "component": "stm32u585ai",
                "device": "steval-stwinbx1"
            },
            "training": {
                "runtime": {
                    "job_id": "",
                    "tool": "jupyter_notebook",
                    "version": "1.0.0"
                },
                "configuration": "configuration.json",
                "artifacts": [
                    "motor_four_classes_mfcc.h5"
                ],
                "reports": ""
            },
            "optimization": {
                "best_configuration": "66d185fa-d6b2-4187-8bec-944a1ae35e46",
                "configurations": [
                    {
                        "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35f46",
                        "name": "baseline_h5_c1",
                        "runtime": {
                            "job_id": "<job_id>",
                            "tool": "stm32ai",
                            "version": "7.3.0"
                        },
                        "configuration": "configuration.json",
                        "artifacts": [
                            "network.h",
                            "network.c",
                            "network_data.h",
                            "network_data.c"
                        ],
                        "reports": [
                            "analyze.json"
                        ]
                    }
                ]
            },
            "building":  {
                "configurations": [
                    {
                        "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35g46",
                        "runtime": {
                            "job_id": "<job_id>",
                            "tool": "stm32cubeide",
                            "version": "1.13.2"
                        },
                        "configuration": "configuration.json",
                        "artifacts": [
                            "motor_four_classes_mfcc.bin"
                        ],
                        "reports": ""
                    }
                ]
            }
        }
    ],
    "deployments": [
        {
            "uuid": "66d185fa-d6b2-4187-8bec-944a1ae35h46",
            "display_name": "Motor Classification end-to-end system.",
            "description": "End-to-end system deployment for Motor Classification scenario.",
            "last_deploy_time": "",
            "last_deploy_result": "",
            "cloud_params": {
                "type": "azure_iotc",
                "app_url": ""
            },
            "configuration": {
                "leaf": [
                    {
                        "device_id": "leaf_0",
                        "description": "Leaf device at position 0.",
                        "gateway_id": "gateway_0",
                        "models": [
                            {
                                "name": "motor_two_classes_mfcc",
                                "datalogging": {
                                    "device_template_uri": "https://raw.githubusercontent.com/STMicroelectronics/appconfig/release/dtmi/appconfig/steval_stwinbx1/FP_SNS_DATALOG2_Datalog2-4.expanded.json",
                                    "device_template_id": "dtmi:appconfig:steval_stwinbx1:FP_SNS_DATALOG2_Datalog2;4",
                                    "protocol": 2,
                                    "firmware_uri": "https://raw.githubusercontent.com/STMicroelectronics/appconfig/release/bluestsdkv2/bin/steval-stwinbx1/FP-SNS-DATALOG2_Datalog2_2_0_1.bin"
                                },
                                "inference": {
                                    "device_template_uri": "e2e_system_deployment/leaf/steval_stwinbx1/pnpl_ai_dpu-1.expanded.json",
                                    "device_template_id": "dtmi:vespucci:steval_stwinbx1:pnpl_ai_dpu;1",
                                    "protocol": 1,
                                    "firmware_uri": "models/motor_two_classes_mfcc/building/motor_two_classes_mfcc.bin",
                                    "ml_uri": "",
                                    "firmware_update": "true"
                                }
                            }
                        ]
                    }
                ],
                "gateway": [
                    {
                        "device_id": "gateway_0",
                        "description": "Gateway device at position 0.",
                        "gateway_id": "",
                        "module_id": "edgeMotorClassificationMCU",
                        "configuration_uri": "e2e_system_deployment/gateway/vespucci_config.ini.template",
                        "device_manifest_uri": "e2e_system_deployment/gateway/motor_classification_mcu_gateway-3.manifest.json",
                        "device_template_uri": "e2e_system_deployment/gateway/motor_classification_mcu_gateway-3.expanded.json",
                        "device_template_id": "dtmi:vespucci:gateway:motor_classification_mcu_gateway;1",
                        "wifi_mode": "off"
                    }
                ]
            }
        }
    ]
    }

]

files_path = 'test/user_training_files'

def mock_get_projects():  # noqa: E501
    """Projects list

    Return project list from user workspace  # noqa: E501


    :rtype: List[Project]
    """

    return jsonify(mock_projects)

def mock_get_project(user: str, project_name: str):  # noqa: E501
    """Project

    Return project from user workspace  # noqa: E501


    :rtype: Project
    """
    project = next((project for project in mock_projects if project["ai_project_name"] == project_name), None)
    if project:
        return jsonify(project)
    else:
        return jsonify({"error": "Project not found"})

def mock_get_training_items(user: str, project_name: str, model_name: str):
    """Return Training items
    """
    query = connexion.request.args.get('item')
    if query == 'config':
        file_path = os.path.join(files_path, "configuration.json")
        return send_file(
            file_path,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename="configuration.json"
        )
    elif query == 'artifacts':
        ucf_file_path = os.path.join(files_path, "lsm6dsv16x_mlc.ucf")
        h_file_path = os.path.join(files_path, "lsm6dsv16x_mlc.h")
        return send_file(
            ucf_file_path,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename="lsm6dsv16x_mlc.ucf"
        )
        #TODO Send both ucf and h file in the reponse
        # send_file(
        #     h_file_path,
        #     mimetype="application/octet-stream",
        #     as_attachment=True,
        #     attachment_filename=F"lsm6dsv16x_mlc.h"
        # )
    elif query == 'reports':
        file_path = os.path.join(files_path, "report.json")
        return send_file(
            file_path,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename="report.json"
        )
    else:
        return jsonify({"error": "Artifact item not found"})

def mock_get_training_config(user: str, project_name: str, model_name: str):
    """Return Training config file
    """
    file_path = os.path.join(files_path, "configuration.json")
    return send_file(
        file_path,
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename="configuration.json"
    )

def mock_get_training_artifacts(user: str, project_name: str, model_name: str):
    ucf_file_path = os.path.join(files_path, "lsmdsv16x_mlc.ucf")
    h_file_path = os.path.join(files_path, "lsmdsv16x_mlc.h")
    return send_file(
        ucf_file_path,
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename="lsmdsv16x_mlc.ucf"
    ), send_file(
        h_file_path,
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename="lsmdsv16x_mlc.h"
    )

def mock_get_training_reports(user: str, project_name: str, model_name: str):
    file_path = os.path.join(files_path, "report.json")
    return send_file(
        file_path,
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename="report.json"
    )


