@all: ./builddir/main.exe

./builddir/main.exe: src/*.cc src/**/*.cc include/**/*.hh
	meson setup builddir
	ninja -C builddir

run: ./builddir/main.exe
	./builddir/main.exe

clean:
	rm -r builddir

plots:
	python3 -m plot variants -f MeanDistanceFromTarget -i ${ARCHIVE} -o ${OUTPUT}
	python3 -m plot variants -f MeanSpeed -i ${ARCHIVE} -o ${OUTPUT}
	python3 -m plot variants -f VarTargetDensityOverTime -i ${ARCHIVE} -o ${OUTPUT}
	python3 -m plot variants -f MeanTargetDensityOverTime -i ${ARCHIVE} -o ${OUTPUT}
	python3 -m plot variants -f MeanTargetSwitchOverTime -i ${ARCHIVE} -o ${OUTPUT}
	python3 -m plot variants -f MeanDistancesWithinSquadron -i ${ARCHIVE} -o ${OUTPUT}
	python3 -m plot variants -f MinDistancesGlobally -i ${ARCHIVE} -o ${OUTPUT}

plots2:
	python3 -m plot variants -f MeanDistanceFromTarget -g LP GP
	python3 -m plot variants -f MeanSpeed -g LP GP
	python3 -m plot variants -f VarTargetDensityOverTime -g LP GP
	python3 -m plot variants -f MeanTargetDensityOverTime -g LP GP
	python3 -m plot variants -f MeanTargetSwitchOverTime -g LP GP
	python3 -m plot variants -f MeanDistancesWithinSquadron -g LP GP
	python3 -m plot variants -f MinDistancesGlobally -g LP GP
