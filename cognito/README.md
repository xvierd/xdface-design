# Cognito Managed Login Branding

Custom branding for the shared Cognito Managed Login at `login.xdface.net`
(user pool `XdfaceUserPool`, defined in `site/infra`).

- `branding-settings.json` — the `Settings` document for
  `AWS::Cognito::ManagedLoginBranding`, aligned with `../tokens.json`.
  Light page `#FBF6EC`, form `#FFFDF8`, action `#166534` with cream text.
  Dark page `#16201A`, form `#1F2B23`, action `#4ADE80` with forest text.
  Focus uses the tangerine accent (`#B03A0A` / `#FB923C`).
- Logo assets are `../logo/logo.svg` (light) and `../logo/logo-dark.svg`
  (forest tile). Cognito accepts SVG assets. Sepia is not a Cognito scheme.

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
