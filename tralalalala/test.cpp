
#define ZTS_STATIC
#include "ZeroTierSockets.h"

#ifndef ZTS_ENABLE_CENTRAL_API
// static_assert(false, "Must have ZTS_ENABLE_CENTRAL_API defined!");
#endif

int main() {
    zts_stop();
}
