from PIL import Image, ImageChops


def compare_images(baseline_path, actual_path, diff_path, tolerance=0):
    """
    :param baseline_path:
    :param actual_path:
    :param diff_path:
    :param tolerance:
    :return:
    """
    baseline = Image.open(baseline_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")

    if baseline.size != actual.size:
        raise ValueError("Las imágenes tienen tamaños diferentes")

    diff = ImageChops.difference(baseline, actual)

    # Si no hay diferencias
    if not diff.getbbox():
        return True, None

    # Opcional: aplicar tolerancia básica
    if tolerance > 0:
        diff = diff.point(lambda x: x > tolerance and 255)

    diff.save(diff_path)
    return False, diff_path