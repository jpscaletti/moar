# Adapted from optimage.py
# Copyright 2015 Sebastian Kreft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections
import contextlib
import logging
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image


def _images_are_equal(filename1, filename2):
    # We need to convert both images to the same format, as the resulting one
    # may have lost the alpha channel (alpha=255) or may be now indexed
    # (L or P mode).
    # We also need to check whether the alpha value is '\x00' in which case the
    # RGB value is not important.
    img1 = Image.open(filename1).convert('RGBA')
    img2 = Image.open(filename2).convert('RGBA')

    img1_bytes = img1.tobytes()
    img2_bytes = img2.tobytes()

    if len(img1_bytes) != len(img2_bytes):
        return False

    # HACK to support comparison in both Python 2 and 3. Subscripting a
    # bytes (string) in Python 2 returns a string, whereas in Python 3 returns
    # ints.
    null_byte = b'\x00'[0]
    for i in range(len(img1_bytes) // 4):
        pos = 4 * i
        if (img1_bytes[pos + 3] == null_byte and
                img2_bytes[pos + 3] == null_byte):
            continue

        if img1_bytes[pos:pos + 4] != img2_bytes[pos:pos + 4]:
            return False

    return True


def _get_temporary_filename(prefix='tmp'):
    temp_file = tempfile.NamedTemporaryFile(prefix=prefix)
    temp_name = temp_file.name
    temp_file.close()

    return temp_name


@contextlib.contextmanager
def _temporary_filenames(total):
    """Context manager to create temporary files and remove them after use."""
    temp_files = [_get_temporary_filename('optimage-') for i in range(total)]
    yield temp_files
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except OSError:
            # Continue in case we could not remove the file. One reason is that
            # the fail was never created.
            pass


class InvalidExtension(Exception):
    """The file extension does not correspond to the file contents."""


if sys.version_info.major == 2:
    FileNotFoundError = OSError
else:
    FileNotFoundError = FileNotFoundError


class MissingBinary(FileNotFoundError):
    """The binary does not exist."""


def _call_binary(args):
    try:
        return subprocess.check_output(args, stderr=subprocess.STDOUT)
    except FileNotFoundError as error:
        raise MissingBinary(error.errno, 'binary not found', args[0])


def _pngcrush(input_filename, output_filename):
    _call_binary(['pngcrush', '-rem', 'alla', '-reduce', '-brute', '-q',
                  input_filename, output_filename])


def _optipng(input_filename, output_filename):
    _call_binary(['optipng', '-out', output_filename, '-o9', '-quiet',
                  input_filename])


def _jpegtran(input_filename, output_filename):
    _call_binary(['jpegtran', '-copy', 'none', '-optimize', '-perfect',
                  '-outfile', output_filename, input_filename])


def _jpegoptim(input_filename, output_filename):
    # jpegoptim replaces the input file with the compressed version, so we first
    # need to copy the input file to the output file.
    shutil.copy(input_filename, output_filename)
    _call_binary(['jpegoptim', '--strip-all', '--quiet', output_filename])


_CompressorResult = collections.namedtuple('_CompressorResult',
                                           ['size', 'filename', 'compressor'])


def _process(compressor, input_filename, output_filename):
    """Helper function to compress an image.

    Returns:
      _CompressorResult named tuple, with the resulting size, the name of the
      output file and the name of the compressor.
    """
    compressor(input_filename, output_filename)
    result_size = os.path.getsize(output_filename)

    return _CompressorResult(result_size, output_filename, compressor.__name__)


def _compress_with(input_filename, output_filename, compressors):
    """Helper function to compress an image with several compressors.

    In case the compressors do not improve the filesize or in case the resulting
    image is not equivalent to the source, then the output will be a copy of the
    input.
    """
    with _temporary_filenames(len(compressors)) as temp_filenames:
        results = []
        for compressor, temp_filename in zip(compressors, temp_filenames):
            results.append(_process(compressor, input_filename, temp_filename))
        best_result = min(results)
        os.rename(best_result.filename, output_filename)

        best_compressor = best_result.compressor
        if best_result.size >= os.path.getsize(input_filename):
            best_compressor = None

        if (best_compressor is not None and
                not _images_are_equal(input_filename, output_filename)):
            logging.info('Compressor "%s" generated an invalid image for "%s"',
                         best_compressor, input_filename)
            best_compressor = None

        if best_compressor is None:
            shutil.copy(input_filename, output_filename)

    logging.info('%s: best compressor for "%s"', best_compressor,
                 input_filename)


def jpeg_compressor(input_filename, output_filename):
    """Loslessly recompress a JPEG.
    """
    _compress_with(input_filename, output_filename, [_jpegtran, _jpegoptim])


def png_compressor(input_filename, output_filename):
    """Loslessly recompress a JPEG.
    """
    _compress_with(input_filename, output_filename, [_pngcrush, _optipng])


_EXTENSION_MAPPING = {
    '.jpeg': jpeg_compressor,
    '.jpg': jpeg_compressor,
    '.png': png_compressor,
}


def optimage(filename):
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    compressor = _EXTENSION_MAPPING.get(extension)
    if compressor is None:
        print(
            'No lossless compressor defined for extension "{}"\n'.format(
                extension))
        return

    with _temporary_filenames(1) as temp_filenames:
        output_filename = temp_filenames[0]
        try:
            compressor(filename, output_filename)
        except MissingBinary as error:
            print(
                'The executable "{}" was not found. '.format(error.filename) +
                'Please install it and re-run this command.\n')
            return
        except subprocess.CalledProcessError as error:
            print(
                'Error when running the command:\n  ' +
                '{}\n'.format(' '.join(error.cmd)))
            print('Status: {}\n'.format(error.returncode))
            print('Output:\n')
            print(error.output.decode('utf-8'))
            return

        original_size = os.path.getsize(filename)
        new_size = os.path.getsize(output_filename)
        reduction = original_size - new_size
        reduction_percentage = reduction * 100 / original_size
        savings = 'savings: {} bytes = {:.2f}%'.format(
            reduction, reduction_percentage)

        if new_size < original_size:
            shutil.copy(output_filename, filename)
            print('File was losslessly compressed to {} bytes ({})'.format(
                new_size, savings))
        else:
            print('No further compression achieved')
