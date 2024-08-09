# Get debugging utilities
nix-install:
	bash -c 'sh <(curl -L https://nixos.org/nix/install) --no-daemon'
	mkdir -p ~/.config/nix
	echo 'experimental-features = nix-command flakes' > ~/.config/nix/nix.conf
nix-develop:
	~/.nix-profile/bin/nix develop

##
# All following targets require tooling to be installed
##

##
# Building of configuration packages
##
gen-openstack:
	ls provider-openstack || git clone --depth 1 https://github.com/crossplane-contrib/provider-openstack.git -b v0.4.0
	python3 openstack-gen.py
login:
	docker login https://registry.scs.community
build-and-push:
	cd openstack && crossplane xpkg build
	cd openstack && crossplane xpkg push registry.scs.community/central-api/openstack:r7-tech-preview
	cd kubernetes && crossplane xpkg build
	cd kubernetes && crossplane xpkg push registry.scs.community/central-api/kubernetes:r7-tech-preview

##
# Setup testing environment for configuration packages
##
cluster:
	kind create cluster
	helm repo add crossplane-stable https://charts.crossplane.io/stable
	helm repo update
	helm install crossplane --namespace crossplane-system --create-namespace crossplane-stable/crossplane
install:
	crossplane xpkg install configuration registry.scs.community/central-api/kubernetes:r7-tech-preview
	crossplane xpkg install configuration registry.scs.community/central-api/openstack:r7-tech-preview