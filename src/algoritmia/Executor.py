from .AlgoritmiaVisitor import AlgoritmiaVisitor
from .AlgoritmiaParser import AlgoritmiaParser
import subprocess
import os
import copy
import shutil
import re
import sys

class AlgoritmiaExecutor(AlgoritmiaVisitor):
    def __init__(self):
        #estado
        self.variables = {}        
        self.procedimientos = {}   
        self.output_notes = []     
        
        #configuracion
        self.output_filename = "salida"  
        self.entry_point = "Main"
        self.DEBUG = False         
        
        #limites de seguridad
        self.MAX_RECURSION = 500
        self._call_depth = 0
        self.MAX_WHILE_ITERS = 100000

        #rutas
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_DIR = os.path.dirname(self.BASE_DIR)
        self.MUSIC_DIR = os.path.join(self.PROJECT_DIR, "music")
        self.OUTPUT_DIR = os.path.join(self.PROJECT_DIR, "media")
        
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        self.CFG_PATH = os.path.normpath(os.path.join(self.MUSIC_DIR, "timgm6mb.cfg"))
        self.SF2_PATH = os.path.normpath(os.path.join(self.MUSIC_DIR, "TimGM6mb.sf2"))

    
    #helpers:logica musical    
    def _nota_a_int(self, nota_str):
        """Convierte 'A0'->0, 'C4'->60. PDF: A0=0."""
        m = re.match(r'^([A-Ga-g])([#b]?)(\d*)$', nota_str)
        if not m: return None 

        letra, alter, oct_str = m.groups()
        letra = letra.upper()
        octava = int(oct_str) if oct_str else 4 
        
        offsets = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
        base_val = offsets[letra]
        
        if letra in ['A', 'B']:
            return (octava * 7) + base_val
        else:
            return ((octava - 1) * 7) + base_val

    def _int_a_nota(self, valor_int):
        """Convierte int->'A0' para LilyPond."""
        if not isinstance(valor_int, int): return str(valor_int)
        
        residuo = valor_int % 7
        octava_math = valor_int // 7
        
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        letra = letras[residuo]
        
        if letra in ['A', 'B']:
            octava_visual = octava_math
        else:
            octava_visual = octava_math + 1
            
        return f"{letra}{octava_visual}"

    
    #visitors:estructura principal    
    
    def visitPrograma(self, ctx: AlgoritmiaParser.ProgramaContext):
        
        if self.DEBUG: print("--- Indexando Procedimientos ---")
        for p in ctx.procedimiento():
            name = p.ID_MAYUS().getText()
            self.procedimientos[name] = p
        
        
        if self.entry_point not in self.procedimientos:
            print(f"Error: Procedimiento '{self.entry_point}' no encontrado.")
            return

        
        if self.DEBUG: print(f"--- Ejecutando {self.entry_point} ---")
        try:
            self.visitProcedimiento(self.procedimientos[self.entry_point])
        except Exception as e:
            print(f"\n[Error de Ejecución]: {e}")
            if self.DEBUG: import traceback; traceback.print_exc()
            return

        
        if self.output_notes:
            print(f"\n--- Generando Salida Musical ({len(self.output_notes)} notas) ---")
            self._generar_archivos_multimedia()
        else:
            if self.DEBUG: print("\n(No se generó música)")

    def visitProcedimiento(self, ctx: AlgoritmiaParser.ProcedimientoContext, args=None):
        self._call_depth += 1
        if self._call_depth > self.MAX_RECURSION:
            raise RecursionError("Stack Overflow: Demasiada recursión.")

        prev_vars = self.variables
        self.variables = {} 

        try:
            if args and ctx.parametros():
                param_names = [n.getText() for n in ctx.parametros().ID_MINUSCULA()]
                for i, name in enumerate(param_names):
                    val = args[i] if i < len(args) else 0
                    self.variables[name] = val
            
            
            self.visit(ctx.instrucciones())

        finally:
            self.variables = prev_vars
            self._call_depth -= 1

    def visitInstrucciones(self, ctx: AlgoritmiaParser.InstruccionesContext):
        
        for instr in ctx.instruccion():
            self.visit(instr)

    
    #instrucciones     
    
    def visitEscritura(self, ctx: AlgoritmiaParser.EscrituraContext):
        
        salida = []
        
        for item in ctx.escritura_item():
            val = self.visit(item)
            
            if isinstance(val, list):
                s = str(val).replace(',', '')
                salida.append(s)
            else:
                salida.append(str(val))
        
        print(" ".join(salida))

    def visitEscritura_item(self, ctx: AlgoritmiaParser.Escritura_itemContext):
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]
        elif ctx.expr():
            return self.visit(ctx.expr())

    def visitLectura(self, ctx: AlgoritmiaParser.LecturaContext):
        name = ctx.ID_MINUSCULA().getText()
        raw = input(f"<?> {name}: ").strip()
        
        try:
            if raw.startswith("{") and raw.endswith("}"):
                inner = raw[1:-1].replace(',', ' ').split()
                val = [int(x) for x in inner if x.lstrip('-').isdigit()]
            elif raw.lstrip('-').isdigit():
                val = int(raw)
            else:
                val = 0 
        except:
            val = 0
            
        self.variables[name] = val

    
    # flujo de control   
   
    def visitAsignacion(self, ctx: AlgoritmiaParser.AsignacionContext):
        name = ctx.ID_MINUSCULA().getText()
        val = self.visit(ctx.expr())
        
        if isinstance(val, list):
            self.variables[name] = copy.deepcopy(val)
        else:
            self.variables[name] = val

    def visitCondicional(self, ctx: AlgoritmiaParser.CondicionalContext):
        cond = self.visit(ctx.expr())
        bloques = ctx.instrucciones()
        
        if cond != 0:
            self.visit(bloques[0])
        elif len(bloques) > 1:
            self.visit(bloques[1])

    
    def visitWhile_stmt(self, ctx: AlgoritmiaParser.While_stmtContext):
        count = 0
        while self.visit(ctx.expr()) != 0:
            self.visit(ctx.instrucciones())
            
            count += 1
            if count > self.MAX_WHILE_ITERS:
                raise RuntimeError("While Infinito detectado (Safety Break)")

    def visitLlamada_proc(self, ctx: AlgoritmiaParser.Llamada_procContext):
        name = ctx.ID_MAYUS().getText()
        
        if name not in self.procedimientos:
            raise RuntimeError(f"Llamada a procedimiento desconocido: '{name}'")
        
        args = [self.visit(e) for e in ctx.expr()]
        self.visitProcedimiento(self.procedimientos[name], args=args)

    
    # operaciones de listas    
    
    def visitAddlista(self, ctx: AlgoritmiaParser.AddlistaContext):
        name = ctx.ID_MINUSCULA().getText()
        val = self.visit(ctx.expr())
        
        if name not in self.variables: self.variables[name] = []
        target = self.variables[name]
        
        if not isinstance(target, list): return

        if isinstance(val, list):
            target.append(copy.deepcopy(val))
        else:
            target.append(val)

    def visitPoplista(self, ctx: AlgoritmiaParser.PoplistaContext):
        name = ctx.ID_MINUSCULA().getText()
        idx = self.visit(ctx.expr())
        
        target = self.variables.get(name)
        if not isinstance(target, list) or not isinstance(idx, int): return 0
        
        py_idx = idx - 1
        
        if 0 <= py_idx < len(target):
            return target.pop(py_idx)
        return 0

    
    # expresiones matematicas         

    def visitComparacion(self, ctx: AlgoritmiaParser.ComparacionContext):
        val = self.visit(ctx.aritmetica(0))
        
        count_ops = (ctx.getChildCount() - 1) // 2
        for i in range(count_ops):
            op = ctx.getChild(2*i + 1).getText()
            right = self.visit(ctx.aritmetica(i+1))
            
            res = False
            if op == '=': res = (val == right)
            elif op == '/=': res = (val != right)
            elif op == '<': res = (val < right)
            elif op == '>': res = (val > right)
            elif op == '<=': res = (val <= right)
            elif op == '>=': res = (val >= right)
            
            val = 1 if res else 0
            
        return val

    def visitAritmetica(self, ctx: AlgoritmiaParser.AritmeticaContext):
        val = self.visit(ctx.termino(0))
        count_ops = (ctx.getChildCount() - 1) // 2
        for i in range(count_ops):
            op = ctx.getChild(2*i + 1).getText()
            right = self.visit(ctx.termino(i+1))
            
            if op == '+':
                if isinstance(val, list) and isinstance(right, list):
                    val = val + right
                else:
                    if isinstance(val, list): val = 0
                    if isinstance(right, list): right = 0
                    val += right
            elif op == '-':
                if isinstance(val, int) and isinstance(right, int):
                    val -= right
                    
        return val

    def visitTermino(self, ctx: AlgoritmiaParser.TerminoContext):
        val = self.visit(ctx.factor(0))
        count_ops = (ctx.getChildCount() - 1) // 2
        for i in range(count_ops):
            op = ctx.getChild(2*i + 1).getText()
            right = self.visit(ctx.factor(i+1))
            
            if not isinstance(val, int) or not isinstance(right, int):
                continue
            
            if op == '*': val *= right
            elif op == '%': val %= right if right != 0 else 1
            elif op == '/': val //= right if right != 0 else 1
            
        return val

    def visitFactor(self, ctx: AlgoritmiaParser.FactorContext):
        #negativo
        if ctx.MINUS():
            return -self.visit(ctx.factor())
        
        #parentesis y acceso array
        if ctx.expr():
            if ctx.getChild(0).getText() == '(': 
                return self.visit(ctx.expr())
            
            if ctx.ID_MINUSCULA() and ctx.getChild(1).getText() == '[':
                name = ctx.ID_MINUSCULA().getText()
                idx = self.visit(ctx.expr())
                val = self.variables.get(name)
                if isinstance(val, list) and isinstance(idx, int):
                    py_idx = idx - 1 # Base-1
                    if 0 <= py_idx < len(val):
                        return val[py_idx]
                return 0

        #literales y variables
        if ctx.INT(): return int(ctx.INT().getText())
        
        if ctx.lista_literal():
            return self.visit(ctx.lista_literal())

        if ctx.LEN():
            name = ctx.ID_MINUSCULA().getText()
            val = self.variables.get(name)
            return len(val) if isinstance(val, list) else 0

        if ctx.ID_MINUSCULA():
            return self.variables.get(ctx.ID_MINUSCULA().getText(), 0)

        #nota musical
        if ctx.ID_MAYUS():
            text = ctx.ID_MAYUS().getText()
            val = self._nota_a_int(text)
            if val is not None:
                return val
            return 0 

        return 0

    
    def visitLista_literal(self, ctx: AlgoritmiaParser.Lista_literalContext):
        if ctx.elements_list():
            return [self.visit(e) for e in ctx.elements_list().expr()]
        return []

    
    #reproduccion musical    
    

    def visitReproduccion(self, ctx: AlgoritmiaParser.ReproduccionContext):
        val = self.visit(ctx.expr())
        
        if isinstance(val, list):
            for v in val:
                self._buffer_nota(v)
        else:
            self._buffer_nota(val)

    def _buffer_nota(self, val):
        if isinstance(val, int):
            if val < 0: return 
            nota_str = self._int_a_nota(val)
            self.output_notes.append(nota_str)

    
    # generacion de archivos  
    
    def _generar_archivos_multimedia(self):
        base_name = os.path.join(self.OUTPUT_DIR, self.output_filename)
        ly_path = base_name + ".ly"
        
        notas_lp = []
        for n in self.output_notes:
            notas_lp.append(self._nota_para_lilypond_syntax(n))
            
        content = r"""\version "2.24.0"
\score {
  \new Staff {
    \tempo 4 = 120
    \absolute {
      %s
    }
  }
  \layout {}
  \midi {}
}
""" % " ".join(notas_lp)

        with open(ly_path, 'w') as f:
            f.write(content)
        print(f"-> Partitura generada: {ly_path}")

        if shutil.which("lilypond"):
            try:
                subprocess.run(
                    ["lilypond", os.path.basename(ly_path)],
                    cwd=self.OUTPUT_DIR,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"-> PDF y MIDI generados en: {self.OUTPUT_DIR}")
            except:
                print("Error ejecutando LilyPond.")
        else:
            print("Warning: LilyPond no encontrado en el PATH.")

        midi_path = base_name + ".midi"
        if not os.path.exists(midi_path): midi_path = base_name + ".mid"
        
        if os.path.exists(midi_path) and shutil.which("timidity") and os.path.exists(self.SF2_PATH):
            wav_path = base_name + ".wav"
            
            sf2_dir = os.path.dirname(self.SF2_PATH).replace("\\", "/")
            sf2_name = os.path.basename(self.SF2_PATH)
            cfg_path = os.path.join(self.OUTPUT_DIR, "timidity.cfg")
            
            with open(cfg_path, "w") as f:
                f.write(f'dir "{sf2_dir}"\nsoundfont "{sf2_name}"\n')
                
            try:
                subprocess.run(
                    ["timidity", midi_path, "-Ow", "-o", wav_path, "-c", cfg_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE
                )
                print(f"-> Audio generado: {wav_path}")
            except Exception as e:
                print(f"Error Timidity: {e}")
            finally:
                if os.path.exists(cfg_path): os.remove(cfg_path)

    def _nota_para_lilypond_syntax(self, nota_std):
        m = re.match(r'^([A-G])([#b]?)(\d+)$', nota_std)
        if not m: return "c"
        
        letra, alter, oct_str = m.groups()
        octava = int(oct_str)
        
        base = letra.lower()
        alter_str = "is" if alter == "#" else "es" if alter == "b" else ""
        
        commas = ""
        quotes = ""
        
        diff = octava - 3
        if diff > 0: quotes = "'" * diff
        elif diff < 0: commas = "," * abs(diff)
        
        return f"{base}{alter_str}{commas}{quotes}"