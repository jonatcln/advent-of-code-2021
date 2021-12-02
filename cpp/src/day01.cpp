#include <iostream>
#include <fstream>
#include <vector>
#include <string>

unsigned int part1(const std::vector<unsigned int> &);
unsigned int part2(const std::vector<unsigned int> &);

int main(int argc, char *argv[])
{
	std::ifstream input_file;
	input_file.open(argv[1]);

	if (!input_file.is_open())
	{
		std::cerr << "Opening input file failed!" << std::endl;
		return 1;
	}

	std::vector<unsigned int> numbers;

	for (std::string line; std::getline(input_file, line);)
	{
		numbers.push_back(stoi(line));
	}

	input_file.close();

	std::cout << "Part 1: " << part1(numbers) << std::endl;
	std::cout << "Part 2: " << part2(numbers) << std::endl;
	return 0;
}

unsigned int part1(const std::vector<unsigned int> &numbers)
{
	unsigned int increased = 0;
	for (auto it = numbers.begin(); it != numbers.end() - 1; ) {
		if (*it++ < *it)
			++increased;
	}
	return increased;
}

unsigned int part2(const std::vector<unsigned int> &numbers)
{
	unsigned int increased = 0;
	for (auto it = numbers.begin(); it != numbers.end() - 2; ++it) {
		if (*it < *(it + 3))
			++increased;
	}
	return increased;
}
