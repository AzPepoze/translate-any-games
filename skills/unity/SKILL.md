---
name: unity
description: Use when the game is a Unity game (it has a *_Data folder). Notes only, no code. Covers where text and textures live, streamed .resS data, and .NET user strings in Assembly-CSharp.dll.
---

# Unity notes

[Back to README](../../README.md)

Facts about Unity games in general. Write no code from this page.

> [!WARNING]
> Every Unity game must still be checked. Versions, build settings, and custom code differ between games.

## Recognize a Unity game

| Sign | Meaning |
|---|---|
| A `*_Data` folder next to the executable | Usually a Unity game |
| `globalgamemanagers` in that folder | Holds the engine version |
| `Managed/Assembly-CSharp.dll` | Game code, when the game uses Mono |
| No `Assembly-CSharp.dll`, and a `GameAssembly` file | Likely IL2CPP. Code strings are not in that DLL. Check first. |

## Where text lives

| File | Holds |
|---|---|
| `.assets` files | Serialized objects. Text fields are often here. |
| `level*`, `sharedassets*`, `resources.assets` | Scene and shared data. |
| `globalgamemanagers` | Engine and project data. |
| `.resS` files | Streamed data, stored outside the `.assets` file. |

- Text can be stored in a component, such as a text label or a data field.
- Some text is a logic key, such as a scene name or an ID. Do not translate it.
- Field names give hints, but check each one in the game.

## Streamed data (.resS)

- Large data can be stored in a `.resS` file.
- The asset file keeps an offset and a size for that data.
- Changing the size of streamed data changes the offsets. Check the size before you write.

## Textures

- Images are `Texture2D` objects in the asset files.
- Pixel data is either inside the asset (inline) or in a `.resS` file (streamed).
- A texture has a mip chain: full size, then smaller copies, one after another.
- Keep the width, height, and format of the original texture.
- Compressed formats need a matching encoder. Check that the tool can write the format before you start.
- Check the result: pixels must match the expected output, or the difference must be small.

## .NET user strings (Assembly-CSharp.dll)

- Mono builds store code strings in the `#US` heap of `Assembly-CSharp.dll`.
- Each entry is UTF-16 with a length prefix.
- A string is limited by its stored length. A longer translation does not fit in place.
- Shorter text can be padded to the same length, but check that the game shows it correctly.
- The `#Strings` heap holds identifiers. Do not translate it.
- Use a .NET metadata reader to find the heap. Do not edit the heap by hand.

## Checks to run for each Unity game

| Check | Why |
|---|---|
| Unity version | Formats change between versions |
| Scripting backend (Mono or IL2CPP) | Decides where code strings live |
| Asset file names | Shows which files hold text |
| Streamed data | Changes how a patch must be written |
| Save files | A text change can break a save |
| Localization system | Some games already have a text table to use |

## Rules

- Keep logic keys unchanged: scene names, IDs, enum values, and tags.
- Keep placeholders and line breaks as in the source.
- Check the in-game layout for text boxes with a fixed size.
