# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.new_model import NewModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestModelsController(BaseTestCase):
    """ModelsController integration test stubs"""

    def test_app_create_model(self):
        """Test case for app_create_model

        Create new model
        """
        body = NewModel()
        query_string = [('owner_uuid', 'owner_uuid_example')]
        response = self.client.open(
            '/projects/{project_name}/models'.format(project_name='project_name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_patch_model(self):
        """Test case for app_patch_model

        Patch a model
        """
        body = NewModel()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}'.format(project_name='project_name_example', model_name='model_name_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
