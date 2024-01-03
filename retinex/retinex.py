import multiprocessing as mp

import numpy as np
import skimage


def msrcr(
    img,
    sigmas,
    G=192.,
    b=-30.,
    alpha=125.,
    beta=46.,
    color_correction=True,
    histogram_match=False,
    ):
    if img.ndim != 3:
        raise ValueError("img.ndim != 3")
    img_orig = img.copy()
    if img.shape[2] == 4:
        img_orig = skimage.color.rgba2rgb(img_orig)
    img_orig = skimage.util.img_as_ubyte(img_orig).astype(np.float64)
    img_min = img_orig.min(axis=(0, 1))
    img_max = img_orig.max(axis=(0, 1))
    zero_supressed_img = img_orig + 1.

    msr_img = _msr(zero_supressed_img, sigmas=sigmas)
    msr_img = _normalize_channels(img=msr_img, vmin=img_min, vmax=img_max)

    if color_correction:
        crf_img = _crf(zero_supressed_img, alpha=alpha, beta=beta)
        msrcr_img = G * (crf_img * msr_img - b)
    else:
        msrcr_img = msr_img.copy()

    # TODO: delete this "functionality"
    if histogram_match:
        msrcr_img = skimage.exposure.match_histograms(msrcr_img, img_orig, channel_axis=2)
    else:
        msrcr_img = _normalize_channels(img=msrcr_img, vmin=img_min, vmax=img_max)
    msrcr_img = msrcr_img.astype(np.ubyte)

    return msrcr_img


def _msr(img, sigmas):  # TODO: docstrings
    args = zip([img] * len(sigmas), sigmas)
    with mp.Pool(processes=len(sigmas)) as pool:
        all_ssr = pool.starmap(_ssr, args)
    msr_img = np.mean(all_ssr, axis=0)
    return msr_img

def _ssr(img, sigma):
    # print("ssr with sigma equals", sigma)
    blurred = skimage.filters.gaussian(
        img,
        sigma=sigma,
        channel_axis=2,
        )
    ssr_img = np.log10(img) - np.log10(blurred)
    return ssr_img

def _crf(img, alpha, beta):
    chromaticity = img / np.sum(img, axis=2, keepdims=True)
    crf_img = beta * np.log10(alpha * chromaticity)
    return crf_img

def _normalize_channels(img, vmin, vmax):
    img_min = img.min(axis=(0,1))
    img_max = img.max(axis=(0,1))
    img_span = img_max - img_min
    vspan = vmax - vmin

    img_norm = (img - img_min) / img_span * vspan + vmin
    return img_norm
