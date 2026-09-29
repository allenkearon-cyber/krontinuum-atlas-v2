# Krontinuum Atlas v2

Public interactive demonstrator for the RAQS / Krontinuum research programme.

## Public links

- Live demonstrator: https://krontinuum-atlas-v2-production.up.railway.app/
- Frozen research record (v085): https://doi.org/10.5281/zenodo.23042784
- Zenodo concept/version history: https://doi.org/10.5281/zenodo.23042440

## Scope

This repository contains only the public visualization client and the minimal Node.js server used to serve it. It does **not** contain the scientific generator code, research datasets, executable discovery pipeline, unpublished methods, or private research files.

Atlas v2 is a pedagogical and exploratory interface. It is not the evidentiary source for the scientific claims. For evidence, provenance, claim-status mapping, reproducibility files, and hashes, use the frozen Zenodo record.

## Frozen build

The public `index.html` in this repository is the same frozen Atlas build served by the live Railway deployment and archived with the v085 Zenodo record.

SHA-256:

`F10BDD9AA3D64F7120B4DD69777C9A8CDD0E15FD13CC2F05CEDD0BFFB396A523`

## Run locally

Requires Node.js 20 or newer.

```bash
npm start
```

Then open http://localhost:3000.

## Research boundary

The visualization is explanatory. Exact/certified numerical readouts shown in the interface are drawn from the archived RAQS / Krontinuum evidence, but no scientific result is established by the interface itself.

## License

Software is licensed under PolyForm Noncommercial 1.0.0 with a required Kearon Allen copyright notice. Research text, documentation, figures, visual design, and other non-software content are licensed CC BY-NC-ND 4.0. Commercial use requires separate written permission. See LICENSE.md.