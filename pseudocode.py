"""
Pseudocode for the software for the Raspberry Pi.
"""

# Set initial values
    # Integration with camera
    # Initial Motor Controller Values
    # Battery Monitoring? (Is it wired?)

# operation loop
    # Receive inputs from vision
        # Get images/video from camera
        # Run through object tracking software (depends on what we use)
            # Pan-tilt tracking Github Link sent in the group chat
    # Decide what to do
        # From placement and depth in image, change motor behavior
        # Is there a brake system?