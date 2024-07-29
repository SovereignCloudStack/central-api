# Get debugging utilities
nix-install:
	bash -c 'sh <(curl -L https://nixos.org/nix/install) --no-daemon'
	mkdir -p ~/.config/nix
	echo 'experimental-features = nix-command flakes' > ~/.config/nix/nix.conf
	~/.nix-profile/bin/nix develop

##
# All following targets require tooling to be installed
##

# Create testing cluster
cluster:
	kind create cluster
	helm repo add crossplane-stable https://charts.crossplane.io/stable
	helm repo update
	helm install crossplane --namespace crossplane-system --create-namespace crossplane-stable/crossplane

gen-openstack:
	ls provider-openstack || git clone https://github.com/crossplane-contrib/provider-openstack.git -b v0.4.0
	python3 openstack-gen.py
login:
	docker login registry.scs.community
build-and-push:
	cd openstack && crossplane xpkg build
	cd openstack && crossplane xpkg push registry.scs.community/central-api/openstack:$$(git rev-parse HEAD)
	cd kubernetes-capi && crossplane xpkg build
	cd kubernetes-capi && crossplane xpkg push registry.scs.community/central-api/kubernetes-capi:$$(git rev-parse HEAD)
	cd kubernetes-gardener && crossplane xpkg build
	cd kubernetes-gardener && crossplane xpkg push registry.scs.community/central-api/kubernetes-gardener:$$(git rev-parse HEAD)
