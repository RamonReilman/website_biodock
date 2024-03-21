import subprocess


class Ledock:
    """
    A class that runs ledock

    ...

    Attributes
    ----------
    path : the path to the directory housing the files you want to run ledock on
    dock_path : the path to the ledock executable

    Methods
    -------
    run(self):
        runs ledock on the correct files in the directory
    """
    def __init__(self, path):
        """
        Constructs all the necessary attributes for the Ledock object

        :param path: the path to the directory housing the files you want to run ledock on
        """
        self.path = path
        self.dock_path = subprocess.run(["find", "-name", "ledock_linux_x86"], check=True, capture_output=True,
                                        text=True)

    def run(self):
        """
        modifies the dock_path to be able to access ledock from the directory in static/history and runs ledock on
        the files in the self.path
        :return: creates the .dok file in the given directory
        """
        # replaces the "." that indicates this directory with the path from a directory in static/history
        ledock_path = "../../.." + self.dock_path.stdout[1:]

        # removes the /n if it is created
        ledock_path = ledock_path.replace("\n", "")

        # runs ledock in the directory on the dock.in
        subprocess.run([f"{ledock_path}", "dock.in"], cwd=f"{self.path}", check=True)

    def __str__(self):
        """
        gives this return when printing this class
        :return: The path given when creating first creating the class
        """
        return f"ledock recieved {self.path}"


if __name__ == "__main__":
    # test
    ledock = Ledock("static/history/test_ledock")
    ledock.run()
    print(ledock)

