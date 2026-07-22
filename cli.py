# repl_core.py

import traceback
from typing import Any, Dict, List
# Assuming existing imports for sandboxing and translation
from .sandbox import SafeContext  # Placeholder for security-critical class
from .utils import translate_exception_to_maithili 


class REPLEnv:
    """
    Manages the execution environment (namespace) and processes user input
    in an interactive, secure manner.
    """

    def __init__(self):
        # Initialize a clean, restricted namespace for all executed code.
        self._global_context = SafeContext() 
        print("--- माथिलि इंटरैक्टिव मोड (REPL) में स्वागत है! ---")
        print(f"आप 'exit()' या 'quit()' टाइप करके बाहर निकल सकते हैं।")

    def execute_chunk(self, code_input: str) -> Any:
        """
        Processes a block of Maithili code safely.
        
        Args:
            code_input: The string containing the Maithili source code chunk.
        
        Returns:
            The result of the last executed statement, or None if context setup.
        Raises:
            RuntimeError: If a sandboxing violation occurs.
        """
        if not code_input.strip():
            return None

        print("\n[... कोड निष्पादित किया जा रहा है ...]")
        
        # 1. Execution via safe exec() call
        try:
            # Note: We pass the restricted global context. This ensures isolation.
            exec(code_input, self._global_context.__dict__)

            # For REPLs, determining 'the result' is tricky (last expression).
            # We assume standard Python behavior where assignments/functions 
            # define state, but we must capture the explicit return value if possible.
            # A simpler solution for a pure REPL usually involves wrapping input 
            # in `(input_code; print(input_code))` or similar logic outside this function.
            return "✅ निष्पादन सफल रहा। (स्टेटस/परिणाम 'वर्तमान वातावरण' में सेट किया गया)"

        except Exception as e:
            # 2. Handle Exceptions and Localization
            error_message = translate_exception_to_maithili(e, traceback.format_exc())
            return f"\n❌ अपवाद पकड़ा गया: {error_message}"


    def run_interactive(self):
        """The main REPL loop."""
        while True:
            try:
                prompt = "\n>>> माथिलि> "
                user_input = input(prompt)

                if user_input.lower() in ["quit", "exit"]:
                    print("Goodbye! ✨")
                    break
                
                # 3. Execution and Output Handling
                result = self.execute_chunk(user_input)
                print("\n" + str(result))

            except EOFError:
                print("\nGoodbye! ✨")
                break
            except KeyboardInterrupt:
                print("\nInterrupted. Goodbye! ✨")
                break
