# Python Port Scanner
The purpose of this script is to show the simplicity of creating an average port scanning program in python. Provided with an IP address or a host web address as well as a list of port numbers, the script will 
determine if the host has any ports open as listed. The script is multi threaded and uses a priority queue to asynchronously test the given ports. It also makes use of the very handy argparse library in python
