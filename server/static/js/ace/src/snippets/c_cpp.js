define("ace/snippets/c_cpp",["require","exports","module"], function(require, exports, module) {
"use strict";

exports.snippetText = "## STL Collections\n\
# std::array\n\
snippet array\n\
	std::array<${1:T}, ${2:N}> ${3};${4}\n\
# std::vector\n\
snippet vector\n\
	std::vector<${1:T}> ${2};${3}\n\
# std::deque\n\
snippet deque\n\
	std::deque<${1:T}> ${2};${3}\n\
# std::forward_list\n\
snippet flist\n\
	std::forward_list<${1:T}> ${2};${3}\n\
# std::list\n\
snippet list\n\
	std::list<${1:T}> ${2};${3}\n\
# std::set\n\
snippet set\n\
	std::set<${1:T}> ${2};${3}\n\
# std::map\n\
snippet map\n\
	std::map<${1:Key}, ${2:T}> ${3};${4}\n\
# std::multiset\n\
snippet mset\n\
	std::multiset<${1:T}> ${2};${3}\n\
# std::multimap\n\
snippet mmap\n\
	std::multimap<${1:Key}, ${2:T}> ${3};${4}\n\
# std::unordered_set\n\
snippet uset\n\
	std::unordered_set<${1:T}> ${2};${3}\n\
# std::unordered_map\n\
snippet umap\n\
	std::unordered_map<${1:Key}, ${2:T}> ${3};${4}\n\
# std::unordered_multiset\n\
snippet umset\n\
	std::unordered_multiset<${1:T}> ${2};${3}\n\
# std::unordered_multimap\n\
snippet ummap\n\
	std::unordered_multimap<${1:Key}, ${2:T}> ${3};${4}\n\
# std::stack\n\
snippet stack\n\
	std::stack<${1:T}> ${2};${3}\n\
# std::queue\n\
snippet queue\n\
	std::queue<${1:T}> ${2};${3}\n\
# std::priority_queue\n\
snippet pqueue\n\
	std::priority_queue<${1:T}> ${2};${3}\n\
##\n\
## Access Modifiers\n\
# private\n\
snippet pri\n\
	private\n\
# protected\n\
snippet pro\n\
	protected\n\
# public\n\
snippet pub\n\
	public\n\
# friend\n\
snippet fr\n\
	friend\n\
# mutable\n\
snippet mu\n\
	mutable\n\
## \n\
## Class\n\
# class\n\
snippet cl\n\
	class ${1:`Filename('$1', 'name')`} \n\
	{\n\
	public:\n\
		$1(${2});\n\
		~$1();\n\
\n\
	private:\n\
		${3:/* data */}\n\
	};\n\
# member function implementation\n\
snippet mfun\n\
	${4:void} ${1:`Filename('$1', 'ClassName')`}::${2:memberFunction}(${3}) {\n\
		${5:/* code */}\n\
	}\n\
# namespace\n\
snippet ns\n\
	namespace ${1:`Filename('', 'my')`} {\n\
		${2}\n\
	} /* namespace $1 */\n\
##\n\
## Input/Output\n\
# std::cout\n\
snippet cout\n\
	std::cout << ${1} << std::endl;${2}\n\
# std::cin\n\
snippet cin\n\
	std::cin >> ${1};${2}\n\
##\n\
## Iteration\n\
# for i \n\
snippet fori\n\
	for (int ${2:i} = 0; $2 < ${1:count}; $2${3:++}) {\n\
		${4:/* code */}\n\
	}${5}\n\
\n\
# foreach\n\
snippet fore\n\
	for (${1:auto} ${2:i} : ${3:container}) {\n\
		${4:/* code */}\n\
	}${5}\n\
# iterator\n\
snippet iter\n\
	for (${1:std::vector}<${2:type}>::${3:const_iterator} ${4:i} = ${5:container}.begin(); $4 != $5.end(); ++$4) {\n\
		${6}\n\
	}${7}\n\
\n\
# auto iterator\n\
snippet itera\n\
	for (auto ${1:i} = $1.begin(); $1 != $1.end(); ++$1) {\n\
		${2:std::cout << *$1 << std::endl;}\n\
	}${3}\n\
##\n\
## Lambdas\n\
# lamda (one line)\n\
snippet ld\n\
	[${1}](${2}){${3:/* code */}}${4}\n\
# lambda (multi-line)\n\
snippet lld\n\
	[${1}](${2}){\n\
		${3:/* code */}\n\
	}${4}\n\
## Main\n\
# main\n\
snippet main\n\
	int main(int argc, const char *argv[])\n\
	{\n\
		${1}\n\
		return 0;\n\
	}\n\
# main(void)\n\
snippet mainn\n\
	int main(void)\n\
	{\n\
		${1}\n\
		return 0;\n\
	}\n\
##\n\
## Preprocessor\n\
# #include <...>\n\
snippet inc\n\
	#include <${1:stdio}.h>${2}\n\
# #include \"...\"\n\
snippet Inc\n\
	#include \"${1:`Filename(\"$1.h\")`}\"${2}\n\
# ifndef...define...endif\n\
snippet ndef\n\
	#ifndef $1\n\
	#define ${1:SYMBOL} ${2:value}\n\
	#endif${3}\n\
# define\n\
snippet def\n\
	#define\n\
# ifdef...endif\n\
snippet ifdef\n\
	#ifdef ${1:FOO}\n\
		${2:#define }\n\
	#endif${3}\n\
# if\n\
snippet #if\n\
	#if ${1:FOO}\n\
		${2}\n\
	#endif\n\
# header include guard\n\
snippet once\n\
	#ifndef ${1:`toupper(Filename('$1_H', 'UNTITLED_H'))`}\n\
\n\
	#define $1\n\
\n\
	${2}\n\
\n\
	#endif /* end of include guard: $1 */\n\
##\n\
## Control Statements\n\
# if\n\
snippet if\n\
	if (${1:/* condition */}) {\n\
		${2:/* code */}\n\
	}${3}\n\
# else\n\
snippet el\n\
	else {\n\
		${1}\n\
	}${3}\n\
# else if\n\
snippet elif\n\
	else if (${1:/* condition */}) {\n\
		${2:/* code */}\n\
	}${3}\n\
# ternary\n\
snippet t\n\
	${1:/* condition */} ? ${2:a} : ${3:b}\n\
# switch\n\
snippet switch\n\
	switch (${1:/* variable */}) {\n\
		case ${2:/* variable case */}:\n\
			${3}\n\
			${4:break;}${5}\n\
		default:\n\
			${6}\n\
	}${7}\n\
# switch without default\n\
snippet switchndef\n\
	switch (${1:/* variable */}) {\n\
		case ${2:/* variable case */}:\n\
			${3}\n\
			${4:break;}${5}\n\
	}${6}\n\
# case\n\
snippet case\n\
	case ${1:/* variable case */}:\n\
		${2}\n\
		${3:break;}${4}\n\
##\n\
## Loops\n\
# for\n\
snippet for\n\
	for (${2:i} = 0; $2 < ${1:count}; $2${3:++}) {\n\
		${4:/* code */}\n\
	}${5}\n\
# for (custom)\n\
snippet forr\n\
	for (${1:i} = ${2:0}; ${3:$1 < 10}; $1${4:++}) {\n\
		${5:/* code */}\n\
	}${6}\n\
# while\n\
snippet wh\n\
	while (${1:/* condition */}) {\n\
		${2:/* code */}\n\
	}${3}\n\
# do... while\n\
snippet do\n\
	do {\n\
		${2:/* code */}\n\
	} while (${1:/* condition */});${3}\n\
##\n\
## Functions\n\
# function definition\n\
snippet fun\n\
	${1:void} ${2:function_name}(${3})\n\
	{\n\
		${4:/* code */}\n\
	}${5}\n\
# function declaration\n\
snippet fund\n\
	${1:void} ${2:function_name}(${3});${4}\n\
##\n\
## Types\n\
# typedef\n\
snippet td\n\
	typedef ${1:int} ${2:MyCustomType};${3}\n\
# struct\n\
snippet st\n\
	struct ${1:`Filename('$1_t', 'name')`} {\n\
		${2:/* data */}\n\
	}${3: /* optional variable list */};${4}\n\
# typedef struct\n\
snippet tds\n\
	typedef struct ${2:_$1 }{\n\
		${3:/* data */}\n\
	} ${1:`Filename('$1_t', 'name')`};${4}\n\
# typedef enum\n\
snippet tde\n\
	typedef enum {\n\
		${1:/* data */}\n\
	} ${2:foo};${3}\n\
##\n\
## Input/Output\n\
# printf\n\
snippet pr\n\
	printf(\"${1:%s}\\n\"${2});${3}\n\
# fprintf (again, this isn't as nice as TextMate's version, but it works)\n\
snippet fpr\n\
	fprintf(${1:stderr}, \"${2:%s}\\n\"${3});${4}\n\
# getopt\n\
snippet getopt\n\
	int choice;\n\
	while (1)\n\
	{\n\
		static struct option long_options[] =\n\
		{\n\
			/* Use flags like so:\n\
			{\"verbose\",	no_argument,	&verbose_flag, 'V'}*/\n\
			/* Argument styles: no_argument, required_argument, optional_argument */\n\
			{\"version\", no_argument,	0,	'v'},\n\
			{\"help\",	no_argument,	0,	'h'},\n\
			${1}\n\
			{0,0,0,0}\n\
		};\n\
\n\
		int option_index = 0;\n\
\n\
		/* Argument parameters:\n\
			no_argument: \" \"\n\
			required_argument: \":\"\n\
			optional_argument: \"::\" */\n\
\n\
		choice = getopt_long( argc, argv, \"vh\",\n\
					long_options, &option_index);\n\
\n\
		if (choice == -1)\n\
			break;\n\
\n\
		switch( choice )\n\
		{\n\
			case 'v':\n\
				${2}\n\
				break;\n\
\n\
			case 'h':\n\
				${3}\n\
				break;\n\
\n\
			case '?':\n\
				/* getopt_long will have already printed an error */\n\
				break;\n\
\n\
			default:\n\
				/* Not sure how to get here... */\n\
				return EXIT_FAILURE;\n\
		}\n\
	}\n\
\n\
	/* Deal with non-option arguments here */\n\
	if ( optind < argc )\n\
	{\n\
		while ( optind < argc )\n\
		{\n\
			${4}\n\
		}\n\
	}\n\
##\n\
## Miscellaneous\n\
# This is kind of convenient\n\
snippet .\n\
	[${1}]${2}\n\
# GPL\n\
snippet gpl\n\
	/*\n\
	 * This program is free software; you can redistribute it and/or modify\n\
	 * it under the terms of the GNU General Public License as published by\n\
	 * the Free Software Foundation; either version 2 of the License, or\n\
	 * (at your option) any later version.\n\
	 *\n\
	 * This program is distributed in the hope that it will be useful,\n\
	 * but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
	 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
	 * GNU General Public License for more details.\n\
	 *\n\
	 * You should have received a copy of the GNU General Public License\n\
	 * along with this program; if not, write to the Free Software\n\
	 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.\n\
	 *\n\
	 * Copyright (C) ${1:Author}, `strftime(\"%Y\")`\n\
	 */\n\
\n\
	${2}\n\
# scanf\n\
snippet sc\n\
	scanf(\"${1:%d}\", &${2});${3}";
exports.scope = "c_cpp";

});                (function() {
                    window.require(["ace/snippets/c_cpp"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            