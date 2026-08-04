import numpy as np
from PIL import Image
from scipy.ndimage import convolve1d
from tifffile import imwrite

DILATIONS = (7, 9)
WEIGHTS = (2, 2, 2, 3, 2, 2, 2)
NORMALIZATION = sum(WEIGHTS) ** (2 * len(DILATIONS))
MAX_NUMERATOR = 255 * NORMALIZATION


def dilated_kernel(dilation: int, weights: tuple) -> np.ndarray:
    kernel = np.zeros(6 * dilation + 1, dtype=np.uint32)
    kernel[::dilation] = weights
    return kernel


def blur(image: np.ndarray) -> np.ndarray:
    result = np.asarray(image, dtype=np.uint32)
    for dilation in DILATIONS:
        kernel = dilated_kernel(dilation, WEIGHTS)

        result = convolve1d(result, kernel, axis=1, mode="nearest")
        result = convolve1d(result, kernel, axis=0, mode="nearest")
    return result


def main() -> None:
    source = np.asarray(Image.open("source.png").convert("RGB"), dtype=np.uint8)

    numerator = blur(source)
    output = (numerator / MAX_NUMERATOR).astype(np.float32)

    imwrite("blurred.tiff", output, photometric="rgb", metadata=None)

    preview = np.rint(output * 255).astype(np.uint8)
    Image.fromarray(preview).save("preview.png")

    print(f"wrote blurred.tiff and preview.png")
    print(f"normalization = {NORMALIZATION}")


if __name__ == "__main__":
    main()
