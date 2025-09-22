import sys
import time
import cv2
from mogu_core import MoguCore


USERNAME = ""  # Username
PASSWORD = ""  # Password
VIDEO_PATH = ""  # Video file path


def main():
    # Create a MoguCore instance
    mogu = MoguCore()
    print(f"Created MoguCore instance: {mogu}")

    # Initialize the system
    print("\n1. Initializing system...")
    if mogu.init():
        print("✓ System initialization successful")
    else:
        print("✗ System initialization failed")
        return

    # Log in to the system
    print("\n2. Logging in...")
    mogu.set_visualization_enabled()
    if mogu.login(USERNAME, PASSWORD):
        print("✓ Login successful")
    else:
        print("✗ Login failed")
        return

    # Check connection status
    print(f"\n3. Connection status check:")
    print(f"   WebSocket status: {mogu.get_status()}")

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"✗ Unable to open video file: {VIDEO_PATH}")
        return
        
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30  # Default to 30fps if retrieval fails
    frame_interval = 1.0 / fps
    print(f"Video FPS: {fps}, Delay per frame: {frame_interval:.4f} seconds")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video reading ended or error occurred")
            break
            
        # Optional: Crop the frame (example commented out)
        # frame = frame[280:480, 480:880]
        
        frame_resized = cv2.resize(frame, (400, 200))
        # Push frame to C++
        success = mogu.push_image(frame_resized)
        if not success:
            print(f"✗ Failed to push frame {frame_count}")
        else:
            print(f"✓ Pushed frame {frame_count}")
            
        frame_count += 1
        time.sleep(frame_interval)  # Maintain approximate FPS
        print(f"   WebSocket status: {mogu.get_status()}")
        print(f"   actionlist: {mogu.get_last_action_index_list()}")
        
    cap.release()


if __name__ == "__main__":
    main()
