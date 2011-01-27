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
    pending = rsrv.instances
    while len(pending) > 0:
        for instance in pending:

            print "checking" , instance.id
            instance.update()

            if instance.state == 'running':
                print instance.id , "is up at" , instance.dns_name
                pending.remove(instance)

                f.write('%s %s\n' % (instance.id, instance.dns_name))

                cmd="cat setup | ssh -o StrictHostKeyChecking=no -i ~/.ec2/*-%s ubuntu@%s &> %s.log &" % (keypair, instance.dns_name, instance.id)

                print cmd
                os.system(cmd)
                
            else:
                print "still pending"
                
        sleep(10)

    f.close()
