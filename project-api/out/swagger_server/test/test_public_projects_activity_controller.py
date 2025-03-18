# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestPublicProjectsActivityController(BaseTestCase):
    """PublicProjectsActivityController integration test stubs"""

    def test_app_get_public_projects_activity(self):
        """Test case for app_get_public_projects_activity

        Get the file contents of artifacts, reports or configuration of the activity for public projects
        """
        query_string = [('type', 'type_example'),
                        ('name', 'name_example')]
        response = self.client.open(
            '/templates/projects/{project_name}/models/{model_name}/{activity_type}'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
