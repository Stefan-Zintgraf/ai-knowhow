# RDP clipboard not working when pasting into Linux (Debian 13)

## What’s going on

With xrdp, pastes from the RDP client (e.g. Windows) into Linux apps often do nothing. In the channel server log you see:

```text
clipboard_event_selection_request: unknown target unknown atom 0x00000211
clipboard_event_selection_request: unknown target unknown atom 0x0000022d
clipboard_event_selection_request: unknown target unknown atom 0x0000023c
```

Those are X11 clipboard targets (e.g. `UTF8_STRING`, `text/plain`, `COMPOUND_TEXT`). xrdp’s `xrdp-chansrv` only handled a few targets and refused the rest, so paste failed.

## Fix applied in this repo

The xrdp source under `xrdp-0.10.1/` has been patched so that:

1. **Atom limit** – The “atom &gt; 512” check in `get_atom_text()` was removed so high atom numbers (common on busy X servers) are resolved correctly.
2. **Extra text targets** – Support was added for the `text/plain` and `COMPOUND_TEXT` targets; they are handled like `UTF8_STRING` so pasted text is delivered to apps that request these types.

After rebuilding and installing xrdp (or at least `xrdp-chansrv`) from this patched source, clipboard paste from the RDP client into Linux apps should work.

## Rebuild and install (Debian)

From the project directory:

```bash
# Install build dependencies
sudo apt-get build-dep xrdp

# Build the package (from the patched source tree)
cd xrdp-0.10.1
dpkg-buildpackage -us -uc -b

# Install the new packages (adjust paths if your version differs)
sudo dpkg -i ../xrdp_*.deb ../xrdp-chansrv*.deb 2>/dev/null || sudo dpkg -i ../xrdp_0.10.1-*.deb

# Restart services
sudo systemctl restart xrdp xrdp-sesman
```

Then start a new RDP session and try pasting again.

## If you don’t want to rebuild

- **Paste in a terminal** – Many terminals only ask for `STRING`/`UTF8_STRING`, which xrdp already supports. Try Ctrl+Shift+V in a terminal; if that works, the problem is the app’s requested target.
- **Try another RDP client** – Some clients expose clipboard in a way that matches what xrdp supports.
- **Wait for an upstream/Debian fix** – This is a known class of xrdp clipboard bugs; a proper fix may appear in a future xrdp or Debian update.

## Patch file

The same changes are captured in `xrdp-clipboard-fix.patch`. To apply them to a fresh Debian xrdp source:

```bash
apt-get source xrdp
cd xrdp-0.10.1
patch -p1 < /path/to/xrdp-clipboard-fix.patch
# Then build as above.
```

Note: the patch was generated against Debian’s xrdp; the first hunk (atom limit) applies with fuzz; the rest of the changes may need to be applied manually if line numbers differ in your tree.
