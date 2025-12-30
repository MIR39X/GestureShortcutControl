<p align="center">
  <img src="https://img.icons8.com/fluency/200/hand-cursor.png" alt="LazyHands Logo"/>
</p>

<h1 align="center">✋ LazyHands</h1>

<p align="center">
  <strong>Touchless Hand Gesture Shortcut Control System</strong>
</p>

<p align="center">
  <em>Control your computer with just a wave of your hand</em>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#gestures">Gestures</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#author">Author</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/MediaPipe-latest-orange?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe"/>
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## 💡 Inspiration

While taking notes on my iPad, I had to constantly switch between **ChatGPT**, **YouTube**, and other tabs. Each time, I needed to touch the keyboard or mouse just to move forward or change a tab.

That repeated interruption led to a simple question:

> **Why not control these actions using hand gestures instead?**

This idea became **LazyHands** — a webcam-based system that allows users to control keyboard shortcuts using hand gestures without touching the keyboard or mouse.

<br/>

## 🎯 Project Overview

**LazyHands** is a real-time hand gesture control system that uses computer vision to detect hand movements through a standard webcam and translate them into keyboard shortcuts or mouse actions.

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   📷 Webcam   │ → │  🔍 OpenCV    │ → │ 🖐️ MediaPipe  │ → │ ⌨️ Execute   │
│    Input     │    │   Capture    │    │  Detection   │    │   Action    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<h2 id="features">✨ Features</h2>

<table>
  <tr>
    <td>🎥</td>
    <td><strong>Real-time Tracking</strong></td>
    <td>Smooth hand tracking using your webcam</td>
  </tr>
  <tr>
    <td>🖐️</td>
    <td><strong>Gesture Recognition</strong></td>
    <td>Finger-level gesture detection with high accuracy</td>
  </tr>
  <tr>
    <td>🖱️</td>
    <td><strong>Mouse Control</strong></td>
    <td>Control your cursor with pointing gestures</td>
  </tr>
  <tr>
    <td>⌨️</td>
    <td><strong>Keyboard Shortcuts</strong></td>
    <td>Execute any keyboard shortcut touchlessly</td>
  </tr>
  <tr>
    <td>⚙️</td>
    <td><strong>Customizable</strong></td>
    <td>Fully configurable gesture-to-action mapping</td>
  </tr>
  <tr>
    <td>🎯</td>
    <td><strong>Context-Aware</strong></td>
    <td>Different profiles for different applications</td>
  </tr>
  <tr>
    <td>🔔</td>
    <td><strong>System Tray</strong></td>
    <td>Runs quietly in the background</td>
  </tr>
  <tr>
    <td>🖥️</td>
    <td><strong>Visual Overlay</strong></td>
    <td>On-screen feedback for gesture recognition</td>
  </tr>
</table>

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<h2 id="gestures">🤟 Supported Gestures</h2>

<div align="center">

| Gesture | Icon | Description | Default Action |
|:-------:|:----:|:------------|:---------------|
| **Open Palm** | 🖐️ | All fingers extended | Customizable |
| **Fist** | ✊ | All fingers closed | Switch Tab |
| **Two Fingers** | ✌️ | Index + Middle up | Play/Pause |
| **Rock Sign** | 🤘 | Index + Pinky up | Toggle Mode |
| **Swipe Left** | 👈 | Hand movement left | Browser Back |
| **Swipe Right** | 👉 | Hand movement right | Browser Forward |
| **Swipe Up** | ☝️ | Hand movement up | Volume Up |
| **Swipe Down** | 👇 | Hand movement down | Volume Down |
| **Pointing** | 👆 | Index finger extended | Mouse Control |
| **Pinch** | 🤏 | Thumb + Index together | Mouse Click |

</div>

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<h2 id="installation">📦 Installation</h2>

### Prerequisites

- Python 3.8 or higher
- Webcam
- Windows OS

### Quick Start

```bash
# Clone the repository
git clone https://github.com/MIR39X/LazyHands.git

# Navigate to the project directory
cd LazyHands

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

```
opencv-python
mediapipe
pyautogui
pystray
pillow
```

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<h2 id="usage">🚀 Usage</h2>

### Starting the Application

1. Run `python main.py`
2. The settings window will appear
3. LazyHands icon will appear in your system tray
4. Point your webcam at your hand and start gesturing!

### Switching Modes

LazyHands has two operational modes:

| Mode | Description | Activation |
|------|-------------|------------|
| **🎯 GESTURE** | Execute keyboard shortcuts | Default mode |
| **🖱️ MOUSE** | Control cursor with hand | Show 🤘 Rock gesture |

> **Tip:** Use the **Rock gesture** (🤘) to toggle between modes!

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<h2 id="configuration">⚙️ Configuration</h2>

Customize gesture mappings in `config.json`:

```json
{
    "default": {
        "TWO_FINGERS": ["k"],
        "SWIPE_LEFT": ["alt", "left"],
        "SWIPE_RIGHT": ["alt", "right"],
        "SWIPE_UP": ["volumeup"],
        "SWIPE_DOWN": ["volumedown"]
    },
    "chrome": {
        "FIST": ["ctrl", "tab"]
    }
}
```

### Context-Aware Profiles

Create app-specific profiles that automatically activate:

| Profile | Application | Example Gestures |
|---------|-------------|------------------|
| `default` | All apps | Volume, Navigation |
| `chrome` | Google Chrome | Tab switching |
| `custom` | Your choice! | Anything you want |

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## 🏗️ Architecture

```
LazyHands/
├── 📄 main.py              # Application entry point
├── 📄 config.json          # Gesture mappings configuration
├── 📄 hand_landmarker.task # MediaPipe model file
└── 📁 src/
    ├── 📄 camera.py          # Webcam capture handler
    ├── 📄 detector.py        # Hand & gesture detection
    ├── 📄 config_manager.py  # Configuration management
    ├── 📄 input_controller.py# Keyboard shortcut executor
    ├── 📄 mouse_controller.py# Mouse movement & clicking
    ├── 📄 gui.py             # Settings GUI (Tkinter)
    ├── 📄 tray_icon.py       # System tray integration
    ├── 📄 overlay.py         # Visual feedback overlay
    └── 📄 window_manager.py  # Active window detection
```

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## 🛠️ Technology Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,opencv" alt="Tech Stack"/>
</p>

<div align="center">

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **OpenCV** | Camera capture & image processing |
| **MediaPipe** | Hand landmark detection |
| **PyAutoGUI** | Keyboard & mouse automation |
| **Tkinter** | Settings GUI |
| **pystray** | System tray integration |

</div>

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## 📌 Use Cases

<table>
  <tr>
    <td align="center">🎬</td>
    <td><strong>Media Control</strong> - Play, pause, adjust volume while watching videos</td>
  </tr>
  <tr>
    <td align="center">📊</td>
    <td><strong>Presentations</strong> - Navigate slides without touching your computer</td>
  </tr>
  <tr>
    <td align="center">🌐</td>
    <td><strong>Browser Navigation</strong> - Switch tabs, go back/forward</td>
  </tr>
  <tr>
    <td align="center">♿</td>
    <td><strong>Accessibility</strong> - Hands-free computer interaction</td>
  </tr>
  <tr>
    <td align="center">🍳</td>
    <td><strong>Cooking</strong> - Control recipes with messy hands</td>
  </tr>
  <tr>
    <td align="center">🏋️</td>
    <td><strong>Workouts</strong> - Change music or videos during exercise</td>
  </tr>
</table>

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## 🚧 Roadmap

- [x] Real-time hand tracking
- [x] Gesture recognition
- [x] Mouse control mode
- [x] System tray integration
- [x] Context-aware profiles
- [x] Visual overlay feedback
- [ ] Cross-platform support (macOS, Linux)
- [ ] Voice + gesture hybrid control
- [ ] Custom gesture training
- [ ] Multi-hand support

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## ⚠️ Known Limitations

| Issue | Workaround |
|-------|------------|
| Lighting affects accuracy | Ensure good lighting conditions |
| Webcam quality matters | Use HD webcam for best results |
| Windows only (for now) | Cross-platform coming soon |

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing`)
3. 💾 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing`)
5. 🎁 Open a Pull Request

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<h2 id="author">👨‍💻 Author</h2>

<p align="center">
  <img src="https://avatars.githubusercontent.com/MIR39X" width="100" style="border-radius: 50%;" alt="Author"/>
</p>

<h3 align="center">Arsalan Mir</h3>

<p align="center">
  <a href="https://github.com/MIR39X">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
  <a href="https://pk.linkedin.com/in/arsalan-mir-24a62328a">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
</p>

<br/>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider"/>
</p>

<p align="center">
  <strong>⭐ If you found this project helpful, please consider giving it a star!</strong>
</p>

<p align="center">
  Made with ❤️ and 🖐️ by <a href="https://github.com/MIR39X">Arsalan Mir</a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" alt="footer"/>
</p>