# Libzt-conan
[Conan](https://conan.io/) recipe for [ZeroTier SDK](https://github.com/zerotier/libzt).

Latest version: `1.0.1`

Currently tested only on Windows.

# License
MIT (see [LICENSE](https://github.com/jbatnozic/libzt-conan/blob/master/LICENSE)).
The licence applies ONLY to the recipe files themselves (the ones in this repository), and NOT to the library being packaged (libzt).

# Instructions

## Getting the package
The package artifacts are not stored in any global repository, so you will have to build the package locally yourself.

To do that, download the repository, and in it run the following command from your terminal:

```
conan create . @<user>/<channel> --profile=<profile> --build=outdated 
```

You can choose the `user` and `channel` arbitrarily, however, for compatibility with other Conan packages created by 
me, I recommend that you use user `jbatnozic` and channel `stable`.

For `profile`, use `default` or one of your own. 

**Note:** If Conan can't resolve the dependency `libcurl`, you need to add the remote where it can be found:
```
conan remote add conan-center https://conan.bintray.com
```

## Consuming the package
Consumed through a conanfile (.txt or .py) like any other Conan package. Supports both `build-type`s (Debug and Release) as you'd excpect.

The only supported options are `fPIC` (except on Windows) and `shared`. Both are boolean (True/False). **Warning:** Due to a defect in the current libzt implementation,
(not all symbols are exported properly) it's impossible to use the global variable `zts_errno` with shared=True on Windows.

# Also see
[ZTCpp](https://github.com/jbatnozic/ztcpp), a user-friendly C++ wrapper over libzt. Also available as a Conan package.
