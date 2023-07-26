from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import patch
from conan.tools.scm import Git


class libztRecipe(ConanFile):
    name = "libzt"
    version = "3.0.0"
    package_type = "library"

    # Optional metadata
    license = "MIT"
    author = "Jovan Batnožić (jovanbatnozic@hotmail.rs)"
    url = "https://github.com/jbatnozic/libzt-conan"
    description = "ZeroTier Sockets - Put a network stack in your app"
    topics = ("libzt", "zerotier", "networking")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "centralapi": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "centralapi": False,
    }

    exports_sources = "patch.txt"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        if self.options.centralapi:
            self.requires("libcurl/8.1.2")

    # def layout(self):
    #     cmake_layout(self)

    def source(self):
        self.output.info("Downloading source files from Git...")
        
        git = Git(self)
        git.clone(url="https://github.com/zerotier/libzt.git", target="libzt")
        git.folder = "libzt"
        git.checkout(commit="8d21a265cc23dd6e6e4d2c2ad068e978f110f8e3")
        git.run("submodule init")
        git.run("submodule update")
        
        patch(self, base_path="libzt", patch_file="patch.txt")

        self.output.success("Source files downloaded and patched successfully")

    def generate(self):
        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

        tc = CMakeToolchain(self)
        tc.variables["ZTS_DISABLE_CENTRAL_API"] = 0 if self.options.centralapi else 1
        # Setting BUILD_HOST to 1 and BUILD_SHARED_LIBS to 0 is a horrible hack
        # but at least it results usable libraries (both static and shared). So
        # the only real difference is which ones are packaged.
        # I don't have time to fix it so that it works properly.
        tc.variables["BUILD_HOST"] = 1
        tc.variables["BUILD_SHARED_LIBS"] = 0
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder ="libzt")     
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = ["zt-shared"]
            else:
                self.cpp_info.libs = ["zt"]
            self.cpp_info.system_libs = [
                "WS2_32",  # Windows sockets
                "ShLwApi", # Windows shell API
                "iphlpapi" # IP helper API
            ]
        else:
            self.cpp_info.libs = ["zt"]
            
        if not self.options.shared:
            self.cpp_info.defines.append("ZTS_STATIC")
            
        if not self.options.centralapi:
            self.cpp_info.defines.append("ZTS_DISABLE_CENTRAL_API")
