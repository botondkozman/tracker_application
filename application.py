import API.python.tracker_sample as tracker_sample

tracker = tracker_sample.TrackerClient()

def initialize_tracker():
    tracker.initialize()

def start_tracker():
    try:
        tracker.start()
        print("Tracking started")
    except Exception as e:
        print(f"Failed to start tracking: {e}")

def tracking_cursor_position():
    tracking_data = tracker.get_tracking_data()
    gaze_x = tracking_data.get("gaze_x")
    gaze_y = tracking_data.get("gaze_y")
    print(f"Gaze coordinates: X={gaze_x}, Y={gaze_y}")

def stop_tracker():
    tracker.stop()
    print("Tracking stopped")

if __name__ == "__main__":
    initialize_tracker()
    start_tracker()
    if (tracker.is_running()):
        tracking_cursor_position()
        stop_tracker()