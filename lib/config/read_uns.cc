// Copyright (C) 1999,2000 Bruce Guenter <bruceg@em.ca>
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#include <config.h>
#include <stdlib.h>
#include <ctype.h>
#include "configrc.h"
#include "configio.h"

unsigned configuration::read_uns(const mystring& file,
				 unsigned def,
				 config_cache<unsigned>& cache) const
{
  if(!cache.value) {
    mystring tmp;
    unsigned result;
    const configuration* node;
    for(node = this; node; node = node->parent)
      if(config_read(node->directory, file, tmp)) {
	const char* ptr = tmp.c_str();
	while(*ptr && isspace(*ptr))
	  ++ptr;
	char* endptr;
	if(*ptr == '-') {
	  result = (unsigned)-1;
	  break;
	}
	else {
	  result = strtoul(ptr, &endptr, 10);
	  if(endptr > ptr)
	    break;
	}
      }
    if(!node)
      result = def;
    cache.value = new unsigned(result);
  }
  return *cache.value;
}
