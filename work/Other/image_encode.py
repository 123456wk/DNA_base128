from locale import normalize

import imagehash
from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct
from skimage.metrics import structural_similarity as ssim
import cv2


def psnr(img1, img2):
    mse = np.mean((img1-img2)**2)
    if mse == 0:
        return float('inf')
    else:
        return 20*np.log10(255/np.sqrt(mse))


def MSE(img1,img2):
    mse = np.mean( (img1 - img2) ** 2 )
    return mse

# 直方图相似度

def hist_similarity(img1, img2, hist_size=256):
    imghistb1 = cv2.calcHist([img1], [0], None, [hist_size], [0, 256])
    imghistg1 = cv2.calcHist([img1], [1], None, [hist_size], [0, 256])
    imghistr1 = cv2.calcHist([img1], [2], None, [hist_size], [0, 256])

    imghistb2 = cv2.calcHist([img2], [0], None, [hist_size], [0, 256])
    imghistg2 = cv2.calcHist([img2], [1], None, [hist_size], [0, 256])
    imghistr2 = cv2.calcHist([img2], [2], None, [hist_size], [0, 256])

    distanceb = cv2.compareHist(normalize(imghistb1), normalize(imghistb2), cv2.HISTCMP_CORREL)
    distanceg = cv2.compareHist(normalize(imghistg1), normalize(imghistg2), cv2.HISTCMP_CORREL)
    distancer = cv2.compareHist(normalize(imghistr1), normalize(imghistr2), cv2.HISTCMP_CORREL)
    meandistance = np.mean([distanceb, distanceg, distancer])
    return meandistance

#   直方图相似度
def histogram_intersection(hist1, hist2):
    minima = np.minimum(hist1, hist2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist2))
    return intersection

def normalize_histogram(hist):
    return hist / np.sum(hist)

def calculate_histogram_similarity(img1, img2, bins=256):
    # 计算图像1的直方图
    hist1 = cv2.calcHist([img1], [0], None, [bins], [0, 256])
    hist1 = normalize_histogram(hist1)

    # 计算图像2的直方图
    hist2 = cv2.calcHist([img2], [0], None, [bins], [0, 256])
    hist2 = normalize_histogram(hist2)

    # 计算直方图相似度
    similarity = histogram_intersection(hist1, hist2)

    return similarity

# 余弦相似度
def cosine_similarity(img1, img2):
    # 将图像转换为一维向量
    img1_vector = img1.flatten()
    img2_vector = img2.flatten()

    # 计算余弦相似度
    similarity = np.dot(img1_vector, img2_vector) / (np.linalg.norm(img1_vector) * np.linalg.norm(img2_vector))

    return similarity

def calculate_cosine_similarity(img1, img2):
    # 将图像转换为灰度图像
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # 计算余弦相似度
    similarity = cosine_similarity(img1, img2)
    return similarity

# 哈希相似度

def calculate_hash_similarity(img1, img2):
    # 将图像转换为灰度图像
#    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算两张图像的哈希值
    hash1 = imagehash.average_hash(Image.fromarray(img1))
    hash2 = imagehash.average_hash(Image.fromarray(img2))
    # 计算哈希相似度
    similarity = 1 - (hash1 - hash2) / len(hash1.hash) ** 2
    return similarity
#均值哈希算法
def aHash(image):
    #缩放为8*8
    image=cv2.resize(image,(8,8),interpolation=cv2.INTER_CUBIC)
    #转换为灰度图
#    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    avreage = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
#计算汉明距离
def Hamming_distance(hash1,hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
if __name__ == '__main__':
    # 读取图像
    img = Image.open('lena.bmp').convert('L')
    # img.show()
    # 转换为Numpy数组
    img_np = np.array(img)
    # 转换为一维数组
    quantized_coef_1d = img_np.flatten()
    # 一维数组转换为二进制数据
    compressed_data = ''.join([format(int(x), '08b') for x in quantized_coef_1d])
    # 将二进制数据转为一维数组
    quantized_coef_1d = np.array([int(compressed_data[i:i+8], 2) for i in range(0, len(compressed_data), 8)])
    # 将量化系数重构为二维数组
    quantized_coef = np.reshape(quantized_coef_1d, img_np.shape)
    quantized_coef = quantized_coef.astype(np.uint8)

    # 显示图像
    cv2.imshow('Reconstructed Image', quantized_coef)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # 将图像写出
    # cv2.imwrite('D:/image/CV2_256.jpg', img_idct)
    # 对比图像的ssim
    img1 = np.array(Image.open('lena.bmp'))
    img2 = np.array(quantized_coef)
    #    img2 = np.array(Image.open('lena.bmp'))
    print(ssim(img1, img2, multichannel=True),"ssim")
    print(calculate_histogram_similarity(img1, img2, bins=256),"直方图")
    print('余弦相似度:', cosine_similarity(img1, img2))
    # print('哈希相似度:', calculate_hash_similarity(img1, img2))
    print(psnr(img1, img2))
    """
    1. 直方图相似度（Histogram Similarity）：直方图相似度用于比较两个直方图之间的相似程度。直方图是对数据分布的离散近似，通过计算两个直方图之间的差异或相似性，可以判断两个数据分布的相似程度。直方图相似度常用于图像处理、计算机视觉和模式识别等领域。较高的直方图相似度表示两个直方图之间的数据分布更相似
    2. 余弦相似度（Cosine Similarity）：余弦相似度用于比较两个向量之间的相似程度。它测量两个向量之间的夹角余弦值，值在-1到1之间。余弦相似度越接近1，表示两个向量之间的方向更相似；越接近-1，表示两个向量之间的方向更相反；接近0表示两个向量之间的夹角较大，方向不太相似。余弦相似度常用于文本挖掘、推荐系统和信息检索等领域。
    """




