// Find_Word.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include <string>
#include <fstream>

#define UP 1
#define UP_RIGHT 2
#define RIGHT 3
#define DOWN_RIGHT 4
#define DOWN 5
#define DOWN_LEFT 6
#define LEFT 7
#define UP_LEFT 8

void search_possible_words_that_start_with_input_and_add_to_possible_list(char input, std::string word_list[], int arrSize1, std::string possible_list[], const int arrSize2);
void init_a_string_array_with_blank(std::string[], const int);
void replace_status(std::string list[], int arrSize, std::string word);

int main()
{
	//Init stuffs
	const int Size = 60;
	const int word_Size = 60;

	char table[Size][Size]; //save the puzzle
	std::string words[word_Size]; //save the word list
	std::fstream fin;
	int ver = 0; int hor = 0;
	int number_of_words = 0;

	
	fin.open("input.txt");
	if (!fin.is_open())
	{
		std::cout << "File not found" << std::endl;
		exit(EXIT_FAILURE);
	}

	fin >> ver >> hor;
	for (int i = 0; i < hor; i++)
	{
		for (int j = 0; j < ver; j++)
		{
			fin >> table[i][j];
		}
	}

	fin >> number_of_words;
	for (int i = 0; i < number_of_words; i++)
	{
		fin >> words[i];
	}

	fin.close();


	std::cout << "Just a moment..." << std::endl;
	int total = 0;
	//--------------------------------------------------
	for (int i = 0; i < hor; i++)
	{
		for (int j = 0; j < ver; j++)
		{
			const int possible_size = 10;
			std::string possible_words[possible_size];

			init_a_string_array_with_blank(possible_words, possible_size);
			search_possible_words_that_start_with_input_and_add_to_possible_list(table[i][j], words, number_of_words, possible_words, possible_size);

			if (possible_words[0] != "")
			{
				int direction = 1;
				switch (direction)
				{
				case UP: //done
				{
					if (i - 1 >= 0)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++) //search entire possible list
						{
							if (possible_words[i_possible] == "") continue; //if the word is already searched then just ignore

							int x = i;
							bool check = true; //just check if the above strings are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++)
							{
								prototype_string += table[x][j];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								x--; //move up => i-- => x--

								if (x < 0 && prototype_string != possible_words[i_possible]) //if x is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}

								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string) 
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word
							{
								int len = i; //same role as x
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << len << "; " << j << "), ";
									len--;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]); //if found then replace it with blank
								possible_words[word_number] = ""; //same thing
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case UP_RIGHT: //done
				{
					if (i - 1 >= 0 && j + 1 <= Size - 1)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++) //search entire possible list
						{
							if (possible_words[i_possible] == "") continue; //if the word is already searched then just ignore

							int x = i;
							int y = j;
							bool check = true; //just check if the above strings are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++)
							{
								prototype_string += table[x][y];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								x--; //move up => i-- => x--
								y++;

								if ((x < 0 || y > Size - 1) && prototype_string != possible_words[i_possible]) //if x is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}

								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word
							{
								int len = i; //same role as x
								int leny = j;
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << len << "; " << leny << "), ";
									len--; leny++;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]); //if found then replace it with blank
								possible_words[word_number] = ""; //same thing
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case RIGHT: //done
				{
					if (j + 1 <= Size - 1)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++)
						{
							if (possible_words[i_possible] == "") continue; //if found then ignore

							int y = j;
							bool check = true; //just check if the strings above are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++) //search entire possible list
							{
								prototype_string += table[i][y];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								y++; //move right => j++ => y++

								if (y > Size - 1 && prototype_string != possible_words[i_possible]) //if y is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}
								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word
							{
								int len = j; //same role as y
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << i << "; " << len << "), ";
									len++;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]); //replace to blank
								possible_words[word_number] = ""; //same thing
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case DOWN_RIGHT: //done
				{
					if (j + 1 <= Size - 1 && i + 1 <= Size - 1)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++)
						{
							if (possible_words[i_possible] == "") continue; //if found then ignore

							int y = j;
							int x = i;
							bool check = true; //just check if the strings above are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++) //search entire possible list
							{
								prototype_string += table[x][y];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								y++; //move right => j++ => y++
								x++;

								if ((y > Size - 1 || x > Size - 1) && prototype_string != possible_words[i_possible]) //if y is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}
								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word
							{
								int len = j; //same role as y
								int lenx = i;
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << lenx << "; " << len << "), ";
									len++; lenx++;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]); //replace to blank
								possible_words[word_number] = ""; //same thing
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case DOWN: //done
				{
					if (i + 1 <= Size - 1)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++)
						{
							if (possible_words[i_possible] == "") continue;

							int x = i;
							bool check = true; //just check if the strings above are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++)
							{
								prototype_string += table[x][j];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								x++; //move down => i++ => x++

								if (x > Size - 1 && prototype_string != possible_words[i_possible]) //if x is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}
								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word.
							{
								int len = i; //same role as x
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << len << "; " << j << "), ";
									len++;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]);
								possible_words[word_number] = "";
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case DOWN_LEFT: //done
				{
					if (i + 1 <= Size - 1 && j - 1 >= 0)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++)
						{
							if (possible_words[i_possible] == "") continue;

							int x = i;
							int y = j;
							bool check = true; //just check if the strings above are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++)
							{
								prototype_string += table[x][y];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								x++; //move down => i++ => x++
								y--;

								if ((x > Size - 1 || y < 0) && prototype_string != possible_words[i_possible]) //if x is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}
								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word.
							{
								int len = i; //same role as x
								int leny = j;
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << len << "; " << leny << "), ";
									len++;
									leny--;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]);
								possible_words[word_number] = "";
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case LEFT: //done
				{
					if (j - 1 >= 0)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++)
						{
							if (possible_words[i_possible] == "") continue;

							int y = j;
							bool check = true; //just check if the strings above are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++)
							{
								prototype_string += table[i][y];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								y--; //move left => j-- => y--

								if (y < 0 && prototype_string != possible_words[i_possible]) //if y is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}
								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word.
							{
								int len = j; //same role as y
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << i << "; " << len << "), ";
									len--;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]);
								possible_words[word_number] = "";
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				case UP_LEFT: //done
				{
					if (j - 1 >= 0 && i - 1 >= 0)
					{
						int word_number = 0; //if detect a word in possible_words then save its digit here
						int check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0; //if the loop does not execute, check will be true, which can
						//mess up with the result

						for (int i_possible = 0; i_possible < possible_size; i_possible++)
						{
							if (possible_words[i_possible] == "") continue;

							int y = j;
							int x = i;
							bool check = true; //just check if the strings above are same or not

							std::string prototype_string = ""; //the string created by moving a direction
							std::string original_string = ""; //the string created by the possible_words

							for (int unsigned k = 0; k < possible_words[i_possible].length(); k++)
							{
								prototype_string += table[x][y];
								original_string += possible_words[i_possible].at(k);

								if (prototype_string != original_string) //if spot any differences, break loop, return false
								{
									check = false; break;
								}

								y--; //move left => j-- => y--
								x--;

								if ((y < 0 || x < 0) && prototype_string != possible_words[i_possible]) //if y is out of bounds
								//and the prototype not match origin then break loop return false
								{
									check = false; break;
								}
								check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 1;
							}

							if (original_string == possible_words[i_possible] && prototype_string == original_string)
								word_number = i_possible;

							if (!check) continue;
							else if (check_if_the_for_int_unsigned_k_loop_is_executed_or_not) //if it's already executed => there is a word.
							{
								int len = j; //same role as y
								int lenx = i;
								std::cout << possible_words[word_number] << ": ";
								for (unsigned int n = 0; n < possible_words[word_number].length(); n++)
								{
									std::cout << "(" << lenx << "; " << len << "), ";
									len--; lenx--;
								}
								std::cout << std::endl;
								total++;
								replace_status(words, number_of_words, possible_words[word_number]);
								possible_words[word_number] = "";
							}
							check_if_the_for_int_unsigned_k_loop_is_executed_or_not = 0;
						}

					}
				}
				}
			}
		}
	}
	//--------------------------------------------------
	std::cout << "Summary: " << total << " words found." << std::endl;
	std::cout << "Words not found: " << number_of_words - total << std::endl;
	if (number_of_words - total != 0)
	{
		std::cout << "Those are: ";
		for (int i = 0; i < number_of_words; i++)
		{
			if (words[i] != " ") std::cout << words[i] << " ";
		}
		std::cout << std::endl;
	}
	return 0;
}

void search_possible_words_that_start_with_input_and_add_to_possible_list(char input, std::string word_list[], int arrSize1, std::string possible_list[], const int arrSize2)
{
	int possible_list_iterator = 0;
	for (int i = 0; i < arrSize1; i++)
	{
		try
		{
			if (word_list[i].at(0) == input)
			{
				possible_list[possible_list_iterator] = word_list[i];
				possible_list_iterator++;
				if (possible_list_iterator >= arrSize2) return;
			}
		}
		catch (std::out_of_range & ou_ra )
		{
			std::cout << "Out of range in search function." << std::endl;
			std::cout << input << std::endl;
			exit(EXIT_FAILURE);
		}
	}
}
void init_a_string_array_with_blank(std::string array[], const int arrSize)
{
	for (int i = 0; i < arrSize; i++)
		array[i] = "";
}
void replace_status(std::string list[], int arrSize, std::string word)
{
	for (int i = 0; i < arrSize; i++)
		if (list[i] == word)
		{
			list[i] = " "; return;
		}
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
