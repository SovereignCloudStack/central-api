1. Bootstrap host in e. g. CSP hidden tenant, install kind+CAPI there
```mermaid
flowchart LR
    A[CSP Bootstrap host] -->|install kind+CAPI| A
```

2. Use bootstrapping kind+CAPI to create Mgmt cluster (in e. g. CSP hidden tenant)
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

5. Use CAPI mgmt cluster to create central-api cluster
```mermaid
flowchart LR
    B(CSP CAPI mgmt cluster) -->|Create+Manage| C(CSP central-api cluster)
    B -->|Manage| B
```

6. Make all required changes to the central-api cluster to serve as central-api (this is where most automation will come in)
```mermaid
flowchart LR
    B(CSP CAPI mgmt cluster) -->|Manage| C(CSP central-api cluster)
    B -->|Manage| B
    C -->|Install central-api components, establish access, setup RBAC etc.| C
```

7. Actually make the central-api acessible to tenants, to manage their resources
```mermaid
flowchart LR
    B(CSP CAPI mgmt cluster) -->|Manage| C(CSP central-api cluster)
    B -->|Manage| B
    C -->|Create+Manage| C1(Tenant workload cluster)
    C -->|Manage| C2(Tenant IAM Realm)
    C -->|Manage| C3(Tenant OpenStack resources)
```
