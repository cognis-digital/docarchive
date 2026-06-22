# Demo 07 - Firmware analysis lab notes

**Where the data came from.** A firmware lab documents analysis performed on
hardware it owns, for defensive research: router update integrity (no signature
verification), default-credential handling on an IoT camera, and an exposed
serial debug interface on an industrial controller. All notes are descriptive
analysis on owned devices.

**What to expect.** A researcher searching across recurring firmware weakness
classes should get all three notes ranked, and a class-specific query should
foreground the matching note.

**Run it.**

```bash
cd demos/07-firmware-notes
docarchive index docs --out firmware.index.json
docarchive search firmware.index.json "signature verification default credentials debug"
docarchive search firmware.index.json "debug serial console" --tag debug
```

**How to act.** The broad query returns all three notes; the integrity note
(missing image signing) ranks first. The tag query isolates the exposed
debug-interface note for a hardware-hardening recommendation to the vendor.
