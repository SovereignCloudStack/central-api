1. Bootstrap host in e. g. CSP hidden Openstack project, install kind+CAPI there
```mermaid
flowchart LR
    A[CSP Bootstrap host] -->|install kind+CAPI| A
```

2. Use bootstrapping kind+CAPI to create Mgmt cluster (in e. g. CSP hidden Openstack project using application credentials)
```mermaid
flowchart LR
    A[CSP Bootstrap host with kind+CAPI] -->|Create| B(CSP CAPI mgmt cluster)
```

3. `clusterctl move` to new cluster, which should start managing itself
```mermaid
flowchart LR
    A[CSP Bootstrap host with kind+CAPI] -->|clusterctl move| B(CSP CAPI mgmt cluster)
```

4. Remove bootstrapping host
```mermaid
flowchart TB
    A[CSP Bootstrap host with kind+CAPI] -->|Delete| A
    B(CSP CAPI mgmt cluster) -->|Manage| B
```

5. Use CAPI mgmt cluster to create central-api cluster (in e. g. CSP hidden Openstack project using application credentials)
```mermaid
flowchart LR
    B(CSP CAPI mgmt cluster) -->|Create+Manage| C(CSP central-api cluster)
    B -->|Manage| B
```

6. Make all required changes to the central-api cluster to serve as central-api. This is where most automation will take care of placing credentials for the tenant's Openstack project (probably application credentials), for the tenant's keycloak realm (probably some client credentials) etc.
```mermaid
flowchart LR
    B(CSP CAPI mgmt cluster) -->|Manage| C(CSP central-api cluster)
    B -->|Manage| B
    C -->|Install central-api components, establish access, setup RBAC etc.| C
```

7. Actually make the central-api accessible to tenants, to manage their resources
```mermaid
flowchart LR
    B(CSP CAPI mgmt cluster) -->|Manage| C(CSP central-api cluster)
    B -->|Manage| B
    C -->|Manage via CAPI| C1(Tenant workload cluster)
    C -->|Manage via Crossplane| C2(Tenant IAM Realm)
    C -->|Manage via Crossplane| C3(Tenant OpenStack resources)
    U(Tenant user/employee) -->|kubectl apply -f resources.yaml| C
```
