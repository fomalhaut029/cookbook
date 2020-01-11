#!/bin/bash

set -eux
set -o pipefail


NODE_NAME=$1
RAM=$2
DISK=$3
VCPUS=$4
HOST_CPU_ARCH=$5
RESOURCE_CLASS=$6
NODE_IPMI_ADDRESS=$7
NODE_IPMI_PORT=$8
NODE_IPMI_TERMINAL_PORT=$9
NODE_IPMI_USER=${10}
NODE_IPMI_PASS=${11}
NODE_NIC_MAC=${12}
SWITCH_ID=${13}
SWITCH_INFO=${14}
SWITCH_PORT_ID=${15}

echo Configuring Ironic node.
openstack baremetal node create --network-interface neutron --driver ipmi --name ${NODE_NAME}
NODE_UUID=$(openstack baremetal node list|grep ${NODE_NAME} |awk -F "| " '{print $2}')

openstack baremetal node set ${NODE_UUID} \
    --driver-info ipmi_username=${NODE_IPMI_USER} \
    --driver-info ipmi_password=${NODE_IPMI_PASS} \
    --driver-info ipmi_address=${NODE_IPMI_ADDRESS} \
    --driver-info ipmi_port=${NODE_IPMI_PORT}


DEPLOY_VMLINUZ_UUID=$(openstack image list|grep deploy-vmlinuz|awk -F "| " '{print $2}')
DEPLOY_INITRD_UUID=$(openstack image list|grep deploy-initrd|awk -F "| " '{print $2}')

openstack baremetal node set ${NODE_UUID} \
    --driver-info deploy_kernel=${DEPLOY_VMLINUZ_UUID} \
    --driver-info deploy_ramdisk=${DEPLOY_INITRD_UUID}

openstack baremetal node set ${NODE_UUID} \
    --property cpus=${VCPUS} \
    --property memory_mb=${RAM} \
    --property local_gb=${DISK} \
    --property cpu_arch=${HOST_CPU_ARCH}

openstack baremetal node set --instance-info capabilities='{"boot_option": "local"}' ${NODE_UUID}

openstack --os-baremetal-api-version 1.21 baremetal node set ${NODE_UUID} \
    --resource-class $RESOURCE_CLASS

openstack baremetal port create --node ${NODE_UUID} \
    --local-link-connection switch_id=${SWITCH_ID} \
    --local-link-connection switch_info=${SWITCH_INFO} \
    --local-link-connection port_id=${SWITCH_PORT_ID} \
    --pxe-enabled true \
    --physical-network physnet1 ${NODE_NIC_MAC}

echo "Configure console enabled"

openstack --os-baremetal-api-version 1.31 baremetal node set ${NODE_UUID} \
    --console-interface ipmitool-socat
openstack baremetal node set ${NODE_UUID} --driver-info ipmi_terminal_port=${NODE_IPMI_TERMINAL_PORT}
openstack baremetal node console enable ${NODE_UUID}

sleep 5s
openstack baremetal node manage ${NODE_UUID}

sleep 5s

openstack baremetal node list |grep $NODE_UUID|grep enroll

if [ $? -eq 0 ];then
    openstack baremetal node provide ${NODE_UUID}
else
    echo "状态异常"

openstack baremetal node list
