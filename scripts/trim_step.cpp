/*
 * trim_step2.cpp
 *
 *  Created on: Jan 19, 2018
 *      Author: seth
 */

#include <algorithm>
#include <map>
#include <string>
#include <sstream>
#include <vector>
#include <fstream>
#include <regex>
#include <iostream>

// trim from end (in place)
static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}
// trim from start (in place)
static inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch) {
        return !std::isspace(ch);
    }));
}
template<typename Out>
void split(const std::string &s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    if (std::getline(ss, item, delim)) {
		*(result++) = item;
	}
    if (std::getline(ss, item)) {
		*(result++) = item;
	}
}

int main( int argc, char **argv)
{
	size_t last_file_lines = (size_t)-1;
	size_t file_lines = last_file_lines - 1;

	std::string input_file(argv[1]);
	std::string output_file(argv[1]);
	std::ofstream log("Log_file.txt");

	while( file_lines < last_file_lines )
//	for(int i = 0; i < 1; i++)
	{

		std::ifstream is(input_file);

		std::map<std::string, unsigned> uniques;
		std::map<unsigned, unsigned> lookup;
		std::vector<std::string> lines;
		std::vector<std::string> footer;
		std::vector<std::string> header;

		bool past_header = false;
		lines.reserve( 100000 );

		while(is)
		{
			std::string line;
			std::getline( is, line );

			rtrim(line);
			std::vector<std::string> elems;
			split(line, '=', std::back_inserter(elems));

			if( line.front() != '#' || elems.size() != 2 )
			{
				std::string is_empty(line);
				ltrim( is_empty );
				rtrim( is_empty );
				if( !is_empty.size() )
					continue;

				if( !past_header )
					header.push_back( line );
				else
					footer.push_back( line );

				continue;
			}

			past_header = true;
			line.clear();
			// remove the #
			elems[0].erase(0,1);
			unsigned oldnum = std::stol(elems[0]);

			ltrim(elems[1]);
			rtrim(elems[1]);

			while( is && elems[1].back() != ';' )
			{
				std::getline( is, line );
				rtrim(line);
				ltrim(line);
				if( std::isalpha(line.front()) )
					elems[1].append( " " );
				elems[1].append( line );
			}

			auto it = uniques.emplace( std::make_pair(elems[1], lines.size() + 1 ) );

			while( ( elems[1].find("PRODUCT_DEFINITION") == 0
					|| elems[1].find("SHAPE_REPRESENTATION") == 0 )&& !it.second )
			{
				elems[1].append( " " );
				it = uniques.emplace( std::make_pair(elems[1], lines.size() + 1 ) );
			}

			if( !it.second )
			{
				log << lines.size() + 1 <<" -> " << it.first->second << " : " << it.first->first << std::endl;

				if( elems[1] != it.first->first )
					std::cout << "Warning! " << elems[1] << " is not the same as " << it.first->first << std::endl;
				// didn't insert!
				lookup.emplace( oldnum, it.first->second );
			}
			else
			{
				lookup.emplace( std::make_pair( oldnum, lines.size() + 1 ) );
				lines.push_back( elems[1] );
			}
		}

		is.close();

		std::cout << "File Lines: " << lines.size() << std::endl;

		std::ofstream os(output_file);

		for( auto line : header )
			os << line << std::endl;

		for( int x = 1; x <= lines.size(); x++ )
		{
			std::string templine( lines[x - 1] );
			std::smatch m;
			std::regex e ("#([0-9]+)");

			os << "#" << x << "=";
			while( std::regex_search( templine, m, e, std::regex_constants::match_not_null) )
			{
				if( m.empty() ) break;
				unsigned oldval = std::stol(m[1]);
				auto newval = lookup.find( oldval );
				os << m.prefix() << "#" << newval->second;
				templine = m.suffix();
			}
			if( templine.size() > 0 )
				os << templine << std::endl;
		}

		for( auto line : footer )
			os << line << std::endl;

		last_file_lines = file_lines;
		file_lines = lines.size();

		os.close();
		input_file = output_file;
	}
}
