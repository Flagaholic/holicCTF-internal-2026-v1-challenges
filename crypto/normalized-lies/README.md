# normalized lies

| Field | Value |
| --- | --- |
| Category | Crypto |
| Author | pavel |
| Stars | ★★★★★ |
| Solves | 1 |

## Description

The release gate verifies an Ed25519-signed Git commit and confirms that its normalized object hash is included in a transparency log. After verification, stock Git checks out the same submitted object and executes release/manifest.json.

The attached release is valid but unprivileged.

Submit one base64-encoded, zlib-compressed loose Git commit object that keeps the trusted signature and transparency proof valid while making the deployment worker enter privileged diagnostics.

Transport format:

`base64(zlib("commit " + decimal_length + NUL + raw_commit_body))`

Connection:

## Files

- [`dist/normalized_lies.tar.gz`](dist/normalized_lies.tar.gz)
