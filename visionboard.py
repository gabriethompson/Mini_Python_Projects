from PIL import Image
import os
from math import ceil

def organize_images_in_columns(images, target_width, num_columns=7):
    """
    Organize images into a fixed number of columns while maintaining aspect ratios
    Returns positions and total height needed
    """
    if not images:
        return [], 0
        
    # Calculate column width
    column_width = target_width / num_columns
    positions = []
    
    # Distribute images into columns
    columns = [[] for _ in range(num_columns)]
    column_heights = [0] * num_columns
    
    # Place each image in the shortest column
    for img in images:
        # Find shortest column
        shortest_col = min(range(num_columns), key=lambda x: column_heights[x])
        
        # Calculate image dimensions maintaining aspect ratio
        aspect_ratio = img.width / img.height
        new_width = column_width
        new_height = new_width / aspect_ratio
        
        # Add image position
        x = shortest_col * column_width
        y = column_heights[shortest_col]
        positions.append((x, y, new_width, new_height))
        
        # Update column height
        column_heights[shortest_col] += new_height
    
    # Get total height needed
    total_height = max(column_heights)
    
    return positions, total_height

def create_vision_board(input_folder, output_path, target_width=2000, num_columns=7):
    """
    Create a vision board from multiple images in the input folder
    
    Args:
        input_folder: Path to folder containing input images
        output_path: Path where the final vision board will be saved
        target_width: Desired width of the final vision board
        num_columns: Number of columns in the layout
    """
    # Get list of image files
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("No images found in the input folder!")
        return
    
    # Load all images
    images = []
    for img_file in image_files:
        img_path = os.path.join(input_folder, img_file)
        img = Image.open(img_path)
        images.append(img)
    
    # Calculate optimal layout
    positions, total_height = organize_images_in_columns(images, target_width, num_columns)
    
    # Create new blank image for the vision board
    vision_board = Image.new('RGB', (int(target_width), int(total_height)), 'white')
    
    # Place images according to calculated positions
    for img, (x, y, width, height) in zip(images, positions):
        resized_img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
        vision_board.paste(resized_img, (int(x), int(y)))
    
    # Save the final vision board
    vision_board.save(output_path, quality=95)
    print(f"Vision board created successfully at: {output_path}")

# Example usage
if __name__ == "__main__":
    input_folder = "input_images"
    output_path = "vision_board.jpg"
    
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"Created input folder: {input_folder}")
        print("Please add your images to this folder and run the program again")
    else:
        create_vision_board(input_folder, output_path)
