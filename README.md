# Punch gift card generator

This is a little python script to generate a gift ![punch card](https://en.wikipedia.org/wiki/Punched_card) ![SVG image](https://en.wikipedia.org/wiki/SVG) from a given text.

The punch holes are represented as white rectangles. They are not meant to be cut out. Just print the SVG on a card or thick paper and cut the whole card out.

I decided to create my own script as I could not find an existing easy solution to create a vector image of a punch card from a given text.

The background texture is taken from ![Sahand's punch card generator](https://github.com/sahandbabali/Punch-Card-Generator/).

## Punch card format

This script implements the IBM 029 alphabet.

Card dimensions are taken from ![Christoph Kummer's punch card project](https://github.com/chkummer/PunchedCard/blob/master/CardDimensions.md). Thanks to him for providing this information!

## Usage

No additional python modules required. Developed and tested in python 3.11.

Simply change the MESSAGE variable at the script beginning. Run the script with `python3 generator.py`. You will find the output in output.svg.

Open the file in inkscape for further editing. For example, remove the plain text to let the giftee decode by himself. Change the paper size to A4 and align the image to print it out.

## Further ideas

- Add an imaginary company name to the left edge and some alignment markers to let the image look more like an original punch card, like ![„The Virtual Keypunch“](https://www.masswerk.at/keypunch/) for example.
- Use embedded fonts for numbers and IBM 029 font. Currently used font „monospace“ will probably render wrong on some well-known proprietary operating systems.
- Add support for a cutter. I do not own one and probably never will, but output could be compatible to Christoph's project.
- getopt command line options to set message, disable plain text, set output filename, etc.