from project_api.vespucciprjmng.dao.db_service.domain.db_tool import DBTool
from project_api.vespucciprjmng.domain.project import Project
from project_api.vespucciprjmng.repository.db_service.project_db_repo import (
    ProjectDBRepo,
)


def synch_project_into_db(db_project_repo: ProjectDBRepo, project: Project):

    # Create project
    db_project_repo.create_project(uuid=project.uuid, name=project.name,
                                 description=project.description, version=project.version)        
    # Create models
    for model in project.models:
        # Create model
        input_obj= None
        for inp in project.inputs:
            if inp.model_ref.uuid == model.uuid:
                input_obj = inp
        output_obj= None
        for out in project.outputs:
            if out.model_ref.uuid == model.uuid:
                output_obj = out

        input_tool=DBTool(name=input_obj.tools[0].name, version=input_obj.tools[0].version, parameters={})
        output_tool=DBTool(name=output_obj.tools[0].name, version=output_obj.tools[0].version, parameters={})
        db_project_repo.create_model(
            model_uuid=model.uuid,
            input_uuid=input_obj.uuid,
            output_uuid=output_obj.uuid,
            project_uuid=project.uuid,
            model_name=model.name,
            model_type=model.model_type,
            model_metadata=model.model_metadata,
            training_type=model.training_type,
            stage=model.stage,
            input_type=input_obj.input_type,
            output_type=output_obj.output_type,
            input_tool=input_tool,
            output_tool=output_tool
        )

        # Create experiments
        for experiment in model.experiments:
            # Create experiment
            db_project_repo.create_experiment(
                project_uuid=project.uuid,
                model_uuid_or_name=model.name, 
                uuid=experiment.uuid, 
                name=experiment.name, 
                description=experiment.description,
                model_dev_file=experiment.model_dev_file
            )

        # Create tests
        for test in output_obj.tests:
            # Create test
            db_project_repo.create_test(
                project_uuid=project.uuid,
                model_uuid_or_name=model.name, 
                experiment_uuid_or_name=test.experiment_ref.uuid, 
                name=test.name, 
                model_file=test.model_file,
                parameters={}
            )

        # Create logs
        for log in input_obj.logs:
            # Create log
            if not log.start_time:
                log.start_time = ''
            if not log.end_time:
                log.end_time = ''
            db_project_repo.create_log_from_board(
                uuid=log.uuid,
                project_uuid=project.uuid,
                model_name=model.name,
                name=log.name,
                description=log.description,
                annotated=log.annotated,
                start_time=log.start_time,
                end_time=log.end_time,
                device_description=log.device_description
            )

        # Update augmentations
        input_dao = db_project_repo.dao_factory.get_input_dao_instance()
        input_db_obj = input_dao.get(project_uuid=project.uuid, model_uuid_or_name=model.uuid, input_uuid=input_obj.uuid)
        input_db_obj.augmentations = input_obj.augmentations
        input_dao.update(project_uuid=project.uuid, input=input_db_obj)
        