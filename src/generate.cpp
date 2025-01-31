#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iostream>
#include <random>

int hole_number = 50;
int WIDTH = 1200;
int HEIGHT = 800;

// std::default_random_engine default_engine;
auto clock_seed = std::chrono::steady_clock::now().time_since_epoch().count();
// std::random_device rd_seed;
std::mt19937 mersenne_twister_engine((uint32_t)clock_seed);
int randint(int a, int b) {
	return std::uniform_int_distribution<int>(a, b)(mersenne_twister_engine);
}

int main() {
	srand(time(nullptr));

	std::ofstream file("info.csv");
	if (!file) {
		std::cerr << "Error opening file!\n";
		return 1;
	}

	file << "hole Number,reveal time,finish time,dot value,x position, y "
	        "position\n";

	for (int i = 0; i < hole_number; i++) {
		int reveal = randint(1, 100);
		int finish = reveal + randint(1, 10);
		int dot_val = randint(3, 10);
		int positionX = randint(5, WIDTH - 5);
		int positionY = randint(5, HEIGHT - 5);

		file << i << "," << reveal << "," << finish << "," << dot_val << ","
		     << positionX << "," << positionY << "\n";
	}

	file.close();

	return 0;
}
