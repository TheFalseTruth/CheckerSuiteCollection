import unittest
from TestUtils import TestChecker
from AST import *

# SHOULD MOVE CHECK ENTRY TO LAST

class CheckerSuite(unittest.TestCase):
    def test_redeclared_variable_1(self):

        input = """ var a:integer; var a: integer;
                    procedure main();
                    begin return; end"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,1))

    def test_redeclared_variable_2(self):

        input = """var a,a:integer;
                   procedure main();
                   begin return; end"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,2))

    def test_redeclared_variable_3(self):

        input = """
                   procedure main(a:integer);
                   var a:integer;
                   begin return; end"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,3))

    def test_redeclared_variable_4(self):

        input = """procedure main(); begin end
                   procedure Main(a:integer ; a:integer);
                   begin return; end"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,4))

    def test_redeclared_variable_5(self):

        input = """
                   procedure main();
                   var a,a:integer;
                   begin return; end"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,5))


    def test_redeclared_variable_6(self):

        input = """procedure main(); begin end
                   procedure Main(a,a:integer);
                   begin return; end"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,6))


    def test_redeclared_function(self):

        input = """ function foo():integer;
                    begin return 1; end

                    function foo():integer;
                    begin return 1; end
                   procedure main();
                   begin return; end"""
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,7))

    def test_no_return(self):

        input = """ function notMain():integer;
                    begin end

                    procedure main();
                    begin end"""
        expect = "Function notMain Not Return"
        self.assertTrue(TestChecker.test(input,expect,8))

    def test_return(self):

        input = """procedure main();
                   begin return 1; end"""
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,9))

    def test_expr(self):

        input = """
                   function foo():integer;
                   begin return 1/1; end
                   procedure main();
                   begin return; end"""
        expect = "Type Mismatch In Statement: Return(Some(BinaryOp(/,IntLiteral(1),IntLiteral(1))))"
        self.assertTrue(TestChecker.test(input,expect,10))

    def test_array(self):

        input = """
                   var a: array [1 .. 2] of integer;
                   procedure foo();
                   begin return; end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,11))


    def test_recursion(self):

        input = """function foo(a:integer):integer;
                   begin return foo(a); end
                   procedure aaa();
                   begin return; end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,12))

    def test_array_expr(self):

        input = """function foo(a:integer):integer;
                   var b: array [1 .. 2] of integer;
                   begin return foo(b); end
                   procedure main();
                   begin return; end"""
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[Id(b)])"
        self.assertTrue(TestChecker.test(input,expect,13))

    def test_assign(self):

        input = """ procedure main();
                    var a,b:integer;
                    begin
                        a := b := 1.1;
                        return;
                    end """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),FloatLiteral(1.1))"
        self.assertTrue(TestChecker.test(input,expect,14))

    def test_assign_2(self):

        input = """ procedure main();
                    var a:integer;
                        b: array [1 .. 2] of integer;
                    begin
                        a := b[1] := 1 + 1.1;
                        return;
                    end """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(Id(b),IntLiteral(1)),BinaryOp(+,IntLiteral(1),FloatLiteral(1.1)))"
        self.assertTrue(TestChecker.test(input,expect,15))

    def test_array_2(self):

        input = """ procedure main();
                    var a:integer;
                        b: array [1 .. 2] of integer;
                    begin
                        a := b[1.2] := 1 + 1;
                        return;
                    end """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),FloatLiteral(1.2))"
        self.assertTrue(TestChecker.test(input,expect,16))

    def test_assign_3(self):

        input = """ procedure foo();
                    var a: real;
                        b: array [1 .. 2] of integer;
                    begin
                        a := b[1] := 1 + 1;
                        return;
                    end """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,17))

    def test_assign_4(self):

        input = """ procedure main();
                    var a: string;
                        b: array [1 .. 2] of integer;
                    begin
                        a := b[1] := 1 + 1;
                        return;
                    end """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),ArrayCell(Id(b),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,18))

    def test_call_stmt_1(self):

        input = """ procedure foo(a : array [1 .. 2] of integer);
                    var b : array [1 .. 2] of integer;
                    begin
                        foo(b);
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,19))

    def test_call_stmt_2(self):

        input = """ procedure foo(a : array [1 .. 2] of integer);
                    var b : array [1 .. 3] of integer;
                    begin
                        foo(b);
                        return;
                    end
                    procedure main(); begin end"""
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(b)])"
        self.assertTrue(TestChecker.test(input,expect,20))

    def test_call_stmt_3(self):

        input = """ procedure foo(a : array [1 .. 2] of integer);
                    var b : array [6 .. 2] of integer;
                    begin
                        foo(b);
                        return;
                    end
                    procedure main(); begin end"""
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(b)])"
        self.assertTrue(TestChecker.test(input,expect,21))

    def test_call_stmt_4(self):

        input = """ procedure foo(a : array [1 .. 2] of integer);
                    var b : array [1 .. 2] of real;
                    begin
                        foo(b);
                        return;
                    end
                    procedure main(); begin end"""
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(b)])"
        self.assertTrue(TestChecker.test(input,expect,22))

    def test_call_stmt_5(self):

        input = """ procedure foo(a : array [1 .. 2] of real);
                    var b : array [1 .. 2] of integer;
                    begin
                        foo(b);
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,23))

    def test_break_1(self):

        input = """ procedure main();
                    begin
                        break;
                        return;
                    end"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,24))

    def test_break_2(self):

        input = """ procedure main();
                    var a : integer;
                    begin
                        if a < 1 then break;
                        return;
                    end"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,25))

    def test_break_3(self):

        input = """ procedure main();
                    var a : integer;
                    begin
                        if a < 1 then return;
                        else break;
                        return;
                    end"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,26))

    def test_break_4(self):

        input = """ procedure main();
                    begin
                        with a:integer; do break;
                        return;
                    end"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,27))

    def test_break_5(self):

        input = """ function foo(): integer;
                    begin
                        with a:integer; do
                            for a := 1 to 2 do
                                break;

                    end

                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,28))

    def test_break_6(self):

        input = """ function foo():integer;
                    begin
                        with a:integer; do
                            for a := 1 to 2 do
                                if a < 1 then
                                    break;
                                else
                                    break;

                    end
                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,29))

    def test_main_1(self):

        input = """ procedure main(a:integer);
                    begin
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,30))

    def test_main_2(self):

        input = """ function main():integer;
                    begin
                        return 1;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,31))

    def test_assign_5(self):

        input = """ procedure main();
                    var a,b,c : string;
                        d : array [1 .. 2] of string;
                    begin
                        a := b := c := d[1] := "1234";
                        return;
                    end"""
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(Id(d),IntLiteral(1)),StringLiteral(1234))"
        self.assertTrue(TestChecker.test(input,expect,32))

    def test_for_1(self):

        input = """
                    procedure main();
                    begin
                        for a := 1 to 2 do
                            break;
                        return;
                    end"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,33))

    def test_for_2(self):

        input = """ var a : integer;
                    function foo():integer;
                    var a : integer;
                    begin
                        for a := 1 to 2 do
                            break;

                    end
                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,34))

    def test_for_3(self):

        input = """
                    procedure main();
                    var b : integer;
                    begin
                        for b := 1 to 2 do
                            for a := 1 to 2 do
                                break;
                        return;
                    end"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,35))

    def test_return_1(self):

        input = """ function foo():integer;
                    begin
                        if 1 > 2 then return 1;
                    end
                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,36))

    def test_return_2(self):

        input = """ procedure notMain();
                    begin
                        if 1 > 2
                            then return;
                        else return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,37))

    def test_return_3(self):

        input = """ procedure notMain();
                    begin
                        if 1 > 2
                            then putIntLn(1);
                        else putIntLn(1);
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,38))

    def test_return_4(self):

        input = """ procedure notMain();
                    begin
                        if 1 > 2
                            then return;
                        else putIntLn(1);
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,39))

    def test_return_5(self):

        input = """ procedure notMain();
                    begin
                        return;
                        if 1 > 2
                            then putIntLn(1);
                        else putIntLn(1);

                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,40))

    def test_return_6(self):

        input = """ function foo():integer;
                    begin
                        if 1 > 2
                            then
                                if 2 > 1
                                    then
                                        return 1;
                                    else
                                        return 1;

                    end
                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,41))

    def test_return_7(self):

        input = """ procedure notMain();
                    begin
                        if 1 > 2
                            then
                                if 2 > 1
                                    then
                                        return;
                                    else
                                        return;
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,42))

    def test_return_8(self):

        input = """ procedure notMain();
                    begin
                        if 1 > 2
                            then
                                begin
                                    putIntLn(1);
                                    if 2 > 1
                                        then
                                            putIntLn(1);
                                        else
                                            putIntLn(1);
                                    return;
                                end
                            else
                                return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,43))

    def test_return_9(self):

        input = """ procedure notMain();
                    begin
                        with a:integer; do putIntLn(a);
                        return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,44))

    def test_return_10(self):

        input = """ procedure notMain();
                    begin
                        with a:integer; do
                            begin
                                putIntLn(a);
                                return;
                            end
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,45))

    def test_return_11(self):

        input = """ procedure notMain();
                    begin
                        with a:integer; do
                            with b: integer; do
                                return;
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,46))

    def test_return_12(self):

        input = """ function foo():integer;
                    begin
                        with a:integer; do
                            begin
                                with b:integer; do putIntLn(b);
                                return 1;
                            end
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,47))

    def test_return_13(self):

        input = """ function foo():integer;
                    var a: integer;
                    begin
                        for a := 1 to 2 do
                            return 1;
                    end

                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,48))

    def test_return_14(self):

        input = """ function foo():integer;
                    var a: integer;
                    begin
                        while a < 1 do
                            return 1;
                    end

                    procedure main();
                    begin end"""
        expect = "Function foo Not Return"
        self.assertTrue(TestChecker.test(input,expect,49))

    def test_return_15(self):

        input = """ function foo():integer;
                    var a: integer;
                    begin
                        if a > 1
                            then
                                if a > 5
                                    then return 1;
                                    else return 1;
                            else return 1;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,50))

    def test_for_4(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        for a := 1 to 2 do
                            for a := 2 to 5 do
                                break;

                        continue;
                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,51))

    def test_for_5(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        for a := 1 to 2 do
                            begin
                                for a := 2 to 5 do
                                    continue;
                                continue;
                            end
                        break;
                    end

                    """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,52))

    def test_while_1(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        while (a < 1.2) do
                            continue;
                        break;
                    end

                    """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,53))

    def test_while_2(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        while (a < 1.2) do
                            begin
                                while (a < 1) do
                                    break;
                                break;
                            end
                        continue;
                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,54))

    def test_while_3(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        while (a < 1.2) do
                            if (a < 0)
                                then break;
                            else break;
                        continue;
                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,55))

    def test_while_4(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        if (a < 1)
                            then
                                begin
                                    for a := 1 to 5 do
                                        break;
                                    continue;
                                end

                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,56))

    def test_with_1(self):
        input = """ procedure main();
                    begin
                        with a: integer; do
                            a := 1;
                        a := 2;

                    end

                    """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,57))

    def test_with_2(self):
        input = """ procedure main();
                    var a:integer;
                    begin
                        for a := 1 to 5 do
                            begin
                                with b : integer; do
                                    b := a;
                                b := 1;
                            end
                    end

                    """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,58))

    def test_return_16(self):
        input = """ function foo():integer;
                    var a:integer;
                    begin
                        if a < 1
                            then
                                putIntLn(a);
                            else
                                putIntLn(a + 1);
                        if a + 10 < 11
                            then return a;
                            else return a + 10;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,59))

    def test_return_17(self):
        input = """ function foo():integer;
                    var a:integer;
                    begin
                        if a < 1
                            then
                                with b:integer; do
                                    putIntLn(b + a);
                            else
                                return a;
                        if a + 10 < 11
                            then return a;
                            else return a + 10;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,60))

    def test_return_18(self):
        input = """ function foo():integer;
                    var a:integer;
                    begin
                        if a < 1
                            then
                                putIntLn(a);
                            else
                                putIntLn(a + 1);
                        with b : integer; do
                            return b + a;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,61))

    def test_return_19(self):
        input = """ function foo():integer;
                    var a:integer;
                    begin
                        with b:integer; do
                            with c:integer; do
                                return a + b + c;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,62))

    def test_return_20(self):
        input = """ function foo():integer;
                    var a:integer;
                    begin
                        with b:integer; do
                            begin
                                if a < 2
                                    then
                                        with c:integer; do return a + b + c;
                                return a + b;
                            end

                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,63))

    def test_return_21(self):
        input = """ function foo():integer;
                    var a:integer;
                    begin
                        with b:integer; do
                            begin
                                if a < 2
                                    then
                                        with c:integer; do return a + b + c;
                                else return a + b;
                            end

                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,64))

    def test_arraycell_1(self):
        input = """ procedure main();
                    var a: integer;
                    begin
                        a[1] := 1;
                    end

                    """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,65))

    def test_arraycell_2(self):
        input = """ procedure main();
                    var a: array [1 .. 2] of integer;
                        b:integer;
                    begin
                        a[1] := 1;
                        b[1] := 1;
                    end

                    """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,66))

    def test_arraycell_3(self):
        input = """ procedure main();
                    var a: array [1 .. 2] of integer;
                        b:integer;
                    begin
                        a := 1;
                        b := 1;
                    end

                    """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,67))

    def test_arraycell_4(self):
        input = """ procedure main();
                    var a,b: array [1 .. 2] of integer;
                    begin
                        a := b;
                    end

                    """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,68))

    def test_arraycell_5(self):
        input = """ procedure main();
                    var a,b: array [1 .. 2] of integer;
                    begin
                        a[1] := b[2];
                        a := b;
                    end

                    """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,69))

    def test_arraycell_6(self):
        input = """ procedure main();
                    var a,b: array [1 .. 2] of integer;
                    begin
                        a[1] := b[a[1]];
                        a := b;
                    end

                    """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,70))

    def test_arraycell_7(self):
        input = """ procedure main();
                    var a,b: array [1 .. 2] of integer;
                    begin
                        a[2][1] := b[a[1]];
                    end

                    """
        expect = "Type Mismatch In Expression: ArrayCell(ArrayCell(Id(a),IntLiteral(2)),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,71))

    def test_arraycell_8(self):
        input = """ procedure main();
                    var a,b: array [1 .. 2] of integer;
                    begin
                        foo(a)[1] := b[2];
                        a := b;
                    end

                    function foo(b: array [1 .. 2] of real): array [1 .. 2] of integer;
                    var a: array [1 .. 2] of integer;
                    begin
                        return a;
                    end
                    """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,72))

    def test_arraycell_9(self):
        input = """ procedure main();
                    var a,b: array [1 .. 2] of integer;
                    begin
                        a[foo(a)[1]] := b[a[2] + foo(b)[2]];
                        a := b;
                    end

                    function foo(b: array [1 .. 2] of real): array [1 .. 2] of integer;
                    var a: array [1 .. 2] of integer;
                    begin
                        return a;
                    end
                    """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,73))

    def test_if_1(self):
        input = """ procedure notMain();
                    var a,b,c: boolean;
                    begin
                        a := b := c := True or False;
                        if (a or b) and c
                            then return;
                            else return;
                    end
                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,74))

    def test_if_2(self):
        input = """ procedure notMain();
                    var a,b,c: boolean;
                    begin
                        a := b := c := True or False;
                        if (a or else b) and then c
                            then return;
                            else return;
                    end
                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,75))

    def test_for_6(self):
        input = """
                    procedure main();
                    begin
                        for a := 1 to 2 do
                            break;
                        return;
                    end
                    """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,76))


    def test_for_7(self):
        input = """ procedure main();
                    var a:integer;
                    begin
                        if a < 1
                            then
                                begin
                                    for a := 1 to 2 do
                                        break;
                                    continue;
                                end
                    end
                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,77))

    def test_for_8(self):
        input = """ procedure main();
                    var a:integer;
                    begin
                        if a < 1
                            then
                                begin
                                    for a := 1 to 2 do
                                        break;
                                    for a := 1.1 to 5 do
                                        break;
                                end
                    end
                    """
        expect = "Type Mismatch In Statement: For(Id(a),FloatLiteral(1.1),IntLiteral(5),True,[Break])"
        self.assertTrue(TestChecker.test(input,expect,78))

    def test_case_sensitive_1(self):
        input = """ procedure main();
                    begin end

                    procedure main();
                    begin end
                    """
        expect = "Redeclared Procedure: main"
        self.assertTrue(TestChecker.test(input,expect,79))

    def test_case_sensitive_2(self):
        input = """ procedure main(); begin end
                    procedure Main(AbC :integer);
                    var AbC : real;
                    begin end

                    """
        expect = "Redeclared Variable: AbC"
        self.assertTrue(TestChecker.test(input,expect,80))

    def test_case_sensitive_3(self):
        input = """ procedure main();
                    begin
                        with abc, abc:integer; do
                            return;
                    end

                    """
        expect = "Redeclared Variable: abc"
        self.assertTrue(TestChecker.test(input,expect,81))

    def test_case_sensitive_4(self):
        input = """ procedure main(); begin end
                    procedure Main(abc :integer);
                    begin
                        abc := 1;
                        break;
                    end

                    """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,82))

    def test_while_5(self):
        input = """ procedure main();
                    var a:integer;
                    begin
                        if a < 1
                            then
                                begin
                                    while a > 1 do
                                        break;
                                    continue;
                                end
                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,83))

    def test_while_6(self):
        input = """ procedure main();
                    var a:integer;
                    begin
                        if a < 1
                            then
                                begin
                                    while a > 1 do
                                        break;
                                end
                            else
                                begin
                                    continue;
                                end
                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,84))

    def test_while_7(self):
        input = """ procedure main();
                    var a:integer;
                    begin
                        if a < 1
                            then
                                begin
                                    while a > 1 do
                                        with b : integer; do
                                            if b < 1 then break;
                                end
                            else
                                begin
                                    continue;
                                end
                    end

                    """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,85))

    def test_function_1(self):
        input = """ procedure noMain();
                    var a:real; b :integer;
                    begin
                        a := foo(b);
                    end

                    function foo(a:real):real;
                    begin
                        return 1;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,86))

    def test_function_2(self):
        input = """ procedure noMain();
                    var a:boolean; b :integer;
                    begin
                        a := foo(b);
                    end

                    function foo(a:real):boolean;
                    begin
                        return True;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,87))

    def test_function_3(self):
        input = """ procedure noMain();
                    var a:boolean; b :integer;
                    begin
                        a := foo(b) or foo(b + 1);
                    end

                    function foo(a:real):boolean;
                    begin
                        return True;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,88))

    def test_function_4(self):
        input = """ procedure noMain();
                    var a:boolean; b :integer;
                    begin
                        a := foo(b, b + 1) or foo(b + 1, b -1);
                    end

                    function foo(a:real; b:real):boolean;
                    begin
                        return a < b;
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,89))

    def test_function_5(self):
        input = """ procedure noMain();
                    var a:boolean; b :integer;
                    begin
                        a := foo(b, b + 1) or foo(b + 1, b -1);
                    end

                    function foo(a:real; b:real):boolean;
                    begin
                        return foo(a,b);
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,90))

    def test_callexpr_1(self):

        input = """ function foo(a:integer):array [1 .. 2] of integer;
                    var b: array [1 .. 2] of integer;
                    begin return b; end
                    procedure notMain();
                    var foo:integer;
                    begin
                        foo(1)[foo(1)[2]] := foo;
                    end        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,91))

    def test_callexpr_2(self):

        input = """ function foo(a:integer; b:boolean):integer;
                    begin return 1; end

                    procedure main();
                    var a:integer;
                    begin
                        a := foo(a, a);
                    end"""
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[Id(a),Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,92))


    def test_somethingidontknowhowtoname_1(self):

        input = """ var int:integer; realNum:real;
                    procedure noMain();
                    var boolArray : array [1 .. 2] of boolean;
                    begin
                        realNum := toReal(int);
                        boolArray[int] := toBool(int);
                    end

                    function toReal(int : integer):real;
                    begin
                        return int;
                    end

                    function toBool(int: integer):boolean;
                    begin
                        return (int = int) or (int <> int);
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,93))

    def test_somethingidontknowhowtoname_2(self):

        input = """ procedure swap(a,b:real);
                    var temp:real;
                    begin
                        temp := a;
                        a := b;
                        b := temp;
                        putStringLn("Swap successful");
                    end

                    procedure notMain();
                    var a,b:integer;
                    begin
                        a := 5;
                        b := 10;
                        swap(a,b);
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,94))

    def test_somethingidontknowhowtoname_3(self):

        input = """ function fibonaci(n : integer):integer;
                    begin
                        if (n = 0) then return 0;
                        if (n = 1) then return 1;
                        return fibonaci(n-1) + fibonaci(n-2);
                    end

                    procedure notMain();
                    var n:integer;
                    begin
                        n := 5;
                        putString("Number is ");
                        putIntLn(n);
                        putString("Fibonaci is ");
                        putIntLn(fibonaci(n));
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,95))

    def test_somethingidontknowhowtoname_4(self):

        input = """ procedure toBinary(n : integer);
                    var i,j:integer;
                        binary: array [1 .. 1000] of integer;
                    begin
                        i := 0;
                        while (n > 0) do
                            begin
                                binary[i] := n mod 2;
                                n := n div 2;
                                i := i + 1;
                            end
                        for j := i - 1 to 0 do
                            begin
                                putInt(binary[j]);
                                j := j - 1;
                            end
                    end

                    procedure notMain();
                    begin
                        toBinary(10);
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,96))

    def test_somethingidontknowhowtoname_5(self):

        input = """ function square(n : integer):integer;
                    begin return n*n; end

                    function addBy1(n : integer):integer;
                    begin return n + 1; end

                    function minusBy1(n : integer):integer;
                    begin return n - 1; end

                    function diff(a: real; b: real ):real;
                    begin
                        if isPositive(a - b) then return a - b;
                        else return b - a;
                    end

                    function isPositive(n : real):boolean;
                    begin return n >= 0; end

                    procedure notMain();
                    var n:integer; diff:real;
                    begin
                        n := 5;
                        diff := diff(square(addBy1(n)) , square(minusBy1(n)));
                        putFloatLn(diff);
                        putBoolLn(isPositive(diff));
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,97))

    def test_somethingidontknowhowtoname_6(self):

        input = """ function getFactorial(n : integer):integer;
                    begin
                        if (n = 1) then return 1;
                        return n * getFactorial(n-1);
                    end

                    procedure notMain();
                    begin
                        putIntLn(getFactorial(5));

                        putIntLn(getFactorial(5 div 3 + 2 mod 5));
                    end"""
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,98))

    def test_somethingidontknowhowtoname_7(self):

        input = """ procedure towerOfHanoi(n : integer; start_disk : string; desination_disk : string; auxiliary_disk : string);
                    begin
                        if (n = 1) (* If only has 1 disk left *) 
                            then
                                begin
                                    putString("Move 1 disk from ");
                                    putString(start_disk);
                                    putString(" to ");
                                    putStringLn(desination_disk);
                                end
                        
                        towerOfHanoi(n - 1, start_disk, auxiliary_disk, desination_disk);

                        putString("Move 1 disk from ");
                        putString(start_disk);
                        putString(" to ");
                        putStringLn(desination_disk);

                        towerOfHanoi(n - 1, auxiliary_disk, desination_disk, start_disk);
                    end
                    

                    procedure notMain();
                    begin
                        towerOfHanoi(15, "A", "C", "B");
                    end
                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,99))

    def test_somethingidontknowhowtoname_8(self):

        input = """ function complexFunc(a,b:integer; c:boolean; d:string; e:real):boolean;
                    var f : array [1 .. 2] of boolean;
                    begin
                        c := complexFunc(-a,b,f[a + b],d,b) or complexFunc(b,a,complexFunc(b,a,f[-a],d,a),d,a);
                        return complexFunc(a,b,complexFunc(b,a,f[a div b],d,e),d,a);
                    end
                    
                    procedure notMain();
                    var a : boolean;
                    begin
                        a := complexFunc(1 mod 0  , 2 + 3 + 4, True or not (False and True), "I dont know what im writing", 5/2 + 3);
                    end

                    """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,100))

    


