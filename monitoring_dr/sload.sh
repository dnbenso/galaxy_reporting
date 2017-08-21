#!/bin/bash
#
# [DNB 2017-08-21] Script to give realtime current queue information. Must
# install sacct on SLURM cluster prior to running. Requires sudo without pass.
#
if [ "$#" -eq "0" ]
then
	echo `basename $0` "[repeat_delay_secs|batch]"
	exit 1
fi
#
while true
do
	clear
	WORKERS=`sinfo -N | awk '/^w/ {
	NODES = $2 + NODES
} END {
print NODES
    }'`
    #
    USED_WORKERS=`squeue | awk '/ w[0-9]/ {
    LOAD[$NF] = LOAD[$NF] + $(NF-1);
    } END {
    k=0
    for (i in LOAD) k++
	    print k }'`
	    #
	    TOTAL_USED_CPUS=`squeue | awk '/ w[0-9]/ {
	    TOTAL = TOTAL + $(NF-1);
    }
    END {
    print TOTAL
    }'`
    #
    squeue | awk 'BEGIN {
    k=0
    i=0
    }
    / w[0-9]/ {
    LOAD[$NF] = LOAD[$NF] + $(NF-1)
    TOTAL = TOTAL + $(NF-1)
    }
    END {
    for (i in LOAD) k++
	    print "\033[31m____________________\033[33m\nWorker\t\033[31m|\033[33m  Free CPUs\n\033[31m--------------------\033[0m"
	    for (var in LOAD) {
		    print "\033[32m" var "\t\033[31m|\033[0m\t\033[34m" 16 - LOAD[var] "\033[0m"
	    }
	    print "\033[31m--------------------\033[0m"
    }' 
    #
    echo -e "\n\e[33mFree workers:\t\t\e[34m $(($WORKERS-$USED_WORKERS)) \e[0m"
    if [ ! $TOTAL_USED_CPUS ];then
	    TOTAL_USED_CPUS=0
    fi
    echo -e "\e[33mTotal free CPUs:\t\e[34m $((($WORKERS*16)-$TOTAL_USED_CPUS))\e[0m / \e[34m$(($WORKERS*16))\e[0m\n"
    sacct -o jobid%-6,jobname%-60,alloccpus,elapsed,NodeList%9 -a --state RUNNING
    echo
    sinfo
    GALAXY_Q=`sudo su -c "psql -p 5930 -c \"select j from job j where j.state = 'queued'\"" galaxy | awk -F'[( ]' '/rows/ { print $2 }'`
    if [ "$1" == "batch" ];then
	    echo -e "\n-----------------------------"
	    echo "Jobs queued within galaxy: ${GALAXY_Q}"
	    break
    fi
    echo -e "\n\e[31m-----------------------------\e[0m"
    echo -e "\e[33mJobs queued within galaxy: \e[34m${GALAXY_Q}\e[0m"
    sleep $1
done

