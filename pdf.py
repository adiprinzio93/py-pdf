import argparse
from PyPDF2 import PdfFileWriter, PdfFileReader


def create_parsers():

    p = argparse.ArgumentParser(
        prog='crop',
        description='"%(prog)s" crop pdfs',
    )

    p.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Input pdf',
    )

    p.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Output pdf',
    )

    return p


if __name__ == '__main__':

    p = create_parsers()
    args = p.parse_args()

    input_filename = args.input
    output_filename = args.output

    input1 = PdfFileReader(open(input_filename, "rb"))
    input2 = PdfFileReader(open(input_filename, "rb"))
    output = PdfFileWriter()

    numPages = input1.getNumPages()
    print("document has %s pages." % numPages)

    for i in range(numPages):
        page_right = input1.getPage(i)
        page_left = input2.getPage(i)

        # Crop de la página izquierda
        page_left.mediaBox.upperRight = (
            page_left.mediaBox.getUpperRight_x() / 2,
            page_left.mediaBox.getUpperRight_y()
        )

        # Crop de la página derecha
        page_right.mediaBox.upperLeft = (
            page_right.mediaBox.getUpperRight_x() / 2,
            page_right.mediaBox.getUpperRight_y()
        )

        page_right.mediaBox.lowerLeft = (
            page_right.mediaBox.getUpperRight_x() / 2,
            page_right.mediaBox.getLowerRight_y()
        )

        output.addPage(page_left)
        output.addPage(page_right)

    outputStream = open(output_filename, "wb")
    output.write(outputStream)
    outputStream.close()
