# Cognito Managed Login Branding

Custom branding for the shared Cognito Managed Login at `login.xdface.net`
(user pool `XdfaceUserPool`, defined in `site/infra`).

- `branding-settings.json` — the `Settings` document for
  `AWS::Cognito::ManagedLoginBranding`, built from `../tokens.json`
  (green `#16A34A` action color, light `#F8F8FA` / dark `#0D0D12` backgrounds).
- Logo assets are the existing `../logo/logo.svg` (light) and
  `../logo/logo-dark.svg` (dark); Cognito accepts SVG assets.

## Consumers (all via CDK, nothing in the console)

Each app client has its own `CfnManagedLoginBranding` resource reading this
file and the SVGs at synth time:

- `site/infra/lib/xdface-auth-stack.ts` → `XdfaceSiteClient`
- `library/infra/lib/library-stack.ts` → library client
- `xdface-vault/infra/lib/constructs/CognitoClientConstruct.ts` → `vault-web`

## Changing the branding

1. Edit colors here (keep them aligned with `../tokens.json`).
2. Redeploy the stacks: `site` (make deploy-auth), `library` (make deploy-infra),
   `xdface-vault/infra` (cdk deploy).
