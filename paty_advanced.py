import subprocess
import random

D8_PATH = './v8/out/x64.release/d8'

def generate_js_payload(gen: int) -> str:
    if gen % 2 == 0:
        return """
        function fuzz(o) {
            let x = o.prop;
            o.prop = 1.337;
            return x;
        }
        %PrepareFunctionForOptimization(fuzz);
        fuzz({prop: 42});
        fuzz({prop: "evil"});
        """;
    else:
        return "print('Wasm placeholder fuzzing');";

def run_v8_campaign(iterations=30):
    for gen in range(1, iterations + 1):
        payload = generate_js_payload(gen)
        try:
            res = subprocess.run(
                [D8_PATH, '--allow-natives-syntax', '-e', payload],
                capture_output=True,
                timeout=2.0
            )
            code = res.returncode
            stderr = res.stderr.decode('utf-8', errors='ignore')
        except subprocess.TimeoutExpired:
            code = -99
            stderr = "TIMEOUT"
        crashed = code != 0 or "Fatal error" in stderr or "Segfault" in stderr
        print(f"[+] [V8-GEN {gen}] ExitCode: {code} | Crashed: {crashed}")

if __name__ == '__main__':
    run_v8_campaign(30)
