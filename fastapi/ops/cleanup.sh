# Kill service
docker kill snek-it-test
# Kill database
docker kill snek-db
# Cleanup Images (Optional)
docker rmi snek:chatting snek:it-test snek:migration snek:base
