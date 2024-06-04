#!/bin/bash

KUBECONFIG_NAME=kubeconfig_centralapi

set -e

debug () {
    echo
    d=$(date +%H:%M:%S)
    echo -e "${d} | $@"
}

# Create KinD cluster locally and use Kubeconfig

debug "Create KinD cluster to be used as ClusterStacks management cluster"
kind create cluster --name centralapi --kubeconfig $KUBECONFIG_NAME

debug "Setting generated kubeconfig"
export KUBECONFIG=$(pwd)/$KUBECONFIG_NAME

debug "Test kubectl by querying nodes"
kubectl get nodes


# Crossplane
# https://docs.crossplane.io/v1.15/software/install/

debug "Crossplane: Fetch helm repo"
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

debug "Crossplane: Install crossplace in cluster"
helm install crossplane --namespace crossplane-system --create-namespace crossplane-stable/crossplane

debug "Check pods in crossplane-system namespace"
kubectl get pods -n crossplane-system


# OpenStack crossplance provider

debug "Applying OpenStack crossplane provider"
until kubectl apply -f ../provider.yaml
do
    sleep 3
done

# TODO: wait for resources
debug "Mirror OpenStack resources (run gen.py)"
python3 ../gen.py


# Configs

# Apply OpenStack provider as cluster admin
debug "Run 01_provider_config_converter.py"
python3 01_provider_config_converter.py

debug "And apply generated config"
until kubectl apply -f generated/01_provider_config.yaml
do
    sleep 5
done

# Apply RBAC as cluster admin
debug "Apply 02_rbac.yaml"
kubectl apply -f 02_rbac.yaml

# Apply a customer resource request as customer (via SA token).
# SSH key admin-keypair is a pre-generated value, just for testing.
debug "Apply customer resource request with SA token in the name of the end-customer"
kubectl --as system:serviceaccount:centralapiuser:centralapiuser -n centralapiuser apply -f 03_create_openstack_vm_as_customer.yaml
