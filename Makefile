.PHONY: dev build deploy deploy-infra invalidate

DIST_ID := $(shell aws --profile theants ssm get-parameter \
  --name /xdface/design/cf-distribution-id \
  --query Parameter.Value --output text --region us-east-1 2>/dev/null)

BUCKET := $(shell aws --profile theants ssm get-parameter \
  --name /xdface/design/bucket-name \
  --query Parameter.Value --output text --region us-east-1 2>/dev/null)

dev:
	cat tokens.css web/src/styles/global.css > web/public/styles/global.css
	cd web && npm run dev

build:
	cat tokens.css web/src/styles/global.css > web/public/styles/global.css
	cd web && npm run build

deploy: build
	aws --profile theants s3 sync web/dist/ s3://$(BUCKET)/ --delete
	aws --profile theants s3 cp web/dist/index.html s3://$(BUCKET)/index.html \
	  --cache-control "no-cache, no-store, must-revalidate"
	aws --profile theants cloudfront create-invalidation \
	  --distribution-id $(DIST_ID) --paths "/*"
	@echo "Deployed to https://design.xdface.net"

deploy-infra:
	cd ../site/infra && AWS_PROFILE=theants npx cdk deploy XdfaceDesignStack

invalidate:
	aws --profile theants cloudfront create-invalidation \
	  --distribution-id $(DIST_ID) --paths "/*"
