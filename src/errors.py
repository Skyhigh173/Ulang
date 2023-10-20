class UError:
    @staticmethod
    def SyntaxErr(err_char, expected_char, pos,info):
        print(f"ULang Syntax error: unexpected '{err_char}' at {pos}. Expected {expected_char}.")
        raise SystemExit
    
    @staticmethod
    def semiColonErr(pos):
        print(f"ULang Syntax error: missing semi colon (';') at {pos}.")
        raise SystemExit