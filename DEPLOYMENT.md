# Deployment

Live application: https://lysisdesk.vercel.app

Vercel project: `lysis` (`prj_EUxlWVYlV9jn9JJ9QBGCLTHd8vGy`). Team: `atharva12081s-projects`.

## Runtime

`api/index.py` exposes the same HTTP handler as the desktop launcher. API routes and the interface are routed to the Python function by `vercel.json`. The derived retrieval index is built in temporary storage because deployed source files are immutable. The corpus and Python source are bundled with the function.

The hosted edition processes search queries and sequence inputs on the hosted server. Reading lists and notes stay in browser local storage. The interface explains this distinction. Do not submit patient-identifiable information or confidential sequences.

## Custom domain

`lysis.atharvaparande.com` is attached to this project. On 19 November 2026 the apex domain had no working DNS delegation, so the custom address was not live.

After restoring the domain's authoritative DNS, add this record at that DNS provider:

| Type | Name | Target |
| --- | --- | --- |
| CNAME | lysis | 9b379fa734a07d16.vercel-dns-017.com |

This is the project-specific target returned by Vercel. Recheck Vercel's domain configuration before changing it in the future. Preserve existing website, email and verification records.

## Checks

The public health endpoint reports 19 records and an 18-dimensional retrieval index. Browser checks confirm that MedCPT retrieval returns paper P007 first and translation displays all six frames. The local 21-test suite also passes through the hosted runtime adapter.

The public address is a production project domain, so subsequent production deployments can retain it.
