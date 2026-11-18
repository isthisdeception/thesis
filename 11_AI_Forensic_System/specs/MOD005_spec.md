# Module Spec: MOD005

**Module ID:** MOD005  
**Name:** Evidence Registry  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Give every evidence item an immutable `EV` id and append it to `evidence_registry.csv`. After this module writes the row, the rest of the pipeline cites the id rather than the collector's private objects.

**Inputs:** Evidence items from collectors, with the id still empty, matching `specs/interfaces.md`.

**Outputs:** The next `EVxxxxxx` id on each item, and one new row in `evidence_registry.csv`. Rows are append-only. A correction is a new row whose Dependencies name the earlier id. The earlier row is not deleted and its id is not reused.

**Dependencies:** MOD003 collectors for items. The evidence schema. No image read.

**Configuration:** The path of `evidence_registry.csv`. The id width is six digits, from the handbook identifier scheme.

**Testing:** Two items written in sequence receive two different ids. Writing the same logical observation twice still yields two ids. A row missing Evidence Type or Source Module is refused and is not given an id. The header of the registry stays the canonical header.

**Future Extensions:** More Evidence Type names, registered under MOD018, without a new column.

**Interfaces:** This module owns id assignment for the evidence schema. It is not a collector and not a fusion strategy.

**Failure Handling:** A malformed item produces a MOD016 `unexpected_error` naming the missing field. The registry file is left unchanged for that item.
