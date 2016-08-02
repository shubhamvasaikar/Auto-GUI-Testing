import subprocess

def checkGtk(program_name, locale_code):
    """Starts a given program in the specified locale.
       Checks whether given program_name is a GTK application or not.
    """

    try:
        locale_var = "LANG='"+locale_code+"' "
        # Start the program with the given name
        program = subprocess.Popen([locale_var + program_name], shell=True)  
    except OSError:
        print "Enter a valid application name"
        isGtk = 1
        return isGtk

    # Get the path of the executable by using pid of program.
    executable_path = subprocess.check_output(['readlink', '/proc/'+str(program.pid)+'/exe'])
    executable_path = executable_path.strip('\n')

    # Check program dependencies to check whether application is Gtk.
    isGtk = subprocess.call("ldd " + executable_path + " | grep gtk", shell='True')

    return isGtk

def test_checkGtk():
    assert checkGtk('no') != 0

def main():

    program_name = raw_input("Enter program name: ")
    locale_code = raw_input("Enter locale code: ")
    isGtk = checkGtk(program_name, locale_code)
    if isGtk == 0:
        print "Application is GTK."
    else:
        print "Application is non-GTK."

if __name__ == '__main__' : main()
