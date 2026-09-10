import os
import tempfile
import pymupdf


def optimize_pdf(uploaded_file):
    """
    Safely optimize a PDF without rasterizing pages.

    Returns:
        optimized_path
        original_size
        optimized_size
    """

    original_bytes = uploaded_file.getvalue()
    original_size = len(original_bytes)

    input_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    )

    input_file.write(original_bytes)
    input_file.close()

    output_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    )

    output_path = output_file.name
    output_file.close()

    try:
        document = PyMuPDF.open(input_file.name)

        document.save(
            output_path,
            garbage=4,
            deflate=True,
            clean=True,
        )

        document.close()

        optimized_size = os.path.getsize(output_path)

        # Sometimes optimization can actually make a PDF larger.
        # In that case, use the original instead.
        if optimized_size >= original_size:

            os.remove(output_path)

            output_path = input_file.name

            return (
                output_path,
                original_size,
                original_size,
            )

        os.remove(input_file.name)

        return (
            output_path,
            original_size,
            optimized_size,
        )

    except Exception:

        # Fall back to original PDF if optimization fails
        if os.path.exists(output_path):
            os.remove(output_path)

        return (
            input_file.name,
            original_size,
            original_size,
        )


def format_mb(size_bytes):
    return size_bytes / (1024 * 1024)