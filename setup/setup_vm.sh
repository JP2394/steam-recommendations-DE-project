#!/bin/bash

# Run using ./setup.sh

if ! [ -d ./bin ];
then
    echo -e '\nCreating ~/bin directory\n'
	echo "=============================================================================="
	echo "---------------------- 'Creating bin directory' -----------------------------"
	echo "=============================================================================="
    mkdir -p bin
fi

if ! [  -d ./bin/anaconda3 ]; then
    cd bin
	echo "=============================================================================="
	echo "---------------------- Installing anaconda3!----------------------------------"
	echo "=============================================================================="
    wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh -O ./Anaconda3-2021.11-Linux-x86_64.sh
    echo -e "Running anaconda3 script..."
    # -b run install in batch mode (without manual intervention), it is expected the license terms are agreed upon
    # -p install prefix, defaults to $PREFIX, must not contain spaces.
    bash ./Anaconda3-2021.11-Linux-x86_64.sh -b -p ~/bin/anaconda3
    rm ./Anaconda3-2021.11-Linux-x86_64.sh


	echo -e "activating conda..."
    #activate conda
    eval "$(/home/$USER/bin/anaconda3/bin/conda shell.bash hook)"

    echo -e "Running conda init..."
    conda init
    # Using -y flag to auto-approve
    echo -e "Running conda update..."
    conda update -y conda

    cd
else
    echo -e "anaconda already installed."
fi

	echo "=============================================================================="
	echo "---------------------- Running sudo apt-get update...-------------------------"
	echo "=============================================================================="
	      sudo apt-get update


	echo "=============================================================================="
	echo "-------------------------- Installing Docker......----------------------------"
	echo "=============================================================================="
	      sudo apt-get -y install docker.io

	echo "=============================================================================="
	echo "-------------------------- Installing docker-compose...-----------------------"
	echo "=============================================================================="
	
        cd 
        cd bin
        wget https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -O docker-compose
        sudo chmod +x docker-compose


	echo "=============================================================================="
	echo "-------------------------- Installing Terraform......-------------------------"
	echo "=============================================================================="
	
		wget https://releases.hashicorp.com/terraform/1.1.4/terraform_1.1.4_linux_amd64.zip
		sudo apt-get install unzip
		unzip terraform_1.1.4_linux_amd64.zip
		rm terraform_1.1.4_linux_amd64.zip


	echo "=============================================================================="
	echo "-------------------------- Installing java 11 .........-----------------------"
	echo "=============================================================================="
			cd
			mkdir spark
			wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
			tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz -C spark/
			rm openjdk-11.0.2_linux-x64_bin.tar.gz
			
	echo "=============================================================================="
	echo "-------------------------- Installing Spark .........-------------------------"
	echo "=============================================================================="		
		wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
		tar xzfv spark-3.3.2-bin-hadoop3.tgz -C spark/
		rm spark-3.3.2-bin-hadoop3.tgz	
					

	echo "=============================================================================="
	echo "---------------------------------Setup .bashrc .........----------------------"
	echo "=============================================================================="
		
		echo 'export PATH="${HOME}/bin:${PATH}"' >> ~/.bashrc
		
		echo 'export JAVA_HOME="${HOME}/spark/jdk-11.0.2"' >> ~/.bashrc
		echo 'export PATH="${JAVA_HOME}/bin:${PATH}"' >> ~/.bashrc
		
		echo 'export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"' >> ~/.bashrc
		echo 'export PATH="${SPARK_HOME}/bin:${PATH}"' >> ~/.bashrc
		
	    echo 'export GOOGLE_APPLICATION_CREDENTIALS="${HOME}/.google/credentials/google_credentials.json"' >> ~/.bashrc

		echo 'export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"' >> ~/.bashrc
		echo 'export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"'  >> ~/.bashrc


# Install Astronomer
	echo "=============================================================================="
	echo "----------------- Installing Astronomer for Apache Airflow -------------------"
	echo "=============================================================================="
		curl -sSL install.astronomer.io | sudo bash -s

# eval "$(cat ~/.bashrc | tail -n +10)" # A hack because source .bashrc doesn't work inside the script
# However, this eval hack does not work when executing ./setup.sh but works when executing . ./setup.sh (which means run script in current shell)
# So it is better just to use newgrp at the end of the script


	echo "=============================================================================="
	echo "-------------------- Setting up Docker without sudo setup .........------------"
	echo "=============================================================================="
		sudo groupadd docker 
		sudo usermod -aG docker $USER  
		newgrp docker
