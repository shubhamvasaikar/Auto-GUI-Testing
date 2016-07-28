import subprocess

def checkGtk(program_name):
    """Checks whether given program_name is a GTK application or not.
    """

    try:
        program = subprocess.Popen([program_name])
    except OSError:
        print "Enter a valid application name"

    executable_path = subprocess.check_output(['readlink', '/proc/'+str(program.pid)+'/exe'])
    executable_path = executable_path.strip('\n');

    isGtk = subprocess.call("ldd " + executable_path + " | grep gtk", shell='True')

    if isGtk == 0:
        print "Application is GTK."
    else:
        print "Application is non-GTK."

def main():

    program_name = raw_input("Enter program name: ")
    checkGtk(program_name)

if __name__ == '__main__' : main()
