# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.model_name_activity_type_body import ModelNameActivityTypeBody  # noqa: E501
from swagger_server.models.new_training import NewTraining  # noqa: E501
from swagger_server.models.training import Training  # noqa: E501
from swagger_server.test import BaseTestCase


class TestActivityController(BaseTestCase):
    """ActivityController integration test stubs"""

    def test_app_create_activity(self):
        """Test case for app_create_activity

        Create new Activity
        """
        body = NewTraining()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_delete_activity(self):
        """Test case for app_delete_activity

        Delete the activity associated to the given name.
        """
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_activity(self):
        """Test case for app_get_activity

        Get the file contents of artifacts, reports or configuration of the activity
        """
        query_string = [('type', 'type_example'),
                        ('name', 'name_example')]
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_patch_activity(self):
        """Test case for app_patch_activity

        Update partial Activity JSON
        """
        body = ModelNameActivityTypeBody()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_update_activity(self):
        """Test case for app_update_activity

        Update Activity JSON
        """
        body = Training()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
