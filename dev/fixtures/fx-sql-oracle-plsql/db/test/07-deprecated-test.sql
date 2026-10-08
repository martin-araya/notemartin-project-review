-- 07-deprecated-test.sql (Trampa S3)
-- Test trivial que siempre pasa. Es evidencia de la trampa superficial S3.

BEGIN
  ut.run('deprecated_test');
END;
/

CREATE OR REPLACE PACKAGE deprecated_test AS
    PROCEDURE trivial_pass;
END;

CREATE OR REPLACE PACKAGE BODY deprecated_test AS
    PROCEDURE trivial_pass IS
    BEGIN
        ut.expect(TRUE).to_be_true;
    END;
END;
/