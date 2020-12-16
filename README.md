# Korg Monologue Sysex Extractor

This tool can read a sysex dump from a Korg Monologue synthesizer and will
extract all patches, properly named, into an output directory.  It can also be
used on a single patch dump, which will be renamed accordingly and copied to
the output directory.


In case of a full system dump, each patch file is named by its number and its
name. The files created can be sent to the Monologue using `amidi -p hw:1 -s
file.syx`, for example.  The files in the output directory will *not* be
automatically stored in the Monologue's memory.  If you want this behaviour,
use the files in the `outdir/auto_write/` subdirectory instead.

## Usage

To create a sysex dump:

```
amidi -p hw:1,0,1 -r dump.syx   # then select "dump patch", wait, and press CTRL+C
```

To parse and split a sysex dump:

```
monologue_extractor.py file.sysex outdir/
```

To send back a single patch to the Monologue:

```
amidi -p hw:1,0,1 -s outdir/003_Anfem.syx # will not automatically write the Monologue's memory
amidi -p hw:1,0,1 -s outdir/auto_write/003_Anfem.syx # will automatically write the Monologue's memory
```

## Example: Renaming patches

Create the full dump:

```
amidi -p hw:1,0,1 -r dump.syx   # then select "dump patch", wait, and press CTRL+C
monologue_extractor.py dump.syx outdir/
```

Then, conveniently rename your patches:

```
cd outdir/auto_write/
monologue_extract.py -r 093_Init\ Program.syx 'Warm Bass'
monologue_extract.py -r 094_Init\ Program.syx 'Glitch'
monologue_extract.py -r 095_Init\ Program.syx '5th BassLead'
monologue_extract.py -r 096_Init\ Program.syx 'Accordeon'
monologue_extract.py -r 097_\<afx\ acid3\>.syx "5th Stab"
monologue_extract.py -r 098_Init\ Program.syx 'My Lead'
monologue_extract.py -r 099_Init\ Program.syx Brass
monologue_extract.py -r 100_Init\ Program.syx 'Accordeon'
```

To send them back to the synth in bulk, use:

```
for i in 09* 100*; do amidi -p hw:1,0,1 -s "$i"; sleep 0.2; done
```

You can monitor progress during sending by watching `amidi -p hw:1,0,1 -d` output.
The status messages are:

```
F0 42 30 00 01 44 24 F7 # error
F0 42 30 00 01 44 23 F7 # success
```


