#!/bin/bash

copy(){
    init_script=(exp attack submit_flag init_hosts check)

    for var in ${init_script[@]};
    do
        cp $var "${1}${count}"
    done
}

create_dir(){

    if [ ! -d "${1}${2}"  ];then
        mkdir "${1}${2}"
      else
            echo "dir exist"
    fi

}

for((count=1; count < 4; count++));
do
    
    create_dir web $count
    copy web $count

    create_dir pwn $count
    copy pwn $count

done
