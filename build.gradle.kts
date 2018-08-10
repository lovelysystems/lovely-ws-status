import com.lovelysystems.gradle.isProductionVersion

plugins {
    `java-library`
    id("com.lovelysystems.gradle") version ("0.0.7")
}

lovely {
    gitProject()
}

repositories {
    jcenter()
}

val envDir = project.file("v")
val binDir = envDir.resolve("bin")
val pip = binDir.resolve("pip")
val python = binDir.resolve("python")
val readme = project.file("README.rst")

tasks {

    val clean = getByName("clean")

    val writeVersion by creating {
        val out = file("VERSION.txt")
        outputs.file(out)
        out.writeText(project.version.toString())
    }

    val venv by creating {
        group = "Bootstrap"
        description = "Bootstraps a python virtual environment"

        outputs.files(pip, python)
        doLast {
            exec {
                commandLine("python3", "-m", "venv", "--clear", envDir)
            }
            exec {
                commandLine(
                    pip, "install", "--upgrade",
                    "pip==18.0",
                    "setuptools==40.0.0",
                    "pip-tools==2.0.2"
                )
            }
        }
    }
    // remove the virtualenv upon clean
    clean.doLast { delete(envDir) }

    val nailRequirements by creating {
        group = "Bootstrap"
        description = "Nails requirements by using pip-compile"
        dependsOn(venv)
        val dev_req_file = file("requirements-dev.in")
        val req_file = file("requirements-dev.txt")
        val setup_file = file("setup.py")
        inputs.files(dev_req_file, setup_file)
        // use pserve script as a marker
        outputs.file(req_file)
        doLast {
            exec {
                commandLine(
                    binDir.resolve("pip-compile"),
                    setup_file,
                    dev_req_file,
                    "--output-file", req_file
                )
            }
        }
    }

    val dev by creating {
        group = "Bootstrap"
        description = "Installs project development dependencies into the venv"
        dependsOn(venv, nailRequirements, writeVersion)
        val req_file = file("requirements-dev.txt")
        // use pytest executable as a marker
        outputs.file(binDir.resolve("pytest"))
        doLast {
            exec {
                commandLine(binDir.resolve("pip-sync"), req_file)
            }
            exec {
                commandLine(
                    pip, "--disable-pip-version-check",
                    "install", "--no-deps", "-e", projectDir
                )
            }
        }
    }

    val sdist by creating {
        group = "Build"
        description = "Builds the source distribution"
        dependsOn(venv, writeVersion)
        inputs.files(fileTree("src"), readme, "MANIFEST.in")
        val out = file("dist/lovely-ws-status-${project.version}.tar.gz")
        outputs.files(out)
        doLast {
            exec {
                commandLine(python, "setup.py", "sdist")
            }
        }
    }
    // remove the python dist folder upon clean
    clean.doLast { delete(file("dist")) }

    val pytest by creating {
        group = "Verification"
        description = "Runs all python tests using pytest"
        dependsOn(dev)
        doLast {
            exec {
                commandLine(binDir.resolve("pytest"), readme)
            }
            exec {
                commandLine(binDir.resolve("pytest"), "tests")
            }
        }
    }

    @Suppress("UNUSED_VARIABLE")
    val upload by creating {
        group = "Publishing"
        description = "Uploads distribution to PyPI after prevalidation"
        dependsOn(sdist, pytest)
        doFirst {
            if (!isProductionVersion(project.version.toString())) {
                error("${project.version} is a dev version which must not be uploaded to PyPI")
            }
        }
        doLast {
            exec {
                commandLine(python, "setup.py", "sdist", "upload")
            }
        }
    }

    getByName("test").dependsOn(pytest)
    getByName("check").dependsOn(sdist)
}

java.sourceSets {
    "main" { java.srcDirs("src") }
    "test" { java.srcDirs("tests") }
}
