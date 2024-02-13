plugins {
    val ktVersion = "1.9.22"

    kotlin("multiplatform") version ktVersion
    kotlin("plugin.serialization") version ktVersion
}

repositories {
    mavenCentral()
}

kotlin {
    linuxX64 {
        binaries { executable() }
    }

    jvm { }

    val versions = object {
        val kotlinLogging = "6.0.3"
        val slf4j = "2.0.12"
        val json = "1.6.2"
        val ktor = "2.3.8"
    }

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("io.github.oshai:kotlin-logging:${versions.kotlinLogging}")

                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:${versions.json}")

                implementation("io.ktor:ktor-client-core:${versions.ktor}")
                implementation("io.ktor:ktor-client-cio:${versions.ktor}")
                implementation("io.ktor:ktor-client-websockets:${versions.ktor}")
                implementation("io.ktor:ktor-client-logging:${versions.ktor}")
                implementation("io.ktor:ktor-client-content-negotiation:${versions.ktor}")
                implementation("io.ktor:ktor-serialization-kotlinx-json:${versions.ktor}")
            }
        }

        val jvmMain by getting {
            dependencies {
                implementation("org.slf4j:slf4j-simple:${versions.slf4j}")
            }
        }

        val linuxX64Main by getting {
            dependencies {
//                implementation("io.github.oshai:kotlin-logging-linuxx64:${versions.logging}")
            }
        }
    }
}
