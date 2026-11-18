# Smart Interactive Whiteboard

A computer vision-based system that transforms a traditional whiteboard into an interactive teaching surface.

## Overview

The **Smart Interactive Whiteboard** project aims to develop an interactive teaching environment using a camera, a projector, and a two-button presentation remote.

A fixed camera captures the whiteboard and is calibrated to establish a reference coordinate system. The application detects the user's hand or a visible pointer, tracks its position, and maps image coordinates to the corresponding board coordinates.

A projector displays the graphical interface directly onto the whiteboard, allowing users to interact with projected content through pointer movements and remote-control button presses.

The presentation remote provides two interactions:

- **Previous:** Triggers a right-click at the current pointer position.
- **Next:** Triggers a left-click at the current pointer position.

## Features

The application is designed to provide the following functionalities:

- **Camera Calibration:** Detect and calibrate the four corners of the whiteboard.
- **Pointer Tracking:** Detect and track the user's hand or a visible pointer.
- **Coordinate Mapping:** Transform camera image coordinates into whiteboard coordinates.
- **Remote Control:** Detect Previous and Next button events and map them to mouse clicks.
- **Interactive Menus:** Navigate through a main menu and submenus.
- **Free Drawing:** Draw on the whiteboard with selectable colors and pen thicknesses.
- **Image Display and Zoom:** Load images, zoom in and out, and restore the original view.
- **Teaching Content:** Navigate through structured educational content.
- **Basic Usability:** Display a visible pointer, reset the application, and return to the main menu.

## Technologies

- **Python**
- **NumPy**
- **OpenCV**
- **Computer Vision**
- **Image Processing**
- **Geometric Transformations**

## Project Structure

```text
smart-interactive-whiteboard/
├── docs/
├── assets/
├── src/
│   ├── camera/
│   ├── detection/
│   ├── geometry/
│   ├── remote/
│   ├── interface/
│   └── utils/
├── tests/
├── results/
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/alaasek/smart-interactive-whiteboard.git
cd smart-interactive-whiteboard
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Once the installation is complete, launch the application using:

```bash
python src/main.py
```

The application will guide the user through camera initialization, calibration, pointer tracking, and interactive whiteboard features.

## Hardware Requirements

- A fixed camera positioned in front of the whiteboard.
- A projector to display the application interface.
- A two-button presentation remote (Previous / Next).
- A computer capable of running Python and OpenCV.

## Project Context

This project is developed as part of the **Three-Week Computer Vision Project (2026–2027)** at the Faculty of Computer Science, USTHB.

**Instructor:** Dr. ABADA Lyes

## Team

*Add team members and their contributions here.*

## Project Status

Under development.

---

*USTHB — Faculty of Computer Science | 2026–2027*
