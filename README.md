# LazyHands
Touchless Hand Gesture Shortcut Control System

## Inspiration
While taking notes on my iPad, I had to constantly switch between ChatGPT, YouTube, and other tabs.  
Each time, I needed to touch the keyboard or mouse just to move forward or change a tab.

That repeated interruption led to a simple question:  
Why not control these actions using hand gestures instead?

This idea became LazyHands — a webcam-based system that allows users to control keyboard shortcuts using hand gestures without touching the keyboard or mouse.

---

## Project Overview
LazyHands is a real-time hand gesture control system that uses computer vision to detect hand movements through a standard webcam and translate them into keyboard shortcuts.

The system detects hand landmarks, determines finger states, recognizes gestures, and executes corresponding shortcuts. All interactions are touchless and require no external hardware.

---

## Features
- Real-time hand tracking using a webcam
- Finger-level gesture detection
- Touchless control of keyboard shortcuts
- Customizable gesture-to-shortcut mapping
- Lightweight and cost-effective solution
- Improves productivity and accessibility

---

## Supported Gestures
- Open Palm
- Fist
- Two Fingers
- Thumb Gesture
- Swipe gestures (extendable)

Each gesture can be mapped to a user-defined keyboard shortcut.

---

## System Architecture
Webcam Input
->
Frame Capture (OpenCV)
->
Hand Landmark Detection (MediaPipe)
->
Gesture Recognition
->
Shortcut Mapping
->
Keyboard Shortcut Execution


---

## Technology Stack
- Python
- OpenCV
- MediaPipe (Tasks API)
- PyAutoGUI
- JSON configuration
- Windows

---

## Use Cases
- Browser tab navigation
- Presentation and slide control
- Hands-free productivity workflows
- Accessibility support
- Touchless system interaction

---

## Advantages
- No external hardware required
- Touchless and hygienic interaction
- Customizable shortcut mapping
- Real-time performance
- Simple and intuitive design

---

## Limitations
- Performance depends on lighting conditions
- Webcam quality affects detection accuracy
- Limited gesture set in the current version

---

## Future Enhancements
- Graphical user interface for configuration
- Machine learning-based gesture recognition
- Multi-hand gesture support
- Voice and gesture hybrid control
- Cross-platform compatibility

---

## Conclusion
LazyHands demonstrates how computer vision can be applied to practical human–computer interaction problems.  
By replacing traditional input devices with intuitive hand gestures, the project provides an efficient and accessible approach to touchless control.

---

## Author
 - Developed by MEE BRUHH DUHH 
 - Yall can find me here!
 ([LinkedIn](https://pk.linkedin.com/in/arsalan-mir-24a62328a))
 ([GitHub](https://github.com/MIR39X))