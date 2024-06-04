# Hackathon'24 Central API

In this folder the manifests for the Central API MVP prototype for OpenStack are stored.
The existing MVP was used as the base for the Hackathon, and it deployed the OpenStack Crossplane provider.

Use the `bootstrap_mvp.sh` script to get an insight into how the workflow is intended.

* `01_provider_config_converter.py` and `01_provider_config.yaml.tmpl`: Provider config for Crossplane which needs to be filled with the credentials from a `clouds.yaml`.
* `02_rbac.yaml`: Setting up RBAC in Central API k8s cluster to allow "customers" to submit resources
* `03_test_resource.yaml`: a customer's resource that Crossplane picks up and creates through the OpenStack API with the stored credentials
