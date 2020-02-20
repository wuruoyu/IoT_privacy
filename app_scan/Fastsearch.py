import pickle

class Fastsearch:
    def __init__(self, string):
        self.string = string
        file_name = 'results_' + string + '_all.db'
        self.path = os.path.join('./fastsearch', file_name) 
        self.result = pickle.load(open(self.path, "rb"))
        self.apps = self.get_apps()

    def get_apps(self):
        apps = set()
        for app in self.result:
            for file_name in self.result[app]:
                if file_name.endswith('.smali'):
                    apps.add(app)
        return apps


