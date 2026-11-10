---
name: understand-game
description: Use before writing any code for an offline game. Covers confirming the engine and version, finding where text and images live, identifying file formats, checking how saves are read, recording checksums, and writing docs/GAME-NOTES.md.
---

# Understand the game

[Back to README](../../README.md)

Study the game first. Write no tool until these notes exist.

> [!WARNING]
> Ask the owner about anything you cannot confirm. Never guess an engine version, a file format, or a save rule.

## Steps

| # | Check | How |
|---|---|---|
| 1 | Engine and version | Look for engine folders and files, such as `*_Data` for Unity. Read the version from the engine's own files. |
| 2 | Executable | Find the main program. Note its name and platform. |
| 3 | Text | Find where the words are: data files, scripts, UI assets, and code strings. |
| 4 | Images | Find baked text in pictures, such as logos and signs. |
| 5 | File formats | Name each format. Note whether it is binary, text, or compressed. |
| 6 | Loading and saving | Find how the game reads its data and saves progress. |
| 7 | Save compatibility | Decide whether a change to text could change a save file. |
| 8 | Checksums | Record SHA-256 for every file you may touch. |
| 9 | Run-time text changes | Look for mods that change text while the game runs, such as AutoTranslator, ReiPatcher, BepInEx, or other plugin folders, and their config files. Note each one found. Ask the owner if it should stay active with the translation. Do not guess. Note its config files too: they are backed up with the game. |
| 10 | Unknowns | List every open question for the owner. |

## Save-file check

> [!CAUTION]
> A change to text or to a data file can break saves. Check this before you patch.

- Does the save store text? Does it store a string length or an offset into the data?
- Does the save store a hash or a checksum of a data file?
- Can an old save load after the patch? Test on a copy with a save file.
- Test with a real save file on a copy of the game. Note whether the save loads after the patch. Record the result in `docs/GAME-NOTES.md`.
- If the answer is not clear, ask the owner.

## Checksums

- Hash every file the tool may change, with SHA-256.
- Keep the list. The backup `manifest.json` uses the same hashes.
- Do this before any write.

## Output

Write `docs/GAME-NOTES.md` in the game's project folder. Use the template below.

Record the owner's answers in `docs/OWNER-CHOICES.md`. The template is in [game-translation](../game-translation/SKILL.md).

## Template: docs/GAME-NOTES.md

```markdown
# Game notes: <game name>

## Identity

| Item | Value |
|---|---|
| Game name | |
| Engine | |
| Engine version | |
| Platform | |
| Executable | |

## Text

| Where | Format | Notes |
|---|---|---|
| | | |

## Images with text

| Where | Format | Notes |
|---|---|---|
| | | |

## File formats

| Format | Read by | Writable? |
|---|---|---|
| | | |

## Loading and saving

- How data is loaded:
- How saves are written:
- Save risk:

## Run-time text changes

| Plugin | Where | Owner decision |
|---|---|---|
| | | |

## Checksums

| File | SHA-256 |
|---|---|
| | |

## Open questions for the owner

- [ ]
```

## Rules

- Ask the owner about every unclear point. Record the answer.
- Do not write code in this step.
- Do not change any game file in this step.
- Keep the notes factual. Mark guesses as open questions.
