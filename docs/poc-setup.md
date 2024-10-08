# Central API MVP

Right now, this repository implements [issue 374](https://github.com/SovereignCloudStack/issues/issues/374).
It contains a script (`gen.py`) to mirror all crossplane openstack provider cluster-scoped resources to namespaced resources in an SCS API group.

Also, these instructions are striving to implement [namespaces as isolation mechanism](https://docs.crossplane.io/knowledge-base/guides/multi-tenant/#namespaces-as-an-isolation-mechanism) to implement a multi-tenant system backed by a single Kubernetes cluster.

[crossplane-contrib/x-generation](https://github.com/crossplane-contrib/x-generation) might be used as soon as [the required feature for namespace mapping](https://github.com/crossplane-contrib/x-generation/issues/21) is implemented.

## Quick Start

1. Setup testing Kubernetes cluster
1. Install crossplane
1. Select fitting configuration package (containing provider definitions, XRD's and composites) and install it
    ```bash
    export VERSION=...
    export XPKG=... # openstack / kubernetes
    crossplane xpkg install configuration registry.scs.community/central-api/$XPKG:$VERSION
    ```
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
1. Setup RBAC for tenants (wearing CSP hat)
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

Right now, it would be expected to hand out the `ServiceAccount` token to the actual tenant; When AuthN is done via OIDC (or other means), the `ServiceAccount` `tenant-name/tenant` may be dropped and `RoleBinding` `tenant-name/scs-bind` may point to an actual user/group.

