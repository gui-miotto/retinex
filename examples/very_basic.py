import os

import matplotlib.pyplot as plt
import skimage

from retinex import msrcr


def main():
    here = os.path.dirname(__file__)
    img_path = os.path.join(here, "..", "sample_images", "leaves.jpg")
    img = skimage.io.imread(img_path)
    msrcr_img = msrcr(img, sigmas=(25., 50., 100.,))

    f, ax = plt.subplots(1, 2, figsize=(7, 5))
    ax[0].set_title("Original")
    ax[1].set_title("MSRCR")

    ax[0].axis("off")
    ax[1].axis("off")

    ax[0].imshow(img)
    ax[1].imshow(msrcr_img)

    f.tight_layout()
    plt.savefig(os.path.join(here, "..", "assets", "leaves_msrcr.png"))
    plt.show()

if __name__ == "__main__":
    main()
