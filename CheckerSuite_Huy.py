import unittest
from TestUtils import TestChecker
from AST import *
from StaticCheck import  *
class CheckerSuite(unittest.TestCase):
    def test_simple_program_no_main(self):
        """Simple program: int main() {} """
        input = """procedure notmain();
        begin
        end"""
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_simple_program_not_main(self):
        """Simple program: int main() {} """
        input = """procedure main(a: integer);
        begin
        end"""
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_simple_program_not_main_function(self):
        """Simple program: int main() {} """
        input = """function main(a: integer): integer;
        begin
            return a;
        end"""
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_simple_program_main_wrong_return(self):
        """Simple program: int main() {} """
        input = """procedure main();
        begin
            return 1;
        end"""
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_simple_program_main_return_nothing(self):
        """Simple program: int main() {} """
        input = """procedure main();
        begin
            return;
            return 1;
        end"""
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_redeclared_globle_variables(self):
        """Simple program: int main() {} """
        input = """
        var a, a: integer;
        procedure main();
        begin
        end"""
        expect = str(Redeclared(Variable(), "a"))
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_redeclared_globle_variables_2(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        var a, b: boolean;
        procedure main();
        begin
        end"""
        expect = str(Redeclared(Variable(), "a"))
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_redeclared_globle_variables_3(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        var b: boolean;
        var b: real;
        procedure main();
        begin
        end"""
        expect = str(Redeclared(Variable(), "b"))
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_redeclared_globle_variables_4(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        var a: integer;
        """
        expect = str(Redeclared(Variable(), "a"))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_redeclared_param(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        procedure foo(a: integer; b: integer; b: string);
        begin
        end
        """
        expect = str(Redeclared(Parameter(), "b"))
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_redeclared_param_1(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        procedure foo(a: integer; b, b: integer; c: string);
        begin
        end
        """
        expect = str(Redeclared(Parameter(), "b"))
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_redeclared_local(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        procedure foo(a: integer; b: integer; c: string);
        var a: integer;
        begin
        end
        """
        expect = str(Redeclared(Variable(), "a"))
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_redeclared_local_2(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        procedure foo(a: integer; b: integer; c: string);
        var d, d: integer;
        begin
        end
        """
        expect = str(Redeclared(Variable(), "d"))
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_redeclared_function(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        function foo(): integer;
        begin
            return 1;
        end
        function foo(): integer;
        begin
            return 1;
        end
        """
        expect = str(Redeclared(Function(), "foo"))
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_redeclared_function_2(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        function foo(): integer;
        begin
            return 1;
        end
        function foo(a: integer): string;
        begin
            return "nothing";
        end
        """
        expect = str(Redeclared(Function(), "foo"))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_redeclared_procedure(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        procedure main();
        begin
        end
        """
        expect = str(Redeclared(Procedure(), "main"))
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_redeclared_combine(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        procedure a();
        begin
        end
        """
        expect = str(Redeclared(Procedure(), "a"))
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_redeclared_combine_2(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        function a(): integer;
        begin
            return 1;
        end
        """
        expect = str(Redeclared(Function(), "a"))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_redeclared_combine_3(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        function foo(): integer;
        begin
            return 1;
        end
        var foo: string;
        """
        expect = str(Redeclared(Variable(), "foo"))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_redeclared_combine_4(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        function foo(): integer;
        begin
            return 1;
        end
        var main: integer;
        """
        expect = str(Redeclared(Variable(), "main"))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_redeclared_combine_5(self):
        """Simple program: int main() {} """
        input = """
        var a: integer;
        procedure main();
        begin
        end
        function main(): integer;
        begin
            return 1;
        end
        """
        expect = str(Redeclared(Function(), "main"))
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_undeclared_identifier(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin end
        function foo(): integer; begin return a; end
        """
        expect = str(Undeclared(Identifier(), "a"))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_undeclared_identifier_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: string;
        begin end
        function foo(): integer; begin return b; return a; end
        var b: integer;
        """
        expect = str(Undeclared(Identifier(), "a"))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_undeclared_function(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
            foo(foo());
        end
        procedure foo(a: integer); begin end
        var b: integer;
        """
        expect = str(Undeclared(Function(), "foo"))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_undeclared_function_in_assignstmt(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        begin
            a:= foo();
        end
        procedure foo(a: integer); begin end
        var b: integer;
        """
        expect = str(Undeclared(Function(), "foo"))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_undeclared_procedure(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        begin
            foo(a);
        end
        function foo(a: integer): integer; begin end
        var b: integer;
        """
        expect = str(Undeclared(Procedure(), "foo"))
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_undeclared_procedure_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        begin
            notdeclared(a);
        end
        function foo(a: integer): integer; begin end
        var b: integer;
        """
        expect = str(Undeclared(Procedure(), "notdeclared"))
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_undeclared_procedure_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        begin
            notdeclared(a);
        end
        function foo(a: integer): integer; begin end
        var b: integer;
        """
        expect = str(Undeclared(Procedure(), "notdeclared"))
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_typemismatch_if(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
            if 1 then return;
        end
        """
        expect = str(TypeMismatchInStatement(If(IntLiteral(1),[Return(None)],[])))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_typemismatch_if_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        begin
            if a > b then return;
            if a then return;
        end
        """
        expect = str(TypeMismatchInStatement(If(Id("a"),[Return(None)],[])))
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_typemismatch_for(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        begin
            for a:= 1 to True do return;
        end
        """
        expect = str(TypeMismatchInStatement(For(Id("a"),IntLiteral(1),BooleanLiteral(True),True,[Return(None)])))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_typemismatch_for_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        begin
            for a:= False to 2 do return;
        end
        """
        expect = str(TypeMismatchInStatement(For(Id("a"),BooleanLiteral(False),IntLiteral(2),True,[Return(None)])))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_typemismatch_for_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var c: real;
        a, b: integer;
        begin
            for c:= b to a do return;
            for a:= 1 to c do return;
        end
        """
        expect = str(TypeMismatchInStatement(For(Id("c"),Id("b"),Id("a"),True,[Return(None)])))
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_typemismatch_while(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        c: boolean;
        begin
            while a < b do return;
            while a do return;
        end
        """
        expect = str(TypeMismatchInStatement(While(Id("a"),[Return(None)])))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_typemismatch_while_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        e: real;
        c: boolean;
        begin
            while a < e do return;
            while c do return;
            while a + b do return;
        end
        """
        expect = str(TypeMismatchInStatement(While(BinaryOp("+",Id("a"),Id("b")),[Return(None)])))
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_typemismatch_assign(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        e: real;
        c: boolean;
        begin
            a := e;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),Id("e"))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_typemismatch_assign_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        e: real;
        c: boolean;
        begin
            e := a;
            a:= c;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),Id("c"))))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_typemismatch_assign_3(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        e: real;
        c: boolean;
        g, f: string;
        begin
            g := f;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("g"),Id("f"))))
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_typemismatch_assign_4(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        e: real;
        c: boolean;
        g, f: string;
        arr: array [1 .. 2] of integer;
        begin
            arr:= arr;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("arr"),Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_typemismatch_assign_5(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a, b: integer;
        e: real;
        c: boolean;
        g, f: string;
        arr: array [1 .. 2] of integer;
        begin
            a:= arr[1] + b;
            c:= e < (b+a);
            c:= a < b;
            c:= a <> b;
            c:= c = c;
        end
        """
        expect = str(TypeMismatchInExpression(BinaryOp("=",Id("c"),Id("c"))))
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_typemismatch_return(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            return a;
        end
        function foo1(): array [1 .. 2] of integer;
        var a: array [1 .. 3] of integer;
        begin
            return a;
        end
        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_typemismatch_return_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            return foo();
        end
        function foo1(): array [1 .. 2] of integer;
        var a: array [1 .. 3] of integer;
        begin
            return a;
        end
        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_typemismatch_return_3(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
            return 1;
        end
        function foo(): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            return foo();
        end
        function foo1(): array [1 .. 2] of integer;
        var a: array [1 .. 3] of integer;
        begin
            return a;
        end
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_typemismatch_return_4(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            return foo();
        end
        function foo1(): array [1 .. 2] of integer;
        var a: array [1 .. 3] of integer;
        begin
            return;
        end
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_typemismatch_return_5(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(b: integer): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            return a;
        end
        function foo1(): array [1 .. 2] of integer;
        var a: array [1 .. 3] of integer;
        begin
            a[1] := foo(foo(a[1])[1])[1];
            return;
        end
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_typemismatch_return_6(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(b: array [1 .. 3] of integer): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            return a;
        end
        function foo1(): array [1 .. 2] of integer;
        var a: array [1 .. 2] of integer;
        begin
            a[1] := foo(foo(a))[1];
            return;
        end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_typemismatch_call(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(a, b, c); end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [0 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[Id("a"), Id("b"), Id("c")])))
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_typemismatch_call_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(a, b, c, c); end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [0 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[Id("a"), Id("b"), Id("c"), Id("c")])))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_typemismatch_call_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(a, b); end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [0 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[Id("a"), Id("b")])))
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_typemismatch_call_3(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(c[1], b, c); return 1; end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [1 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_typemismatch_call_4(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(a, b, c); return 1; end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [1 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_typemismatch_call_5(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(a + (c[1] - a) * c[2], b, c); return 1; end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [1 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_typemismatch_call_6(self):
        """Simple program: int main() {} """
        input = """
        procedure main(); begin foo(a + (c[1] - a) * c[2], b, c+    c); return 1; end
        var a: integer;
        b: string;
        c: array [1 .. 5] of integer;
        procedure foo(a: integer; b: string; c: array [1 .. 5] of integer); begin end
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("c"),Id("c"))))
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_typemismatch_expr(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            a := a := a < b;
        end
        """
        expect = str(TypeMismatchInExpression(BinaryOp("<",Id("a"),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_typemismatch_expr_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            a := a := a < a;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BinaryOp("<",Id("a"),Id("a")))))
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_typemismatch_expr_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            a := a := a/a;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BinaryOp("/",Id("a"),Id("a")))))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_typemismatch_expr_3(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            b := a := a + a;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("b"),Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_typemismatch_expr_4(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            a := d := a + a;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),Id("d"))))
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_typemismatch_expr_5(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            c := a < a;
            c := arr[1] + arr;
        end
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+", ArrayCell(Id("arr"),IntLiteral(1)), Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_typemismatch_expr_6(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            c := a < a;
            a:= arr[1]:= c:= True and True;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), ArrayCell(Id("arr"),IntLiteral(1)))))
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_typemismatch_expr_7(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            c := a < a;
            a := d := a/a;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), Id("d"))))
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_typemismatch_expr_8(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        begin
            d:= a := d := a;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), Id("d"))))
        self.assertTrue(TestChecker.test(input,expect,462))

    def test_typemismatch_expr_9(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        var a: integer;
        b: string;
        c: boolean;
        d: real;
        arr: array [1 .. 2] of boolean;
        inta: array [1 .. 3] of integer;
        begin
            inta[1] := inta[2] := inta[3] := arr[4];
        end
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("inta"), IntLiteral(3)), ArrayCell(Id("arr"), IntLiteral(4)))))
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_typemismatch_expr_10(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a: integer):integer;
        begin a:= foo(); return; end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[])))
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_typemismatch_expr_11(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a: integer;b: string):integer;
        begin a:= foo(b, a); return; end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("b"), Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_typemismatch_expr_12(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a: integer;b: string):integer;
        begin a:= foo(a); return; end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_typemismatch_expr_13(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a: integer):integer;
        begin a:= foo(True); return; end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[BooleanLiteral(True)])))
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_typemismatch_expr_14(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a: integer):integer;
        begin a:= foo(1.1); return; end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[FloatLiteral(1.1)])))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_typemismatch_expr_15(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a: integer):integer;
        begin a:= foo("string"); return; end
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[StringLiteral("string")])))
        self.assertTrue(TestChecker.test(input,expect,469))

    def test_typemismatch_expr_16(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin a[1]:= foo(a)[1]; return; end
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_typemismatch_expr_17(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin a[1]:= foo(a)[1] ; return; end
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_not_return(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_not_return_if(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_not_return_if_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then begin end else return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,474))

    def test_not_return_if_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then if True then return a; else begin end else begin end
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_not_return_if_3(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then return a; else return a;
            return 1.1;
        end
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_not_return_if_4(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        var c:integer;
        begin
            if True then for c := 1 to 2 do return a; else return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_not_return_if_5(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        var c: integer;
        begin
            if True then return a; else for c := 1 to 2 do return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,478))

    def test_not_return_if_6(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then while True do return a; else return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,479))

    def test_not_return_if_7(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then return a; else while True do return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,480))

    def test_not_return_if_8(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then if True then return a; else return a; else if True then return a; else return a;
            return 1.1;
        end
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_not_return_if_9(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        var c: integer;
        begin
            for c := 1 to 2 do return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,482))

    def test_not_return_if_10(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            while True do return a;
        end
        """
        expect = str(FunctionNotReturn("foo"))
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_not_return_if_11(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            with a: integer; do return;
        end
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_not_return_if_12(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then with a: integer; do return a; else return a;
        end
        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_not_return_if_13(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then with a: integer; do return a; else return a;
        end
        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,486))

    def test_not_return_if_14(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then with b: integer; do return a; else with b: integer; do return a;
            return;
        end
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,487))

    def test_not_in_loop(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            Break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,488))

    def test_not_in_loop_1(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            continue;
            return a;
        end
        """
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,489))

    def test_not_in_loop_2(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        var c: integer;
        begin
            for c:= 1 to 2 do break;
            continue;
            return a;
        end
        """
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,490))

    def test_not_in_loop_3(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        var c: integer;
        begin
            for c:= 1 to 2 do continue;
            break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,491))

    def test_not_in_loop_4(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            while True do continue;
            break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,492))

    def test_not_in_loop_5(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            while True do break;
            continue;
            return a;
        end
        """
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,493))

    def test_not_in_loop_6(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            while True do Continue;
            break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_not_in_loop_7(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then while True do break; else continue;
            return a;
        end
        """
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_not_in_loop_8(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then while True do continue; else break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_not_in_loop_9(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then while True do if True then continue; else begin end else break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,497))

    def test_not_in_loop_10(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            if True then while True do with b: integer; do continue; else break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_not_in_loop_11(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            with c: integer; do break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,499))

    def test_not_in_loop_12(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
        end
        function foo(a:array [1 .. 2] of integer):array [1 .. 2] of integer;
        begin
            with c: integer; do if True then while True do continue; else break;
            return a;
        end
        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,500))
