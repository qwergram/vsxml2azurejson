try:
    from pyscripts import util
except ImportError:
    import util
import io

class SolutionParser(object):

    def __init__(self, sln_path):
        assert util.test_path(sln_path, 'f')
        self.path = sln_path
        self.raw_content = []
        self.data = {
            "version": None,
            "vsversion": {
                "min": None,
                "current": None
            },
            "projects": [],
            "csdef": None,
            "cscfg": None,
            "ccproj": None,
        }

    def get_content(self):
        with io.open(self.path) as context:
            self.raw_content = [[line.lower().strip(), line.strip()] for line in context.readlines()]
    
    def feed(self, content):
        self.raw_content = [[line.lower().strip(), line.strip()] for line in content.split("\n") if line.strip()]

    def parse_content(self):
        for line_lower, line in self.raw_content:
            if line_lower.startswith("microsoft visual studio solution file"):
                self.data['version'] = float(line_lower.replace('microsoft visual studio solution file, format version ', '').strip())
            elif line_lower.startswith("minimumvisualstudioversion"):
                self.data['vsversion']['min'] = line_lower.split('=')[-1].strip()
            elif line_lower.startswith("visualstudioversion"):
                self.data['vsversion']['current'] = line_lower.split('=')[-1].strip()
            elif line_lower.startswith("project("):
                parse = line.split('\"')
                self.data['projects'].append(parse)