cd ../

git pull

sudo docker rm -f $(sudo docker ps -aq)
sudo docker rmi -f $(sudo docker images -q)

echo "> Build Docker Image"
sudo docker build -t comfortchat .

echo "> Run Docker Container"
sudo docker run --name api -d -p 80:80 comfortchat
