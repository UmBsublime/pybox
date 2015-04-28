from subprocess import check_output

from wheel import WheelText
from variables import *


def cmd(command):
    result = check_output(command, shell=True)
    return result


def ipconfig():
    interfaces = cmd("ifconfig | grep 'Link encap'  | awk '{print $1}'").split('\n')
    ips = cmd("ifconfig | grep 'inet addr' | awk '{print $1 $2}' | cut -d: -f2").split('\n')
    subnets = cmd("ifconfig | grep 'inet addr' | awk '{print $NF}' | cut -d: -f2").split('\n')

    for interface in interfaces:
        if interface == '':
            interfaces.remove(interface)
    for ip in ips:
        if ip == '':
            ips.remove(ip)
    for subnet in subnets:
        if subnet == '':
            subnets.remove(subnet)

    result = []
    for i in range(len(interfaces)):
        result.append(interfaces[i])
        result.append(ips[i])
        result.append(subnets[i])
        result.append('-'*16)

    return result


def uptime():
    result = cmd('uptime')
    load = result.split(' ')[-3:]
    up = result.split(',')[0].split('up')[1].strip(' ')
    return ('{:^16}'.format(up),
            '{}  {}  {}'.format(load[0].strip(','),
                                load[1].strip(','),
                                load[2].strip(',')))


def mem_info():
    mem_total = cmd("grep MemTotal /proc/meminfo | awk '{print $2NF}'")
    mem_total = 'MemTotal:' + str(int(mem_total)/1024)+'Mb'
    mem_free = cmd("grep MemFree /proc/meminfo | awk '{print $2NF}'")
    mem_free = 'MemFree: ' + str(int(mem_free)/1024)+'Mb'
    return mem_total, mem_free


def hostname():
    result = cmd('hostname')
    date = cmd('date +"%b %d %H:%M:%S"')
    return '{:^16}'.format(result.strip('\n')), date.strip('\n')

def help():
    help = ['pybox 0.1',
            '----------------',
            'Use Up/Down to',
            'navigate through',
            'the menus',
            '----------------',
            'Everything that',
            'scrolls, loops',
            '----------------',
            'Use Right to',
            'select an option',
            '----------------',
            'Use Left to go',
            'back',
            '----------------',
            'Back all the',
            'way to exit',
            '----------------']
    return help

def who():
    command = r''' w | tail -n +3| awk '{print $1" "$4}' '''
    who = cmd(command).split('\n')

    final = ['{:<7} {:<8}'.format('USER', 'LOGIN@'),
             '-'*16]
    for w in who:
        w = w.split(' ')
        if len(w) >= 2:
            final.append('{:<7} {:<8}'.format(w[0], w[1]))
    final.append('-'*16)
    return final

def df():
    from collections import deque
    command = r''' df | grep -v "Filesystem" | awk '{$1=""; print $2" "$5" "$6}' | uniq '''
    all_parts = cmd(command).split('\n')
    sorted_part = ['{:<6} {:>3} {:>5}Gb'.format('mount', '%', 'size')]
    for part in all_parts:
        part = part.split(' ')

        if len(part) >= 3 and len(part[2]) <= 6:
            pretty = '{:<6} {:>3} {:.2f}Gb'.format(part[2],
                                               part[1],
                                               float(part[0])/1024/1024)
            sorted_part.append(pretty)
            print repr(pretty)



    print (sorted_part)
    return sorted_part

def ls():
    result = cmd('ls').split('\n')
    for e in result:
        if e == '':
            result.remove(e)


    return result
