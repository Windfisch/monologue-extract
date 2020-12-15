# Copyright (c) 2020, Florian Jung (flo@windfis.ch)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os

def ex(data, indices):
	return [data[i] if i < len(data) else -1 for i in indices]

def no_auto_write(auto_write_data):
	return auto_write_data[0:6] + bytes([0x40, 0x00]) + auto_write_data[10:]

def auto_write(no_auto_write_data, index):
	if not (0 <= index and index < 100):
		raise IndexError("program index must be between 0 and 99")
	
	return no_auto_write_data[0:6] + bytes([0x4c, index, 0x00, 0x00]) + no_auto_write_data[8:]

def get_name(data):
	bs = data[0:3] + data[4:11] + data[12:14]
	result = ""
	for b in bs:
		if b <= 0x1F:
			pass
		elif b == 0x2F or b >= 0x7F: # /
			result += "_"
		else:
			result += bytes([b]).decode('ascii')
	return result

if len(sys.argv) != 3:
	print("""Korg Monologue Sysex Extractor.
Reads a sysex dump from a Korg Monologue synthesizer and extracts all
patches, properly names, into outdir/. Can also be used on a single
patch dump, which will be renamed accordingly and copied to outdir/.

Dumps can be created using `amidi -p hw:1 -r dump.syx`.

Usage: %s file.sysex outdir/""" % sys.argv[0])

data = open(sys.argv[1], 'rb').read()
path = sys.argv[2]

if not os.path.exists(path):
	os.makedirs(path)

SYSEX_BEGIN = bytes([0xF0])
messages = [ SYSEX_BEGIN + part for part in data.split(SYSEX_BEGIN)[1:] ]

for message in messages:
	if ex(message, [0,6,8,9,10,11,519]) == [0xf0, 0x40, 0x50, 0x52, 0x4f, 0x47, 0xf7]:
		print(get_name(message[12:]).strip())
		filename = "%s.syx" % get_name(message[12:]).strip()
		open(path + "/" + filename, 'wb').write(message)

	elif ex(message, [0,6,10,11,12,13,521]) == [0xf0, 0x4c, 0x50, 0x52, 0x4f, 0x47, 0xf7]:
		print(get_name(message[14:]).strip())
		filename = "%03d_%s.syx" % (message[7]+1, get_name(message[14:]).strip())
		if not os.path.exists(path + "/auto_write"): os.makedirs(path + "/auto_write")
		open(path + "/auto_write/" + filename, 'wb').write(message)
		open(path + "/" + filename, 'wb').write(no_auto_write(message))
	else:
		print("<ignored>")
