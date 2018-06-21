#!/usr/bin/python3
import time, pychromecast, requests, json, sched

volume_set, old_volume = False, 0
cast = next(cc for cc in pychromecast.get_chromecasts() if cc.device.friendly_name == "TS1 Chromecast")
scheduler = sched.scheduler(time.time, time.sleep)
noc_url="http://changethistothenocurl.com/"

def set_volume(v):
  cast.wait()
  cast.set_volume(v)

def lower_volume(v):
  ov = cast.status.volume_level
  set_volume(ov*.8)
  return ov

def get_noc_data():
  try:
    noc = requests.get(url=noc_url).json()
    return noc
  except json.decoder.JSONDecodeError as e:
    print('Unexpected JSON response from the NOC', e)
    return None

def get_queue_status(noc_data):
  if noc_data != None:
    for ext in noc['queues']['QUEUE284']['loggedIn']:
      if ext['status'] == 6 or ext['status'] == 2: 
        return True 
  return False 

def handle_noc_volume():
  if get_queue_status(get_noc_data()): 
    old_volume = lower_volume(vol)
    volume_set = True
  else:
    set_volume(old_volume)
    volume_set = False

def main(args):
  scheduler.enter(1, 1, handle_noc_volume(), ())
  scheduler.run()

if __name__ == "__main__":
  main(sys.argv)

