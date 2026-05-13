# Dlegoream Version Policy

Version format:

A.B.C

Example:

1.00.1

---

## Philosophy

Dlegoream uses a structured versioning system to clearly indicate:

- Scale of change
- Compatibility impact
- Development progress
- Stability level

Each digit group has a distinct meaning.

---

## A — Major Version

Definition:

Core architecture or system philosophy changes.

When increased:

- B resets to 00
- C resets to 0

Example:

1.05.8 → 2.00.0

Examples of major changes:

- Storage architecture redesign
- Orchestrator redesign
- Single-node → Distributed system
- Core indexing/search philosophy changes
- Fundamental engine restructuring
- Large-scale incompatible refactor

Rule:

Increase **A** only when the system's foundation changes.

---

## B — Feature Version

Definition:

New features or subsystems added.

When increased:

- C resets to 0

Example:

1.00.9 → 1.01.0

Examples of feature changes:

- New crawler plugin
- Downloader system added
- Ranking engine added
- Vector search added
- New storage backend support
- New plugin category added
- New API integration

Rule:

Increase **B** when functionality expands.

---

## C — Patch Version

Definition:

Bug fixes, optimizations, or minor internal improvements.

Example:

1.01.3 → 1.01.4

Examples of patch changes:

- Bug fixes
- Import fixes
- Query logic fixes
- SQLite optimization
- Thread safety improvements
- Memory optimization
- Stability improvements
- Small refactoring without behavior change

Rule:

Increase **C** for maintenance changes.

---

## Examples

### Initial Release

1.00.0

Initial public system build.

---

### Patch Update

1.00.0 → 1.00.1

Changes:

- Score plugin fix
- Filter interface fix
- SQLite optimization

Reason:

Bug fixes only.

---

### Feature Update

1.00.4 → 1.01.0

Changes:

- Added crawler plugin system

Reason:

New capability added.

---

### Major Update

1.08.6 → 2.00.0

Changes:

- Migrated to distributed orchestrator architecture

Reason:

Core architecture changed.

---

## Quick Reference

| Type | Change | Example |
|------|---------|----------|
| A | Core/System redesign | 1.x.x → 2.00.0 |
| B | New feature | 1.00.x → 1.01.0 |
| C | Fix/Optimization | 1.01.0 → 1.01.1 |

---

## Practical Rule

Ask:

### "Did the foundation change?"

Yes → Increase A

No ↓

### "Did functionality expand?"

Yes → Increase B

No ↓

### "Did I only fix/improve?"

Yes → Increase C

---

## Current Example

dlegoream_1.00.1.zip

Reason:

Patch release.

Changes:

- Query bug fix
- Filter interface fix
- SQLite search optimization
- Thread safety improvements
