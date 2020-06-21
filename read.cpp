// reading a text file
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main (int argc , char** argv) {
  string line;
  ifstream myfile (argv[1]);
  if (myfile.is_open())
  {
	for(long j = 0; j < 200000; j++){
    	for(long i = 0 ; i < 230; i++) {
			getline (myfile,line);
			if(j%1000 == 0){
				cout << line << '\n';
			}
    	}
    	
	}
	myfile.close();
  }

  else cout << "Unable to open file"; 

  return 0;
}