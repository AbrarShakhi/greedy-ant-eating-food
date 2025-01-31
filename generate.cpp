#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

int hole_number = 50;

int main() {
    srand(time(nullptr)); 

    std::ofstream file("info.csv"); 
    if (!file) {
        std::cerr << "Error opening file!\n";
        return 1;
    }

    file << "hole Number,reveal time,finish time,flag value,x position, y position\n";

    for(int i = 0; i < hole_number; i++) {
        int reveal = 1 + rand() % (100 - 1 + 1);
        int finish = (reveal + 1) + rand() % (101 - reveal);
        int flag = 1 + rand() % (100 - 1 + 1);
        int positionX = 1 + rand() % (800 - 1 + 1);
        int positionY = 1 + rand() % (800 - 1 + 1);

        file << i << "," << reveal << "," << finish << "," << flag << "," << positionX << "," << positionY << "\n";
    }
    
    file.close();
    
    return 0;
}
