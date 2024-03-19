import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Concatenate
from pose.images_to_poses import image_to_poses
from pose.transform import change_coord
import pickle


# Assume poses_array is your array of poses from the video
# Adjust input_dim based on your specific pose representation (36 in this case)

input_dim = 36

# Generate pairs of adjacent poses with labels
def generate_pairs(poses_array, range_size=100):
    pairs = []
    labels = []
    for i in range(len(poses_array) - 1):
        pair = [poses_array[i], poses_array[i+1]]
        pairs.append(pair)
        # Label 1 indicates similar poses, 0 indicates different poses
        labels.append(1)  # Similar poses
    for i in range(len(poses_array)):
        # Generate a random index outside the specified range
        rand_index = get_random_index(i, len(poses_array), range_size)
        different_pose = poses_array[rand_index]
        pairs.append([poses_array[i], different_pose])
        labels.append(0)  # Different poses
    return np.array(pairs), np.array(labels)

# Function to get a random index outside a specified range
def get_random_index(current_index, array_length, range_size):
    lower_bound = max(0, current_index - range_size)
    upper_bound = min(array_length - 1, current_index + range_size)
    indices_outside_range = np.concatenate([np.arange(0, lower_bound), np.arange(upper_bound + 1, array_length)])
    return np.random.choice(indices_outside_range)

try:
    with open("poses.bin",'rb') as f:
        poses_array = pickle.load(f)
        print("\nretrieved poses")
except:
    print("\ngetting poses from images\n")
    poses_array = image_to_poses(['data/'+str(i)+'.jpg' for i in range(0, 916)])
    with open("poses.bin",'wb') as f:
        pickle.dump(poses_array,f)


poses_array = [change_coord(pose).flatten() for pose in poses_array]

# Create pairs and labels for training
X_train, y_train = generate_pairs(poses_array)

# Shared layers
shared_layer1 = Dense(64, activation='relu')
shared_layer2 = Dense(32, activation='relu')

# Define input layers
input_pose1 = Input(shape=(input_dim,), name='pose1_input')
input_pose2 = Input(shape=(input_dim,), name='pose2_input')

# Apply shared layers to both input poses
output_pose1 = shared_layer2(shared_layer1(input_pose1))
output_pose2 = shared_layer2(shared_layer1(input_pose2))

# Concatenate the outputs of both poses
merged_output = Concatenate()([output_pose1, output_pose2])

# Additional layers if needed
merged_output = Dense(32, activation='relu')(merged_output)

# Final binary classification layer
output_layer = Dense(1, activation='sigmoid', name='output')(merged_output)

# Create the Siamese model
siamese_model = Model(inputs=[input_pose1, input_pose2], outputs=output_layer)

# Compile the model
siamese_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
siamese_model.fit([X_train[:, 0, :], X_train[:, 1, :]], y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the same array
X_test, y_test = generate_pairs(poses_array)
accuracy = siamese_model.evaluate([X_test[:, 0, :], X_test[:, 1, :]], y_test)
print(f"Accuracy on test set: {accuracy[1]}")

# Use the trained model for predictions
new_pose_pair_index = get_random_index(0, len(poses_array), 100)
pose1 = poses_array[new_pose_pair_index]
pose2 = poses_array[new_pose_pair_index + 1]


new_pose_pair = np.array([pose1, pose2])

# Reshape inputs for prediction
prediction = siamese_model.predict([new_pose_pair[0].reshape(1, -1), new_pose_pair[1].reshape(1, -1)])

# Print the prediction result
print("Prediction for new pose pair:")
print(prediction)
print(new_pose_pair_index)
