package one.spyteam.lili

import org.jooq.impl.DSL

val Database = DSL.using("jdbc:sqlite:./lili.db")
