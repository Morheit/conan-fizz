from conans import ConanFile, CMake, tools
from conans.tools import Version
import os


class FizzConan(ConanFile):
    name = "fizz"
    version = "2019.11.11.00"
    description = "C++14 implementation of the TLS-1.3 standard"
    homepage = "https://github.com/facebookincubator/fizz"
    url = "https://github.com/Morheit/conan-fizz"
    license = "BSD"
    author = "Yaroslav Stanislavyk (stl.ros@outlook.com)"
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "folly/2019.11.11.00@morheit/stable",
        "fmt/6.0.0@bincrafters/stable",
        "openssl/1.0.2t",
        "libsodium/1.0.18@bincrafters/stable"
    )
    exports = ["LICENSE"]
    exports_sources = ["patches/*.patch"]
    generators = "cmake_paths"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.shared
        elif self.settings.os == "Macos":
            del self.options.shared

    def configure(self):
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("The package currently doesn't support the Windows platform")

        compiler_version = Version(self.settings.compiler.version.value)

        if self.settings.os == "Linux":
            if self.settings.compiler.libcxx == "libstdc++":
              raise ConanInvalidConfiguration("libstdc++ is not supported. Please use the new one: libstdc++11")
            if self.settings.compiler == "clang":
                if compiler_version < "6.0":
                    raise ConanInvalidConfiguration("The minimal Clang version is 6.0")
            elif self.settings.compiler == "gcc":
                if compiler_version < "5":
                    raise ConanInvalidConfiguration("The minimal GCC version is 5")
        elif self.settings.os == "Macos":
            if self.settings.compiler == "apple-clang":
                if compiler_version < "8.0":
                    raise ConanInvalidConfiguration("The minimal apple-clang version is 8.0")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _source_subfolder_path(self):
        return (self.source_folder + ("/" + self._source_subfolder))

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + '-' + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = "conan_paths.cmake"
        cmake.configure(source_folder=(self._source_subfolder_path + "/fizz"))
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder_path, patch_file='patches/fizz-deps-fix.patch')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self) + ["fizz"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "m", "dl"])
