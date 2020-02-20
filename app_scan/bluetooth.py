import pickle
import os
from IPython import embed

class Fastsearch:
    def __init__(self, string, type):
        self.string = string
        file_name = 'results_' + string + '_all.db'
        self.path = os.path.join('./fastsearch', file_name) 
        self.result = pickle.load(open(self.path, "rb"))
        if type == 'pm':
            self.apps = self.get_apps_pm()
        elif type == 'code':
            self.apps = self.get_apps_code()
        else:
            raise Exception

    def get_apps_code(self):
        apps = set()
        for app in self.result:
            for file_name in self.result[app]:
                if file_name == 'AndroidManifest.xml':
                    apps.add(app)
        return apps

    def get_apps_pm(self):
        apps = set()
        for app in self.result:
            for file_name in self.result[app]:
                if file_name.endswith('.smali'):
                    apps.add(app)
        return apps

bt_pm = Fastsearch("android.permission.BLUETOOTH", 'pm')
fine_pm = Fastsearch("android.permission.ACCESS_FINE_LOCATION", 'pm')
coarse_pm = Fastsearch("android.permission.ACCESS_COARSE_LOCATION", 'pm')

# bt_pm + (fine_pm, coarse_pm)
bt_good_pm = bt_pm.apps.intersection(fine_pm.apps.union(coarse_pm.apps))

# with BluetoothDevice, BluetoothAdapter or BluetoothServerSocket in code
bt_device = Fastsearch("BluetoothDevice", 'code')
bt_socket = Fastsearch("BluetoothSocket", 'code')
bt_adapter = Fastsearch("BluetoothAdapter", 'code')
bt_server = Fastsearch("BluetoothServerSocket", 'code')
interface_list = [bt_device.result, bt_socket.result, bt_adapter.result, bt_server.result]
interface_union = set().union(*interface_list)

# pm with interface
bt_app = bt_good_pm.intersection(interface_union)

with open('./list/bluetooth.pickle', 'wb') as file:
    pickle.dump(bt_app, file)
    pass
