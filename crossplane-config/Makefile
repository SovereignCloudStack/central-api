login:
	docker login registry.scs.community
build:
	crossplane xpkg build
push:
	crossplane xpkg push registry.scs.community/central-api/configuration:$$(git rev-parse HEAD)
