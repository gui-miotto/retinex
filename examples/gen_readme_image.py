import os

import matplotlib.pyplot as plt
import skimage

from retinex import msrcr


def main():
    here = os.path.dirname(__file__)
    img_names = ["man", "park", "street"]

    sigmas = (25., 50., 100.,)

    f, ax = plt.subplots(len(img_names), 2, figsize=(7, 7))
    ax[0, 0].set_title("Original")
    ax[0, 1].set_title("MSRCR")

    for n_img, img_name in enumerate(img_names):
        img = skimage.io.imread(os.path.join(here, "..", "sample_images", f"{img_name}.jpg"))
        msrcr_img = msrcr(img, sigmas=sigmas)

        ax[n_img, 0].axis("off")
        ax[n_img, 1].axis("off")

        ax[n_img, 0].imshow(img)
        ax[n_img, 1].imshow(msrcr_img)

    f.tight_layout()
    plt.savefig(os.path.join(here, "..", "assets", "img_grid.png"))
    plt.show()

if __name__ == "__main__":
    main()
