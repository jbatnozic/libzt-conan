
#include <iostream>

#include "ZeroTierSockets.h"

int main() {
    // Basic API
    zts_node_stop();
    std::cout << "zts_errno is " << zts_errno << '\n';
    
    // Central API
#ifndef ZTS_DISABLE_CENTRAL_API
    zts_central_set_verbose(1);
    std::cout << "Central API is enabled.\n";
#else
    std::cout << "Central API is disabled.\n";    
#endif
    return 0;
}
