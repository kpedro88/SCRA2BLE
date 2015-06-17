#ifndef KBUILDERVARIATORS_H
#define KBUILDERVARIATORS_H

//custom headers
#include "KVariation.h"
#include "KBuilder.h"

//ROOT headers
#include <TLorentzVector.h>

//STL headers
#include <string>
#include <vector>

using namespace std;

//base class for variators is in KVariation.h

namespace KParser {
	template <>
	KVariator<KBuilder>* processVariator<KBuilder>(KNamed* tmp){
		KVariator<KBuilder>* vtmp = 0;
		string vname = tmp->first;
		OptionMap* omap = tmp->second;
		
		//check for all known variators
		//skip unknown variators

		if(!vtmp) cout << "Input error: unknown variator " << vname << ". This variator will be skipped." << endl;

		return vtmp;
	}
}

#endif