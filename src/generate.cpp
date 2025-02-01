#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>

int number_of_foods = 50;
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
	const char *filename = "info.csv";

	std::ofstream file("info.csv");
	if (!file) {
		std::cerr << "Error opening file!\n";
		return 1;
	}

	file << "food_number,"
	        "food_appear_time,"
	        "food_waste_time,"
	        "taste_value,"
	        "x_pos,"
	        "y_pos\n";

	for (int food_number = 0; food_number < number_of_foods; food_number++) {
		int food_appear_time = randint(1, 100);
		int food_waste_time = food_appear_time + randint(1, 10);
		int taste_value = randint(5, 13);
		int x_pos = randint(5, WIDTH - 5);
		int y_pos = randint(5, HEIGHT - 5);

		file << food_number << "," << food_appear_time << "," << food_waste_time
		     << "," << taste_value << "," << x_pos << "," << y_pos << "\n";
	}

	std::cout << number_of_foods << " Number of foods has been written in "
	          << filename << '\n';

	file.close();

	return 0;
}
