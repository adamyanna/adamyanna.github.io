# How to Reset SMC and NVRAM on Mac

> 2021-02-15

A quick reference for resetting the System Management Controller (SMC) and Non-Volatile RAM (NVRAM/PRAM) on Intel-based Macs. These resets resolve a wide range of hardware and firmware issues — power management, display problems, keyboard backlight, boot anomalies, and more.

## Step 1: Reset the SMC

The SMC controls low-level hardware functions: power, battery, thermal management, fans, and sleep/wake behavior.

1. Shut down your Mac.
2. Connect the MagSafe or USB-C power adapter to both the power source and your Mac.
3. On the built-in keyboard, press and hold **Shift-Control-Option** on the left side, then **simultaneously press the power button**.
4. Release all keys, then press the power button again to turn on your Mac.

## Step 2: Reset NVRAM (PRAM)

NVRAM stores settings like display resolution, startup disk selection, time zone, and recent kernel panic info.

1. Shut down your Mac.
2. Locate these keys on your keyboard: **Command (⌘), Option, P, and R**.
3. Turn on your Mac.
4. Immediately after hearing the startup chime, press and hold **Command-Option-P-R**.
5. Keep holding until the computer restarts and you hear the startup chime again.

> **Note for MacBook Pro 2016 and later (T2/Apple Silicon):** These models do not have a startup chime. Hold the keys for at least 20 seconds to ensure the process completes correctly, then release.
