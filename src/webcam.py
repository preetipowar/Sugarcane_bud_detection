"""
Real-Time Bud Detection with Webcam + Arduino Servo Control
Optimized for VS Code/Local Python Environment
NO BOUNDING BOXES SHOWN
"""

import cv2
from ultralytics import YOLO
import serial
import time

# Configuration
MODEL_PATH = r'C:\Users\HP\Downloads\mest_bud_detection (1).pt'
CONFIDENCE_THRESHOLD = 0.5
WINDOW_NAME = 'Bud Detection - Press Q to Quit'

# Arduino Setup
arduino_connected = False
try:
    print("🔌 Attempting to connect to Arduino on COM4...")
    arduino = serial.Serial(
        port='COM4',
        baudrate=9600,
        timeout=1,
        write_timeout=1
    )
    time.sleep(3)
    arduino.flushInput()
    arduino.flushOutput()
    print("✓ Connected to Arduino on COM4")
    arduino_connected = True
except serial.SerialException as e:
    print(f"⚠️ Serial Exception: {e}")
    print("  → Check: Arduino IDE Serial Monitor is CLOSED")
    print("  → Check: COM port is correct in Device Manager")
except Exception as e:
    print(f"⚠️ Connection Error: {e}")
    print("  → Proceeding without Arduino hardware")

def main():
    print("=" * 60)
    print("🌿 Real-Time Bud Detection System")
    print("=" * 60)
    
    # Load the trained model
    print(f"📦 Loading model from: {MODEL_PATH}")
    try:
        import warnings
        warnings.filterwarnings('ignore')
        
        model = YOLO(MODEL_PATH)
        print("✓ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Initialize webcam
    print("\n📸 Initializing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not access webcam!")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✓ Webcam initialized successfully!")
    print("\n🚀 Starting real-time detection...")
    print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")
    print("=" * 60)
    print("Controls:")
    print("  - Press 'Q' to quit")
    print("  - Press 'S' to save current frame")
    print("=" * 60)
    
    frame_count = 0
    fps_start_time = time.time()
    fps = 0
    last_detection_time = 0
    detection_cooldown = 2.0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Error: Failed to grab frame")
                break
            
            # Run YOLOv8 detection (but don't show boxes)
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            
            # Use original frame instead of annotated frame
            display_frame = frame.copy()
            
            # Calculate FPS
            frame_count += 1
            if frame_count % 30 == 0:
                fps_end_time = time.time()
                fps = 30 / (fps_end_time - fps_start_time)
                fps_start_time = fps_end_time
            
            # Add FPS counter
            cv2.putText(
                display_frame,
                f'FPS: {fps:.1f}',
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Get detection count
            num_detections = len(results[0].boxes)
            cv2.putText(
                display_frame,
                f'Detections: {num_detections}',
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Arduino Control: Send signal when bud is detected
            current_time = time.time()
            if num_detections > 0 and arduino_connected:
                if current_time - last_detection_time > detection_cooldown:
                    arduino.write(b'1')
                    last_detection_time = current_time
                    print(f"🎯 Bud detected! Servo activated (Pin 9)")
                    
                    # Visual indicator without boxes
                    cv2.putText(
                        display_frame,
                        'SERVO TRIGGERED!',
                        (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )
            
            # Display clean frame (no boxes)
            cv2.imshow(WINDOW_NAME, display_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == ord('Q'):
                print("\n✓ Quitting...")
                break
            elif key == ord('s') or key == ord('S'):
                filename = f'detection_{int(time.time())}.jpg'
                cv2.imwrite(filename, display_frame)
                print(f"📸 Saved frame as: {filename}")
            
            # Print progress every 100 frames
            if frame_count % 100 == 0:
                print(f"✓ Processed {frame_count} frames | FPS: {fps:.1f} | Detections: {num_detections}")
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    
    except Exception as e:
        print(f"\n❌ Error during detection: {e}")
    
    finally:
        print("\n🧹 Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
        if arduino_connected:
            arduino.close()
            print("✓ Arduino connection closed")
        print(f"✓ Total frames processed: {frame_count}")
        print("✓ Done!")

if __name__ == "__main__":
    main()
