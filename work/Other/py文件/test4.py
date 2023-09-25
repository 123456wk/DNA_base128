from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np




def ssim1 (img1 ,img2):
    red_channel, green_channel, blue_channel = img1.split()
    img_np = np.array(red_channel)
    img_np1 = np.array(green_channel)
    img_np2 = np.array(blue_channel)


    red_channel2, green_channel2, blue_channel2 = img2.split()
    img_np_2 = np.array(red_channel2)
    img_np1_2 = np.array(green_channel2)
    img_np2_2 = np.array(blue_channel2)


    ssim_score1 = ssim(img_np, img_np_2, multichannel=True)
    ssim_score2 = ssim(img_np1, img_np1_2, multichannel=True)
    ssim_score3 = ssim(img_np2, img_np2_2, multichannel=True)
    ssim_score = (ssim_score1 + ssim_score2 + ssim_score3)/3
    return ssim_score

image1 = Image.open("4.1.01.tiff")
image2 = Image.open("4.1.01.tiff")

"""
red_channel, green_channel, blue_channel = image1.split()
img_np = np.array(red_channel)
img_np1 = np.array(green_channel)
img_np2 = np.array(blue_channel)


red_channel2, green_channel2, blue_channel2 = image2.split()
img_np_2 = np.array(red_channel2)
img_np1_2 = np.array(green_channel2)
img_np2_2 = np.array(blue_channel2)
"""
# 计算两张彩色图像之间的 SSI
# ssim_score = ssim(img_np, img_np_2, multichannel=True)
ssim_score = ssim1(image1, image2)
print("SSIM Score:", ssim_score)
