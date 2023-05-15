import nu.studer.gradle.jooq.JooqEdition

plugins {
    kotlin("jvm") version "1.8.20"
    id("nu.studer.jooq") version "8.2"
    application
}

group = "one.spyteam"
version = "0.1"

repositories {
    mavenCentral()
}

dependencies {
    implementation("dev.kord:kord-core:0.9.0")
    implementation("org.slf4j:slf4j-simple:2.0.7")
    implementation("org.xerial:sqlite-jdbc:3.41.2.1")

    jooqGenerator("org.xerial:sqlite-jdbc:3.41.2.1")
}

kotlin {
    jvmToolchain(17)
}

application {
    mainClass.set("one.spyteam.lili.MainKt")
}


jooq {
    version.set("3.18.2")
    edition.set(JooqEdition.OSS)

    configurations {
        create("main") {
            jooqConfiguration.apply {
                logging = org.jooq.meta.jaxb.Logging.WARN
                jdbc.apply {
                    driver = "org.sqlite.JDBC"
                    url = "jdbc:sqlite:lili.db"
                }
                generator.apply {
                    name = "org.jooq.codegen.DefaultGenerator"
                    database.apply {
                        name = "org.jooq.meta.sqlite.SQLiteDatabase"
                    }
                    target.apply {
                        packageName = "${project.group}.${project.name}.jooq"
                        directory = "src/generated/jooq"
                    }
                    strategy.name = "org.jooq.codegen.DefaultGeneratorStrategy"
                }
            }
        }
    }
}
