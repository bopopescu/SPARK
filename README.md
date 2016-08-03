# SPARK

> There are two parts of explanation in this file : **HowTo Run Spark on [Emulab](https://www.emulab.net/)** and **Unstructured Notes for Debugging**



## 1. HowTo Run Spark on [Emulab](https://www.emulab.net/)

### Overview
> The Spark that we want to build is not the full version of Spark. It means that the current Spark is not compiling any extensions for particular systems such as Hive, Docker, Flume, etc. Actually there is no difference for the main functionality if you just want to try the Spark itself. The extension is only needed when we want to integrate Spark with other systems. In this research, I do not need any external integration, so I just modify the [pom.xml](https://github.com/daniarherikurniawan/SPARK/blob/master/spark-1.6.1/pom.xml) file to compile just the necessary package for my research purpose. Besides, by reducing the number of compiled package, the size of the Spark is much more smaller (1 GB for compiling the core Spark and 4.5 GB for compiling the full Spark). That is one of the biggest reason for me because my internet connection is too slow (upload speed: 10 Kbps) to upload such a big file. According to the Spark tutorial, here is the most useful link that you should read:

- http://spark.apache.org/docs/latest/spark-standalone.html
- https://cwiki.apache.org/confluence/display/SPARK/Useful+Developer+Tools#UsefulDeveloperTools-ReducingBuildTimes

> In my case, I should build the Spark from the source, so I can ignore some explanations in those documents that are not related to it. First of all we need to download any version of Spark source from http://spark.apache.org/downloads.html . Basically, there are two different type of build process. The first one is according to this (http://spark.apache.org/docs/latest/building-spark.html) link. It will take a long time to finish. I tried that out by entering this command 

```sh
build/mvn -Pyarn -Phadoop-2.7 -Dhadoop.version=2.7.0 -DskipTests clean package
```

> It is success after solving some problem in the pom.xml files. You have to make sure that the version of Hadoop you gave above is the same with the version in the pom file. The error will show you wich pom file that cause an error. However, this way of building Spark is not suitable for my condition because I do not have much time to wait >10 minutes each time I modify the source code that I need to re-build.

> The second is faster than before. All the explanation is described at [this file] (https://cwiki.apache.org/confluence/display/SPARK/Useful+Developer+Tools#UsefulDeveloperTools-ReducingBuildTimes) in detail. Generally, it is so simple but I faced a lot of problem. Btw, here is the specs of my machine that I use to build the source:

- Core i7 Ram 12 GB, Ubuntu Gnome, Java 8, Maven 3.3.9, Python, Scala, and Hadoop are installed.
- Core 2 Duo (Emulab Machine) Ram 2 GB, Fedora15, Java 8 (manual installation), disk agent, mvn, ant and ssh python.

> Here is the step by step process that we need to follow in order to realize the main goal (Run and compile Spark on Emulab)

###Step by Step
1. Download the Spark's source codes or just simply clone this repository in your local machine. The version that I use in this repo is 1.6.1.
2. Edit the pom.xml file so it just compile the core Spark. It will reduce the compile time and the size as well.
3. Create a normal assembly. All of the codes and jars should be kept as its original position. The total size is around 700MB.

	``` $ build/sbt clean assembly```

4. Upload all the codes and jars to Emulab. You can use Github, but it cannot be done easily because Github only allows maximum 100 MB size for a single file. You can include that file into gitignore and add it later. There are some ways to upload the file that is bigger than 100 MB, including: Use Filezilla, upload to Google Drive, and Upload as Github released apps. I reccomend you to use the first technique after working around. 
5. Now, we can continue our work on Emulab. As I mention before, the OS Image that I use is FEDORA15-DAGENT-JAVA. I think we can use any other OS as long as it is compatible with Java 8.

6. Upload manual to the Emulab the jar of spark-1.6.1/assembly/target/scala-2.10/ using Filezilla [you can ignore this step if you don't have enough internet speed]

7. Since the OS that I used is not having java 8. Here are the way to install and set the environment variable. We have to do this every single time we start Emulab.
	```
	wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u92-b14/jdk-8u92-linux-i586.rpm"

	mv jdk-8u92-linux-i586.rpm********* jdk-java-8.rpm

	sudo yum localinstall jdk-java-8.rpm

	setenv JAVA_HOME /usr/java/jdk1.8.0_92/jre
	``` 
	> If you clone this repository, you can simply run ***bash scripts.sh*** right after login in the emulab server. To update the script, you can run 
	```
	cp /proj/cs331-uc/daniar/SPARK/EMULAB/scripts.sh /users/daniar/ 
	chmod u+x scripts.sh
	and run:
	bash scripts.sh 
	move directory to:
	cd /proj/cs331-uc/daniar/SPARK/spark-1.6.1/
	```

	> In the above script, I clone the repository at cp /proj/cs331-uc/daniar/SPARK/ and /users/daniar/ is my current directory after I got logged in.  


8. Then tell the Spark that we would not compile everything from the start
	
	``` 
	setenv SPARK_PREPEND_CLASSES true 
	or
	export SPARK_PREPEND_CLASSES=true [if you are working on Ubuntu]
	``` 

9. Do some local development! You can modify the source in ***core*** folder as you need and then run:
	
	``` sudo build/sbt compile -mem 1500 evicted ```
	
	To compile just the core and it just need a few minutes. 
	***[Note: It will failed at the first try due to dependency error. But after the second try it will success]***
	Btw, you have to make sure that your Spark is not running during this step. You can simply run :

	``` ./sbin/stop-all.sh ```

	To stop any Spark instances.

10. Run the Spark as described in [this file](http://spark.apache.org/docs/latest/spark-standalone.html). The simple one is by running :
	
	``` ./sbin/start-all.sh ```
	
	or

	``` 
	./sbin/start-master.sh

	./sbin/start-slave.sh spark://n1.testspark.cs331-uc.emulab.net:7077 --memory 1g --cores 2
	```

11. Create the payload. It depends on what kind of process you need. In my case, I want Spark to sort the array of integers in ascending order and then save the result in the folder generated_file/result_py. So I create a Python program to generate the integers by running:
	
	``` python res-generator/generate_list_int.py ```

12. All of the task will be run as Python apps which can be found in file [sort.py](https://github.com/daniarherikurniawan/SPARK/blob/master/spark-1.6.1/sort.py). You can create your own task and specify the process as you need. To submit the app, use this following command:

	``` 
	for Emulab: 
	./bin/spark-submit sort.py --master spark://n1.testspark.cs331-uc.emulab.net:7077 --deploy-mode cluster --num-executors 4
	
	for localhost: 
	./bin/spark-submit sort_localhost.py --master spark://daniar-X450JF:7077 --deploy-mode cluster --num-executors 1

	```


13. The log files will be stored in folder [generated_driver_log](https://github.com/daniarherikurniawan/SPARK/tree/master/generated_driver_log).

14. For the ease, you can retrieve the html page of master and slave nodes by running:
	
	```wget -O - "http://localhost:8080/" >> spark_home.html```

	Of course you need to know the URL in order to get the detail visualizations. You can get the URL by opening Spark visualization when you run Spark in your local machine. In Emulab, we cannot exactly see the web page. That is why you need to understand the bigger picture of the visualization before analyzing the downloaded html page from Emulab's node.

	> Apparently, you don't need to download all the page manually. You can visit *http://n1.testspark.cs331-uc.emulab.net:8080/ *. The link is not always the same, it depends on your project name, your experiment name, and the port that is open in your Emulab server.




## 2. Configure Emulab

### Create the ns file
```
set ns [new Simulator]                  
source tb_compat.tcl

set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]

set lan0 [$ns make-cloud "$n1 $n2 $n3 $n4" 100Mb 0ms]

tb-set-node-lan-bandwidth $n2 $lan0 20Mb

tb-set-node-os $n1 FEDORA15-DAGENT-JAVA
tb-set-node-os $n2 FEDORA15-DAGENT-JAVA
tb-set-node-os $n3 FEDORA15-DAGENT-JAVA
tb-set-node-os $n4 FEDORA15-DAGENT-JAVA

#d710
tb-set-hardware $n1 pc3000
tb-set-hardware $n2 pc3000
tb-set-hardware $n3 pc3000
tb-set-hardware $n4 pc3000

tb-set-node-rpms $n1 /proj/cs331-uc/resources//iperf-2.0.5-3.fc15.i686.rpm
tb-set-node-rpms $n2 /proj/cs331-uc/resources//iperf-2.0.5-3.fc15.i686.rpm
tb-set-node-rpms $n3 /proj/cs331-uc/resources//iperf-2.0.5-3.fc15.i686.rpm
tb-set-node-rpms $n4 /proj/cs331-uc/resources//iperf-2.0.5-3.fc15.i686.rpm

$ns run
```

### Slow down the link/network
> You can modify the bandwidth by declaring the necessary value in the ns file. The detail tutorial about the syntax can be found at [https://wiki.emulab.net/wiki/Emulab/wiki/nscommands](https://wiki.emulab.net/wiki/Emulab/wiki/nscommands) If you need to modify the bandwidth on the fly, then you can use the menu in the Emulab project called ***Modify Traffic Shaping***. After entering the needed bandwidth value, you should check the **save** and then click the **execute** button.


## 3. Unstructured Notes for Debugging

### Check the bandwidth
> We will use iperf tool to check the bandwidth, you can read the detail at : [iperf.fr](https://iperf.fr/). Here is the simple tutorial that suitable to our needs: [http://www.slashroot.in/iperf-how-test-network-speedperformancebandwidth](http://www.slashroot.in/iperf-how-test-network-speedperformancebandwidth). I wrapped it up in the following points:

- There is two syntax, the first to be run on the host and the second is for the client.
- The idea is iperf will transfer some amount of data from the client to the host and then they will record the bandwidth.
- Here is the script:

```
for the host/server (it will listen for the incoming package from the client) :
iperf -s    (suppose that the IP is 10.1.1.3) 

for the client :
iperf -c 10.1.1.3  

you should run the second script in every other node in order to know the bandwidth 
between the host and the specified client nodes

``` 


### Check which file is slowing down the git push :

- **Write all file SHA1s to a text file:**

	git rev-list --objects --all | sort -k 2 > allfileshas.txt

- **Sort the blobs from biggest to smallest and write results to text file:**

	git gc && git verify-pack -v .git/objects/pack/pack-*.idx | egrep "^\w+ blob\W+[0-9]+ [0-9]+ [0-9]+$" | sort -k 3 -n -r > bigobjects.txt

- **Combine both text files to get file name/sha1/size information:**
	
	for SHA in `cut -f 1 -d\  < bigobjects.txt`; do
		echo $(grep $SHA bigobjects.txt) $(grep $SHA allfileshas.txt) | awk '{print $1,$3,$7}' >> bigtosmall.txt 
	done;

- **Now you can look at the file bigtosmall.txt in order to decide which files you want to remove from your Git history.**



### Generate integer to be sorted:
	python res-generator/generate_list_int.py



### Run the cluster
```sh
cd spark-1.6.1/

$ build/sbt clean assembly # Create a normal assembly

$ export SPARK_PREPEND_CLASSES=true

$ build/sbt compile
# ... do some local development ... #

./sbin/start-master.sh --host '192.168.1.3'

spark://n2.testspark.cs331-uc.emulab.net:7077

./sbin/start-slave.sh spark://n1.testspark.cs331-uc.emulab.net:7077 --memory 1g --cores 2

./sbin/start-slave.sh spark://daniar-X450JF:7077 --memory 1g --cores 2

./sbin/start-slave.sh spark://192.168.1.3:7077 --host '192.168.1.12' --memory 1g --cores 2

./bin/spark-submit sort.py --master spark://n2.testspark.cs331-uc.emulab.net:7077 --deploy-mode cluster 
```



### Install java 8
```sh
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u92-b14/jdk-8u92-linux-i586.rpm"

mv jdk-8u92-linux-i586.rpm********* jdk-java-8.rpm

sudo yum localinstall jdk-java-8.rpm

setenv JAVA_HOME /usr/java/jdk1.8.0_92/jre
```
	

### Install maven 3.3.3 (not needed | Just FYI)

```sh
wget http://mirror.olnevhost.net/pub/apache/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz

tar xvf apache-maven-3.3.3-bin.tar.gz

setenv M2 /users/daniar/MAVEN/apache-maven-3.3.3
```



### Scratch 
- setenv SPARK_PREPEND_CLASSES true
- sudo build/sbt clean assembly -mem 1500 evicted
- sudo build/sbt compile -mem 1500 evicted (make sure that master and slave are terminated)



### Additional notes
- sha1sum file.jar
- wget -O - "http://localhost:8080/" >> spark_home.html
- copy folder: cp SPARK/ backup_spark/ -r
- check size : du -sh file.txt
- find a word in the file folder : grep -nr 'yourString*' .
	or [in sublime](http://stackoverflow.com/questions/20519040/search-in-all-files-in-a-project-in-sublime-text-3) 


###Finding
- we can specify minimum core to start the process
- worker will connect to driver
- worker will create executor as the number specified when submitting the app
- CoarseGrainedExecutorBackend will be run by the worker 
- TaskSchedulerImpl:
	The task id is consist of two index X.Y. So the first task is marked as 0.0. If the task is duplicated, the Y index will be incremented. The 0.0 task will be duplicated to 0.1. If one of them is finished, the driver will ignore the other redundant tasks. 

	The driver offers task to every worker that will be managed in this class. Since the number of partition is two, it will choose the most two available worker to run the task. So far, the worker that run both of the partition are always the same because I sorted the tasks by its taskid. 


- FileSystemPersistenceEngine
	 * Stores data in a single on-disk directory with one file per application and worker.
	 * Files are deleted when applications and workers are removed.

- SparkSubmitArguments
	
	```
	def isStandaloneCluster: Boolean = {
    	master.startsWith("spark://") && deployMode == "cluster"
  	}
  	```

- 