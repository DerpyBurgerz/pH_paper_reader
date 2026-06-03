from io_utils import load_image, save_image
from processor import process_image

def run():
    input_path = "pH_colors.png"
    output_path = "output_processed.png"

    # Load image
    image = load_image(input_path)
    if image is None:
        return

    processed_image = process_image(image)

    save_image(processed_image, output_path)

if __name__ == "__main__":
    run()