import bpy
import csv

# Specify the output CSV file path
output_csv_path = "C:/Your_Path_Here/Your_File_Name.csv"

# Set Target Reference Scale
target_width = 1920
target_height = 1080

# Get the active scene
scene = bpy.context.scene

# Get the active movie clip (assuming there's one in the scene)
clip = bpy.data.movieclips[0]

# Ensure there's a tracking object in the clip
tracking_object = clip.tracking.objects.active

# Ensure there are tracks in the tracking object
if not tracking_object.tracks:
    print("No tracks found in the active tracking object.")
else:
    # Get the active track (assuming you want to export positions for all tracks)
    tracks = tracking_object.tracks

    # Collect data for each frame
    data = []
    for frame in range(scene.frame_start, scene.frame_end + 1):
        bpy.context.scene.frame_set(frame)
        frame_data = {"frame": frame}
        for track in tracks:
            marker = track.markers.find_frame(frame)
            if marker:
                # Remap coordinates to 1920x1080
                x, y = marker.co[0] * target_width, marker.co[1] * target_height
                frame_data[track.name] = (x, y)
            else:
                frame_data[track.name] = (None, None)
        data.append(frame_data)

    # Write data to CSV
    with open(output_csv_path, mode='w', newline='') as csv_file:
        fieldnames = ["frame"] + [track.name for track in tracks]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for frame_data in data:
            row = {"frame": frame_data["frame"]}
            for track in tracks:
                row[track.name] = frame_data[track.name]
            writer.writerow(row)

    print(f"Motion tracker's position data exported to {output_csv_path}")
