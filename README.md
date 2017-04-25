# Auto-GUI-Testing

## Purpose of Project
This project is made to test Gnome applications in an automated way related to internationalization (i18n) and localization (l10n) aspects. This task was previously being done manually and this project aims to automate that task.

## Project Scope
This scope of the project is as follows:
- Gnome Applications
- Gnome Desktop
- Xorg Display Server

## Modules
This project consists of the following modules:
- checkgtk : Used to check whether an application is a GTK application.
- checklocales : Used to check for the availability of language pack on the system.
- extractpot : Used to extract .pot file from source and generate translation statistics from it.
- qualitychecks : Used to perform technicale quality checks on .po files.
- pyatspiwrapper : Wrapper for pyatspi to automate desktop applications.
- translationcheck : Check whether strings are translated in running applications.
- extractwidgets : Take screenshots of application widgets and perform font rendering checks.

## Technologies Used
- pyatspi
- tesseract
- PIL
- polib
- PyGTK3.0+

## Prerequisites
- PyGObject and GNOME-Python
- Applications to test, e.g. from the GNOME desktop:
    http://gnome.org/
- Xvfb and xinit:
    http://xorg.freedesktop.org/

## System Requirements
### Minimum Hardware Specifications
Processor: 64-bit Processor
RAM: 4GB
Disk Space: 100MB

## Deployment Procedure
- Run setup.py and install application.
- Use autotest2.py as an entrypoint.

## Maintainence Procedure
Each module stands independent of other modules and can be maintained and changed seperately. Also there is no requirement to use all the modules at the same time. Some modules can be used while others can be left out.

## Further scope
- Use dogtail in place of pyatspi.
- Use length checking to find out some clipping issues in the application component.
