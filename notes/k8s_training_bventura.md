# Cluster organization
Argo workflow is used on top of k8s to manage cluster

### namespaces
dedicated namespace for each service

- how to deploy a new service in k8s cluster
    - ingress resource is supported by istio
    - ingress is required to expose a service on internet