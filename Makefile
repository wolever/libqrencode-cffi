libqrencode/_ffi.so: libqrencode/ffi_build.py
	python $<

clean:
	rm libqrencode/_ffi.*
