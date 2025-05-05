PUT  /projects/puuid

Traceback (most recent call last):
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 2077, in wsgi_app
vespucci_ai_projects_db_service       |     response = self.full_dispatch_request()
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1525, in full_dispatch_request
vespucci_ai_projects_db_service       |     rv = self.handle_user_exception(e)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1523, in full_dispatch_request
vespucci_ai_projects_db_service       |     rv = self.dispatch_request()
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1509, in dispatch_request
vespucci_ai_projects_db_service       |     return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/connexion/decorators/decorator.py", line 48, in wrapper
vespucci_ai_projects_db_service       |     response = function(request)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/connexion/decorators/uri_parsing.py", line 144, in wrapper
vespucci_ai_projects_db_service       |     response = function(request)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/connexion/decorators/validation.py", line 184, in wrapper
vespucci_ai_projects_db_service       |     response = function(request)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/connexion/decorators/validation.py", line 384, in wrapper
vespucci_ai_projects_db_service       |     return function(request)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/connexion/decorators/parameter.py", line 121, in wrapper
vespucci_ai_projects_db_service       |     return function(**kwargs)
vespucci_ai_projects_db_service       |   File "/usr/local/lib/python3.9/site-packages/ai_projects_db_service/controllers/project_controller.py", line 259, in update_project
vespucci_ai_projects_db_service       |     updatedProject = projectRepository.update(uuid=uuid, bodyJsoned=bodyJsoned)
vespucci_ai_projects_db_service       | TypeError: update() got an unexpected keyword argument 'bodyJsoned'


Single model without input and output
vespucci_ai_projects_db_service       | 172.25.0.1 - - [2022-04-22 14:49:15] "POST /projects/p3/models HTTP/1.1" 400 243 0.005726
vespucci_ai_projects_db_service       | 2022-04-22 14:49:37,745.745 connexion.apis.flask_api DEBUG flask_api - get_request: Getting data and status code
vespucci_ai_projects_db_service       | 2022-04-22 14:49:37,745.745 connexion.decorators.validation DEBUG validation - wrapper: http://0.0.0.0:6060/projects/p1/models validating schema...
vespucci_ai_projects_db_service       | 2022-04-22 14:49:37,746.746 connexion.decorators.validation ERROR validation - validate_schema: http://0.0.0.0:6060/projects/p1/models validation error: 'model' is a required property



Tool version tool long -> max 3 chars


Output tool , input tool , test
Into parameters is not possibile to put any content

Log -> end_time start time cannot be None/undefined