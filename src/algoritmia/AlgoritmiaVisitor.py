# Generated from C:/Users/Yosselin/Documents/DDD/Algoritmia.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AlgoritmiaParser import AlgoritmiaParser
else:
    from AlgoritmiaParser import AlgoritmiaParser

# This class defines a complete generic visitor for a parse tree produced by AlgoritmiaParser.

class AlgoritmiaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AlgoritmiaParser#programa.
    def visitPrograma(self, ctx:AlgoritmiaParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#procedimiento.
    def visitProcedimiento(self, ctx:AlgoritmiaParser.ProcedimientoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#bloq_inicio.
    def visitBloq_inicio(self, ctx:AlgoritmiaParser.Bloq_inicioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#bloq_fin.
    def visitBloq_fin(self, ctx:AlgoritmiaParser.Bloq_finContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#parametros.
    def visitParametros(self, ctx:AlgoritmiaParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#instrucciones.
    def visitInstrucciones(self, ctx:AlgoritmiaParser.InstruccionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#instruccion.
    def visitInstruccion(self, ctx:AlgoritmiaParser.InstruccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#asignacion.
    def visitAsignacion(self, ctx:AlgoritmiaParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#lectura.
    def visitLectura(self, ctx:AlgoritmiaParser.LecturaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#escritura.
    def visitEscritura(self, ctx:AlgoritmiaParser.EscrituraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#escritura_item.
    def visitEscritura_item(self, ctx:AlgoritmiaParser.Escritura_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#reproduccion.
    def visitReproduccion(self, ctx:AlgoritmiaParser.ReproduccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#llamada_proc.
    def visitLlamada_proc(self, ctx:AlgoritmiaParser.Llamada_procContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#addlista.
    def visitAddlista(self, ctx:AlgoritmiaParser.AddlistaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#poplista.
    def visitPoplista(self, ctx:AlgoritmiaParser.PoplistaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#condicional.
    def visitCondicional(self, ctx:AlgoritmiaParser.CondicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#while_stmt.
    def visitWhile_stmt(self, ctx:AlgoritmiaParser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#expr.
    def visitExpr(self, ctx:AlgoritmiaParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#comparacion.
    def visitComparacion(self, ctx:AlgoritmiaParser.ComparacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#aritmetica.
    def visitAritmetica(self, ctx:AlgoritmiaParser.AritmeticaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#termino.
    def visitTermino(self, ctx:AlgoritmiaParser.TerminoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#factor.
    def visitFactor(self, ctx:AlgoritmiaParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#lista_literal.
    def visitLista_literal(self, ctx:AlgoritmiaParser.Lista_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#elements_list.
    def visitElements_list(self, ctx:AlgoritmiaParser.Elements_listContext):
        return self.visitChildren(ctx)



del AlgoritmiaParser