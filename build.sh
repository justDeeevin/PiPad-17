cargo build --release
cargo objcopy --release -- -O binary PiPad17.bin
dfu-util -a0 -s 0x08000000  -D PiPad17.bin