from PIL import Image
import os
from pathlib import Path

def _resize_and_copy_image(image_path, output_dir, sizes):
    """
    Resize the image based on the given sizes if the resized image does not already exist.
    Copy the image directly if it's smaller than the smallest size.
    Returns the srcset string and a flag indicating if the original image was copied.
    """
    min_size = min(sizes)
    image = Image.open(image_path)
    srcset = []
    output_path = output_dir / image_path.name

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Handle images smaller than the smallest target size
    if image.width <= min_size:
        if not output_path.exists():
            image.save(output_path)
        return f"{output_path.name} {image.width}w", True

    for size in sizes:
        resized_filename = f"{image_path.stem}-{size}w{image_path.suffix}"
        resized_path = output_dir / resized_filename
        
        # Check if resized image already exists
        if not resized_path.exists():
            if size >= image.width:
                # If the current size is larger than the original, no need to resize; copy the original instead
                if not output_path.exists():
                    image.save(output_path)
                srcset.append(f"{image_path.name} {image.width}w")
                break
            else:
                # Resize and save the image
                aspect_ratio = image.height / image.width
                new_height = round(size * aspect_ratio)
                resized_img = image.resize((size, new_height), Image.Resampling.LANCZOS)
                resized_img.save(resized_path)
                srcset.append(f"{resized_filename} {size}w")
        else:
            # If the resized image exists, just add its info to the srcset
            srcset.append(f"{resized_filename} {size}w")

    return ", ".join(srcset), False


def _generate_html(srcset, alt_text, classes, relative_path_to_images):
    """
    Generates HTML for the <img> element with srcset and sizes attributes.
    """
    sizes_attr = "(min-width: 992px) 50vw, 100vw" # Below breakpoint lg (992px), use 100% of the viewport width
    srcset_with_path = ", ".join([str(Path(relative_path_to_images) / src) for src in srcset.split(", ")])
    return f'<img srcset="{srcset_with_path}" sizes="{sizes_attr}" alt="{alt_text}" class="{classes}">'

def process_images_and_generate_html(data, output_dir, sizes, html_output):
    """
    Recursively process the dictionary to resize images and generate HTML markup.
    """
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == 'img' and isinstance(value, dict):
                img_path = Path(value['path'])
                srcset, copied_directly = _resize_and_copy_image(img_path, Path(output_dir), sizes)
                relative_path = os.path.relpath(output_dir, html_output.parent)
                img_html = _generate_html(srcset, value.get('alt', ''), value.get('classes', ''), relative_path)
                data[key + '_html'] = img_html if not copied_directly else f'<img src="{relative_path}/{img_path.name}" alt="{value.get("alt", "")}" class="{value.get("classes", "")}">'
            else:
                process_images_and_generate_html(value, output_dir, sizes, html_output)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            process_images_and_generate_html(item, output_dir, sizes, html_output)
