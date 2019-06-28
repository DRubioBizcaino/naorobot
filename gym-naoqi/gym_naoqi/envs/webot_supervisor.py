import subprocess
from time import sleep

class WebotsSupervisor:
 
    process = None
    cmd = ""

    def __init__(self, cmd="webots.exe", worldfile=None):
        if (worldfile == None):
            self.cmd = cmd
        else:
            self.cmd = cmd + " " + worldfile
        self.process = subprocess.Popen(self.cmd)
        sleep(13)

    def __del__(self):
        self.stop()

    def start(self):
        if (self.process == None):
            self.process = subprocess.Popen(self.cmd)
            #maybe sleep(x) would be good here
            sleep(13)

    def stop(self):
        if (self.process!=None):
            self.process.terminate()
            self.process = None

    def restart(self):
        self.stop
        self.start

if __name__=="__main__":
    print "Starting Webots"
    test_super = WebotsSupervisor()
    sleep(10)
    print "Stopping Webots"
    test_super.stop()
    sleep(10)
    print "Starting Webots"
    test_super.start()
    sleep(10)
    print "Program ended"