#!/usr/bin/env python

import boto
import sys
import os
from os.path import expanduser
from time import sleep

if __name__=='__main__':

    if len(sys.argv) == 1:
        print "usage:" , sys.argv[0] , "<ami> <keypair> <n>"
        sys.exit(1)

    ami = sys.argv[1]
    keypair = sys.argv[2]
    num_instances = sys.argv[3]

    f = open('%s/.awssecret' % expanduser('~'), 'r')
    AWS_KEY = f.readline().strip()
    AWS_SECRET = f.readline().strip()
    f.close()

    print AWS_KEY
    print AWS_SECRET

    print "connecting to ec2"
    ec2_conn = boto.connect_ec2(AWS_KEY, AWS_SECRET)

    print "getting image", ami
    images = ec2_conn.get_all_images(image_ids=[ami])

    print "requesting", num_instances , "instance(s)"
    rsrv = images[0].run(1, num_instances, keypair)

    f = open('instances','w')
    pending = list(rsrv.instances)
    running = []
    configured = []
    while len(configured) < len(rsrv.instances):

        print "pending:" , pending
        print "running:" , running
        print "configured: " , configured
        for instance in rsrv.instances:

            print "checking" , instance.id
            instance.update()

            if instance.state == 'running':
                if instance not in running:
                    print instance.id , "is up at" , instance.dns_name
                    f.write('%s %s\n' % (instance.id, instance.dns_name))
                    pending.remove(instance)
                    running.append(instance)
            else:
                print "still pending"
                
            if (instance in running) and (instance not in configured):
                print "configuring" , instance.id
                cmd="ssh -o StrictHostKeyChecking=no -i ~/.ec2/*-%s ubuntu@%s 'hostname'" % (keypair, instance.dns_name)
                status = os.system(cmd)

                if status == 0:
                    cmd="cat setup | ssh -o StrictHostKeyChecking=no -i ~/.ec2/*-%s ubuntu@%s &> %s.log &" % (keypair, instance.dns_name, instance.id)
                    print cmd
                    status = os.system(cmd)

                    configured.append(instance)
                else:
                    print "configuration failed"

        print "sleeping"
        sleep(10)

    f.close()
