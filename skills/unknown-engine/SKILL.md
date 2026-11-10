---
name: unknown-engine
description: Use when the game's engine has no skill in this repo. Covers how to identify the engine from its files, what to ask the owner, which workflow steps still apply, and when to stop.
---

# Unknown engine

[Back to README](../../README.md)

Use this page only when no engine skill matches the game. Notes only. No engine facts are given here.

> [!WARNING]
> Do not guess the engine, the file format, or the save rule. Ask the owner.

## Identify the engine

| Look at | What to note |
|---|---|
| Folder layout | Engine folders, such as a `*_Data` folder or a `www` folder |
| Executable | Name, platform, and any launcher |
| Library files | Engine `.dll`, `.so`, or `.dylib` files |
| Strings | Engine name or version text inside the executable or data files |

- Record each finding in `docs/GAME-NOTES.md`.
- If the engine is still unclear, list it as an open question.

## Ask the owner first

Ask before you go on:

- The engine name and version, if the owner knows them.
- The target language, scope, quality level, and lore.
- Whether a run-time plugin should stay active.
- Whether the owner has a save file to test with.

## Steps that still apply

| Step | Still needed? |
|---|---|
| Understand the game | Yes. Finish the notes. |
| Back up | Yes. Back up every file before the first write. |
| Verify after writing | Yes. Reload from disk and compare with the catalog. |
| Restore test | Yes. Check each hash after restore. |
| Engine skill | No. There is none for this engine. |

Follow [game-translation](../game-translation/SKILL.md) for the rest of the workflow.

## When to stop

> [!CAUTION]
> Stop and tell the owner when any of these is true:

- The file format cannot be read or written safely.
- The save format cannot be checked.
- The text cannot be found with confidence.
- The restore test cannot be run.

Say that no safe tool can be built for this game yet. List what is missing.
