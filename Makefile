qrc:
	pyside2-rcc -o GUI/qtrc.py QT_GUI/qtrc.qrc 

ui:
	pyside2-uic QT_GUI/main_configs.ui -o GUI/main_configs.py
	sed -i '/import qtrc_rc/d' GUI/main_configs.py
