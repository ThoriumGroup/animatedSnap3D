Animated Snap 3D
================

- **Author:** Ivan Busquets
- **Maintainer:** Sean Wallitsch
- **Email:** sean@grenadehop.com
- **License:** MIT
- **Status:** Development
- **Python Versions:** 2.6-2.7
- **Nuke Versions:** 6.3 and up

An extension to Nuke's "snap" options for animated 3D objects. Based on a
selection of vertices, this allows for objects to match the position, rotation
and scale of that selection over a specified frame range.

Usage
-----

As the name suggests, this adds "animated" options to the snap_menu in 3d
nodes since Nuke 6.1. The 3 new options work exactly the same way as their
original counterparts, but extends their use to animated geometry.

Installation
------------

To install, simply ensure the "animatedSnap3D" directory is in your .nuke
directory or anywhere else within the Nuke python path.

Then, add the following lines to your 'menu.py' file:
::
    import animatedSnap3D
    animatedSnap3D.run()

Changelog
---------

*New in version 1.2:*

- Refactor and code cleanup
- Will no longer install menu items automatically on import, you need to call `animatedSnap3D.run()`
- Removed all convenience and intermediate functions, leaving only `animated_snap`
- `animated_snap` has had it's arguments reworked.
    - The first and only mandatory argument is now `transforms`, which expects a list containing one or more of 'translate', 'rotate' and 'scaling'
    - The two optional args are `node` and `vertices`. If not provided they will be derived automatically.

License
-------

    The MIT License (MIT)

    animatedSnap3D
    Copyright (c) 2011 Ivan Busquets

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
