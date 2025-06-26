import pandas as pd
import numpy as np

class AnalizadorEjercicio:
    """
    Agente que analiza datos de ejercicio y sugiere mejoras en las rutinas
    """
    def __init__(self, data):
        self.data = data
        self.version = "1.0"
        self.autor = "Sistema Automatizado"

    def analyze_data(self):
        """
        Analiza los datos de ejercicio
        """
        try:
            # Aquí puedes agregar tu lógica de análisis de datos
            # Por ejemplo, puedes calcular la media, la mediana, etc.
            mean = self.data.mean()
            median = self.data.median()
            return mean, median
        except Exception as e:
            print(f"Error al analizar los datos: {str(e)}")
            return None

    def suggest_improvements(self):
        """
        Sugiere mejoras en las rutinas de ejercicio basado en el análisis de los datos
        """
        try:
            # Aquí puedes agregar tu lógica para sugerir mejoras
            # Por ejemplo, si la media de los ejercicios es baja, puedes sugerir incrementar la intensidad
            mean, median = self.analyze_data()
            if mean < 5:
                return "Sugerencia: Incrementa la intensidad de tus ejercicios"
            else:
                return "Sugerencia: Mantén la intensidad de tus ejercicios"
        except Exception as e:
            print(f"Error al sugerir mejoras: {str(e)}")
            return None

if __name__ == "__main__":
    # Ejemplo de uso
    data = pd.Series(np.random.randint(0,10,100))
    analizador = AnalizadorEjercicio(data)
    print(analizador.analyze_data())
    print(analizador.suggest_improvements())