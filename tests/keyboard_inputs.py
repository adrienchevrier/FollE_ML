import getch

def main():
	while 1:
		n= getch.getch()
		if n=='q':
			exit()
		elif(n=='r'):
			print("you killed yourself")
		else:
			pass

if __name__ == '__main__':
	main()