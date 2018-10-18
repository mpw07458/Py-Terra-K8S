#!/usr/bin/env bash
echo "Setting environment variables for Terraform"
export ARM_SUBSCRIPTION_ID=f19a7ca5-0d83-44b9-a9c2-6b4a402b5b38
export ARM_CLIENT_ID=168f8ef0-c532-45f3-af0b-12934bebd639
export ARM_CLIENT_SECRET=okcDpETZgekzT59euC4I52kjuNmD3SR9WR42G07+SVE=
export ARM_TENANT_ID=4d0ddf71-4b9d-4636-8016-f3699c4bf368

# Not needed for public, required for usgovernment, german, china
export ARM_ENVIRONMENT=public