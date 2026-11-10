---
name: game-translation
description: Use when translating any offline game. Covers the full workflow, from understanding the game to a verified patch, a restore test, and a player package. Each game gets its own tool.
---

# Game translation

[Back to README](../../README.md)

Read `AGENTS.md` first. It holds the non-negotiable rules.

## Terms

| Term | Meaning |
|---|---|
| Project | The folder for one game: notes, catalog, glossary, tool, venv. |
| Catalog | CSV files that hold each string. You edit only `target` and `notes`. |
| Glossary | `glossary.csv`. One row per terminology decision. |
| Owner choices | `docs/OWNER-CHOICES.md`. The owner's answers. |
| Backup | Copies of the original files in `<game>/original/`, with `manifest.json`. |
| Dry run | A preview. It lists the changes and writes nothing. |
| Restore test | Put the originals back and check the hashes. |

## File formats

### Catalog CSV

| Rule | Value |
|---|---|
| Encoding | UTF-8 |
| Line endings | LF |
| Quoting | Quote every field |
| Columns | `id,file,kind,source,target,notes` |
| `id` | Stable across re-extracts. Never change it. |
| `kind` | `text`, `image` or `code` |
| Edited by hand | `target` and `notes` only |

### glossary.csv

| Column | Content |
|---|---|
| `term` | The source term |
| `translation` | The chosen translation |
| `context` | Where it is used |
| `note` | Why this choice was made |

### docs/OWNER-CHOICES.md

Copy this template and fill it in. Ask the owner for each answer.

```markdown
# Owner choices: <game name>

| Choice | Answer |
|---|---|
| Target language (with code, for example `de`) | |
| Scope (what to translate) | |
| Quality level | |
| Lore: how much to keep | |
| Run-time plugin: keep active? | |
| Font | |
| Shipped text | |
| Save test approved | |
| Live game approved | |
```

## Workflow

```text
understand -> notes -> build tool -> backup -> extract -> translate
  -> audit -> owner review -> dry run -> apply -> verify -> restore test
  -> package
```

## Steps

| # | Step | Skill | Output |
|---|---|---|---|
| 1 | Understand the game | [understand-game](../understand-game/SKILL.md) | Checked facts |
| 2 | Write notes | [understand-game](../understand-game/SKILL.md) | `docs/GAME-NOTES.md` |
| 3 | Build the game's tool | [build-game-tool](../build-game-tool/SKILL.md) | `tool/` in the project |
| 4 | Back up | [build-game-tool](../build-game-tool/SKILL.md) | `<game>/original/` and `manifest.json` |
| 5 | Extract text (read-only) | [build-game-tool](../build-game-tool/SKILL.md) | Catalog files |
| 6 | Translate | This page | `target` column filled |
| 7 | Audit | This page | No errors |
| 8 | Owner review | This page | Owner approval, recorded in `OWNER-CHOICES.md` |
| 9 | Dry run | This page | List of planned changes |
| 10 | Apply | This page | Patched game |
| 11 | Verify | This page | Values match the catalog |
| 12 | Restore test | This page | Originals and hashes match |
| 13 | Package | [install-uninstall](../install-uninstall/SKILL.md) | Player package, no game files |

Also read the engine skill when the engine matches, for example [unity](../unity/SKILL.md).

## Steps in detail

### 1 and 2. Understand and write notes

- Follow `skills/understand-game/SKILL.md`.
- Ask the owner about anything unclear. Do not guess.
- Ask the owner four things: target language, scope, quality level, and how much lore to keep.
- Record the answers in `docs/OWNER-CHOICES.md`.

### 3. Build the game's tool

- Follow `skills/build-game-tool/SKILL.md`.
- The tool is for this game only.

### 4. Back up

- The tool backs up every file it will change, before any write.
- Run the backup first. A dry run does not create a backup.

### 5. Extract (read-only)

- The tool reads the game and writes the catalog. The game is not changed.

### 6. Translate

- Fill in `target` only. Use `notes` for remarks.
- Keep line breaks, tabs, tags, and placeholders exactly as in the source.
- Do not translate logic keys: scene names, enum values, IDs, hashes, internal tags.
- Add each terminology decision to `glossary.csv`.

### 7. Audit

- Check for empty targets, changed placeholders, leftover source-language text, and long lines.
- Stop on any error. Fix it, then audit again.

### 8. Owner review

- Show the owner a sample of translated lines. Include lines with placeholders and long lines.
- Wait for approval. Do not apply before it.
- Record the answer in `docs/OWNER-CHOICES.md`.

### 9. Dry run

- Run the tool in dry-run mode.
- Read the list of planned changes. Check that only the expected files appear.

### 10. Apply

- Apply only after the dry run looks right.
- The tool refuses to run while the game is open, or when the version does not match.

### 11. Verify

- Reload each changed file from disk.
- Compare each value with the catalog.
- Report success only after this check passes.

### 12. Restore test

- On a copy of the game, restore the originals from `<game>/original/`.
- Check that each restored file matches its hash in `manifest.json`.

### 13. Package

- Follow `skills/install-uninstall/SKILL.md`.

## Fonts

- Check that the game font has the glyphs of the target language. Use a glyph list or a font viewer.
- If a glyph is missing, ask the owner before you add a font.
- Record the font and its licence in `docs/GAME-NOTES.md`.

## Run-time plugins

- If the owner keeps a plugin, such as AutoTranslator or BepInEx, back up its config files too.
- Test the game with the plugin on and off.
- Record the owner's decision in `docs/OWNER-CHOICES.md`.

## Rules

> [!WARNING]
> Never patch before a backup exists.

- Never clone or redistribute the game.
- Only edit `target` and `notes` in the catalog.
- Keep `docs/OWNER-CHOICES.md` and the glossary up to date.
- Check the in-game layout for text that may not fit.

## Report

When you finish, list:

| Item | Content |
|---|---|
| Scope | What was translated |
| Files changed | Each file |
| Verify result | Pass or fail, with details |
| Not translated | What was left out, and why |
| Check in game | Layout or visual risks |
