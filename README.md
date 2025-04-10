# RF Frequency Capture & Simulation Toolkit

This toolkit includes two Python-based utilities for working with radio frequency (RF) data: one for real-time signal capture using RTL-SDR hardware, and another for simulating signal propagation and device-level RF characteristics. Both tools use 3D visualization to help researchers, hardware hackers, and RF engineers better understand signal environments.

---

## 📁 Overview of Scripts

### 🔊 Frequency Capture (`Frequency_Capture.py`)

**Purpose:**  
Captures real-time RF signals using an RTL-SDR dongle and visualizes the power spectral density in a 3D interactive grid.

**Key Features:**
- Interfaces with RTL-SDR to capture I/Q samples.
- Applies FFT and converts to power density (dB scale).
- Updates a 3D `pyvista` grid in real-time to visualize spectrum intensity.
- Saves the 3D visualization to an OBJ file (`rf_capture.obj`).

**Requirements:**
- RTL-SDR USB dongle
- Python libraries:
  - `numpy`
  - `matplotlib`
  - `pyrtlsdr`
  - `pyvista`

**How to Use:**
```bash
python Frequency_Capture.py
```


### 📘 Overview

The `frequency_simulation.py` script models a hypothetical embedded or IoT device emitting RF signals across a 3D space. It factors in hardware characteristics like processor clock speed, power consumption, and utilization to simulate realistic transmission behavior.

Using NumPy and PyVista, the simulation:

- Builds a volumetric 3D mesh of signal propagation.
- Calculates signal strength attenuation based on distance from the source.
- Adjusts signal behavior dynamically based on device-level resource usage.
- Visualizes the results in both 3D point cloud and 2D depth image formats.

The output helps conceptualize how hardware performance and physical environment affect wireless signal distribution, making it useful for threat modeling, testing, and RF design analysis.

# 📡 Frequency Simulation Toolkit

This toolkit provides a simulation of signal strength propagation in a 3D space and models basic processor characteristics under varying utilization and power load. It is ideal for testing, teaching, or visualizing RF behavior in synthetic environments.

---

## 📄 Script: `frequency_simulation.py`

### 🎯 Purpose

Simulates signal strength propagation in a 3D environment and models processor characteristics under varying power and utilization loads.

---

### ✨ Key Features

- Emulates a device transmitting across a defined 3D spatial grid.
- Simulates signal attenuation based on distance and processor utilization.
- Visualizes signal strength as a 3D point cloud using `pyvista`.
- Generates a grayscale depth image to represent the RF environment's topology.
- Saves the simulation results as a 3D object file: `rf_sim.obj`.

---

## 📦 Requirements

Python libraries:

- `numpy`
- `matplotlib`
- `pyvista`

---

## ▶️ How to Use

Run the simulation script:

```bash
python frequency_simulation.py
