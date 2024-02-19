# Example:
# python process_img.py ./content/img_raw ./static/img

from PIL import Image
import shutil
import os

def resize_or_copy_image(input_path, output_dir, sizes):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)

    srcset_entries = []
    copied_original = False

    with Image.open(input_path) as img:
        original_width, original_height = img.size
        if original_width < min(sizes):
            # Copy the original image if it's smaller than the smallest size
            output_path = os.path.join(output_dir, base_name)
            shutil.copy(input_path, output_path)
            srcset_entries.append(f"{base_name} {original_width}w")
            copied_original = True
        else:
            for width in sizes:
                if width > original_width:
                    continue  # Skip sizes larger than the original
                
                ratio = width / original_width
                new_height = int(original_height * ratio)
                resized_img = img.resize((width, new_height), Image.Resampling.LANCZOS)

                output_filename = f"{name}-{width}w{ext}"
                output_path = os.path.join(output_dir, output_filename)
                resized_img.save(output_path)
                srcset_entries.append(f"{output_filename} {width}w")

    return srcset_entries, copied_original

def generate_html_example(image_name, srcset_entries, output_dir, copied_original):
    if copied_original:
        # Use only the src attribute for the original image
        img_tag = f"""<img src="{srcset_entries[0].split()[0]}" alt="{image_name}">"""
    else:
        srcset_str = ", ".join(srcset_entries)
        img_tag = f"""<img src="{srcset_entries[0].split()[0]}" srcset="{srcset_str}" sizes="(max-width: 575.98px) 100vw, (max-width: 767.98px) 100vw, (max-width: 991.98px) 50vw, (max-width: 1199.98px) 50vw, 100vw" alt="{image_name}" class="clickable-image">"""
    
    example_filename = os.path.splitext(image_name)[0] + "_example.html"
    with open(os.path.join(output_dir, example_filename), "w") as f:
        f.write(img_tag)

def process_directory(input_dir, output_dir):
    sizes = [320, 480, 640, 768, 992, 1200, 1400, 1600, 1920]
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path) and input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            print(f"Processing {filename}...")
            srcset_entries, copied_original = resize_or_copy_image(input_path, output_dir, sizes)
            generate_html_example(filename, srcset_entries, output_dir, copied_original)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_dir, output_dir = sys.argv[1], sys.argv[2]
    process_directory(input_dir, output_dir)
