# Korg Monologue Sysex Extractor

This tool can read a sysex dump from a Korg Monologue synthesizer and will
extract all patches, properly named, into an output directory.  It can also be
used on a single patch dump, which will be renamed accordingly and copied to
the output directory.


In case of a full system dump, each patch file is named by its number and its
name. The files created can be sent to the Monologue using `amidi -p hw:1 -s
file.syx`, for example.  The files in the output directory will *not* be
automatically stored in the Monologue's memory.  If you want this behaviour,
use the files in the `outdir/auto_write/` subdirectory instead.  You can
concatenate files in `outdir/auto_write/` at will, to restore a subset of
patches automatically.

## Usage

To create a sysex dump:

```
amidi -p hw:1 -r dump.syx   # then select "dump patch", wait, and press CTRL+C
```

To parse and split a sysex dump:

```
monologue_extractor.py file.sysex outdir/
```

To send back a single patch to the Monologue:

```
amidi -p hw:1 -s outdir/003_Anfem.syx # will not automatically write the Monologue's memory
amidi -p hw:1 -s outdir/auto_write/003_Anfem.syx # will automatically write the Monologue's memory
```
