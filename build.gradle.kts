plugins {
    kotlin("jvm") version "1.8.20"
    application
}

group = "one.spyteam"
version = "0.1"

repositories {
    mavenCentral()

}

dependencies {
    testImplementation(kotlin("test"))
    implementation("dev.kord:kord-core:0.9.0")
    implementation("org.slf4j:slf4j-simple:2.0.7")
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(11)
}

application {
    mainClass.set("one.spyteam.lili.MainKt")
}
