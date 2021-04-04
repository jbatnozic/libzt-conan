from conans import ConanFile, CMake, tools
import shutil

class LibztConan(ConanFile):
    name = "libzt"
    version = "1.0"
    
    # Information for humans
    license = "MIT"
    author = "Jovan Batnožić (jovanbatnozic@hotmail.rs)"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libzt here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    
    # Information for computers
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True], # Couldn't get static to work
        "fPIC": [True, False]
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
        # but at least somehow results in a usable shared library.
        cmake.definitions["BUILD_HOST"] = 1
        cmake.definitions["BUILD_SHARED_LIBS"] = 0
        cmake.configure(source_folder="libzt")     
        cmake.build()

    def package(self):
        self.copy("ZeroTierSockets.h", dst="include", src="libzt/include")
        
        if self.settings.os == "Windows":
            self.copy("lib/zt-shared.lib", dst="lib", keep_path=False)
            self.copy("bin/zt-shared.dll", dst="lib", keep_path=False)
            self.copy("bin/zt-shared.pdb", dst="lib", keep_path=False)
        else:
            self.output.error(
                "Automatic packaging currently not implemented on platforms other than Windows");

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["zt-shared"]
            self.cpp_info.system_libs = [
                "WS2_32",  # Windows sockets
                "ShLwApi", # Windows shell API
                "iphlpapi" # IP helper API
            ]
            self.cpp_info.define = [
                "ZTS_ENABLE_CENTRAL_API",
            ]
        else:
            self.output.error(
                "Automatic packaging currently not implemented on platforms other than Windows");

