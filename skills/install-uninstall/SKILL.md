---
name: install-uninstall
description: Use when packaging a finished translation for players. Covers the package layout, one binary per OS, the four launchers (install and uninstall for shell and Windows), the player README, and the privacy check.
---

# Install and uninstall

[Back to README](../../README.md)

Make a player package for one game. The package holds the translation, never the game.

## Package layout

```text
<game>-<lang>-package/
  bin/
    <tool>-linux-x86_64
    <tool>-windows-x86_64.exe
  catalogs/
  install.sh
  uninstall.sh
  install.bat
  uninstall.bat
  README.md
```

| Part | Content |
|---|---|
| `bin/` | One binary per OS. |
| `catalogs/` | The translated text and images. |
| Launchers | Four scripts. See below. |
| `README.md` | Short steps for players. |

## Launchers

| File | Runs on | Does |
|---|---|---|
| `install.sh` | Linux, macOS | Backs up the originals, then applies the translation. |
| `uninstall.sh` | Linux, macOS | Restores the originals from the backup. |
| `install.bat` | Windows | Backs up the originals, then applies the translation. |
| `uninstall.bat` | Windows | Restores the originals from the backup. |

> [!IMPORTANT]
> Install always backs up the originals first. Uninstall always restores them.

## Player steps

Put in `README.md`:

1. Close the game.
2. Copy this folder next to the game folder, or into it.
3. Run the install launcher for your system.
4. To remove the translation, run the uninstall launcher.

## Rules

| Rule | Why |
|---|---|
| One binary per OS | A binary runs only on the system it was built for. |
| A Windows build needs a Windows machine | The build tool cannot cross-build. |
| No game files in the package | The owner ships no game content. |
| No personal paths in the package | Protects the owner's privacy. |

> [!WARNING]
> Do not include any game file, even a backup, in the package.

## Privacy check

Run before any package is shared. Replace the pattern with the owner's own values, from their private notes. Do not write those values into this repo.

```bash
grep -rIn -i "<owner-name-or-folder>" <package-folder>
```

- No hits are allowed.
- Check the binary as well. Use `strings` on it, then grep the output.
- Check the README and all launchers.

## Testing

1. Copy the package to a test folder with a copy of the game.
2. Run install. Check the game files and hashes.
3. Run uninstall. Check that the originals are back.
4. On Windows, test the `.bat` files on a Windows machine.
