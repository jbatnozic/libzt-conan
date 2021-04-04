from conans import ConanFile, CMake, tools
import shutil

class LibztConan(ConanFile):
    name = "libzt"
    version = "1.0"
    
    # Information for humans
    license = "MIT"
    author = "Jovan Batnožić (jovanbatnozic@hotmail.rs)"
    url = "https://github.com/jbatnozic/libzt-conan"
    description = "ZeroTier Sockets - Put a network stack in your app"
    
    # Information for computers
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
        # TODO Option to disable central API (and then not include CURL)
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }
    generators = "cmake"
    
    requires = "libcurl/7.75.0"
    
    exports_sources = "patch.txt"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.output.info("Downloading source files from Git...")
        
        git = tools.Git(folder="libzt")
        git.clone("https://github.com/zerotier/libzt.git")
        git.checkout("36256ea1b2a3251721a2b60e8165f59190e3f1a1")
        git.run("submodule init")
        git.run("submodule update")
        
        self.output.success("Source files downloaded successfully")

    def build(self):
        tools.patch(base_path="libzt", patch_file="patch.txt")
        
        cmake = CMake(self)
        cmake.definitions["ZTS_ENABLE_CENTRAL_API"] = 1
        # Setting BUILD_HOST to 1 and BUILD_SHARED_LIBS to 0 is a horrible hack
        # but at least it results usable libraries (both static and shared). So
        # the only real difference is which ones are packaged.
        # I don't have time to fix it so that it works properly.
        cmake.definitions["BUILD_HOST"] = 1
        cmake.definitions["BUILD_SHARED_LIBS"] = 0
        cmake.configure(source_folder="libzt")     
        cmake.build()

    def package(self):
        self.copy("ZeroTierSockets.h", dst="include", src="libzt/include")
        
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy("lib/zt-shared.lib", dst="lib", keep_path=False)
                self.copy("bin/zt-shared.dll", dst="bin", keep_path=False)
                self.copy("bin/zt-shared.pdb", dst="lib", keep_path=False)
            else:
                self.copy("lib/zt.lib", dst="lib", keep_path=False)
        else:
            self.output.error(
                "Automatic packaging currently not implemented on platforms other than Windows");

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = ["zt-shared"]
                self.cpp_info.system_libs = [
                    "WS2_32",  # Windows sockets
                    "ShLwApi", # Windows shell API
                    "iphlpapi" # IP helper API
                ]
                self.cpp_info.defines = [
                    "ZTS_ENABLE_CENTRAL_API",
                ]
            else:
                self.cpp_info.libs = ["zt"]
                self.cpp_info.system_libs = [
                    "WS2_32",  # Windows sockets
                    "ShLwApi", # Windows shell API
                    "iphlpapi" # IP helper API
                ]
                self.cpp_info.defines = [
                    "ZTS_STATIC",
                    "ZTS_ENABLE_CENTRAL_API",
                ]
        else:
            self.output.error(
                "Automatic packaging currently not implemented on platforms other than Windows");

