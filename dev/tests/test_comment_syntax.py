"""Tests de la tabla de sintaxis de comentarios (F06a2 T2)."""
from __future__ import annotations

from pathlib import Path

from dev.tools.comment_syntax import detect, mask_comments, has_comment_syntax


class TestDetect:
    def test_by_extension_python(self) -> None:
        p = Path("foo.py")
        assert detect(p) == [("#", "\n")]

    def test_by_extension_javascript(self) -> None:
        p = Path("foo.js")
        assert detect(p) == [("//", "\n"), ("/*", "*/")]

    def test_by_extension_ruby(self) -> None:
        p = Path("foo.rb")
        assert detect(p) == [["#", "\n"], ["=begin", "=end"]] or detect(p) == [("#", "\n"), ("=begin", "=end")]

    def test_by_extension_cobol(self) -> None:
        p = Path("foo.cob")
        assert detect(p) == [("*>", "\n")]

    def test_by_filename_makefile(self) -> None:
        p = Path("Makefile")
        assert detect(p) == [("#", "\n")]

    def test_by_filename_dockerfile(self) -> None:
        p = Path("Dockerfile")
        assert detect(p) == [("#", "\n")]

    def test_by_filename_jenkinsfile(self) -> None:
        p = Path("Jenkinsfile")
        assert detect(p) == [("//", "\n"), ("/*", "*/")]

    def test_unknown_extension(self) -> None:
        p = Path("foo.unknownext")
        assert detect(p) == []

    def test_uppercase_extension(self) -> None:
        p = Path("foo.PY")
        assert detect(p) == [("#", "\n")]


class TestMaskComments:
    def test_python_line_comment(self) -> None:
        text = "x = 1\n# comentario\ny = 2\n"
        masked = mask_comments(text, [("#", "\n")])
        assert "x = 1" in masked
        assert "y = 2" in masked
        assert "comentario" not in masked
        # la cantidad de lineas y la longitud de cada una se preservan
        assert len(masked) == len(text)
        assert masked.count("\n") == text.count("\n")

    def test_javascript_block_comment(self) -> None:
        text = "a;\n/* uno\ndos */\nb;\n"
        masked = mask_comments(text, [("//", "\n"), ("/*", "*/")])
        assert "uno" not in masked
        assert "dos" not in masked
        assert "a;" in masked
        assert "b;" in masked
        assert masked.count("\n") == text.count("\n")

    def test_javascript_line_comment(self) -> None:
        text = "a;\n// hola\nb;\n"
        masked = mask_comments(text, [("//", "\n"), ("/*", "*/")])
        assert "hola" not in masked
        assert "a;" in masked
        assert "b;" in masked
        assert masked.count("\n") == text.count("\n")

    def test_unterminated_block_comment(self) -> None:
        text = "a;\n/* sin cierre\nb;\n"
        masked = mask_comments(text, [("//", "\n"), ("/*", "*/")])
        assert "sin cierre" not in masked
        assert "a;" in masked
        # ``/*`` sin ``*/`` enmascara hasta el final del archivo
        assert "b;" not in masked
        assert len(masked) == len(text)

    def test_xml_comment(self) -> None:
        text = "<root>\n<!-- doc -->\n<child/>\n</root>\n"
        masked = mask_comments(text, [("<!--", "-->")])
        assert "doc" not in masked
        assert "<root>" in masked
        assert "<child/>" in masked

    def test_no_syntax(self) -> None:
        text = "hola\n"
        assert mask_comments(text, []) == text

    def test_ruby_block(self) -> None:
        text = "x = 1\n=begin\nbloque\n=end\ny = 2\n"
        masked = mask_comments(text, [("#", "\n"), ("=begin", "=end")])
        assert "bloque" not in masked
        assert "x = 1" in masked
        assert "y = 2" in masked

    def test_haskell_block(self) -> None:
        text = "x = 1\n{- hola -}\ny = 2\n"
        masked = mask_comments(text, [("--", "\n"), ("{-", "-}")])
        assert "hola" not in masked
        assert "x = 1" in masked
        assert "y = 2" in masked

    def test_cobol_line_comment(self) -> None:
        text = "      *> comentario\nIDENTIFICATION DIVISION.\n"
        masked = mask_comments(text, [("*>", "\n")])
        assert "comentario" not in masked
        assert "IDENTIFICATION" in masked


class TestHasCommentSyntax:
    def test_known(self) -> None:
        assert has_comment_syntax(Path("a.py"))
        assert has_comment_syntax(Path("a.go"))

    def test_unknown(self) -> None:
        assert not has_comment_syntax(Path("a.qwer"))
