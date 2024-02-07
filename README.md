# SCS Central API

## Premise

By embracing existing open source solutions and bundling them, SCS is intended to
provide a viable alternative to widely adopted proprietary cloud offerings, including
Infrastructure-as-a-Service offerings, Kubernetes-as-a-Service offerings and other
X-as-a-Service offerings.

The choice to embrace existing technology has huge advantages over starting from
scratch.
By not reinventing wheels, a lot of effort can be saved. Existing communities can
be strengthened. The adoption of existing open standards is supported, reducing
market fragmentation and increasing interoperability.

## Challenge

The challenge: Using popular open source components at cloud service providers
does not result in a consistent experience for their users, yet.

Each part of the stack is consistent within its own scope: E.g. The
[OpenStack Networking API](https://docs.openstack.org/api-ref/network/v2/) is sort of
consistent with the
[OpenStack Load Balancer API](https://docs.openstack.org/api-ref/load-balancer/v2/).

The OpenStack API's share API idioms like the used AuthN/AuthZ
(Authentication/Authorization) mechanisms. But these are not applicable beyond
OpenStack services.

Entering general IAM (Identity and Access Management), Keycloak has its own set of
API endpoints and authentication flows.  
Entering Kubernetes, CAPI ([Kubernetes Cluster API](https://cluster-api.sigs.k8s.io/))
uses the Kubernetes API with its own authentication configuration, RBAC (Role Based
Access Control) and opinionated resource management idioms.

So, without a central API harmonizing at least the semantics of AuthN/AuthZ and
resource management, users are left with a bunch of semantically incompatible API's.
If resources in different API's are somehow interconnected, the users have to take
care of bridging these differences themselves.

Providing a consistent API across many different offerings with sort of consistent
API idioms is something that primarily the big proprietary cloud providers manage to
do. And while that serves users well in that regard, it also serves as an effective
vendor lock-in feature.

## Alternatives and other potential solutions

<details><summary>Self-Service solution</summary>

### Self-Service solution

Users that want to avoid such vendor lock-in as well as want to avoid spending much
time bridging technologies manually, the best bet would probably be to setup
e.g. Terraform (or OpenTofu)
with a number of specialized providers to bring all their interdependent resources into
a single place keeping track of relationships between resources across multiple API's.
Caveat: Terraform/OpenTofu/... gets admin access, while RBAC for human access is still
inconsistent.
Organizations with a lot of time/money to spend probably are able/willing to build/buy
themselves out of this situation, but that is not a solution for everyone.

Also an option especially for smaller setups: Just accept the differences between
API's and use the automation tooling that seems most native to each API. For example,
Terraform or Ansible for OpenStack VM's, ArgoCD/Flux/... for Kubernetes CAPI resources
and workload resources. The trade-off would be choosing between the full power of
all offered cloud resources (and integrating these as user) or just using a few ones,
like only Kubernetes-as-a-Service (and build the rest as user).

</details>

<details><summary>The intuitive choice: Abstract away all the things!</summary>

### The intuitive choice: Abstract away all the things!

The ideal form of API: An API that is extremely consistent in itself, each resource
defined using consistent patterns and terminology, never leaking implementation details.

- `OpenStack Compute Instance`? Very OpenStack specific, creating lock-in to OpenStack API's
- `SCS Instance`? Perfection, right?

Imagine CLI access like:

```bash
scs create subnet --group foo
scs create k8s --group foo my-k8s-01
```

Imagine using a Terraform provider like:

```hcl
resource "scs_group" "mygroup" {
  name = "mygroup"
}
resource "scs_subnet" "mysubnet" {
  group = scs_group.name
  name  = "mysubnet"
  # ...
}
resource "scs_kubernetes" "mykubernetes" {
  group  = scs_group.name
  name   = "mykubernetes"
  subnet = scs_subnet.mysubnet.id
  # ...
}
```

Imagine a Crossplane provider (or DIY similar Kubernetes controller framework) like:

```yaml
apiVersion: networking.scs.community/v1
kind: Subnet
metadata:
  name: mysubnet
spec:
  # ...
---
apiVersion: kubernetes.scs.community/v1
kind: Kubernetes
metadata:
  name: mykubernetes
spec:
  forProvider:
    subnetRef:
      name: mysubnet
  # ...
```

This is obviously desirable from a user's perspective.
However, unfortunately, it is also much more work than the SCS project can
realistically build and maintain in the short/medium term.

It also comes with the requirement to make many tough trade-off decisions.
For example:

Provider "A" offers to hide Kubernetes API server endpoints from the public
internet, utilizing some sort of bastion host. Provider "B" instead implements
IP based firewall blocking on the public endpoints. Provider "C" does neither.  
Should the API follow either provider "A" or "B"? Should both approaches be
implemented, but as optional features? If any of these approaches is defined
to be a mandatory feature to support, provider "C" cannot be compliant.

Any choice brings significant disadvantages:

- If such features are included as features that are mandatory to support,
  some providers may have difficulties adopting the API.
- If such features are included as optional features, the ability to migrate
  from one provider to another suffers significantly. Without this ability,
  users also may opt to use provider-specific API's, instead.
- If such features are excluded, the API becomes overall less useful for the
  users who may opt to use more powerful provider-specific API's, instead.

In sum: Going this route would be technically the best thing to do, yet does
not seem feasible given tough trade-offs and limited resources.  
If the opportunity arises to partner with some other organization with a lot
of staff and resources, this option may be reevaluated, though.

</details>

## The chosen approach (for now)

Goal: **Provide a "semantically" consistent API modelling most cloud resources
that are in scope for SCS**.

### Kubernetes API

Instead of creating SCS-specific API idioms and building the implementation
from scratch, the Kubernetes API will be "reused". Essentially, the Kubernetes
API is just an opinionated REST API which has opinions on how a resource
is defined, how it looks like, how it is reconciled/handled, how AuthN/AuthZ
can be implemented. The Kubernetes ecosystem provides much tooling for working
with such (custom) resource definitions: For creating the definitions
themselves, building controllers, making them discoverable and deployable.

As such, Kubernetes is a great choice for building any sort of resource
management API - with some caveats regarding its deployment and the legacy
of starting off as container orchestration tooling.

### Crossplane tooling

Crossplane even extends the Kubernetes API with "Composite Resource Definitions"
(XRD) to make Kubernetes the base for platform engineering within organizations.

Secondly, it provides an API machinery to bring any cloud resource into Kubernetes
using backend-specific "providers" (roughly comparable with Terraform providers).
As such, Crossplane with its provider ecosystem actually already did most of
the heavy lifting for providing e.g. OpenStack resources inside of Kubernetes.

On top, the platform engineering concepts in Crossplane make building multi-tenancy
systems pretty straight-forward.

Alright. Crossplane takes care of exposing OpenStack resources and does some
fancy stuff regarding multi-tenancy. What about providing actual Kubernetes
**workload** clusters?

### Cluster stacks

Cluster stacks are basically an abstraction over Cluster API. As such, Cluster
Stacks are already native to Kubernetes.

How to bring multi-tenancy tenancy concepts from Crossplane into ClusterStacks/CAPI?
That is to be determined. Yet, just building a composition including a Cluster
Stacks resource seems to be good enough to get started.

## Implementation

See [the POC for inspiration](./poc-setup.md) for now.
