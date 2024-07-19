@all: ./builddir/main.exe

./builddir/main.exe: src/*.cc src/**/*.cc include/**/*.hh
	meson setup builddir
	ninja -C builddir

run: ./builddir/main.exe
	./builddir/main.exe

clean:
	rm -r builddir

allocator:
	python3 -m plot variants -f MeanDistanceFromTarget -g RANDOM NEAREST
	python3 -m plot variants -f MeanSpeed -g RANDOM NEAREST
	python3 -m plot variants -f VarTargetDensityOverTime -g RANDOM NEAREST
	python3 -m plot variants -f MeanTargetDensityOverTime -g RANDOM NEAREST
	python3 -m plot variants -f MeanTargetSwitchOverTime -g RANDOM NEAREST
	python3 -m plot variants -f MeanDistancesWithinSquadron -g RANDOM NEAREST
	python3 -m plot variants -f MinDistancesGlobally -g RANDOM NEAREST

executor:
	python3 -m plot variants -f MeanDistanceFromTarget -g LP GP
	python3 -m plot variants -f MeanSpeed -g LP GP
	python3 -m plot variants -f VarTargetDensityOverTime -g LP GP
	python3 -m plot variants -f MeanTargetDensityOverTime -g LP GP
	python3 -m plot variants -f MeanTargetSwitchOverTime -g LP GP
	python3 -m plot variants -f MeanDistancesWithinSquadron -g LP GP
	python3 -m plot variants -f MinDistancesGlobally -g LP GP
