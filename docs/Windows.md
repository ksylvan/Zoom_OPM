# Running Zoom OPM Tools on Windows

## Background and Context

The centerpiece of the automation, the [zoom-manage][zoom-manage] command, is
an AppleScript application that uses the GUI and automation frameworks of macOS
to manage the Zoom application, navigate its menus, and gather information
dynamically from the "Particiapants" panel (or standalone window).

This approach was chosen since it allowed me to quickly gather information
that the Zoom Application was already rendering, and the macOS GUI standards
and tools made it relatively "simple" (once you get familiar with the
AppleScript syntax).

## Alternatives for Windows (and Linux)

### Port the Zoom Manage tool

If there is an equivalent frameork for controlling and querying the Zoom application
on Windows, then we might be able to use that to create the equivalent functionality on
Windows 10 and Windows 11.

Note: We would only have to port the [zoom-manage][zoom-manage] script.
The other two components, the backend server (written in Python), and the
`Vue.js` based Web GUI frontend, will work on Windows (or Linux).

A possibile path is to use a platform independant automation framework like
[PyAutoGui][py-auot-gui] with [PyTesseract][py-tesseract] to do the same
thing we are doing with AppleScript.

However, when using PyAutoGui and PyTesseract, we would be using
image screen captures and [OCR][tesseract-ocr] under the hood to read the
information from the Participants panel, it would not be as seamless as it
is on the Mac.

### Using a Virtual Machine

If you have access to a MacOS running the latest macOS 14 (code name "Sonoma"),
you can follow these steps to create an installer image of the latest macOS:

[Download/Create macOS Sonoma ISO for VMware or VirtualBox][sonoma-iso-instructions]

You can then use the image to boot up a macOS VM on your windows machine, using,
for instance, [Oracle VirtualBox](https://www.virtualbox.org/).

This would require that you have a laptop or desktop with enough resources
to accomplish this feat.

[zoom-manage]: ../zoom-manage
[py-auot-gui]: https://pyautogui.readthedocs.io/en/latest/
[py-tesseract]: https://github.com/madmaze/pytesseract
[tesseract-ocr]: https://github.com/tesseract-ocr/tesseract
[sonoma-iso-instructions]: https://iboysoft.com/howto/macos-sonoma-iso.html
