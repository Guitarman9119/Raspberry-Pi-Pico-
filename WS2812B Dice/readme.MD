---
title: "Raspberry Pi Pico WS2812B Dice"
description: "Raspberry Pi Pico WS2812B Dice"
lead: ""
date: 2020-10-06T08:48:57+00:00
lastmod: 2020-10-06T08:48:57+00:00
draft: false
images: []
menu:
weight: 205

---

### YouTube Video
<iframe width="728" height="410" src="https://www.youtube.com/embed/xxxxxxxxxxxx" title="YouTube video player" frameborder="10" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


## Introduction

In this project, we are recreating a previous Raspberry Pi Pico Dice build using WS2812B through-hole LEDs. With three push buttons, you can roll either the left die, the right die, or both dice together using the middle button.
The PCB design for this project will to mimic the face patterns of a standard die shown below.

<figure><img src="images/dice_patterns.jpg" alt=""><figcaption></figcaption></figure>

**Disclaimer** - JLCPCB was generous enough to sponsor this project and provide the PCB used in this project.

## Components + Tools Breakdown

| Components          | Quantity            |
| ------------------- | ------------------- |
| Custom PCB (JLCPB) | 1 |
| Raspberry Pi Pico  | 1 |
| WS2812B 8mm THT    | 14 |
| 2.54 20 pin Header | 2 |
| 12x12 PCB mount buttons | 3 |
| 3D printed enclosure | 1 |

<table><thead><tr><th>Tools / Equipment</th><th data-hidden></th></tr></thead><tbody><tr><td>Soldering Iron + Solder</td><td></td></tr><tr><td>Computer + Thonny IDE</td><td></td></tr><tr><td>Screw driver</td><td></td></tr></tr><tr><td>3D printer</td><td></td></tr></tbody></table>


## WS2812B 8mm

I purchased the LEDs online from Taobao and discovered that their pinout was different from the commonly available part. To fix this, I edited the footprint in EasyEDA to match the LEDs I received. For easier soldering, I also changed the pads to oval shapes and slightly staggered the pins.

<figure><img src="images/ws2812_through.png" alt=""><figcaption></figcaption></figure>

This is the edited part in EasyEDA. The Din and Dout pins were swapped.

<figure class="text-center">
  <img src="images/ws2812bedited.png" alt="">
  <figcaption></figcaption>
</figure>


## PCB ( JLCPCB )

### PCB Design

Once the prototype was working, I designed a custom PCB in EasyEDA.  
The schematic for the Pico Dice PCB is shown below:

<figure><img src="images/picodiceschematic.png" alt=""><figcaption></figcaption></figure>

Here is the PCB layout. As shown, the LEDs are arranged to mimic the face patterns of a standard die.

<figure><img src="images/picodicepcb.png" alt=""><figcaption></figcaption></figure>

The PCB was manufactured by JLCPCB, who offer high-quality boards at low cost, often with discounts and coupons available throughout the year. You can support me as a creator by signing up using this link:

[https://jlcpcb.com/?from=Nerd](https://jlcpcb.com/?from=NerdCave) that will support me as a creator to keep making content that is accessible and open source at no charge to you.

Ordering the PCB is very simple:

Download the Gerber file [here](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/raw/main/Pico%20Dice/Pico%20Dice%20Gerber.zip).

Click on Add Gerber file

<figure><img src="images/gerber.png" alt=""><figcaption></figcaption></figure>

Leave all the settings as default. You may change the PCB color here:

<figure><img src="images/pcb color.png" alt=""><figcaption></figcaption></figure>

Enter your shipping details, save to cart

<figure><img src="images/Screenshot 2023-08-17 090943.png" alt=""><figcaption></figcaption></figure>

Then after a few days depending on your location you will receive your PCB.

### Final Code

```python
# (code unchanged)
