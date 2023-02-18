import numpy as np
import cv2


def generate_text_direction(bboxes):
    for blk in bboxes:
        for line_idx in range(len(blk.lines)):
            yield blk, line_idx


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def crop_text(image: np.ndarray, text_regions):
    text_height = 48
    max_chunk_size = 16

    quadrilaterals = list(generate_text_direction(text_regions))
    region_imgs = [t.get_transformed_region(
        image, d, 48) for t, d in quadrilaterals]
    perm = range(len(region_imgs))
    ix = 0

    for indices in chunks(perm, max_chunk_size):
        N = len(indices)
        widths = [region_imgs[i].shape[1] for i in indices]
        max_width = (4 * (max(widths) + 7) // 4) + 128
        region = np.zeros((N, text_height, max_width, 3), dtype=np.uint8)

        for i, idx in enumerate(indices):
            W = region_imgs[idx].shape[1]
            region[i, :, : W, :] = region_imgs[idx]
            cv2.imwrite(f'results/ocrs/{ix}.png', cv2.rotate(cv2.cvtColor(
                region[i, :, :, :], cv2.COLOR_RGB2BGR), cv2.ROTATE_90_CLOCKWISE))
            # cv2.imwrite(f'results/ocrs/{ix}.png', cv2.cvtColor(region[i, :, :, :], cv2.COLOR_RGB2BGR))
            ix += 1

    return text_regions
