# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.activity_type_configuration_body import ActivityTypeConfigurationBody  # noqa: E501
from swagger_server.models.activity_type_configuration_body1 import ActivityTypeConfigurationBody1  # noqa: E501
from swagger_server.test import BaseTestCase


class TestConfigurationController(BaseTestCase):
    """ConfigurationController integration test stubs"""

    def test_app_create_activity_configuration(self):
        """Test case for app_create_activity_configuration

        Create activity configuration file of the project/model/activity
        """
        body = ActivityTypeConfigurationBody()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}/configuration'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_patch_activity_configuration(self):
        """Test case for app_patch_activity_configuration

        Update activity configuration file of the project/model/activity
        """
        body = ActivityTypeConfigurationBody1()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}/configuration'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
