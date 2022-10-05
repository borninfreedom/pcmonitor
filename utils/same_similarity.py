import cv2
from skimage.metrics import structural_similarity as ssim

def same_similarity(img1, img2,with_logger=False):
    """
    :param img1: cv2 image
    :param img2: cv2 image
    :return: True or False

    If two img is the same, the ssim will return a value >=0.9.
    """
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    similarity = ssim(img1, img2)

    return similarity
    # # 0.88 is from experiences
    # if similarity > 0.87:
    #     return True
    # else:
    #     return False
