# normalized lies

| Field | Value |
| --- | --- |
| Category | Crypto |
| Author | pavel |
| Stars | ★★★★★ |
| Solves | 1 |
| Rating | 9.0/10.0 (1 rating) |

## Description

The release gate verifies an Ed25519-signed Git commit and confirms that its normalized object hash is included in a transparency log. After verification, stock Git checks out the same submitted object and executes release/manifest.json.

The attached release is valid but unprivileged.

Submit one base64-encoded, zlib-compressed loose Git commit object that keeps the trusted signature and transparency proof valid while making the deployment worker enter privileged diagnostics.

Transport format:

`base64(zlib("commit " + decimal_length + NUL + raw_commit_body))`

Connection:

## Flag hashes

| Type | Hash |
| --- | --- |
| md5 | `0e48dbcf2d4f8e54d2d4c033a9d5058b` |

## Files

- [`dist/normalized_lies.tar.gz`](dist/normalized_lies.tar.gz)

## Reviews

Average rating: 9.0/10.0 (1 rating)

| User | Rating | Review | Date |
| --- | ---: | --- | --- |
| xzhiyouu | 9/10 | (no written comment) | 2026-07-30 19:38:11 |
