For this lab, I was to expand on the previous lab to include Threading and
Mutex instead of using fork to handle multiple clients.

the program will be able to handle files that have the same name by adding a
number to the end of the file name.

example:
	if you are transfering a file named foo.txt and a file with the same
	name is already present on the server. the file will be saved as a new
	file named foo(2).txt and so on.


to run the program simply run the server program framedThreadServer.py before
running the client program framedThreadClient.py. The client program will
client threads that are all sending the same file to demonstrate how the
server saves files with similar names.
