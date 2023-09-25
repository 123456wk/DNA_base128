from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct
from skimage.metrics import structural_similarity as ssim
from Other.image_encode import calculate_histogram_similarity, cosine_similarity, psnr

def image_to_bit(img1):
    img = Image.open(img1)
    red_channel, green_channel, blue_channel = img.split()
    # img.show()
    # 转换为Numpy数组
    img_np = np.array(red_channel)
    img_np1 = np.array(green_channel)
    img_np2 = np.array(blue_channel)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    quantized_coef_1d1 = img_np1.flatten()
    quantized_coef_1d2 = img_np2.flatten()

    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])
    compressed_data1 = ''.join([format(int(x), '08b') for x in quantized_coef_1d1])
    compressed_data2 = ''.join([format(int(x), '08b') for x in quantized_coef_1d2])

    return  compressed_data , compressed_data1 ,compressed_data2

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
    ssim_score = (ssim_score1 + ssim_score2 + ssim_score3) / 3
    return ssim_score

def bit_to_image(img, compressed_data , compressed_data1 ,compressed_data2):
    img = Image.open(img)
    red_channel, green_channel, blue_channel = img.split()
    img_np = np.array(red_channel)
    img_np1 = np.array(green_channel)
    img_np2 = np.array(blue_channel)

    quantized_coef_1d = np.array([int(compressed_data[i:i + 8], 2) for i in range(0, len(compressed_data), 8)])
    quantized_coef_1d1 = np.array([int(compressed_data1[i:i + 8], 2) for i in range(0, len(compressed_data1), 8)])
    quantized_coef_1d2 = np.array([int(compressed_data2[i:i + 8], 2) for i in range(0, len(compressed_data2), 8)])
    # 将量化系数重构为二维数组
    quantized_coef = np.reshape(quantized_coef_1d, img_np.shape)
    quantized_coef = quantized_coef.astype(np.uint8)
    print(quantized_coef, "quantized_coef")

    quantized_coef1 = np.reshape(quantized_coef_1d1, img_np.shape)
    quantized_coef1 = quantized_coef1.astype(np.uint8)

    quantized_coef2 = np.reshape(quantized_coef_1d2, img_np.shape)
    quantized_coef2 = quantized_coef2.astype(np.uint8)

    # 将numpy 转为通道数据
    reconstructed_red_channel = Image.fromarray(quantized_coef)
    reconstructed_red_channel1 = Image.fromarray(quantized_coef1)
    reconstructed_red_channel2 = Image.fromarray(quantized_coef2)

    # 数据合并
    reconstructed_image = Image.merge("RGB", (reconstructed_red_channel, reconstructed_red_channel1, reconstructed_red_channel2))
    # reconstructed_image = Image.merge("RGB", (red_channel, green_channel, blue_channel))

    reconstructed_image.show()
    reconstructed_image.save("base128_colord_0.005.jpg")
    # 显示图像    方式2
    img1 = np.array(Image.open("4.1.01.tiff").convert("L"))
    img2 = np.array(reconstructed_image.convert("L"))

    # 计算两张彩色图像之间的 SSIM
    mse = np.mean((img1 - img2) ** 2)
    print(mse, "mse")
    ssim_score = ssim1(Image.open("4.1.01.tiff"), reconstructed_image)
    print("SSIM Score:", ssim_score)
    print(calculate_histogram_similarity(img1, img2, bins=256), "直方图")
    print('余弦相似度:', cosine_similarity(img1, img2))
    # print('哈希相似度:', calculate_hash_similarity(img1, img2))
    print(psnr(img1, img2), "psnr")


compressed_data , compressed_data1 ,compressed_data2 = image_to_bit("4.1.01.tiff")
bit_to_image("4.1.01.tiff" ,compressed_data , compressed_data1 ,compressed_data2  )




