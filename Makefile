all:
	python setup.py build_ext --inplace

cleanso:
	find . -type f -name "*.so" -delete
	rm -f voicesep/separators/neural/chord_level/features/__init__.cpp
	rm -f voicesep/separators/neural/chord_level/features/levels/*.cpp
	rm -f voicesep/separators/neural/chord_level/features/assignments_generator/__init__.cpp
	rm -rf build

cleancache:
	find . -type d -name "__pycache__" -exec rm -r {} +
