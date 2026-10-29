# Container Security Scan

## Purpose

Scan the AI Helpdesk Copilot Docker image for known
operating-system and Python dependency vulnerabilities.

## Tooling

- Scanner: Trivy
- Scanner version: 0.76.1
- Image: ai-helpdesk-copilot:ci
- Scan date: 2026-10-29

## Findings

The initial scan reported:

- 44 HIGH Debian package vulnerability entries
- 0 CRITICAL Debian package findings
- 5 HIGH Python findings associated with pip's bundled SBOM

Pip was removed from the runtime image after application
dependencies were installed. The application does not need
pip to run, and verification confirmed that its runtime
dependencies remained available.

A subsequent scan reported zero Python findings and
44 HIGH Debian package entries.

The 44 Debian entries represent repeated package/CVE
combinations, not 44 distinct CVEs.

## Debian Finding Assessment

The image uses Debian 13 (Trixie).

At the time of investigation, the configured Debian
repositories offered no newer candidate versions for the
checked packages:

- util-linux
- libacl1
- ncurses-base
- libsystemd0
- perl-base

The findings remain tracked and are not considered fixed.

## CI Policy

The GitHub Actions workflow:

1. Generates a Trivy report for HIGH and CRITICAL findings.
2. Uploads the JSON report as a workflow artifact.
3. Fails the security gate for HIGH or CRITICAL findings
   that Trivy classifies as fixable.

Unfixed findings remain visible in the complete report.

A successful CI run does not mean that the image is
free from all known vulnerabilities.

## Follow-Up Actions

- Re-scan the image after base-image updates.
- Check Debian security advisories for available fixes.
- Review new HIGH and CRITICAL findings.
- Avoid switching to unsupported Debian releases merely
  to reduce the scanner's finding count.
- Re-run application tests after security-related changes.
