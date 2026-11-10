---
name: build-game-tool
description: Use when writing the translation tool for one specific offline game, after its notes exist. Covers detection, refusing unsafe runs, backups with a manifest, applying catalogs, verifying by reloading, restoring, and the Python venv setup.
---

# Build the game's tool

[Back to README](../../README.md)

Write one tool for one game. Put it in that game's project folder. Do not reuse a tool from another game.

Read `AGENTS.md` and `docs/GAME-NOTES.md` first.

## Setup

- Language: Python.
- Use `uv`. Never use system-wide pip.
- Create the venv inside the project:

```bash
uv venv .venv
uv pip install -p .venv/bin/python <packages>
```

- Run the tool with `.venv/bin/python`.
- Name the tool `<game-slug>-translator`. Do not use `tag` or a generic name.

> [!WARNING]
> Test on a copy of the game, never the live one.

## Shared code

Each game has its own tool. Only two exceptions exist:

| Exception | Rule |
|---|---|
| Shared helper | `skills/image-text/overlay.py` may be used by any game. Keep the game's image config, fonts, and output images in its own project. |
| Owner-approved code copy | Copy engine code from another project only after the owner approves it in writing for that game. The copy is then independent. Record the approval and the source in `docs/GAME-NOTES.md`. |

For image text, see [image-text](../image-text/SKILL.md).

## What the tool must do

| # | Requirement | Detail |
|---|---|---|
| 1 | Detect | Confirm the game and its version. Stop if they do not match the notes. |
| 2 | Refuse when unsafe | Stop if the game is running. Stop if the version differs. |
| 3 | Back up | Copy every file the tool will change into `<game>/original/`. |
| 4 | Manifest | Write `manifest.json` with the SHA-256 of each backed-up file. |
| 5 | Never overwrite | If a backup already exists, keep it. Never replace it. |
| 6 | Extract | Read the game and write the catalog. Never write to the game. |
| 7 | Apply | Write translations from the catalog. Support a dry-run mode. |
| 8 | Verify | Reload each changed file from disk and compare it with the catalog. |
| 9 | Restore | Copy the originals back from `<game>/original/`. Check each hash. |
| 10 | Log | Print clear messages: what it did, what it skipped, and why. |

## Order of a write run

```text
detect -> check not running -> check version -> back up -> manifest
  -> plan changes in memory -> write each file -> verify
```

## Rules for writes

- Back up before the first write. No exceptions.
- Plan all changes in memory first. Check lengths and limits before any write.
- Write each file to a temporary path, then rename it into place.
- Stop on the first error. Do not leave a half-written file.
- A dry run must write nothing.

## Catalog

- Keep one row per string or asset.
- Keep stable IDs, so a re-extract keeps existing translations.
- Only the `target` and `notes` columns are edited by hand.
- Keep the source text. Never change it after extract.

## Backup manifest

Example layout:

```text
<game>/original/
  manifest.json
  <copied files, same relative paths>
```

```json
{
  "game": "Game Name",
  "version": "1.0.0",
  "files": [
    {"path": "relative/path/file.ext", "sha256": "..."}
  ]
}
```

## Verify and restore

- Verify reads from disk, not from memory.
- Restore copies each file back and checks its SHA-256 against the manifest.
- Report a hash mismatch as an error. Do not continue.

## Testing

1. Make a copy of the game in a test folder.
2. Run the dry run on the copy.
3. Run apply on the copy.
4. Run verify on the copy.
5. Run restore on the copy. Check the hashes.
6. Only then consider the live game, and only with the owner's approval.

## Rules

- One tool per game.
- Keep logic keys out of translation.
- Keep placeholders and line breaks exactly as in the source.
- The tool must not contain personal paths. Use arguments for paths.
