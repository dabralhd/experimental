# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.job import Job  # noqa: E501
from swagger_server.test import BaseTestCase


class TestJobController(BaseTestCase):
    """JobController integration test stubs"""

    def test_app_create_job_for_activity(self):
        """Test case for app_create_job_for_activity

        Create new Activity Job and add a job json object to the model activity in Project JSON file
        """
        body = Job()
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}/job'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
