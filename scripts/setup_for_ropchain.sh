#!/usr/bin/env bash
# set up host system

# Disable aslr
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

# set core dump location
echo '/tmp/core.%e.%p' | sudo tee /proc/sys/kernel/core_pattern

