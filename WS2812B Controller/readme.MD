# WS2812B LED Controller

WS2812B LED Controller based on the **Raspberry Pi Pico / Pico W** and **ESP8266 D1 Mini**.

This project demonstrates how to design and build a **custom through-hole PCB** that simplifies controlling WS2812B addressable LEDs. You can choose between:

- **Raspberry Pi Pico / Pico W** using MicroPython + NeoPixel  
- **ESP8266 D1 Mini** using **WLED firmware**

Perfect for desk lighting, classroom projects, IoT builds, or creative LED installations.

---

## 📺 YouTube Video

[![WS2812B LED Controller](https://img.youtube.com/vi/ZWx3QPG5xbE/0.jpg)](https://www.youtube.com/watch?v=ZWx3QPG5xbE)

---

## 📖 Introduction

Welcome to this tutorial on creating a **custom PCB controller for WS2812B LEDs** using either the Raspberry Pi Pico or the D1 Mini.

This PCB simplifies the process of controlling addressable LEDs by supporting:

- **NeoPixel library** (Raspberry Pi Pico / Pico W)
- **WLED firmware** (ESP8266 D1 Mini)

Whether you're enhancing ambient lighting, learning MicroPython, or building classroom kits, this guide walks you through **PCB design, ordering, assembly, and code**.

---

## 🧰 Components – Breakdown

| Component | Quantity |
|---------|---------|
| Custom PCB | 1 |
| Raspberry Pi Pico / Pico W | 1 |
| ESP8266 D1 Mini | 1 |
| 12×12 mm Push Buttons | 2 |
| 2.54 mm 20-Pin Header | 2 |
| 2-Pin Screw Terminals (2.54 mm pitch) | 7 |
| Miscellaneous | As needed |

---

## 📐 Schematic Diagram

The schematic was created using **EasyEDA**.  
All components are **through-hole**, making this project beginner-friendly and mechanically robust.

![Schematic Diagram](ws2182_led_controller.png)

---

## 🧩 PCB Design

The PCB was designed in **EasyEDA**, a free web-based EDA tool.

### Key Features

- Two Push Buttons  
- Bluetooth Header (HC-05)  
- Four 3 mm Mounting Holes  

![PCB Top](ws2818_pcb.png)

---

## 🛒 Ordering the PCB (JLCPCB)

Support the project:  
https://jlcpcb.com/?from=NerdCave

Gerber files:  
https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/WS2812B%20Controller

---

## 💻 Code – Raspberry Pi Pico (MicroPython)

See `main.py` and `neopixel.py` in this repository.

---

## ✅ Conclusion

This project provides a flexible and beginner-friendly way to control WS2812B LEDs using either MicroPython or WLED.

Happy building! 🚀
