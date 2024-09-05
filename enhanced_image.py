from PIL import Image

def enhance_image(file_path):
    # Open the image file
    img = Image.open(file_path)

    # Define new width and height
    new_width = 3897
    new_height = 4896
    
    # Resize the image
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Define DPI
    dpi = (300, 300)  
    
    # Save the image with the specified DPI
    filename = 'enhanced_image.png'
    img.save(filename, dpi=dpi)
    
    return filename

# Example usage
file_path = "/home/jay/Downloads/download.png" 
enhanced_img = enhance_image(file_path)


