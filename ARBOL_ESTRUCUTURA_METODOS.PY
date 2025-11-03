import tkinter as tk
from tkinter import messagebox
from collections import deque 

class Nodo:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class ArbolBinarioBusqueda:
    
    def __init__(self):
        self.root = None

    # --- [1] Insertar ---
    def insertar(self, data):
        self.root = self._insertar_recursivo(self.root, data)

    def _insertar_recursivo(self, nodo, data):
        if nodo is None: return Nodo(data)
        if data == nodo.data: return nodo 
        if data < nodo.data:
            nodo.left = self._insertar_recursivo(nodo.left, data)
        else:
            nodo.right = self._insertar_recursivo(nodo.right, data)
        return nodo

    # --- [8] y [9] Eliminar ---
    def _get_min_nodo(self, nodo):
        actual = nodo
        while actual.left is not None: actual = actual.left
        return actual

    def _get_max_nodo(self, nodo):
        actual = nodo
        while actual.right is not None: actual = actual.right
        return actual

    def eliminar(self, data, estrategia="sucesor"):
        self.root = self._eliminar_recursivo(self.root, data, estrategia)

    def _eliminar_recursivo(self, nodo, data, estrategia):
        if nodo is None: return None 
        if data < nodo.data:
            nodo.left = self._eliminar_recursivo(nodo.left, data, estrategia)
        elif data > nodo.data:
            nodo.right = self._eliminar_recursivo(nodo.right, data, estrategia)
        else:
            if nodo.left is None: return nodo.right
            if nodo.right is None: return nodo.left
            if estrategia == "predecesor":
                temp = self._get_max_nodo(nodo.left)
                nodo.data = temp.data
                nodo.left = self._eliminar_recursivo(nodo.left, temp.data, estrategia)
            else:
                temp = self._get_min_nodo(nodo.right)
                nodo.data = temp.data
                nodo.right = self._eliminar_recursivo(nodo.right, temp.data, estrategia)
        return nodo

    # --- [17] Eliminar Árbol ---
    def eliminar_arbol(self):
        self.root = None

    # --- [5, 6, 7] Recorridos ---
    def recorrer_preorden(self):
        resultado = []
        self._recorrer_preorden(self.root, resultado)
        return resultado
    def _recorrer_preorden(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.data)
            self._recorrer_preorden(nodo.left, resultado)
            self._recorrer_preorden(nodo.right, resultado)

    def recorrer_inorden(self):
        resultado = []
        self._recorrer_inorden(self.root, resultado)
        return resultado
    def _recorrer_inorden(self, nodo, resultado):
        if nodo is not None:
            self._recorrer_inorden(nodo.left, resultado)
            resultado.append(nodo.data)
            self._recorrer_inorden(nodo.right, resultado)

    def recorrer_postorden(self):
        resultado = []
        self._recorrer_postorden(self.root, resultado)
        return resultado
    def _recorrer_postorden(self, nodo, resultado):
        if nodo is not None:
            self._recorrer_postorden(nodo.left, resultado)
            self._recorrer_postorden(nodo.right, resultado)
            resultado.append(nodo.data)

    # --- [11] Altura ---
    def get_altura(self):
        return self._get_altura_recursiva(self.root)
    def _get_altura_recursiva(self, nodo):
        if nodo is None:
            return -1 
        altura_izq = self._get_altura_recursiva(nodo.left)
        altura_der = self._get_altura_recursiva(nodo.right)
        return 1 + max(altura_izq, altura_der)

    # --- [13] Cantidad de nodos ---
    def get_cantidad_nodos(self):
        return self._get_cantidad_nodos_recursivo(self.root)
    def _get_cantidad_nodos_recursivo(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._get_cantidad_nodos_recursivo(nodo.left) + \
               self._get_cantidad_nodos_recursivo(nodo.right)

    # --- [NUEVO] Grado del árbol ---
    def get_grado_arbol(self):
        return self._get_grado_recursivo(self.root)
    def _get_grado_recursivo(self, nodo):
        if nodo is None:
            return 0
        grado_actual = 0
        if nodo.left: grado_actual += 1
        if nodo.right: grado_actual += 1
        grado_izq = self._get_grado_recursivo(nodo.left)
        grado_der = self._get_grado_recursivo(nodo.right)
        return max(grado_actual, grado_izq, grado_der)

    # --- [15] Revisa si es un árbol binario completo ---
    def es_completo(self):
        if self.root is None:
            return True
        
        cola = deque([self.root])
        bandera_de_none_encontrado = False
        
        while cola:
            nodo = cola.popleft()
            
            if nodo is None:
                bandera_de_none_encontrado = True
            else:
                if bandera_de_none_encontrado:
                    return False # Encontró un nodo después de un None
                cola.append(nodo.left)
                cola.append(nodo.right)
        return True

    # --- [16] Revisa si es un árbol binario lleno ---
    def es_lleno(self):
        return self._es_lleno_recursivo(self.root)

    def _es_lleno_recursivo(self, nodo):
        if nodo is None:
            return True # Un árbol vacío se considera lleno
        
        if nodo.left is None and nodo.right is None:
            return True # Es hoja
        
        if nodo.left is not None and nodo.right is not None:
            # Si tiene 2 hijos, checa recursivamente
            return self._es_lleno_recursivo(nodo.left) and \
                   self._es_lleno_recursivo(nodo.right)
                   
        # Si llegó aquí, es porque tiene 1 solo hijo
        return False

# -----------------------------------------------------------------
# 2. APLICACIÓN GRÁFICA (Tkinter)
# (Botones de 'Lleno' y 'Completo' AÑADIDOS)
# -----------------------------------------------------------------

class AppVisualizadorArbol:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Árbol Binario de Búsqueda")
        self.root.geometry("1000x800")
        
        self.arbol = ArbolBinarioBusqueda()
        
        # --- Frame de Controles (Fila 1) ---
        self.control_frame = tk.Frame(root, pady=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.control_frame, text="Valor (número):").pack(side=tk.LEFT, padx=5)
        self.entry_valor = tk.Entry(self.control_frame, width=10)
        self.entry_valor.pack(side=tk.LEFT, padx=5)
        self.btn_insertar = tk.Button(self.control_frame, text="[1] Insertar", command=self.insertar_nodo)
        self.btn_insertar.pack(side=tk.LEFT, padx=5)
        self.btn_elim_pre = tk.Button(self.control_frame, text="[8] Eliminar (Predecesor)", command=self.eliminar_predecesor, fg="red")
        self.btn_elim_pre.pack(side=tk.LEFT, padx=5)
        self.btn_elim_suc = tk.Button(self.control_frame, text="[9] Eliminar (Sucesor)", command=self.eliminar_sucesor, fg="orange")
        self.btn_elim_suc.pack(side=tk.LEFT, padx=5)
        self.btn_eliminar_todo = tk.Button(self.control_frame, text="[17] Eliminar Árbol", command=self.eliminar_arbol_completo, bg="#FF5252", fg="white")
        self.btn_eliminar_todo.pack(side=tk.LEFT, padx=20)
        
        # --- Frame de Recorridos (Fila 2) ---
        self.recorrido_frame = tk.Frame(root, pady=5)
        self.recorrido_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.recorrido_frame, text="Recorridos:").pack(side=tk.LEFT, padx=10)
        self.btn_preorden = tk.Button(self.recorrido_frame, text="[5] PreOrden", command=self.mostrar_preorden)
        self.btn_preorden.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_inorden = tk.Button(self.recorrido_frame, text="[6] InOrden", command=self.mostrar_inorden)
        self.btn_inorden.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_postorden = tk.Button(self.recorrido_frame, text="[7] PostOrden", command=self.mostrar_postorden)
        self.btn_postorden.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # --- Frame de Info (Fila 3) ---
        self.info_frame = tk.Frame(root, pady=5)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.info_frame, text="Información:").pack(side=tk.LEFT, padx=10)
        self.btn_altura = tk.Button(self.info_frame, text="[11] Altura", command=self.mostrar_altura)
        self.btn_altura.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_nodos = tk.Button(self.info_frame, text="[13] Total Nodos", command=self.mostrar_total_nodos)
        self.btn_nodos.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_grado = tk.Button(self.info_frame, text="Grado", command=self.mostrar_grado)
        self.btn_grado.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # --- ¡BOTONES NUEVOS AÑADIDOS AQUÍ! ---
        self.btn_completo = tk.Button(self.info_frame, text="[15] Es Completo", command=self.mostrar_es_completo)
        self.btn_completo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_lleno = tk.Button(self.info_frame, text="[16] Es Lleno", command=self.mostrar_es_lleno)
        self.btn_lleno.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # --- Canvas (Lienzo para dibujar) ---
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1, 
                                highlightbackground="black")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # --- Árbol de ejemplo ---
        # Prueba con este para ver 'Lleno' = True
        for val in [50, 30, 70, 20, 40, 60, 80]:
        # Prueba con este para ver 'Completo' = True (pero 'Lleno' = False)
        # for val in [50, 30, 70, 20, 40, 60]:
            self.arbol.insertar(val)
        self.dibujar_arbol()

    # --- Acciones de Botones (principales) ---
    def _get_valor(self):
        try:
            val = int(self.entry_valor.get())
            return val
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un número entero.")
            return None

    def insertar_nodo(self):
        val = self._get_valor()
        if val is not None:
            self.arbol.insertar(val)
            self.dibujar_arbol()
            self.entry_valor.delete(0, tk.END)

    def eliminar_predecesor(self):
        val = self._get_valor()
        if val is not None:
            self.arbol.eliminar(val, "predecesor")
            self.dibujar_arbol()
            self.entry_valor.delete(0, tk.END)

    def eliminar_sucesor(self):
        val = self._get_valor()
        if val is not None:
            self.arbol.eliminar(val, "sucesor")
            self.dibujar_arbol()
            self.entry_valor.delete(0, tk.END)

    def eliminar_arbol_completo(self):
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar el árbol completo?"):
            self.arbol.eliminar_arbol()
            self.dibujar_arbol()

    # --- Acciones de Botones (Recorridos) ---
    def _formatear_resultado(self, lista):
        if not lista: return "(Árbol vacío)"
        return " -> ".join(map(str, lista))

    def mostrar_preorden(self):
        lista_resultado = self.arbol.recorrer_preorden()
        texto_resultado = self._formatear_resultado(lista_resultado)
        messagebox.showinfo("Recorrido PreOrden", texto_resultado)

    def mostrar_inorden(self):
        lista_resultado = self.arbol.recorrer_inorden()
        texto_resultado = self._formatear_resultado(lista_resultado)
        messagebox.showinfo("Recorrido InOrden", f"{texto_resultado}\n(Nota: InOrden siempre da la lista ordenada)")

    def mostrar_postorden(self):
        lista_resultado = self.arbol.recorrer_postorden()
        texto_resultado = self._formatear_resultado(lista_resultado)
        messagebox.showinfo("Recorrido PostOrden", texto_resultado)

    # --- ¡NUEVAS FUNCIONES PARA BOTONES DE INFO! ---

    def mostrar_altura(self):
        altura = self.arbol.get_altura()
        messagebox.showinfo("Altura del Árbol", 
                            f"La altura del árbol es: {altura}\n(Un árbol con solo la raíz tiene altura 0)")

    def mostrar_total_nodos(self):
        total = self.arbol.get_cantidad_nodos()
        messagebox.showinfo("Total de Nodos", f"El árbol tiene {total} nodos.")

    def mostrar_grado(self):
        grado = self.arbol.get_grado_arbol()
        messagebox.showinfo("Grado del Árbol", 
                            f"El grado del árbol es: {grado}\n(Para un árbol binario, el máximo es 2)")

    def mostrar_es_completo(self):
        es_completo = self.arbol.es_completo()
        messagebox.showinfo("¿Es Árbol Completo?", f"El árbol ES completo: {es_completo}")

    def mostrar_es_lleno(self):
        es_lleno = self.arbol.es_lleno()
        messagebox.showinfo("¿Es Árbol Lleno?", f"El árbol ES lleno: {es_lleno}")

    # --- Lógica de Dibujo (Sin cambios) ---
    def dibujar_arbol(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 2: canvas_width = 1000 
        start_x = canvas_width / 2
        start_y = 50
        x_offset = 250 
        y_offset = 70
        self._dibujar_nodo_recursivo(self.arbol.root, start_x, start_y, x_offset, y_offset)

    def _dibujar_nodo_recursivo(self, nodo, x, y, x_offset, y_offset):
        if nodo is None: return
        radius = 20 
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="lightblue", outline="black", width=2)
        self.canvas.create_text(x, y, text=str(nodo.data), font=("Arial", 12, "bold"))
        next_y = y + y_offset
        if nodo.left:
            x_left = x - x_offset
            self.canvas.create_line(x, y+radius, x_left, next_y-radius, fill="black", width=2)
            self._dibujar_nodo_recursivo(nodo.left, x_left, next_y, x_offset / 2, y_offset)
        if nodo.right:
            x_right = x + x_offset
            self.canvas.create_line(x, y+radius, x_right, next_y-radius, fill="black", width=2)
            self._dibujar_nodo_recursivo(nodo.right, x_right, next_y, x_offset / 2, y_offset)

# -----------------------------------------------------------------
# 3. EJECUCIÓN PRINCIPAL
# -----------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppVisualizadorArbol(root)
    root.mainloop()