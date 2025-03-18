# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.deployments_deployment_id_body import DeploymentsDeploymentIdBody  # noqa: E501
from swagger_server.models.project_name_deployments_body import ProjectNameDeploymentsBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDeploymentController(BaseTestCase):
    """DeploymentController integration test stubs"""

    def test_app_create_deployment_id(self):
        """Test case for app_create_deployment_id

        Create deployment of a project
        """
        body = ProjectNameDeploymentsBody()
        response = self.client.open(
            '/projects/{project_name}/deployments'.format(project_name='project_name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_delete_deployment_id(self):
        """Test case for app_delete_deployment_id

        Delete the deployment ID of a project
        """
        response = self.client.open(
            '/projects/{project_name}/deployments/{deployment_id}'.format(project_name='project_name_example', deployment_id='deployment_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_deployment_gateway(self):
        """Test case for app_get_deployment_gateway

        Get files relating to a gateway device
        """
        query_string = [('resource', 'resource_example')]
        response = self.client.open(
            '/projects/{project_name}/deployments/{deployment_id}/gateway/{device_id}'.format(device_id='device_id_example', project_name='project_name_example', deployment_id='deployment_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_deployment_leaf(self):
        """Test case for app_get_deployment_leaf

        Get files relating to a leaf device
        """
        query_string = [('resource', 'resource_example')]
        response = self.client.open(
            '/projects/{project_name}/deployments/{deployment_id}/leaf/{device_id}'.format(device_id='device_id_example', project_name='project_name_example', deployment_id='deployment_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_update_deployment_id(self):
        """Test case for app_update_deployment_id

        Update deployment of a project
        """
        body = DeploymentsDeploymentIdBody()
        response = self.client.open(
            '/projects/{project_name}/deployments/{deployment_id}'.format(project_name='project_name_example', deployment_id='deployment_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
