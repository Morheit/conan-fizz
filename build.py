import platform
from bincrafters import build_template_default

if __name__ == "__main__":
    builder = build_template_default.get_builder(pure_c=False)

    if platform.system() == "Linux":
        builder.remove_build_if(lambda build: build.settings["compiler.libcxx"] == "libstdc++" or
                                              build.settings["compiler.libcxx"] == "libc++")

    builder.run()