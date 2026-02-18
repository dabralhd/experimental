# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestModelController(BaseTestCase):
    """ModelController integration test stubs"""

    def test_app_delete_model(self):
        """Test case for app_delete_model

        Delete model associated to the given name.
        """
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}'.format(project_name='project_name_example', model_name='model_name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
