import os
import sys
import time
import yaml
import argparse
import subprocess
import schedule
import signal


parser = argparse.ArgumentParser()
parser.add_argument('--cfg', type=str, default='config.yaml')
args = parser.parse_args()


def send_message_now(env):
    print("running...")
    subprocess.run([f"{sys.executable}", "main.py"], env=env)
    return


def signal_handler(signum, frame):
    print("\n程序结束！")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    with open(args.cfg, "r", encoding="utf-8") as fd:
        config = yaml.safe_load(fd)
    config['USER_ID'] = '\n'.join(config['USER_ID'])

    if type(config['BIRTHDAY']) is list:
        config['BIRTHDAY'] = '\n'.join(config['BIRTHDAY'])
    else:
        config['BIRTHDAY'] = config['BIRTHDAY']

    env = {**os.environ, **config}
    print("开始运行，等待定时触发...")

    schedule.every().day.at(config['DAILY_TIME']).do(send_message_now, env)

    while True:
        schedule.run_pending()
        time.sleep(50) # wait
