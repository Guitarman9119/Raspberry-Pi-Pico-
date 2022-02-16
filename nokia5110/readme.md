### PCD8544 (Nokia 5110) LCD sample for Raspberry Pi Pico

Required library:

https://github.com/mcauser/micropython-pcd8544

## Connections:
Connect the screen up as shown below using the
physical pins indicated (physical pin on pico)

- RST - Reset:                     Pico GP8 (11) 

- CE - Chip Enable / Chip select   Pico GP5 ( 7)

- DC - Data/Command :              Pico GP4 ( 6) 

- Din - Serial Input (Mosi):       Pico GP7 (10)

- Clk - SPI Clock:                 Pico GP6 ( 9)

- Vcc:                             Pico 3V3 (36)

- BL :                             Pico GP9(12)

- Gnd:                             Pico GND (38)

![schematic](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/blob/main/nokia5110/schematic.png)

