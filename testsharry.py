import pytest
from tests import _image_as_bytes, _bytes_as_img

############ PHASE 4 ############

def test_decode_depth_1():
    IMAGE_BYTES = bytes.fromhex("554c424d50031400020002000100000000ffffff05")
    image = _bytes_as_img(IMAGE_BYTES)

def test_encode_depth_1():
    from pixel import Pixel
    from image import Image
    expected = bytes.fromhex("554c424d5003110064000100010000000000000000000000000000000000")
    BLACK = Pixel(0, 0, 0)
    img = Image(100, 1, [BLACK] * 100)
    assert _image_as_bytes(img, version=3, depth=1, rle=False) == expected

def test_decode_depth_2():
    IMAGE_BYTES = bytes.fromhex("554c424d50031400020002000200000000ffffff14")
    image = _bytes_as_img(IMAGE_BYTES)

def test_encode_depth_2():
    from pixel import Pixel
    from image import Image
    expected = bytes.fromhex("554c424d50031400020002000200000000ffffff14")
    BLACK = Pixel(0, 0, 0)
    WHITE = Pixel(255, 255, 255)
    img = Image(2, 2, [BLACK, WHITE, WHITE, BLACK])
    assert _image_as_bytes(img, version=3, depth=2, rle=False) == expected

def test_decode_depth_4():
    IMAGE_BYTES = bytes.fromhex("554c424d50031400020002000400000000ffffff0110")
    image = _bytes_as_img(IMAGE_BYTES)

def test_encode_depth_4():
    from pixel import Pixel
    from image import Image
    expected = bytes.fromhex("554c424d50031400020002000400000000ffffff0110")
    BLACK = Pixel(0, 0, 0)
    WHITE = Pixel(255, 255, 255)
    img = Image(2, 2, [BLACK, WHITE, WHITE, BLACK])
    assert _image_as_bytes(img, version=3, depth=4, rle=False) == expected

def test_decode_depth_8():
    IMAGE_BYTES = bytes.fromhex("554c424d50031400020002000800000000ffffff00010100")
    image = _bytes_as_img(IMAGE_BYTES)

def test_encode_depth_8():
    from pixel import Pixel
    from image import Image
    expected = bytes.fromhex("554c424d50031400020002000800000000ffffff00010100")
    BLACK = Pixel(0, 0, 0)
    WHITE = Pixel(255, 255, 255)
    img = Image(2, 2, [BLACK, WHITE, WHITE, BLACK])
    assert _image_as_bytes(img, version=3, depth=8, rle=False) == expected

def test_decode_depth_8_rle():
    IMAGE_BYTES = bytes.fromhex("554c424d50031400020002000801000000ffffff010002010100")
    image = _bytes_as_img(IMAGE_BYTES)

def test_encode_depth_8_rle():
    from pixel import Pixel
    from image import Image
    expected = bytes.fromhex("554c424d50031400020002000801000000ffffff010002010100")
    BLACK = Pixel(0, 0, 0)
    WHITE = Pixel(255, 255, 255)
    img = Image(2, 2, [BLACK, WHITE, WHITE, BLACK])
    assert _image_as_bytes(img, version=3, depth=8, rle=True) == expected