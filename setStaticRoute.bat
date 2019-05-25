route print
route delete 0.0.0.0
route -p add 10.0.0.0 mask 255.0.0.0 10.85.1.254 metric 1
route -p add 0.0.0.0 mask 0.0.0.0 172.20.10.1 metric 1
route -p add 0.0.0.0 mask 0.0.0.0 10.85.1.254 metric 2