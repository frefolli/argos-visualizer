@all: ./builddir/main.exe

./builddir/main.exe: src/*.cc src/**/*.cc include/**/*.hh
	meson setup builddir
	ninja -C builddir

run: ./builddir/main.exe
	./builddir/main.exe

clean:
	rm -r builddir
