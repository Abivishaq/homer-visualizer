from virtualhome.virtualhome.simulation.unity_simulator import comm_unity

comm = comm_unity.UnityCommunication()


# Start the first environment
comm.reset(0)
# Get an image of the first camera
success, image = comm.camera_image([0])

# Check that the image exists
print(image[0].shape)