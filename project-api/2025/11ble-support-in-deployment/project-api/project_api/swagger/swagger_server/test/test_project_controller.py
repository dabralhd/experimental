# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProjectController(BaseTestCase):
    """ProjectController integration test stubs"""

    def test_app_delete_project(self):
        """Test case for app_delete_project

        Delete project associated to the given name.
        """
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}'.format(project_name='project_name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_project(self):
        """Test case for app_get_project

        Get project associated to the given name.
        """
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}'.format(project_name='project_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_project_icon(self):
        """Test case for app_get_project_icon

        Get project icon associated to the given name.
        """
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}/icon'.format(project_name='project_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_template_project_icon(self):
        """Test case for app_get_template_project_icon

        Get project icon associated to the given name.
        """
        response = self.client.open(
            '/templates/projects/{project_name}/icon'.format(project_name='project_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
