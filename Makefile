@all: ./builddir/main.exe

./builddir/main.exe: src/*.cc src/**/*.cc include/**/*.hh
	meson setup builddir
	ninja -C builddir

run: ./builddir/main.exe
	./builddir/main.exe

clean:
	rm -r builddir

plots:
	python3 -m plot variants -f MeanDistanceFromTarget
	python3 -m plot variants -f MeanSpeed
	python3 -m plot variants -f VarTargetDensityOverTime
	python3 -m plot variants -f MeanTargetDensityOverTime
	python3 -m plot variants -f MeanTargetSwitchOverTime
	python3 -m plot variants -f MeanDistancesGlobally
	python3 -m plot variants -f MeanDistancesWithinSquadron
	mv *.png ~/Desktop
