# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.new_project import NewProject  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProjectsController(BaseTestCase):
    """ProjectsController integration test stubs"""

    def test_app_create_project(self):
        """Test case for app_create_project

        Create new project
        """
        body = NewProject()
        query_string = [('is_user_project', true)]
        response = self.client.open(
            '/projects',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_projects(self):
        """Test case for app_get_projects

        Projects list
        """
        response = self.client.open(
            '/projects',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
