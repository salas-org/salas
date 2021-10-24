
source ../conf/0_load_conf.sh

# need write on all directories for the deletes to succeed
read -p "This will remove all patched ethereum for this node from your system. Do you want to continue? y/n [n] " yn
case $yn in
    [Yy]* ) ;;
    [Nn]* ) exit;;
    * ) exit;;
esac

# removing data from chain
echo "removing $ETHPATH (if exists)"
if [ -d "$ETHPATH" ]; then echo "found $ETHPATH, modifying permissions"; chmod -R 777 $ETHPATH; fi
if [ -d "$ETHPATH" ]; then echo "found $ETHPATH, removing"; rm -rf $ETHPATH; fi   
