#include <iostream>
#include <unordered_set>
#include <vector>

using namespace std;

bool check_repeated_nums(vector<int> v) {
    bool ret = false;
    unordered_set<int> s;

    for(int x: v) {
        if (s.find(x) != s.end()) {
            cout << "duplicate found" << endl;
            return true;
        }
        cout << "inserting number into set. num: " << x << endl;
        s.insert(x);
    }
    return false;
}

int main() {
    vector<int> seq1 = {1,2,3,4,5,6,7};
    //vector<int> seq2 = {3, 100, 4, 5};

    cout << "trying with seq1: " << check_repeated_nums(seq1) << endl;
    return 0;
}