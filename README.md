# PiCarX Challenge2 mit Sound

Dieses Projekt fährt autonom auf einer hellen Fahrbahn und vermeidet dunkle Ränder.  
Während der Fahrt spielt das Auto Musik ab und gibt Sprachkommentare.

## Anforderungen

- Raspberry Pi OS
- PiCar-X von Sunfounder
- Python 3
- Lautsprecher (Klinke oder USB)
- Kamera aktiviert (`picamera2`)

## Installation

```bash
sudo apt update
sudo apt install python3-picamera2 mpg123 espeak -y
