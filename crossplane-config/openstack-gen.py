import yaml, copy, json, subprocess, os, os.path

xrd = yaml.load("""
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xsomethingv2.api.scs.community
spec:
  group: api.scs.community
  names:
    kind: XSomethingV2
    plural: xsomethingv2
  claimNames:
    kind: SomethingV2
    plural: somethingv2s
  versions:
  - name: v1alpha1
    referenceable: true
    served: true
    schema:
      openAPIV3Schema: {}
""", Loader=yaml.SafeLoader)

comp = yaml.load("""
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xsomethingv2.api.scs.community
spec:
  resources:
  - name: SomethingV2
    base:
      apiVersion: sometech.openstack.upbound.io/v1alpha1
      kind: SomethingV2
      spec:
        forProvider: {}
    patches:
    - fromFieldPath: spec.claimRef.namespace
      toFieldPath: spec.providerConfigRef.name
      policy:
        fromFieldPath: Required
    - type: FromCompositeFieldPath
      fromFieldPath: spec
      toFieldPath: spec.forProvider
      policy:
        fromFieldPath: Required
  compositeTypeRef:
    apiVersion: api.scs.community/v1alpha1
    kind: XSomethingV2
""", Loader=yaml.SafeLoader)

for crd_file in os.listdir("provider-openstack/package/crds"):
    with open(os.path.join("provider-openstack/package/crds", crd_file)) as f:
        crd = yaml.safe_load(f.read())
    name = crd["metadata"]["name"]
    if not name.endswith(".openstack.upbound.io") and not name.endswith(".openstack.crossplane.io"):
        print("Skipping item {}".format(name))
        continue

    if "providerconfig" in name or "storeconfig" in name:
        print("Skipping item {}".format(name))
        continue

    print("Processing {}".format(name))

    local_xrd = copy.deepcopy(xrd)
    print("process", crd["spec"]["names"])
    local_xrd["spec"]["versions"][0]["schema"]["openAPIV3Schema"] = {"properties": {"spec": {"type": "object", "properties": {}}}}
    local_xrd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"] = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["forProvider"]["properties"]
    local_xrd["metadata"]["name"] = f"x{crd['spec']['names']['plural']}.api.scs.community"
    local_xrd["spec"]["names"] = {"kind": f"x{crd['spec']['names']['kind'].lower()}", "plural": f"x{crd['spec']['names']['plural']}"}
    local_xrd["spec"]["claimNames"] = crd["spec"]["names"]
    os.makedirs(f"openstack/apis/{crd['spec']['names']['singular']}", exist_ok=True)
    with open(f"openstack/apis/{crd['spec']['names']['singular']}/definition.yaml", "w") as f:
        f.write(yaml.dump(local_xrd))

    local_comp = copy.deepcopy(comp)
    local_comp["metadata"]["name"] = f"x{crd['spec']['names']['plural']}.api.scs.community"
    local_comp["spec"]["compositeTypeRef"]["kind"] = local_xrd['spec']['names']['kind']
    local_comp["spec"]["compositeTypeRef"]["apiVersion"] = "api.scs.community/v1alpha1"
    local_comp["spec"]["resources"][0]["base"]["kind"] = crd['spec']['names']['kind']
    local_comp["spec"]["resources"][0]["base"]["apiVersion"] = crd['spec']['group'] + "/v1alpha1"
    local_comp["spec"]["resources"][0]["name"] = crd['spec']['names']['kind']
    with open(f"openstack/apis/{crd['spec']['names']['singular']}/composition.yaml", "w") as f:
        f.write(yaml.dump(local_comp))
