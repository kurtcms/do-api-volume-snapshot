import time
from os import environ
from dotenv import load_dotenv, find_dotenv

from do_api_client import Do

class Main():
    '''
    Create and rotate the DigitalOcean volume snapshot
    '''
    def __init__(self):
        if load_dotenv(find_dotenv()) == False:
            raise SystemExit('Problem locating the .env file')

        try:
            base_url = environ['DO_BASE_URL']
            token = environ['DO_TOKEN']
            volume_id = environ['DO_VOLUME_ID']
            snapshot = environ['DO_SNAPSHOT']
        except KeyError:
            # Raise a system exit on error reading the base_url
            raise SystemExit('Problem reading the environment variables')

        self.client = Do(base_url, token)
        self.volume_id = volume_id

        try:
            snapshot = int(snapshot)
        except ValueError:
            raise SystemExit('DO_SNAPSHOT must be an interger')

        if isinstance(snapshot, int) and snapshot > 0:
            self.snapshot = snapshot
        else:
            raise SystemExit('DO_SNAPSHOT must larger than 0')

    def _list_snapshot_by_volume(self):
        snapshot = self.client.call(
                    'GET', '/volumes/' + self.volume_id + '/snapshots')
        return snapshot

    def _delete_snapshot_by_snapshot_id(self, snapshot_id):
        snapshot = self.client.call(
                    'DELETE', '/snapshots/' + snapshot_id)
        return snapshot

    def create_snapshot_from_volume(self):
        '''Create volume snapshot'''
        time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())
        snapshot = self.client.call(
                    'POST', '/volumes/' + self.volume_id + '/snapshots',
                    {
                        'name': time_stamp,
                        'tags': ['do_api_volume_snapshot']
                    })
        print('Snapshot ' + snapshot['snapshot']['name'] +
            ' is created at ' + snapshot['snapshot']['created_at'])

    def rotate_snapshot(self):
        '''Rotate the volume snapshot'''
        list_snapshot = self._list_snapshot_by_volume()
        if self.snapshot >= list_snapshot['meta']['total']:
            raise SystemExit('No snapshot needs to be rotated')
        else:
            list_snapshot_sorted = sorted(
                list_snapshot['snapshots'], key=lambda k: k['created_at'])
            for i in range(list_snapshot['meta']['total'] - self.snapshot):
                self._delete_snapshot_by_snapshot_id(
                    list_snapshot_sorted[i]['id'])
                print('Snapshot ' + list_snapshot_sorted[i]['name'] +
                ' is removed at ' +
                time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))

if __name__ == '__main__':
    conn = Main()
    conn.create_snapshot_from_volume()
    conn.rotate_snapshot()
