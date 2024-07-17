# Get debugging utilities
nix-install:
	bash -c 'sh <(curl -L https://nixos.org/nix/install) --no-daemon'
	mkdir -p ~/.config/nix
	echo 'experimental-features = nix-command flakes' > ~/.config/nix/nix.conf
	cd .. && ~/.nix-profile/bin/nix develop

##
# All following targets require tooling to be installed
##

# Create testing cluster
cluster:
	kind create cluster
	helm repo add crossplane-stable https://charts.crossplane.io/stable
	helm repo update
	helm install crossplane --namespace crossplane-system --create-namespace crossplane-stable/crossplane

gen:
	ls provider-openstack || git clone https://github.com/crossplane-contrib/provider-openstack.git -b v0.4.0
	python3 gen.py
login:
	docker login registry.scs.community
build:
	crossplane xpkg build
push:
	crossplane xpkg push registry.scs.community/central-api/configuration:$$(git rev-parse HEAD)
install:
	crossplane xpkg install configuration registry.scs.community/central-api/configuration:$$(git rev-parse HEAD)
