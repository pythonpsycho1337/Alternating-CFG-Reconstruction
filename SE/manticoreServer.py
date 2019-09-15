"""
Author: Thomas Peterson
Year: 2019
"""

#Built in modules
import sys, logging

#Custom modules
import symbolicExecutor, pathsObject, pathObject, communication

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

def main():
    if (len(sys.argv) < 2):
        print("Usage: Python manticoreServer.py [port number]")
        sys.exit(0)
    port=sys.argv[1]
    logger.info("[*] Starting server..")
    server = Server(int(port))
    server.run()

class Server():
    connection = None

    def __init__(self, port):
        self.connection = communication.Communication(port)

    def run(self):
        # Work loop
        while True:
            logger.info("[*] Waiting for connection..")
            self.connection.connect()
            logger.info("[*] Connection received!")
            request = self.connection.getWork()
            request = request.split("\n")
            program = request[0]
            paths = formatPaths(request[1:])

            logger.info(request)
            logger.info("Program: "+program)
            logger.info("Number of paths received: " + str(paths.pathsLen))

            symbolicExecutor.executeDirected(program, paths)

            self.connection.sendAnswer("Everything okay")

def formatPaths(lines):
    paths = []
    id = 0
    for line in lines:
        if line == '':
            continue
        path = line.split(",")
        path = [int(i.strip(), 16) for i in path]  # Remove newline characters and convert to integers
        paths.append(pathObject.PathObject(path,id))
        id +=1
        
    return pathsObject.PathsObject(paths)

#Deprecated
def loadPathsFromFile(filename):

    with open(filename, "r") as f:
        lines = f.readlines()

    return formatPaths(lines)


if __name__ == "__main__":
    main()
