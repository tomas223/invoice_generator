.PHONY: help build run

# self-documented Makefile
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


IMAGE_NAME := invoices_python


build: ## Build docker image
	@docker build -t $(IMAGE_NAME) .



run:
	@docker run -it --rm  \
		-v$(shell pwd):/app \
		$(IMAGE_NAME)

invoice: run ## Start docker container, create invoice and convert it to PDF

CMD ?= bash
run-dev: ## Run docker container for development purposes
	@docker run -it --rm  \
		$(IMAGE_NAME) \
		$(CMD)
