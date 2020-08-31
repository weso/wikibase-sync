package es.weso.shexl.ast

import es.weso.shexl.ast.{Constraint, FieldConstraint, PrefixDef, PrefixInv, ShExL, ShapeDef, ShapeInv, TypeConstraint, URL}

class ASTBasicTest {

  def main(args: Array[String]): Unit = {

    ShExL(0,0,
      List(
        PrefixDef(0,0,"xsd", URL(0,0,"http://scheema.org/xsd/>")),
        PrefixDef(0,0,"foaf", URL(0,0,"http://scheema.org/foaf/>")),
        ShapeDef(0,0,"Person",
          List(
            Constraint(0,0,FieldConstraint(0,0,PrefixInv(0,0,"foaf", "name")), TypeConstraint(0,0,PrefixInv(0,0,"xsd", "string"))),
            Constraint(0,0,FieldConstraint(0,0,PrefixInv(0,0,"xsd", "knows")), TypeConstraint(0,0,ShapeInv(0,0,"Person")))
          )
        )
      )
    )

  }

}
