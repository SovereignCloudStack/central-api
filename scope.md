# SCS-SIG-Central-API Scope (Proposal)

1. The SCS-SIG-Central-API creates software and documentation for SCS-providers to provide a single endpoint for SCS-Users to consume SCS-certified products.
2. All work done for 1. aims to enhance interoperability and the freedom for SCS-users to migrate between SCS-providers
3. Ordering of SCS-products instances by SCS-users should be made as easy as possible. The ideal model is 1 request results in 1 SCS-product instance (or its cancellation).

### SCS Personas

1. IaaS Provider ("CSP", bare metal, OpenStack)
2. KaaS Provider ("KSP", consumes IaaS APIs)
3. End-user (Client, Consumer of provided APIs)


### Flow and dependency graph


![](https://input.scs.community/uploads/816e81fa-fc20-48a9-9c42-e9d319f8ed8c.png)

^(Made by @bitkeks, draw.io chart available)

### Glossary:

**SCS-certified-product**: A defined product (of any kind, VM, k8s-cluster, IAM-solution, Car, coffee) that is 
A.) described via a defined API 
B.) fulfils a defined feature-set.
**SCS-certified-provider**: An entity which serves the SCS-central-API to offer at least a defined subset of SCS-certified-products.
**SCS-user**: An entity that uses the SCS-central-API of a SCS-certified-provider to order (or cancel) SCS-certified products.
**endpoint**: a URL that is under the control of a SCS-certified-Provider


---
*Comment (mxmxchere): We had the discussion about 2 or 3 personas. I personally see a benefit in a lower amount of personas (I think there are good arguments for additional personas: for example provider with subset x, scs-developer, scs-auditor, scs-operator...). But the benefit of a cleaner (the one above is already way to wobbly for my taste (too many "includes" via the word "defined")) definition outweighs imho the gain of more specific text for more personas. Nevertheless i hope that there is enough room to be a provider that only wants to offer a subset. As everything is open source we do not have under control what happens to the code that we offer. The only control that SCS can enforce is labeling things as SCS-certified or not. I hope that i made not too much and not too little use of this enforcing in the proposal.*
