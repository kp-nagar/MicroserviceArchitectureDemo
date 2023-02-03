sudo rm -r ../setup_temp
sudo rm -r ../micro_util/build

sudo mkdir ../setup_temp
sudo cp -r ../micro_util ../setup_temp
sudo cp -r ../Account ../setup_temp

docker-compose down && docker system prune && docker-compose up --build

sudo rm -r ../setup_temp