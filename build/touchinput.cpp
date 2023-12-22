#include <iostream>
#include "touchinput.h"
#include <boost/python.hpp>
// #include <pybind11/eigen.h>

namespace py = pybind11;


int main(){
    string answer = "";
    cout << "I hate c++\nDo YOU hate c++?" << endl;
    cin >> answer;
    cout << answer << " is wrong/right depending on if you said no/yes respectively" << endl;
    return 0; 
}