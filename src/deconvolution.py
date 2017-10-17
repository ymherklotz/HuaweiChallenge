#!/usr/bin/env python

"""
Wiener deconvolution.

Sample shows how DFT can be used to perform Weiner deconvolution [1]
of an image with user-defined point spread function (PSF)

Usage:
  deconvolution.py  [--circle]
      [--angle <degrees>]
      [--d <diameter>]
      [--snr <signal/noise ratio in db>]
      [<input image>]

  Use sliders to adjust PSF paramitiers.
  Keys:
    SPACE - switch btw linear/cirular PSF
    ESC   - exit

Examples:
  deconvolution.py --angle 135 --d 22  ../data/licenseplate_motion.jpg
    (image source: http://www.topazlabs.com/infocus/_images/licenseplate_compare.jpg)

  deconvolution.py --angle 86 --d 31  ../data/text_motion.jpg
  deconvolution.py --circle --d 19  ../data/text_defocus.jpg
    (image source: compact digital photo camera, no artificial distortion)


[1] http://en.wikipedia.org/wiki/Wiener_deconvolution
"""

from utils.exceptions import ValidImagePathError

import numpy as np
import cv2

import sys
import getopt


def blur_edge(img, d=20):
    h, w  = img.shape[:2]
    img_pad = cv2.copyMakeBorder(img, d, d, d, d, cv2.BORDER_WRAP)
    img_blur = cv2.GaussianBlur(img_pad, (2*d+1, 2*d+1), -1)[d:-d,d:-d]
    y, x = np.indices((h, w))#!/usr/bin/env python
    dist = np.dstack([x, w-x-1, y, h-y-1]).min(-1)
    w = np.minimum(np.float32(dist)/d, 1.0)
    return img*w + img_blur*(1-w)


def motion_kernel(angle, d, sz=30):
    kern = np.ones((1, d), np.float32)
    c, s = np.cos(angle), np.sin(angle)
    A = np.float32([[c, -s, 0], [s, c, 0]])
    sz2 = sz // 2
    A[:,2] = (sz2, sz2) - np.dot(A[:,:2], ((d-1)*0.5, 0))
    kern = cv2.warpAffine(kern, A, (sz, sz), flags=cv2.INTER_CUBIC)
    return kern


def defocus_kernel(d, sz=30):
    kern = np.zeros((sz, sz), np.uint8)
    cv2.circle(kern, (sz, sz), d, 255, -1, cv2.LINE_AA, shift=1)
    kern = np.float32(kern) / 255.0
    return kern


def update(img, IMG, win, defocus):
    ang = np.deg2rad( cv2.getTrackbarPos("angle", win) )
    d = cv2.getTrackbarPos("d", win)
    noise = 10**(-0.1*cv2.getTrackbarPos("SNR (db)", win))

    if defocus:
        psf = defocus_kernel(d)
    else:
        psf = motion_kernel(ang, d)
    cv2.imshow("psf", psf)

    psf /= psf.sum()
    psf_pad = np.zeros_like(img)
    kh, kw = psf.shape
    psf_pad[:kh, :kw] = psf
    PSF = cv2.dft(psf_pad, flags=cv2.DFT_COMPLEX_OUTPUT, nonzeroRows = kh)
    PSF2 = (PSF**2).sum(-1)
    iPSF = PSF / (PSF2 + noise)[...,np.newaxis]
    RES = cv2.mulSpectrums(IMG, iPSF, 0)
    res = cv2.idft(RES, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )
    res = np.roll(res, -kh//2, 0)
    res = np.roll(res, -kw//2, 1)
    cv2.imshow(win, res)
    return res


def start_deconvolution(argv):
    print(__doc__)
    opts, args = getopt.getopt(argv[1:], "", ["circle", "angle=", "d=", "snr="])
    opts = dict(opts)

    if len(args) == 0:
        raise ValidImagePathError("File path not specified")

    fn = args[0]

    img = cv2.imread(fn, cv2.IMREAD_COLOR)
    cv2.imshow("input", img)
    height, width = img.shape[:2]
    img = cv2.copyMakeBorder(img, (width-height)//2, (width-height)//2, 0, 0, cv2.BORDER_CONSTANT)
    if img is None:
        print("Failed to load fn1:", fn1)
        sys.exit(1)

    b, g, r = cv2.split(img)

    b = np.float32(b)/255.0
    g = np.float32(g)/255.0
    r = np.float32(r)/255.0
    cv2.imshow("input blue", b)
    cv2.imshow("input green", g)
    cv2.imshow("input red", r)

    b = blur_edge(b)
    g = blur_edge(g)
    r = blur_edge(r)
    B = cv2.dft(b, flags=cv2.DFT_COMPLEX_OUTPUT)
    G = cv2.dft(g, flags=cv2.DFT_COMPLEX_OUTPUT)
    R = cv2.dft(r, flags=cv2.DFT_COMPLEX_OUTPUT)

    defocus = "--circle" in opts

    win = "deconvolution"
    def update_deconv(_):
        return (update(b, B, win, defocus),
                update(g, G, win, defocus),
                update(r, R, win, defocus))

    cv2.namedWindow(win)
    cv2.createTrackbar("angle", win, int(opts.get("--angle", 135)), 180, update_deconv)
    cv2.createTrackbar("d", win, int(opts.get("--d", 22)), 50, update_deconv)
    cv2.createTrackbar("SNR (db)", win, int(opts.get("--snr", 25)), 50, update_deconv)
    update_deconv(None)

    while True:
        ch = cv2.waitKey()
        if ch == 27:
            b_res, g_res, r_res = update_deconv(None)
            b_res = b_res*255.0
            g_res = g_res*255.0
            r_res = r_res*255.0
            b_res = np.int32(b_res)
            g_res = np.int32(g_res)
            r_res = np.int32(r_res)
            img_res = cv2.merge((b_res, g_res, r_res))
            cv2.imwrite("output.png", img_res)
            break
        if ch == ord(" "):
            defocus = not defocus
            update_deconv(None)


if __name__ == "__main__":
    start_deconvolution(sys.argv)
