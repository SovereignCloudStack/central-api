# Central API MVP

Right now, this repository contains a script to mirror all crossplane openstack provider cluster-scoped resources to namespaced resources.

## Quick Start

1. Setup testing Kubernetes cluster
1. Install crossplane
1. Install openstack provider (See `provider.yaml`)
1. Mirror openstack resources (See `gen.py`)
1. Setup provider config (wearing CSP hat)
    ```yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: tenant-name
    ---
    apiVersion: openstack.upbound.io/v1beta1
    kind: ProviderConfig
    metadata:
      name: tenant-name
    spec:
      credentials:
        secretRef:
          namespace: crossplane-system
          name: tenant-name-clouds-yaml
          key: clouds.json
        source: Secret
    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: tenant-name-clouds-yaml
      namespace: crossplane-system
    stringData:
      clouds.json: |
        {
          "auth_url": "https://api.gx-scs.sovereignit.cloud:5000",
          "application_credential_id": "...",
          "application_credential_secret": "...",
          "tenant_name": "tenant-name"
        }
    ```
1. Setup RBAC for tenants
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: tenant
    rules:
    - apiGroups:
      - api.scs.community
      resources:
      - '*'
      verbs:
      - '*'
    ---
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: tenant
      namespace: tenant-name
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: scs-bind
      namespace: tenant-name
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: tenant
    subjects:
    - kind: ServiceAccount
      name: tenant
      namespace: tenant-name
    ```
1. Create resource (wearing tenant hat, `kubectl --as system:serviceaccount:tenant-name:tenant -n tenant-name`)
    ```yaml
    apiVersion: api.scs.community/v1alpha1
    kind: KeypairV2
    metadata:
      name: admin
      namespace: tenant-name
    spec:
      name: admin-keypair
      publicKey: |-
        ssh-rsa ...
    ---
    apiVersion: api.scs.community/v1alpha1
    kind: InstanceV2
    metadata:
      name: testing-vm
      namespace: tenant-name
    spec:
      name: testing-vm
      keyPair: admin-keyPair
      imageName: 'Debian 12'
      flavorName: 'SCS-1V:1:20'
    ```
1. Observe creation of resources

Right now, it would be expected to hand out the `ServiceAccount` token to the actual tenant; When AuthN is done via OIDC, the `ServiceAccount` `tenant-name/tenant` may be dropped.
