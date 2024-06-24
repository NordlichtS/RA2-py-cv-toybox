#记得把脚本和渲染输出的PNG堆放在同一文件夹
import os
import numpy as np
from PIL import Image

def make_gif_with_layers(output_filename, special_color=(0, 255, 0), fps=20):
# special color is gif background! 
# # special color 是 GIF 文件背景色！

    input_folder = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(input_folder)
    foregrounds = [f for f in files if f.endswith('.png') and f[0].isdigit()]
    backgrounds = [f for f in files if f.endswith('.png') and f[0].isalpha()]
    # 戴子玲的自动工具把阴影帧都以字母开头命名，可以通过这个区分

    foregrounds.sort()
    backgrounds.sort()

    combined_images = []

    # Iterate through the shortest list length to prevent index errors
    num_frames = min(len(foregrounds), len(backgrounds))
    for i in range(num_frames):
        fg_path = os.path.join(input_folder, foregrounds[i])
        bg_path = os.path.join(input_folder, backgrounds[i])

        fg_img = Image.open(fg_path).convert('RGBA')
        bg_img = Image.open(bg_path).convert('RGBA')

        # Convert images to NumPy arrays for faster processing
        fg_array = np.array(fg_img)
        bg_array = np.array(bg_img)

        # Reduce alpha of the background image
        bg_array[:, :, 3] = (bg_array[:, :, 3] * 0.5).astype(np.uint8)  
        # this 0.5 is actually the density of shadow
        #这个0.5其实是阴影浓度

        # Compute the combined alpha as per the new specification
        alpha_fg = fg_array[:, :, 3] / 255.0
        alpha_bg = bg_array[:, :, 3] / 255.0
        combined_alpha = alpha_bg + alpha_fg - alpha_bg * alpha_fg

        # Compute the composite image using alpha compositing
        composite_array = np.zeros_like(fg_array)
        for channel in range(3):  # For R, G, B channels
            composite_array[:, :, channel] = (fg_array[:, :, channel] * alpha_fg +
                                              bg_array[:, :, channel] * alpha_bg * (1 - alpha_fg)) / combined_alpha
        composite_array[:, :, 3] = (combined_alpha * 255).astype(np.uint8)

        # Lerp with special color using combined_alpha
        special_color_array = np.array(special_color)
        for channel in range(3):  # Only need RGB channels
            composite_array[:, :, channel] = np.clip((composite_array[:, :, channel] * combined_alpha +
                                                      special_color_array[channel] * (1 - combined_alpha)), 0, 255).astype(np.uint8)

        # Convert back to Image and remove alpha for GIF
        combined_image = Image.fromarray(composite_array[:, :, :3])
        combined_images.append(combined_image)

    # Save the images as a GIF
    output_path = os.path.join(input_folder, output_filename)
    if combined_images:
        combined_images[0].save(
            output_path,
            save_all=True,
            append_images=combined_images[1:],
            duration=1000 / fps,
            loop=0
        )
        print(f"GIF created successfully: {output_path}")
    else:
        print("No images to combine.")

# Usage
make_gif_with_layers('output.gif', fps=20)
